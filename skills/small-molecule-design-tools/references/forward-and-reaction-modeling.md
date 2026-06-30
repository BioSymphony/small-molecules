# Forward Reaction & Mechanism Prediction

Models that go **forward**: reactants (+ conditions) → products, or reactants → **mechanism** (elementary steps / electron movement). Use these to **validate generated routes** — a predicted retro disconnection that doesn't forward-predict back to the target is suspect (the "round-trip" check; see [synthesizability-scoring.md](synthesizability-scoring.md)).

> Readiness varies sharply here. **DeepMech** is fully usable (code + released weights); **ProPreT5** is MIT code but ships no weights; **ChemDual** has code but no released model; **Reactron** is paper-only with no public code.

## DeepMech — *mechanism prediction; fully usable*

> Interpretable graph-based framework predicting **complete reaction mechanisms** (elementary steps) via atom/bond attention guided by Templates of Mechanistic Operations (TMOps).

- **Repo:** https://github.com/alhqlearn/DeepMech (IIT Bombay).
- **License:** **MIT** code; **weights + data on Zenodo dual CC-BY-4.0 / MIT** — all permissive, commercial OK with attribution.
- **Paper:** *DeepMech: A Machine Learning Framework for Chemical Reaction Mechanism Prediction*, arXiv:2509.15872 (2025). Preprint.
- **Weights:** Zenodo DOI 10.5281/zenodo.20305780 (`DeepMech_Dataset_Model.zip`, ~45 MB: ReactMech splits + pretrained models). Reported 98.98% elementary-step / 95.94% full-CRM accuracy.
- **Install / run:** conda py3.6 + `rdkit-pypi` + PyTorch/**CUDA 11.3** + **DGL** (`dgl-cuda11.3`) + DGLLife; download Zenodo zip into `./models` and `./data`; `python NewCRM_Prediction.py`.
- **Deps / hardware:** RDKit, PyTorch, DGL/DGLLife. GPU (CUDA 11.3) required. ⚠️ legacy Python 3.6 / CUDA 11.3 stack — may need care on modern drivers.
- **Use it when:** you want mechanism-level prediction (elementary steps, arrow-style attention) with a real, runnable model. Best-supported tool in this file.

## ReaDISH — *reaction-property prediction (yield / selectivity), 2026 — code + weights*

> Permutation-invariant reaction-property model: extends DRFP fingerprints into continuous embeddings + geometry-structure attention to predict **yield / selectivity / conversion** robustly under atom-order permutation (+8.76% R² robustness). Fills the **yield/condition** gap this file otherwise lacks (RXNGraphormer does yield only as a side task).

- **Repo:** `Meteor-han/ReaDISH` — **MIT**; ships a checkpoint (`checkpoint/last.ckpt`).
- **Paper:** *Reaction Prediction via Interaction Modeling of Symmetric Difference Shingle Sets*, arXiv:2511.06356 (v1 2025-11, v3 2026-02).
- **Maintenance:** pushed Dec 2025 (quiet but complete).
- **Commercial:** ✅ MIT code + released checkpoint — the only verified-new reaction-property model with code **and** weights. Use it when you need a yield/selectivity predictor rather than product prediction.

## ProPreT5 / BRS — *SMARTS-template product prediction (MIT code, no weights)*

> T5 chemistry LM for **product prediction** that directly handles and applies **SMARTS reaction templates** (template-based and template-free settings). **BRS = "Broad Reaction Set"** — a new dataset of 20 hand-written generic SMARTS templates introduced for more realistic evaluation, plus the first SMARTS-augmentation strategy.

- **Repo:** https://github.com/DerinOzer/ProPreT5 (University of Angers).
- **License:** **MIT** code. ⚠️ **No pretrained weights released** — training-from-scratch pipeline only. `data/` is partial; you may need to assemble BRS/USPTO-MIT splits yourself.
- **Paper:** *A Transformer Model for Predicting Chemical Products from Generic SMARTS Templates with Data Augmentation*, arXiv:2503.05810 (v3 2025-09). Reported 85.8% on BRS.
- **Install / run:** `cd training && python main.py` (single-GPU) or SLURM/DDP multi-GPU; config edited in code, not via CLI flags.
- **Deps / hardware:** PyTorch (CUDA), HF transformers/datasets, sacrebleu, RDKit. GPU required.
- **Use it when:** you want SMARTS-template-aware forward prediction and are willing to train. BRS is a genuine eval contribution.

## ChemDual — *dual-task retro+forward LLM (code only, weights "coming soon")*

> LLaMA-3.1-8B enhanced with a multi-scale tokenizer and **dual-task learning** treating forward prediction and retrosynthesis as coupled recombination/fragmentation, plus molecule/reaction understanding.

- **Repo:** https://github.com/JacklinGroup/ChemDual.
- **License:** **Apache-2.0** code. Weights are listed as coming soon; `ollama pull ChemDual` is aspirational. Only small eval JSONs in `dataset/`; the 4.4M instruction set is unreleased. Base LLaMA-3.1-8B carries Meta's restrictive Community License.
- **Paper:** *Enhancing Chemical Reaction and Retrosynthesis Prediction with LLM and Dual-task Learning*, IJCAI 2025 (arXiv:2505.02639).
- **Install / run:** conda py3.10; `llamafactory-cli train conf/train_ChemDual.yaml`; you supply the base model and (currently missing) training data — so **end-to-end reproduction isn't possible today**.
- **Use it when:** watch for the weight release. Not usable as a model yet — see [watchlist.md](watchlist.md). Also documented in [chemical-language-models.md](chemical-language-models.md).

## Reactron — *electron/arrow-pushing prediction* ⚠️ paper only, no code

> Claims to be the first **electron-based** ML model for general reaction prediction, sequentially predicting electron movement / arrow-pushing for 100%-valid products.

- **Repo:** ⚠️ **None.** Verified absent from the authors' org (`snu-micc`) and personal accounts; no code/data link in the paper. **Paper-only — not a runnable tool.** See [watchlist.md](watchlist.md).
- **Paper:** *Predicting Chemical Reaction Outcomes Based on Electron Movements Using Machine Learning*, arXiv:2503.10197 (2025), Jung group (SNU).
- **Don't confuse with:** the same group's **MechFinder** (which *is* public, different tool), or the separate **FlowER** (Nature 2025), the JACS polar-reaction model, or the arrow-pushing LLM preprint arXiv:2512.05722.

## Also do forward prediction (documented in single-step file)

- **ReactionT5v2** — `sagawa/ReactionT5v2-forward` (and `-forward-USPTO_MIT`), MIT, HF weights.
- **RXNGraphormer** — forward + retro + yield/selectivity in one pretrained model, MIT.

See [singlestep-retrosynthesis.md](singlestep-retrosynthesis.md) for both.

## Choosing

- **Forward validation of generated routes (round-trip):** ReactionT5v2-forward (easiest, MIT, HF weights) or RXNGraphormer.
- **Mechanism-level prediction:** **DeepMech** (only fully-runnable option).
- **SMARTS-template product prediction:** ProPreT5 (train it yourself).
- **Not ready:** ChemDual (no weights), Reactron (no code).
