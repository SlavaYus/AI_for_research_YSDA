"""Lipschitz regularization for SASRec layers (attention and/or MLP/FFN).

Follows the parent SemantID repo's spectral-norm approach
(src/models/spectral_norm_attention.py for attention-only, and
src/models/lipschitz_norm.py for attention+FFN), model family 'sasrec':
before every forward pass of each block, the targeted projection weight
matrices are renormalized to unit spectral (Lipschitz) constant:

    W <- W / sigma_max(W)

Modes:
- 'attn':    in_proj_weight and out_proj.weight of every MultiheadAttention.
             The hook is registered on the MultiheadAttention module itself
             (in PyTorch >= 2.0 its forward calls F.linear on out_proj.weight
             directly, so a hook on the out_proj submodule would never fire).
- 'mlp':     conv1.weight and conv2.weight of every PointWiseFeedForward
             (the SASRec FFN; Conv1d weights [H, H, 1] are reshaped to 2D).
             The hook is registered on the PointWiseFeedForward module.
- 'attn+mlp' (aka 'all'): both of the above — every linear sub-layer of every
             transformer block is Lipschitz-constrained.

sigma_max is estimated with power iteration (10 steps).
"""

from __future__ import annotations

import torch
import torch.nn as nn


def _power_iteration_sigma(weight: torch.Tensor, n_iters: int = 10,
                           eps: float = 1e-12) -> float:
    """Estimate the largest singular value of *weight* via power iteration."""
    w = weight.data
    if w.dim() > 2:
        w = w.reshape(w.shape[0], -1)
    u = torch.randn(w.shape[0], device=w.device, dtype=w.dtype)
    for _ in range(n_iters):
        v = torch.mv(w.t(), u)
        v = v / (v.norm() + eps)
        u = torch.mv(w, v)
        u = u / (u.norm() + eps)
    sigma = u.dot(torch.mv(w, v)).abs().item()
    return sigma


def _spectral_norm_weights_hook(weights, eps: float = 1e-12, n_iters: int = 10):
    """Forward-pre-hook: normalize every weight in *weights* to sigma_max = 1."""

    def hook(module, _input):
        with torch.no_grad():
            for w in weights:
                sigma = _power_iteration_sigma(w, n_iters=n_iters, eps=eps)
                if sigma > eps:
                    w.data.div_(sigma)

    return hook


def apply_lipschitz_attention(model: nn.Module) -> int:
    """Register the Lipschitz (spectral-norm) hook on every SASRec attention block.

    Returns the number of instrumented weight matrices (2 per block:
    in_proj_weight and out_proj.weight).
    """
    count = 0
    for attn in model.attention_layers:
        weights = [attn.in_proj_weight, attn.out_proj.weight]
        attn.register_forward_pre_hook(_spectral_norm_weights_hook(weights))
        count += len(weights)
    return count


def apply_lipschitz_mlp(model: nn.Module) -> int:
    """Register the Lipschitz (spectral-norm) hook on every SASRec FFN block.

    Targets conv1.weight and conv2.weight of each PointWiseFeedForward
    (the SASRec MLP/FFN). Returns the number of instrumented weight matrices
    (2 per block).
    """
    count = 0
    for ffn in model.forward_layers:
        weights = [ffn.conv1.weight, ffn.conv2.weight]
        ffn.register_forward_pre_hook(_spectral_norm_weights_hook(weights))
        count += len(weights)
    return count


def apply_lipschitz(model: nn.Module, mode: str) -> int:
    """Apply Lipschitz regularization by mode: 'none' | 'attn' | 'mlp' | 'attn+mlp'.

    Returns the number of instrumented weight matrices.
    """
    if mode in (None, "none", "", False):
        return 0
    if mode == "attn":
        return apply_lipschitz_attention(model)
    if mode == "mlp":
        return apply_lipschitz_mlp(model)
    if mode in ("attn+mlp", "all"):
        return apply_lipschitz_attention(model) + apply_lipschitz_mlp(model)
    raise ValueError(
        f"Unknown lipschitz mode: {mode!r}. "
        "Expected 'none', 'attn', 'mlp' or 'attn+mlp'."
    )
