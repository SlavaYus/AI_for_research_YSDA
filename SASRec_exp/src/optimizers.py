"""Optimizers: Muon (2D weights) hybridized with AdamW (1D weights + embeddings).

Muon and the Newton-Schulz orthogonalization are copied from the parent SemantID
repo (src/generative/trainer.py); the hybrid wrapper follows the repo recipe and
the Muon paper: Muon updates the 2D *hidden* weight matrices (attention
projections, FFN), while AdamW updates everything else — 1D parameters (biases,
LayerNorm) and the embedding tables (item_emb / pos_emb lookup tables are routed
to AdamW per the Muon recipe; flip `muon_embeddings` to include them in Muon).
"""

import torch
from torch.optim import Optimizer


def newton_schulz_5(G: torch.Tensor, eps: float = 1e-7) -> torch.Tensor:
    """Quintic Newton-Schulz, 5 iterations. Returns approximately-orthogonal matrix."""
    assert G.dim() >= 2
    a, b, c = 3.4445, -4.7750, 2.0315
    X = G.float()
    if X.size(-2) > X.size(-1):
        X = X.transpose(-2, -1)
        transposed = True
    else:
        transposed = False
    X = X / (X.norm() + eps)
    for _ in range(5):
        A = X @ X.transpose(-2, -1)
        B = b * A + c * (A @ A)
        X = a * X + B @ X
    if transposed:
        X = X.transpose(-2, -1)
    return X.to(G.dtype)


class Muon(Optimizer):
    """Muon optimizer for 2D+ parameters."""

    def __init__(
        self,
        params,
        lr: float = 3e-3,
        momentum: float = 0.95,
        nesterov: bool = True,
        weight_decay: float = 0.0,
    ):
        defaults = dict(lr=lr, momentum=momentum, nesterov=nesterov, weight_decay=weight_decay)
        super().__init__(params, defaults)
        for group in self.param_groups:
            for p in group["params"]:
                assert p.dim() >= 2, f"Muon expects 2D+ params; got shape {tuple(p.shape)}."

    def step(self, closure=None):
        loss = closure() if closure is not None else None
        with torch.no_grad():
            for group in self.param_groups:
                lr = group["lr"]
                beta = group["momentum"]
                nesterov = group["nesterov"]
                wd = group["weight_decay"]
                for p in group["params"]:
                    if p.grad is None:
                        continue
                    g = p.grad
                    state = self.state[p]
                    if "momentum_buffer" not in state:
                        state["momentum_buffer"] = torch.zeros_like(p)
                    buf = state["momentum_buffer"]
                    buf.mul_(beta).add_(g)
                    update = g + beta * buf if nesterov else buf
                    orig_shape = update.shape
                    if update.dim() > 2:
                        update = update.reshape(update.shape[0], -1)
                    ortho = newton_schulz_5(update)
                    fan_out, fan_in = ortho.shape[-2], ortho.shape[-1]
                    adj = max(1.0, fan_out / fan_in) ** 0.5
                    if ortho.shape != orig_shape:
                        ortho = ortho.reshape(orig_shape)
                    if wd != 0.0:
                        p.add_(p, alpha=-lr * wd)
                    p.add_(ortho, alpha=-lr * adj)
        return loss


EMBEDDING_PATTERNS = ("item_emb", "pos_emb")


def is_muon_param(name: str, param: torch.Tensor, muon_embeddings: bool = False) -> bool:
    """Routing rule: Muon takes 2D hidden weight matrices; 1D params and
    embeddings go to AdamW (unless muon_embeddings=True)."""
    if param.ndim < 2:
        return False
    if not muon_embeddings and any(p in name for p in EMBEDDING_PATTERNS):
        return False
    return True


class HybridMuonAdamW:
    """Routes 2D hidden weights to Muon, the rest (1D params, embeddings) to AdamW."""

    def __init__(
        self,
        named_params,
        muon_lr: float,
        adamw_lr: float,
        muon_momentum: float = 0.95,
        adamw_betas=(0.9, 0.95),
        weight_decay: float = 0.0,
        muon_embeddings: bool = False,
    ):
        muon_params = []
        adamw_params = []
        self.muon_param_names, self.adamw_param_names = [], []
        for name, p in named_params:
            if not p.requires_grad:
                continue
            if is_muon_param(name, p, muon_embeddings):
                muon_params.append(p)
                self.muon_param_names.append(name)
            else:
                adamw_params.append(p)
                self.adamw_param_names.append(name)

        if not muon_params:
            raise ValueError("HybridMuonAdamW found no 2D params for Muon.")
        if not adamw_params:
            raise ValueError("HybridMuonAdamW found no params for AdamW.")

        self.muon = Muon(
            muon_params,
            lr=muon_lr,
            momentum=muon_momentum,
            nesterov=True,
            weight_decay=weight_decay,
        )
        self.adamw = torch.optim.AdamW(
            adamw_params,
            lr=adamw_lr,
            betas=tuple(adamw_betas),
            weight_decay=weight_decay,
        )
        self.param_groups = self.muon.param_groups + self.adamw.param_groups

    def step(self, closure=None):
        if closure is not None:
            raise NotImplementedError("HybridOptimizer does not support closure.")
        self.muon.step()
        self.adamw.step()

    def zero_grad(self, set_to_none: bool = True):
        self.muon.zero_grad(set_to_none=set_to_none)
        self.adamw.zero_grad(set_to_none=set_to_none)

    def state_dict(self):
        return {"muon": self.muon.state_dict(), "adamw": self.adamw.state_dict()}

    def load_state_dict(self, sd):
        self.muon.load_state_dict(sd["muon"])
        self.adamw.load_state_dict(sd["adamw"])


def make_optimizer(model, kind: str, lr: float, *, muon_lr: float = 0.01,
                   muon_momentum: float = 0.99, betas=(0.9, 0.95),
                   weight_decay: float = 0.0, muon_embeddings: bool = False):
    """Build the optimizer for a SASRec model.

    kind='adamw': AdamW on all parameters.
    kind='muon':  Muon on 2D hidden weights + AdamW on 1D params and embeddings.
    Both share lr (AdamW part), betas and weight_decay so that runs differ only
    in how the 2D weights are updated.
    """
    if kind == "adamw":
        return torch.optim.AdamW(model.parameters(), lr=lr,
                                 betas=tuple(betas), weight_decay=weight_decay)
    if kind == "muon":
        return HybridMuonAdamW(
            model.named_parameters(),
            muon_lr=muon_lr,
            adamw_lr=lr,
            muon_momentum=muon_momentum,
            adamw_betas=tuple(betas),
            weight_decay=weight_decay,
            muon_embeddings=muon_embeddings,
        )
    raise ValueError(f"Unknown optimizer kind: {kind!r}")
