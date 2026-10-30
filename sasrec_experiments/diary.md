---
Fri Oct 23 09:37:47 AM MSK 2026
---
Implemented depth-scaled LR (lr~1/sqrt(L)) and mixed optimizers (Muon for 2D, AdamW for 1D/emb). Ran AdamW and Muon variants for L in {2,4,6} on Beauty SASRec; results saved to sasrec_depth_lr_results.json.

---
Fri Oct 23 18:25:29 MSK 2026
---

## Experiment: AdamW + StackRec for SASRec (Beauty)

### Goal
Implement StackRec-style progressive layer stacking for a 6-layer SASRec
trained with AdamW, and obtain validation/test metrics for three effective
depths within one continuous training run:

1. last 2 of 6 transformer layers,
2. middle 4 layers,
3. all 6 layers.

### Implementation
- `src/models/sequence.py`
  - Added per-layer forward coefficients (`layer_scales`). A coefficient of
    0 makes the layer an identity (the layer is skipped), so the model acts
    as a shallower network.
  - Replaced the internal `nn.TransformerEncoder` forward call with an
    equivalent manual layer loop so individual layers can be scaled/skipped.
    Verified numerically that with all coefficients = 1 the output is bitwise
    identical to the original `nn.TransformerEncoder(...)` call.
  - Added helpers: `set_layer_scales`, `get_layer_scales`,
    `set_layers_trainable`, `copy_layer_weights`.
- `configs/beauty_sasrec_stackrec.yaml`
  - New Hydra config: 6-layer SASRec, AdamW, StackRec stage definitions.
- `run_stackrec.py`
  - One-process progressive training loop with stage-wise validation/test
    evaluation and JSON result saving.

### Protocol
- Dataset: Beauty (`reviews_Beauty_5`), seed 42, batch size 128.
- Optimizer: AdamW, weight_decay=0, betas=(0.9, 0.999), grad clip 10.0.
- Stage learning rates follow the existing depth scaling
  `lr(L) = lr_ref * sqrt(4/L)`, `lr_ref = 0.0021002963516611`
  (so each stage uses a smaller LR than the previous one).
- Stage 1 (`2_layers`, 90 epochs): layers 4,5 trainable; layers 0-3 frozen
  and their forward coefficient is 0. LR = 0.0029702675855218593.
- Stage 2 (`4_layers`, 60 epochs, 10-epoch ramp): copy layer 4 -> layer 2 and
  layer 5 -> layer 3. Train layers 2-5. Coefficients of layers 2,3 are ramped
  linearly from 0 to 1, while layers 4,5 stay at 1. LR = 0.0021002963516611.
- Stage 3 (`6_layers`, 60 epochs, 10-epoch ramp): copy the middle two layers
  2 -> 0 and 3 -> 1. Train all six layers. Coefficients of layers 0,1 are
  ramped from 0 to 1. LR = 0.0017148847900662653.
- Best-checkpoint selection per stage: best validation `ndcg@10` among epochs
  where all ramp coefficients reached their final values. The selected
  checkpoint is restored before the next stage, so new layers are copied from
  the best previous-stage weights.
- The stage-start check with new coefficients = 0 exactly reproduced the
  previous stage metrics (continuity validated).

### Results (best complete-gate checkpoint per stage)

| effective layers | lr | best global epoch | val ndcg@10 | test ndcg@10 | val recall@10 | test recall@10 | val ndcg@100 | test ndcg@100 | val recall@100 | test recall@100 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 (layers 4,5) | 0.00297027 | 88 | 0.014714 | 0.011958 | 0.029630 | 0.023380 | 0.032305 | 0.021223 | 0.122751 | 0.071633 |
| 4 (layers 2-5) | 0.00210030 | 129 | 0.015451 | 0.012964 | 0.031746 | 0.025370 | 0.034820 | 0.022722 | 0.134392 | 0.075737 |
| 6 (all layers) | 0.00171488 | 194 | 0.016095 | 0.013299 | 0.033439 | 0.025494 | 0.035022 | 0.023203 | 0.133968 | 0.076607 |

Total training time: ~854 s (248 s + 270 s + 336 s).

### Validation
- JSON/history parsed successfully; history lengths are 90/60/60 for the
  three stages.
- Continuity checks passed exactly:
  - Stage 4 start val ndcg@10 = 0.0147142793 = stage 2 best.
  - Stage 6 start val ndcg@10 = 0.0154509362 = stage 4 best.
