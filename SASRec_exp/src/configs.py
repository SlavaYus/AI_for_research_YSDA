"""Experiment configurations (the "optimal config" per dataset).

Provenance (parent SemantID repo, configs/) plus in-project validation:
- Both datasets use the optuna-tuned SASRec setup from configs/beauty_sasrec.yaml
  and configs/yambda_sasrec.yaml: hidden 128, num_heads 2, dropout 0.4,
  lr 3.94e-4, SCE loss, patience 10; Beauty max_sequence_length 20 with
  filter_seen, Yambda 100 without.
- The Beauty variant was validated in-project against configs/beauty_sasrec_best.yaml
  (hidden 64, heads 1, dropout 0.3, lr 2.50e-4, CE): 15-epoch val NDCG@10
  0.0716 vs 0.0558, see diary 2026-10-13.
- Muon hyperparameters: muon_lr 0.0025 selected in-project on Beauty val.
  At 0.005 the 2-block model trains fine (15-epoch val NDCG@10 0.0701) but 4/6
  block models diverge (train loss rises, val NDCG ~0.02); 0.0025 is stable for
  all depths (12-epoch val NDCG@10: l2 0.0706, l4 0.0705, l6 0.0677). momentum
  0.99 per repo precedent; the AdamW part keeps the tuned lr with betas
  (0.9, 0.95), weight_decay 0, so AdamW and Muon runs differ only in the
  update rule for 2D weights.
"""

from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
RESULTS_DIR = REPO_ROOT / "results"
FIGURES_DIR = REPO_ROOT / "figures"
DIARY_PATH = REPO_ROOT / "diary.md"


@dataclass
class DatasetConfig:
    key: str
    name: str
    data_dir: Path
    split: str = "leave-one-out-no_cold_items"
    max_sequence_length: int = 20
    filter_seen: bool = True
    loss: str = "ce"  # 'ce' (full cross-entropy) or 'sce' (scalable cross-entropy)
    hidden_units: int = 128
    num_heads: int = 2
    dropout_rate: float = 0.4
    lr: float = 3.9400340300651556e-4
    batch_size: int = 128
    eval_batch_size: int = 256
    num_workers: int = 2
    patience: int = 10
    max_epochs: int = 200
    val_size: int = 5000
    random_state: int = 42
    sce: dict = field(default_factory=lambda: dict(
        n_buckets=32, bucket_size_x=512, bucket_size_y=512, mix_x=True))


DATASETS = {
    "beauty": DatasetConfig(
        key="beauty", name="Beauty",
        data_dir=DATA_DIR / "Beauty",
        max_sequence_length=20, filter_seen=True, loss="sce",
        hidden_units=128, num_heads=2, dropout_rate=0.4,
        lr=3.9400340300651556e-4,
        batch_size=64, eval_batch_size=256, num_workers=2,
        patience=10, max_epochs=200,
    ),
    "yambda": DatasetConfig(
        key="yambda", name="Yambda",
        data_dir=DATA_DIR / "Yambda",
        max_sequence_length=100, filter_seen=False, loss="sce",
        hidden_units=128, num_heads=2, dropout_rate=0.4,
        lr=3.9400340300651556e-4,
        batch_size=128, eval_batch_size=128, num_workers=4,
        patience=5, max_epochs=40, val_size=5000,
    ),
}

OPTIMIZER_SETTINGS = {
    "adamw": dict(),
    "muon": dict(muon_lr=0.0025, muon_momentum=0.99),
}
ADAMW_BETAS = (0.9, 0.95)
WEIGHT_DECAY = 0.0

NUM_BLOCKS = (2, 4, 6)
TOP_K = 10


def split_paths(cfg: DatasetConfig):
    base = cfg.data_dir / cfg.split
    return {name: base / f"{name}.csv" for name in
            ("train", "validation_input", "validation_target",
             "test_input", "test_target")}
