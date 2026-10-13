"""Metrics: HR@k, NDCG@k, Coverage@k — overall and by buckets.

Self-contained reimplementation of the parent SemantID evaluation protocol
(src/eval/metrics.py + src/eval/bucketed_eval.py) for a single target per user
(leave-one-out), without the replay dependency.

Definitions:
- HR@k:      share of users whose target item is inside the top-k list.
- NDCG@k:    mean over users of 1/log2(rank+1) when the target is found at
             position `rank` in the top-k list, else 0 (single relevant item).
- Coverage@k: number of distinct items appearing across all top-k lists divided
             by the catalog size (item_count, embedding rows incl. padding id).
- User buckets: users split by test input-sequence length as a percent of
             max_sequence_length, thirds (<=33%, 34-66%, 67-100%).
- Item buckets: target items split into thirds by popularity — items ordered
             most-to-least popular by interaction count, buckets hold ~1/3 of
             total interaction mass (cumulative-mass boundaries, as in the
             parent repo's bucketed_eval).
- Per-bucket Coverage: user buckets use the full catalog; item buckets restrict
             the catalog to the bucket's items (distinct recommended items that
             belong to the bucket / bucket size).
"""

import numpy as np
import pandas as pd


def ranking_metrics(recs: dict, targets: dict, k: int = 10) -> dict:
    """HR@k and NDCG@k for a single target per user.

    recs: user_id -> sequence of recommended items (best first, length >= k).
    targets: user_id -> target item id.
    """
    hits, ndcgs = [], []
    for user, target in targets.items():
        top = list(recs.get(user, []))[:k]
        try:
            rank = top.index(target)
        except ValueError:
            rank = -1
        if rank >= 0:
            hits.append(1.0)
            ndcgs.append(1.0 / np.log2(rank + 2))
        else:
            hits.append(0.0)
            ndcgs.append(0.0)
    if not hits:
        return {f"HR@{k}": 0.0, f"NDCG@{k}": 0.0}
    return {f"HR@{k}": float(np.mean(hits)), f"NDCG@{k}": float(np.mean(ndcgs))}


def coverage_at_k(recs: dict, catalog_size: int, k: int = 10,
                  catalog_items=None) -> float:
    """Coverage@k: distinct recommended items / catalog size.

    If catalog_items is given (a set), only recommended items inside it are
    counted and the denominator becomes its size (bucket-restricted catalog).
    """
    seen = set()
    for user, top in recs.items():
        seen.update(list(top)[:k])
    if catalog_items is not None:
        seen = seen & set(catalog_items)
        denom = len(catalog_items)
    else:
        denom = catalog_size
    if denom == 0:
        return 0.0
    return len(seen) / denom


def assign_user_buckets(test_input: pd.DataFrame, max_sequence_length: int,
                        boundaries=(33, 66, 100), user_col="user_id") -> pd.Series:
    """Bucket users by test input-sequence length as a percent of max_sequence_length.

    boundaries: ascending upper bounds in percent of max_sequence_length (last >= 100).
    Returns a Series indexed by user_id with the 1-based bucket number.
    """
    lengths = test_input.groupby(user_col).size().clip(upper=max_sequence_length)
    pct = lengths / max_sequence_length * 100
    idx = np.searchsorted(np.asarray(boundaries, dtype=float), pct.values, side="left")
    idx = np.clip(idx, 0, len(boundaries) - 1)
    return pd.Series(idx + 1, index=pct.index)


def assign_item_buckets(interactions: pd.DataFrame, boundaries=(33, 66, 100),
                        item_col="item_id") -> pd.Series:
    """Bucket items by popularity using cumulative interaction mass.

    Items are ordered most-to-least popular; each bucket holds ~1/N of the total
    interaction mass. Returns a Series indexed by item_id with the 1-based
    bucket number.
    """
    counts = interactions[item_col].value_counts()  # descending by popularity
    cum_before = (counts.cumsum() - counts) / counts.sum() * 100
    idx = np.searchsorted(np.asarray(boundaries, dtype=float), cum_before.values, side="right")
    idx = np.clip(idx, 0, len(boundaries) - 1)
    return pd.Series(idx + 1, index=counts.index)


def evaluate(recs: dict, targets: dict, test_input: pd.DataFrame,
             catalog_size: int, max_sequence_length: int, k: int = 10,
             user_boundaries=(33, 66, 100), item_boundaries=(33, 66, 100)) -> dict:
    """Overall metrics + per-user-bucket and per-item-bucket metrics.

    Item popularity for bucketing is estimated on test_input + test_target
    (item_freq_source='all' in the parent repo protocol).
    """
    results = ranking_metrics(recs, targets, k=k)
    results[f"Coverage@{k}"] = coverage_at_k(recs, catalog_size, k=k)

    # ---- user buckets: by test input length, full catalog ----
    user_bucket = assign_user_buckets(test_input, max_sequence_length,
                                      user_boundaries)
    lengths = test_input.groupby("user_id").size()
    for b in range(1, len(user_boundaries) + 1):
        users_b = [u for u in user_bucket.index if user_bucket[u] == b]
        recs_b = {u: recs[u] for u in users_b if u in recs}
        targets_b = {u: targets[u] for u in users_b if u in targets}
        lens_b = lengths.reindex(users_b)
        results[f"ubucket{b}_n_users"] = int(len(users_b))
        if len(lens_b):
            results[f"ubucket{b}_mean_len"] = round(float(lens_b.mean()), 2)
        metrics_b = ranking_metrics(recs_b, targets_b, k=k)
        results[f"ubucket{b}_HR@{k}"] = metrics_b[f"HR@{k}"]
        results[f"ubucket{b}_NDCG@{k}"] = metrics_b[f"NDCG@{k}"]
        results[f"ubucket{b}_Coverage@{k}"] = coverage_at_k(recs_b, catalog_size, k=k)

    # ---- item buckets: by target-item popularity, bucket-restricted catalog ----
    freq_src = test_input
    if targets:
        target_df = pd.DataFrame(
            {"user_id": list(targets.keys()), "item_id": list(targets.values())}
        )
        freq_src = pd.concat([test_input[["user_id", "item_id"]], target_df], axis=0)
    item_bucket = assign_item_buckets(freq_src, item_boundaries)

    for b in range(1, len(item_boundaries) + 1):
        bucket_items = set(item_bucket.index[item_bucket == b])
        users_b = [u for u, t in targets.items() if t in bucket_items]
        recs_b = {u: recs[u] for u in users_b if u in recs}
        targets_b = {u: targets[u] for u in users_b if u in targets}
        results[f"ibucket{b}_n_users"] = int(len(users_b))
        results[f"ibucket{b}_n_items"] = int(len(bucket_items))
        metrics_b = ranking_metrics(recs_b, targets_b, k=k)
        results[f"ibucket{b}_HR@{k}"] = metrics_b[f"HR@{k}"]
        results[f"ibucket{b}_NDCG@{k}"] = metrics_b[f"NDCG@{k}"]
        results[f"ibucket{b}_Coverage@{k}"] = coverage_at_k(
            recs_b, catalog_size, k=k, catalog_items=bucket_items)

    return results