- All recorded metrics are finite.
- Note: `meanrank@*` is 0.0 because of the pre-existing metric-name mismatch
  in `src/metrics.py` / `src/utils.py` (the metric emits `mean_rank`, while
  the aggregator looks for `meanrank@k`). This is not specific to StackRec;
  the same behaviour is present in earlier result files. NDCG/Recall and
  coverage are unaffected.

### Comparison with AdamW without stacking (select-epoch, train-only test)
Reference: `sasrec_depth_lr_results.json`, `adamw` branches
(`test/ndcg@10` at the selected epoch, no train+val refit).

| layers | AdamW select test ndcg@10 | StackRec test ndcg@10 |
|---:|---:|---:|
| 2 | 0.012762 | 0.011958 |
| 4 | 0.004797 | 0.012964 |
| 6 | 0.005645 | 0.013299 |

StackRec is substantially better for 4 and 6 effective layers (about 2.3-2.7x
higher test ndcg@10) and close for 2 layers (the 2-layer stage is a warm-start
stage trained for 90 epochs, not a separately tuned 2-layer model).

### Files
- Config: `configs/beauty_sasrec_stackrec.yaml`
- Script: `run_stackrec.py`
- Run directory: `outputs/stackrec_adamw/`
  - `stackrec_results.json` - full stage results + config + interpretation
  - `stackrec_history.json` - per-epoch metrics and layer coefficients
  - `2_layers_best_metrics.json`, `4_layers_best_metrics.json`,
    `6_layers_best_metrics.json`
  - `config.yaml` - resolved config of the run
- Aggregated results: `sasrec_stackrec_results.json` (project root)
- Log: `logs/stackrec_adamw.log`
- `RUN.txt` updated with the StackRec run instructions.

### Run command
```bash
CUDA_VISIBLE_DEVICES=0 python run_stackrec.py \
  -cn beauty_sasrec_stackrec \
  hydra.run.dir=outputs/stackrec_adamw \
  hydra.job.chdir=false
```

---
Fri Oct 23 18:55:39 MSK 2026
---

## Experiment: Muon + StackRec for SASRec (Beauty)

### Goal
Repeat the progressive StackRec experiment with the Muon optimizer instead of
AdamW, keeping the same layer schedule, epoch budget, copy plan and ramp
schedule.

### Implementation
- `run_stackrec.py` was made optimizer-agnostic:
  - `optimizer.type` can be `adamw` or `muon`;
  - for `muon`, 2D hidden weights are optimized by Muon and embeddings / 1D
    parameters by AdamW (`exclude_embeddings: true`, same split as
    `beauty_sasrec_muon.yaml`);
  - stages now support `muon_lr` and `adamw_lr`;
  - history/summary JSON records the optimizer type and both LRs.
- New config: `configs/beauty_sasrec_stackrec_muon.yaml`.
- The previous AdamW StackRec config and results are unchanged.

### Protocol
- Same as the AdamW StackRec run: 90 / 60 / 60 epochs, 10-epoch ramps in
  stages 2 and 3, identical copy plan (`4->2`, `5->3`, then `2->0`, `3->1`).
- Muon LRs use depth scaling `lr_muon(L) = 0.02 * sqrt(4/L)`:
  - 2 layers: Muon 0.028284271247461905, AdamW 0.0029702675855218593;
  - 4 layers: Muon 0.02, AdamW 0.0021002963516611;
  - 6 layers: Muon 0.016329931618554522, AdamW 0.0017148847900662653.
- Muon: momentum 0.95, nesterov, 5 Newton-Schulz steps, weight_decay 0.
- AdamW part: betas (0.9, 0.999), eps 1e-8, weight_decay 0, grad clip 10.0.

### Results (best complete-gate checkpoint per stage)

| effective layers | muon lr | adamw lr | best global epoch | val ndcg@10 | test ndcg@10 | val recall@10 | test recall@10 | val ndcg@100 | test ndcg@100 | val recall@100 | test recall@100 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 (layers 4,5) | 0.02828427 | 0.00297027 | 85 | 0.007215 | 0.004602 | 0.013122 | 0.009825 | 0.016025 | 0.011337 | 0.060106 | 0.046139 |
| 4 (layers 2-5) | 0.02000000 | 0.00210030 | 119 | 0.007884 | 0.004518 | 0.014392 | 0.009203 | 0.017564 | 0.011704 | 0.065820 | 0.047009 |
| 6 (all layers) | 0.01632993 | 0.00171488 | 173 | 0.007008 | 0.004341 | 0.012698 | 0.009327 | 0.016286 | 0.011098 | 0.062857 | 0.046263 |

Total training time: ~971 s (296 s + 285 s + 390 s).

