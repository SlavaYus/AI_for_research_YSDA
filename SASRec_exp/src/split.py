"""Leave-one-out split, copied from the parent SemantID repo
(src/preprocess/splits.py + src/preprocess/target_selection.py) and made
standalone: no hydra, plain argparse CLI.

The existing splits under data/<Dataset>/leave-one-out-no_cold_items were
produced by exactly this splitter (leave-one-out, remove_cold_items=True),
so the CLI is only needed to regenerate them from data/<Dataset>/preprocessed.csv.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

LOGGER = logging.getLogger(__name__)


def leave_last(holdout_data: pd.DataFrame,
               input_data: pd.DataFrame = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Leave-last-out: last interaction per user is the target, the rest is input."""
    data_sorted = holdout_data.sort_values(["user_id", "timestamp"], kind="stable")
    data_sorted["_time_idx_reversed"] = data_sorted.groupby("user_id").cumcount(ascending=False)
    final_input = data_sorted[data_sorted["_time_idx_reversed"] > 0].drop(columns=["_time_idx_reversed"])
    targets = data_sorted[data_sorted["_time_idx_reversed"] == 0].drop(columns=["_time_idx_reversed"])

    if input_data is not None:
        final_input = pd.concat([input_data, final_input], ignore_index=True).sort_values(
            ["user_id", "item_id"], kind="stable"
        )
    return final_input, targets


