"""Scalable Cross-Entropy (SCE) objective.

Copied unchanged from the parent SemantID repo (src/models/sce.py). Used for the
Yambda catalog (535k+ items) where a full softmax per position is too expensive.
"""

import torch
import torch.nn.functional as F


class SCEObjectiveFlat:
    """
    SCE loss, when padding is already removed by mask.
    Expected inputs:
      - "sce_x": FloatTensor (N, D)          # embeddings for valid positions only
      - "sce_y": LongTensor  (N,)           # target item ids for those positions
      - "item_emb_weight": FloatTensor (C, D)  # item embedding matrix (classes)
    """

    def __init__(
        self,
        n_buckets: int,
        bucket_size_x: int,
        bucket_size_y: int,
        mix_x: bool,
    ):
        self.n_buckets = n_buckets
        self.bucket_size_x = bucket_size_x
        self.bucket_size_y = bucket_size_y
        self.mix_x = mix_x

    def __call__(self, inputs):
        x = inputs["sce_x"]  # (N, D)
        y = inputs["sce_y"]  # (N,)
        w = inputs["item_emb_weight"]  # (C, D)

        assert x.dim() == 2 and y.dim() == 1 and w.dim() == 2
        assert x.shape[0] == y.shape[0]
        assert x.shape[1] == w.shape[1]

        N, hd = x.shape
        if N == 0:
            return x.new_zeros(())

        scale = float(hd**-0.25)

        # correct logits for each sample: (N,)
        correct_class_logits_ = (x * torch.index_select(w, dim=0, index=y)).sum(dim=1)

        # buckets (no grad)
        with torch.no_grad():
            if self.mix_x:
                omega = scale * torch.randn(
                    N, self.n_buckets, device=x.device, dtype=x.dtype
                )
                buckets = omega.T @ x  # (n_b, D)
                del omega
            else:
                buckets = scale * torch.randn(
                    self.n_buckets, hd, device=x.device, dtype=x.dtype
                )

            # pick top-x per bucket
            x_bucket_scores = buckets @ x.T  # (n_b, N)
            _, top_x_bucket = torch.topk(
                x_bucket_scores, dim=1, k=min(self.bucket_size_x, N)
            )
            del x_bucket_scores

            # pick top-y per bucket
            y_bucket_scores = buckets @ w.T  # (n_b, C)
            _, top_y_bucket = torch.topk(
                y_bucket_scores, dim=1, k=min(self.bucket_size_y, w.shape[0])
            )
            del y_bucket_scores

        bs_x = top_x_bucket.shape[1]
        bs_y = top_y_bucket.shape[1]

        # gather x/y buckets
        x_bucket = torch.gather(x, 0, top_x_bucket.reshape(-1, 1).expand(-1, hd)).view(
            self.n_buckets, bs_x, hd
        )
        y_bucket = torch.gather(w, 0, top_y_bucket.reshape(-1, 1).expand(-1, hd)).view(
            self.n_buckets, bs_y, hd
        )

        # wrong logits + mask coincidences with the correct class
        wrong_class_logits = x_bucket @ y_bucket.transpose(-1, -2)  # (n_b, bs_x, bs_y)

        y_for_top_x = torch.index_select(y, dim=0, index=top_x_bucket.reshape(-1)).view(
            self.n_buckets, bs_x
        )
        mask = y_for_top_x[:, :, None] == top_y_bucket[:, None, :]  # (n_b, bs_x, bs_y)
        wrong_class_logits = wrong_class_logits.masked_fill(mask, float("-inf"))

        correct_class_logits = torch.index_select(
            correct_class_logits_, dim=0, index=top_x_bucket.reshape(-1)
        ).view(
            self.n_buckets, bs_x
        )[
            :, :, None
        ]  # (n_b, bs_x, 1)

        logits = torch.cat(
            (wrong_class_logits, correct_class_logits), dim=2
        )  # (n_b, bs_x, bs_y+1)

        target = (logits.shape[-1] - 1) * torch.ones(
            logits.shape[0] * logits.shape[1],
            dtype=torch.int64,
            device=logits.device,
        )

        loss_ = F.cross_entropy(
            logits.view(-1, logits.shape[-1]), target, reduction="none"
        )  # (n_b*bs_x,)

        # aggregate back to N using amax across buckets
        loss = torch.zeros(N, device=x.device, dtype=loss_.dtype)
        loss.scatter_reduce_(
            0, top_x_bucket.reshape(-1), loss_, reduce="amax", include_self=False
        )

        # drop samples that never got selected (remain 0)
        loss = loss[loss != 0]
        if loss.numel() == 0:
            return correct_class_logits_.sum() * 0.0
        return loss.mean()