### Validation
- JSON/history parsed successfully; history lengths are 90/60/60.
- Continuity checks passed exactly:
  - Stage 4 start val ndcg@10 = 0.0072150917 = stage 2 best.
  - Stage 6 start val ndcg@10 = 0.0078838427 = stage 4 best.
- All recorded metrics are finite.
- Same pre-existing `meanrank@* = 0.0` naming issue as before.
- The AdamW StackRec config was smoke-tested after the optimizer-agnostic
  refactor; the saved AdamW results were not overwritten.

### Comparison
AdamW StackRec (same protocol, previous run):

| layers | AdamW StackRec val ndcg@10 | AdamW StackRec test ndcg@10 | Muon StackRec val ndcg@10 | Muon StackRec test ndcg@10 |
|---:|---:|---:|---:|---:|
| 2 | 0.014714 | 0.011958 | 0.007215 | 0.004602 |
| 4 | 0.015451 | 0.012964 | 0.007884 | 0.004518 |
| 6 | 0.016095 | 0.013299 | 0.007008 | 0.004341 |

Plain Muon without stacking (`sasrec_depth_lr_results.json`, select-epoch
train-only test):

| layers | plain Muon val ndcg@10 | plain Muon test ndcg@10 | Muon StackRec val ndcg@10 | Muon StackRec test ndcg@10 |
|---:|---:|---:|---:|---:|
| 2 | 0.008019 | 0.005187 | 0.007215 | 0.004602 |
| 4 | 0.004953 | 0.003540 | 0.007884 | 0.004518 |
| 6 | 0.005443 | 0.003692 | 0.007008 | 0.004341 |

Conclusion: Muon + StackRec improves over plain Muon for 4 and 6 effective
layers (and is close for 2 layers), but it remains clearly below AdamW +
StackRec on this dataset. The best Muon stage is 4 layers; adding the last two
layers slightly decreases validation/test NDCG. Muon also produces much lower
coverage than AdamW in this setup.

### Files
- Config: `configs/beauty_sasrec_stackrec_muon.yaml`
- Run directory: `outputs/stackrec_muon/`
  - `stackrec_results.json`, `stackrec_muon_history.json`,
    `config.yaml`, `{2,4,6}_layers_best_metrics.json`
- Aggregated results: `sasrec_stackrec_muon_results.json`
- Log: `logs/stackrec_muon.log`

### Run command
```bash
CUDA_VISIBLE_DEVICES=0 python run_stackrec.py \
  -cn beauty_sasrec_stackrec_muon \
  hydra.run.dir=outputs/stackrec_muon \
  hydra.job.chdir=false
```

---
Mon Oct 26 2026
---

## Experiment: StackRec with boundary identity auxiliary loss

### Goal
When a new group of 2 layers is stacked below the already trained subnet,
1. add one extra trainable scalar at the output of the last layer of the
   newly added group (the interface between the new lower stack and the
   pretrained upper subnet);
2. add an auxiliary loss that drives the ratio between the output of the new
   lower stack and the representation that the pretrained subnet originally
   received to 1;
3. decay the auxiliary loss coefficient linearly while the stacking
   coefficient of the new group grows.

### Theoretical relation between the two coefficients
Let `alpha` be the forward scale of the newly added lower group (it grows
linearly from 0 to 1 during the ramp) and `lambda` the weight of the identity
loss, with initial value `lambda0`.

To first order the input to the pretrained subnet is
```
h(alpha) = x + alpha * (F(x) - x),
```
where `x` is the representation the pretrained subnet used to receive and
`F` is the new lower stack. The fraction of the representation still coming
from the pretrained model is `1 - alpha`, so the identity constraint should
be weighted by the remaining old-network fraction:
```
lambda(alpha) / lambda0 = 1 - alpha
<=>  alpha + lambda(alpha) / lambda0 = 1
<=>  lambda(alpha) = lambda0 * (1 - alpha).
```
Because `alpha` is ramped linearly, `lambda` decreases linearly and reaches 0
exactly when the new group is fully enabled. This is the "linear
complement" law. The code also supports `lambda = lambda0 * (1 - alpha)^p`
(`power` in the config); `p=1` is the linear law above, `p<1` keeps the
auxiliary weight higher for longer and `p>1` makes it decay faster.