def leave_first_no_input(holdout_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """First interaction per user is input, second is target (cold users)."""
    data_sorted = holdout_data.sort_values(["user_id", "timestamp"], kind="stable")
    data_sorted["_time_idx"] = data_sorted.groupby("user_id").cumcount(ascending=True)
    input_data = data_sorted[data_sorted["_time_idx"] == 0].drop(columns=["_time_idx"])
    targets = data_sorted[data_sorted["_time_idx"] == 1].drop(columns=["_time_idx"])
    return input_data, targets


def leave_first(holdout_data: pd.DataFrame,
                input_data: pd.DataFrame = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Leave-first-out: first interaction per user is the target."""
    data_sorted = holdout_data.sort_values(["user_id", "timestamp"], kind="stable")

    if input_data is not None:
        warm_users = input_data["user_id"].unique()
        warm_user_mask = data_sorted["user_id"].isin(warm_users)

        warm_target = data_sorted[warm_user_mask].groupby("user_id").head(1)

        cold_full = data_sorted[~warm_user_mask]
        cold_input, cold_target = leave_first_no_input(cold_full)
        targets = pd.concat([warm_target, cold_target], ignore_index=True)

        final_input = pd.concat([input_data, cold_input], ignore_index=True).sort_values(
            ["user_id", "item_id"], kind="stable"
        )
    else:
        final_input, targets = leave_first_no_input(data_sorted)

    final_input["timestamp"] = final_input["timestamp"].astype(int)
    targets["timestamp"] = targets["timestamp"].astype(int)
    return final_input, targets


def leave_random(holdout_data: pd.DataFrame,
                 input_data: pd.DataFrame = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Leave-random-out: one random interaction per user is the target."""
    data_sorted = holdout_data.sort_values(["user_id", "timestamp"], kind="stable")
    data_sorted["_time_idx"] = data_sorted.groupby("user_id").cumcount()

    if input_data is not None:
        warm_users = input_data["user_id"].unique()
        warm_user_mask = data_sorted["user_id"].isin(warm_users)

        warm_full = data_sorted[warm_user_mask]
        warm_target = warm_full.groupby("user_id").sample(n=1)

        cold_full = data_sorted[~warm_user_mask]
        cold_target = (
            cold_full[cold_full["_time_idx"] > 0].groupby("user_id").sample(n=1)
            if not cold_full.empty
            else cold_full
        )

        targets = pd.concat([warm_target, cold_target], ignore_index=True)
    else:
        targets = data_sorted[data_sorted["_time_idx"] > 0].groupby("user_id").sample(n=1)

    max_time_id_map = targets.set_index("user_id")["_time_idx"]
    data_sorted["sampled_time_idx"] = data_sorted["user_id"].map(max_time_id_map)

    final_input = data_sorted[
        data_sorted["_time_idx"] < data_sorted["sampled_time_idx"]
    ].drop(columns=["_time_idx", "sampled_time_idx"])

    if input_data is not None:
        final_input = pd.concat([input_data, final_input], ignore_index=True).sort_values(
            ["user_id", "item_id"], kind="stable"
        )

    return final_input, targets.drop(columns=["_time_idx"])


def drop_duplicate_interactions(
    data: pd.DataFrame,
    user_col: str = "user_id",
    item_col: str = "item_id",
    timestamp_col: str = "timestamp",
) -> pd.DataFrame:
    """Keep one row per (user, item, timestamp).

    A repeated triple is the same event recorded twice, not two events. Left in place it leaks
    the holdout: leave-one-out positions rows by time, so one copy becomes the target while its
    twin stays in the input the model trains on. Two plays of the same item at *different*
    timestamps are genuinely two events and are kept.
    """
    before = len(data)
    data = data.drop_duplicates(subset=[user_col, item_col, timestamp_col], keep="first")
    dropped = before - len(data)
    if dropped:
        LOGGER.warning(
            "Dropped %s duplicate interactions (%.2f%% of %s rows) before splitting",
            dropped, 100 * dropped / before, before,
        )
    return data


def align_input_target(
    df_input: pd.DataFrame,
    df_target: pd.DataFrame,
    user_col_name: str = "user_id",
    keep_targets_with_empty_inputs: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Remove users with no target or input from input and target data."""
    users_with_targets = df_target[user_col_name].unique()
    users_with_input = df_input[user_col_name].unique()
    common_users = np.intersect1d(users_with_targets, users_with_input)

    df_input = df_input[df_input[user_col_name].isin(common_users)]
    if not keep_targets_with_empty_inputs:
        df_target = df_target[df_target[user_col_name].isin(common_users)]
    return df_input, df_target


def filter_cold(
    filter_col_name: str,
    base: pd.DataFrame,
    df_input: pd.DataFrame,
    df_target: pd.DataFrame,
    user_col_name: str = "user_id",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Filter out cold items/users not present in the base dataset."""
    warm_entities = base[filter_col_name].unique()
    df_target = df_target[df_target[filter_col_name].isin(warm_entities)]
    df_input = df_input[df_input[filter_col_name].isin(warm_entities)]
    return df_input, df_target


class LeaveOneOutSplitter:
    """Leave-one-out splitter.

    Train keeps all but the last two interactions per user; validation input is
    all but the last one with the last as target; test input is all but the very
    last with the last as target. Optionally removes cold items (not present in
    train) from validation/test.
    """

    def __init__(
        self,
        user_col: str = "user_id",
        item_col: str = "item_id",
        timestamp_col: str = "timestamp",
        remove_cold_items: bool = False,
    ) -> None:
        self.user_col = user_col
        self.item_col = item_col
        self.timestamp_col = timestamp_col
        self.remove_cold_items = remove_cold_items

    def split(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, ...]:
        data = drop_duplicate_interactions(
            data, self.user_col, self.item_col, self.timestamp_col
        )
        data = data.sort_values([self.user_col, self.timestamp_col], kind="stable")

        data["time_idx_reversed"] = data.groupby(self.user_col).cumcount(
            ascending=False
        )

        # Train contains all interactions except last two for each user
        train = data[data.time_idx_reversed >= 2].drop(columns=["time_idx_reversed"])

        # Validation contains all interactions except last one for each user
        validation = data[data.time_idx_reversed >= 1].drop(
            columns=["time_idx_reversed"]
        )

        # Split validation and test into input sequences and target
        validation_input, validation_target = leave_last(validation)
        test_input, test_target = leave_last(data.drop(columns=["time_idx_reversed"]))

        if self.remove_cold_items:
            validation_input, validation_target = filter_cold(
                self.item_col, train, validation_input, validation_target, self.user_col
            )
            test_input, test_target = filter_cold(
                self.item_col, train, test_input, test_target, self.user_col
            )

        validation_input, validation_target = align_input_target(
            validation_input, validation_target, self.user_col,
            keep_targets_with_empty_inputs=False,
        )
        test_input, test_target = align_input_target(
            test_input, test_target, self.user_col,
            keep_targets_with_empty_inputs=False,
        )

        return train, validation_input, validation_target, test_input, test_target


def main():
    parser = argparse.ArgumentParser(description="Make leave-one-out split")
    parser.add_argument("--data", type=Path, required=True,
                        help="path to preprocessed.csv (user_id, item_id, timestamp)")
    parser.add_argument("--out-dir", type=Path, required=True,
                        help="output directory for the five split csv files")
    parser.add_argument("--remove-cold-items", action="store_true", default=True)
    args = parser.parse_args()

    data = pd.read_csv(args.data)
    splitter = LeaveOneOutSplitter(remove_cold_items=args.remove_cold_items)
    parts = splitter.split(data)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for name, part in zip(
        ["train", "validation_input", "validation_target", "test_input", "test_target"],
        parts,
    ):
        path = args.out_dir / f"{name}.csv"
        part.to_csv(path, index=False)
        print(f"{name}: {len(part)} rows -> {path}")


if __name__ == "__main__":
    main()