### Implementation
- `src/models/sequence.py`
  - Added `_layer_aux_scalars`: one trainable scalar per layer, initialised
    to 1.0. Inactive scalars have `requires_grad=False`.
  - `enable_layer_aux_scalar(layer_idx, init)`: resets and unfreezes the
    scalar of the last layer of the new group. The scalar stays in the
    network after the stage, so the next stacking stage is continuous.
  - `set_aux_boundary(lower_start, upper_start)` / `clear_aux_boundary()`:
    track the hidden state entering and leaving the new lower group.
  - `_encode_sequence` multiplies every active layer output by its scalar and
    returns the boundary hidden states. The scalar is skipped together with
    its layer when the layer scale is 0.
- `run_stackrec.py`
  - `identity_ratio_loss`: `mean ||g*y - x||^2 / ||x||^2` over valid tokens,
    where `y` is the new lower stack output, `g` its boundary scalar and `x`
    the original pretrained-subnet input (detached; the loss only trains the
    new lower group and `g`). Zero loss means the output/input ratio is 1.
  - `identity_projection_ratio`: diagnostic least-squares ratio
    `mean <g*y, x> / <x, x>` (a plain norm ratio is degenerate because both
    representations are LayerNorm-ed to the same norm).
  - `train_one_epoch`: adds `lambda * identity_ratio_loss` to the main
    cross-entropy and records rec/aux losses and the identity ratio.
  - `stage_progress`, `aux_loss_coefficient`: implement the schedule above.
  - Per-stage history/summary record `aux_alpha`, `aux_loss_coeff`,
    `layer_aux_scalars`, train losses, identity ratio and the boundary/scalar
    indices.
- Configs `configs/beauty_sasrec_stackrec.yaml` and
  `configs/beauty_sasrec_stackrec_muon.yaml`
  - New `stackrec.aux_identity` block: `enabled=true`, `initial_coeff=1.0`,
    `power=1.0`, `eps=1e-8`, `scalar_init=1.0`.

### Validation
- `py_compile` passed for the modified files.
- Model-level smoke test: at `alpha=0` the boundary output equals the input
  exactly; at `alpha=1` the auxiliary loss is finite and the boundary scalar
  receives a non-zero gradient; the stage-2 scalar remains in the network at
  the start of stage 3, so continuity is preserved.
- Full-loop smoke tests (1-2 epochs per stage, `ramp_epochs=2`) for both
  AdamW and Muon: at `alpha=0.5` the run logs `lambda=0.5` and a finite
  `aux_loss`; at `alpha=1` `lambda=0`. Stage-start validation metrics match
  the previous stage exactly. Temporary smoke outputs were removed.
- Note: one smoke run used the default aggregated `results_path` and
  overwrote `sasrec_stackrec_results.json`; it was restored byte-for-byte
  from `outputs/stackrec_adamw/stackrec_results.json`. Subsequent smoke runs
  used temporary result paths.

### Run
Aux is enabled by default in both configs, so explicit result/history paths
are required to avoid overwriting the plain StackRec aggregated files.
```bash
CUDA_VISIBLE_DEVICES=0 python run_stackrec.py \
  -cn beauty_sasrec_stackrec \
  hydra.run.dir=outputs/stackrec_adamw_aux \
  hydra.job.chdir=false \
  stackrec.results_path=sasrec_stackrec_aux_results.json \
  stackrec.history_path=stackrec_aux_history.json
```
```bash
CUDA_VISIBLE_DEVICES=0 python run_stackrec.py \
  -cn beauty_sasrec_stackrec_muon \
  hydra.run.dir=outputs/stackrec_muon_aux \
  hydra.job.chdir=false \
  stackrec.results_path=sasrec_stackrec_muon_aux_results.json \
  stackrec.history_path=stackrec_muon_aux_history.json
```
To reproduce plain StackRec, add `stackrec.aux_identity.enabled=false` and
use separate `results_path`/`history_path` values.

---
Mon Oct 26 2026
---

## Experiment: auxiliary-loss StackRec vs plain StackRec (full runs)

### Protocol
- Same schedule as the plain StackRec runs: 90 / 60 / 60 epochs, 10-epoch
  ramps in stages 2 and 3, identical copy plan, seed 42, batch size 128.
- Auxiliary loss: `initial_coeff=1.0`, `power=1.0`, `scalar_init=1.0`.
- AdamW run: GPU 0. Muon run: first attempt on GPU 1 aborted before training
  with an uncorrectable ECC error; rerun succeeded on GPU 2.
- Outputs:
  - `outputs/stackrec_adamw_aux/`, aggregated
    `sasrec_stackrec_aux_results.json`;
  - `outputs/stackrec_muon_aux/`, aggregated
    `sasrec_stackrec_muon_aux_results.json`;
  - logs: `logs/stackrec_adamw_aux.log`, `logs/stackrec_muon_aux.log`.
- The 2-layer stage is identical by construction (the auxiliary loss is only
  active when a new group is stacked), so all its deltas are exactly zero.

### Results
Cells are `plain / aux (relative delta)`, best complete-gate checkpoint.

**NDCG@10**

| optimizer | layers | val | test |
|---|---:|---|---|
| AdamW | 2 | 0.014714 / 0.014714 (+0.00%) | 0.011958 / 0.011958 (+0.00%) |
| AdamW | 4 | 0.015451 / 0.015920 (+3.04%) | 0.012964 / 0.012934 (-0.23%) |
| AdamW | 6 | 0.016095 / 0.016328 (+1.45%) | 0.013299 / 0.013086 (-1.60%) |
| Muon | 2 | 0.007215 / 0.007215 (+0.00%) | 0.004602 / 0.004602 (+0.00%) |
| Muon | 4 | 0.007884 / 0.007327 (-7.06%) | 0.004518 / 0.004591 (+1.61%) |
| Muon | 6 | 0.007008 / 0.006883 (-1.79%) | 0.004341 / 0.004351 (+0.24%) |

**Recall@10**

| optimizer | layers | val | test |
|---|---:|---|---|
| AdamW | 2 | 0.029630 / 0.029630 (+0.00%) | 0.023380 / 0.023380 (+0.00%) |
| AdamW | 4 | 0.031746 / 0.031958 (+0.67%) | 0.025370 / 0.024251 (-4.41%) |
| AdamW | 6 | 0.033439 / 0.033439 (+0.00%) | 0.025494 / 0.024748 (-2.93%) |
| Muon | 2 | 0.013122 / 0.013122 (+0.00%) | 0.009825 / 0.009825 (+0.00%) |
| Muon | 4 | 0.014392 / 0.013122 (-8.82%) | 0.009203 / 0.009576 (+4.05%) |
| Muon | 6 | 0.012698 / 0.012063 (-5.00%) | 0.009327 / 0.008332 (-10.67%) |

**NDCG@100**

| optimizer | layers | val | test |
|---|---:|---|---|
| AdamW | 2 | 0.032305 / 0.032305 (+0.00%) | 0.021223 / 0.021223 (+0.00%) |
| AdamW | 4 | 0.034820 / 0.035401 (+1.67%) | 0.022722 / 0.022911 (+0.83%) |
| AdamW | 6 | 0.035022 / 0.035418 (+1.13%) | 0.023203 / 0.023030 (-0.74%) |
| Muon | 2 | 0.016025 / 0.016025 (+0.00%) | 0.011337 / 0.011337 (+0.00%) |
| Muon | 4 | 0.017564 / 0.017245 (-1.82%) | 0.011704 / 0.011472 (-1.98%) |
| Muon | 6 | 0.016286 / 0.015772 (-3.15%) | 0.011098 / 0.011201 (+0.93%) |

**Recall@100**

| optimizer | layers | val | test |
|---|---:|---|---|
| AdamW | 2 | 0.122751 / 0.122751 (+0.00%) | 0.071633 / 0.071633 (+0.00%) |
| AdamW | 4 | 0.134392 / 0.135026 (+0.47%) | 0.075737 / 0.075488 (-0.33%) |
| AdamW | 6 | 0.133968 / 0.134603 (+0.47%) | 0.076607 / 0.075861 (-0.97%) |
| Muon | 2 | 0.060106 / 0.060106 (+0.00%) | 0.046139 / 0.046139 (+0.00%) |
| Muon | 4 | 0.065820 / 0.066032 (+0.32%) | 0.047009 / 0.046387 (-1.32%) |
| Muon | 6 | 0.062857 / 0.059259 (-5.72%) | 0.046263 / 0.045144 (-2.42%) |

### Learned boundary scalars
- AdamW, 4 layers: layer 3 scalar = 1.2146.
- AdamW, 6 layers: layer 1 scalar = 1.3315, layer 3 scalar = 1.2248.
- Muon, 4 layers: layer 3 scalar = 1.1516.
- Muon, 6 layers: layer 1 scalar = 1.1481, layer 3 scalar = 1.1814.

All active scalars end above 1, i.e. the network learns to compensate the
sub-unit forward ramp at the stacking boundary while the identity loss is
active.

### Conclusions
- For AdamW, the auxiliary loss improves validation NDCG@10 at 4 and 6
  layers (+3.0% and +1.5%) and validation NDCG@100/Recall@100 as well, but
  test NDCG@10 and Recall@10 become slightly worse (-0.2% and -1.6% for
  NDCG@10; larger for Recall@10). The 6-layer test NDCG@100 is also slightly
  lower. Overall this is a mixed result with a small validation gain and a
  small test loss.
- For Muon, the auxiliary loss is mixed/negative: validation NDCG@10 drops
  at 4 and 6 layers (-7.1%, -1.8%), while test NDCG@10 improves slightly
  (+1.6%, +0.2%). Recall@10 at 6 layers drops noticeably on test (-10.7%).
- The identity constraint is active only during the 10-epoch ramp, after
  which `lambda=0`; this may be too short to regularise the stacked block
  without distorting the fine-tuning phase. Possible next steps: larger
  `initial_coeff`, a slower decay (`power < 1`), a longer `ramp_epochs`, or
  keeping a small residual `lambda` after the ramp.

---

Mon Oct 26 2026
---

## Experiment: hyperbolic heads at StackRec group boundaries

### Goal
Add a hyperbolic (Poincare-ball) next-item head at the output of every group
that StackRec stacks below the already trained subnet, so that the new lower
group is trained with a geometry that can represent item hierarchies.  The
first 2-layer stage remains the plain base model (no group has been added yet),
so it stays directly comparable with the previous StackRec runs.

### Curvature schedule
A Poincare ball of curvature `-c` has radius `1/sqrt(c)`.  If each of the `L`
layers contributes a bounded radial step, the maximal usable radius grows
linearly with `L` (`r_max ~ L * step`).  Numerical stability requires
`sqrt(c) * r_max < 1`, hence
```
c(L) ~ c_ref * (L_ref / L) ** p,   p in [1, 2],
```
i.e. the curvature magnitude must *decrease* as the model gets deeper (the
ball becomes flatter and larger).  A constant curvature eventually saturates
at the boundary, and `p=2` is the conservative choice.  Point of view on the
hierarchy: item leaves live near the ball boundary and high-level/abstract
concepts near the origin; therefore shallow heads (item-like features) should
use stronger curvature, while deep/upper heads use a flatter ball.  The code
therefore uses the absolute depth `d = layer_index + 1` by default:
```
c(d) = c_ref * (d_ref / d) ** power.
```
`depth_mode=cumulative` instead ties `c` to the number of active layers in the
current stage (L = 2, 4, 6), and `schedule=constant` disables the decay.
Curvature can also be learned (`learnable_curvature=true`), but the scheduled
value is still used as initialisation and as a stability prior.

### Implementation
- `src/models/hyperbolic.py`
  - `expmap0(x, c)`: tangent-space exponential map onto the ball.
  - `poincare_distance(u, v, c)`: stable distance computed from
    `||u-v||^2 = ||u||^2 + ||v||^2 - 2<u,v>` (no pairwise difference tensor).
  - `HyperbolicHead`: linear projections of the boundary state and item table,
    exponential maps, negative (squared) distance logits, learned logit scale
    and optional learned curvature.
- `src/models/sequence.py`
  - `add_hyperbolic_head(layer_idx, ...)`, lazy `_hyperbolic_heads`
    `ModuleDict`; heads are created when a stage actually stacks a group.
  - `_encode_sequence` collects the boundary state after the layer scale and
    the auxiliary scalar; `forward` returns `hyperbolic_logits_<layer>` in the
    training output.
  - `set_hyperbolic_heads_trainable` / `get_hyperbolic_curvatures`.
- `run_stackrec.py`
  - `hyperbolic_head_loss`: mean CE over active hyperbolic heads.
  - Stage setup picks `head_layer = max(new_layers)` and the scheduled
    curvature; old heads are frozen by default (`freeze_previous=true`) but
    still provide deep supervision to the shared trunk.
  - Loss coefficient is `loss_coeff * alpha` while the new group ramps in and
    `loss_coeff` afterwards (`warmup=true`); history/summary record the head
    layer, depth, scheduled/learned curvature and per-head losses.
- Configs: `hyperbolic_heads` block added to both StackRec configs (disabled
  by default) and a dedicated
  `configs/beauty_sasrec_stackrec_hyperbolic.yaml` (enabled, absolute-depth
  schedule, `power=2`, `loss_coeff=0.1`, previous heads frozen).

### Protocol
- AdamW, 6-layer SASRec, same 90 / 60 / 60 epochs, 10-epoch ramps, copy plan
  and depth-scaled LRs as the plain/aux StackRec runs. Seed 42, batch 128.
- Heads: stage 4 layers -> layer 3 (`depth=4`, `c=0.25`); stage 6 layers ->
  layer 1 (`depth=2`, `c=1.0`). The layer-3 head is kept (frozen) in stage 6.
- Run time: ~22 min on GPU 0 (GPU 1 is still unusable because of the ECC
  error).

### Results (best complete-gate checkpoint, test split)

| effective layers | plain ndcg@10 | aux ndcg@10 | hyperbolic ndcg@10 | hyp vs plain | hyp vs aux |
|---:|---:|---:|---:|---:|---:|
| 2 | 0.011958 | 0.011958 | 0.011958 | +0.00% | +0.00% |
| 4 | 0.012964 | 0.012934 | 0.012428 | -4.13% | -3.91% |
| 6 | 0.013299 | 0.013086 | 0.013419 | +0.90% | +2.54% |

Validation ndcg@10: 2 layers 0.014714 (all three), 4 layers 0.015657
(hyperbolic; plain 0.015451, aux 0.015920), 6 layers 0.016040 (hyperbolic;
plain 0.016095, aux 0.016328).

Recall@10 at 6 layers: hyperbolic 0.025867 vs plain 0.025494 (+1.46%) and
aux 0.024748 (+4.52%).  NDCG@100 / Recall@100 at 6 layers: 0.023455 /
0.077478 vs plain 0.023203 / 0.076607 and aux 0.023030 / 0.075861.
At 4 layers the hyperbolic head is consistently the weakest
(test NDCG@100 0.022377 vs 0.022722 plain / 0.022911 aux).

The hyperbolic CE decreases from ~9.34 (uniform over ~12k items is 9.4) to
~6.33 at the end of the 6-layer stage; the weighted contribution is
`0.1 * hyp_loss`, while the main rec loss ends at ~6.06.

### Conclusions
- The depth-decaying curvature schedule works mechanically and the 6-layer
  model gains on test NDCG/Recall/coverage relative to both plain and
  auxiliary-identity StackRec (+0.9%/+1.5% NDCG@10 vs plain, +2.5%/+4.5% vs
  aux).  This is the regime where hierarchy-aware geometry is expected to
  help.
- The 4-layer stage is worse, and validation gains do not always transfer to
  test.  The strongest candidate causes are the fixed `loss_coeff=0.1`
  (hyperbolic CE is still high), the relatively strong `c=0.25` at depth 4,
  and the frozen old head still adding loss in stage 6.
- Next sweeps: `loss_coeff` in {0.02, 0.05, 0.1}; `power` in {1, 1.5, 2};
  `depth_mode=cumulative`; `learnable_curvature=true`; and optionally
  `freeze_previous` heads excluded from the loss (diagnostics only).

### Files
- `src/models/hyperbolic.py`
- `src/models/sequence.py`, `run_stackrec.py`
- `configs/beauty_sasrec_stackrec_hyperbolic.yaml`
- `outputs/stackrec_hyperbolic/stackrec_results.json`,
  `outputs/stackrec_hyperbolic/stackrec_hyperbolic_history.json`
- `sasrec_stackrec_hyperbolic_results.json`, `logs/stackrec_hyperbolic.log`

### Run command
```bash
CUDA_VISIBLE_DEVICES=0 python run_stackrec.py \
  -cn beauty_sasrec_stackrec_hyperbolic \
  hydra.run.dir=outputs/stackrec_hyperbolic \
  hydra.job.chdir=false
```

---

Mon Oct 26 2026
---

## Experiment: Lorentz hyperbolic residual on StackRec group boundaries

### Goal
Introduce the hyperbolic geometry *into the hidden representation* of a newly
copied StackRec group instead of only adding an auxiliary hyperbolic
prediction.  Starting from the first copy operation:

1. attach a Lorentz/hyperboloid head to the copied group;
2. make its geometry contribution exactly zero at the moment of stacking by
   multiplying a residual by a gate ramped from 0;
3. ramp the curvature from 0 to 0.2 after the first copy and from 0 to 1 after
   the second copy (final: head over layers 3-4 has c=0.2, head over the last
   copied layers 0-1 has c=1);
4. add the residual with a norm-preserving operation so that initially (and
   throughout the ramp) the norm of the input to the existing pretrained layer
   equals the norm produced by the new group with the hyperbolic head.

### Implementation
- `src/models/hyperbolic.py`
  - `lorentz_expmap0(x, c)`: exponential map at the origin onto the Lorentz
    hyperboloid `-t^2 + ||s||^2 = -1/c`, with a stable `sinhc`.
  - `lorentz_distance(...)`: Minkowski-difference form
    `-c<u,v>_L = 1 + (c/2)<u-v,u-v>_L`, computed through `torch.cdist` so no
    `(num_events, num_classes, d)` tensor is materialised; falls back to the
    Euclidean limit for `c <= 1e-4` (avoids `acosh(1+O(c))/sqrt(c)`).
  - `LorentzResidualHead`: separate item-scoring branch (`proj`, `item_proj`)
    and residual branch (`res_proj`, `res_out`).  The residual is
    `r = (sinhc(sqrt(c)||u||) - 1) * res_out(u)`, i.e. the curvature correction
    of the Lorentz map; it is exactly zero at `c=0`.  `set_curvature` supports
    the stage ramp (also for learnable curvature).
- `src/models/sequence.py`
  - `_lorentz_heads` ModuleDict and `_lorentz_gates` (python floats, no GPU
    sync).  `add_lorentz_head`, `set_lorentz_gate`, `set_lorentz_curvature`,
    `get_lorentz_gates`, `get_lorentz_curvatures`,
    `set_lorentz_heads_trainable`.
  - `_apply_lorentz_residual`: returns the input bitwise unchanged when
    gate=0; otherwise rescales the residual to `||h||`, adds `gate * r` and
    renormalises the sum back to `||h||`.  The residual is applied after the
    layer scale and the boundary auxiliary scalar, before the next layer, in
    both training and inference; the pre-residual state is used for the
    auxiliary CE logits.
- `run_stackrec.py`
  - `hyp_res_cfg` handling, per-stage curvature targets
    (`curvature_targets`), and separate `residual_ramp_epochs` /
    `curvature_ramp_epochs`.
  - `ramp_fraction`: linear 0 -> 1 that is *exactly zero* at stage epoch 0
    (the existing `stage_progress` starts at `1/ramp`).
  - gate and curvature are set before each training epoch; old Lorentz heads
    keep their final curvature (frozen by default, `freeze_previous=true`);
    the stage-start sanity check sets the new head to gate=0, c=0.
  - best-complete selection additionally requires the gate and curvature ramps
    to be complete; gates are restored from the selected checkpoint.
  - history/summary record the head layer, target/current curvature,
    curvature fraction, residual gate, all gates/curvatures and the Lorentz
    CE loss.
- `configs/beauty_sasrec_stackrec_hyperbolic_residual.yaml`
  - enables `stackrec.hyperbolic_residual`, disables the old Poincare heads,
    sets `curvature_targets: {4_layers: 0.2, 6_layers: 1.0}`, ramps of 10
    epochs, `loss_coeff=0.1`, separate result/history files.

### Verification
- Unit-level checks (CPU):
  - hyperboloid constraint `-t^2 + ||s||^2 = -1/c` holds for c in
    {0.05, 0.2, 1}; distance is symmetric, self-distance is zero and the
    `c -> 0` limit equals the Euclidean distance;
  - `LorentzResidualHead.residual` is exactly zero at c=0;
  - `_apply_lorentz_residual` is a bitwise identity at gate=0 (even at c>0),
    is exactly the identity at c=0 with gate=1, and preserves the norm of `h`
    for gate>0;
  - end-to-end training forward/backward populates gradients of the Lorentz
    residual branch and produces finite logits/loss.
- Short end-to-end smoke run (2/3/3 epochs, ramps of 2, temporary outputs,
  removed afterwards), on Beauty:
  - stage-start continuity is exact: 4-layer start val ndcg@10 = 2-layer best
    (0.002281), 6-layer start = 4-layer best (0.003470);
  - stage 4 logs (gate, c): (0, 0) -> (0.5, 0.1) -> (1, 0.2);
  - stage 6 logs (gate, c): (0, 0) -> (0.5, 0.5) -> (1, 1.0);
  - during stage 6 the layer-3 head remains at c=0.2 and the layer-1 head
    reaches c=1.0, matching the requested final state.
- The first smoke attempt OOMed because the Lorentz distance built an
  `(events, classes, d)` tensor; it was rewritten with `torch.cdist` and the
  rerun succeeded.

No full-length training was run yet; the config is ready for the standard
90/60/60 protocol.

### Files
- `src/models/hyperbolic.py`, `src/models/sequence.py`, `run_stackrec.py`
- `configs/beauty_sasrec_stackrec_hyperbolic_residual.yaml`
- `RUN.txt` updated with the run instructions and knob list.

### Run command
```bash
CUDA_VISIBLE_DEVICES=0 python run_stackrec.py \
  -cn beauty_sasrec_stackrec_hyperbolic_residual \
  hydra.run.dir=outputs/stackrec_hyperbolic_residual \
  hydra.job.chdir=false
```
