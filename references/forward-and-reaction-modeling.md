# Forward Reaction and Mechanism Prediction

Forward models predict products from reactants and optional reaction conditions.
Mechanism models predict elementary steps or electron movement. Use a forward
model to test whether proposed retrosynthetic precursors reproduce the target.
This test is called a round-trip check; see
[synthesizability-scoring.md](synthesizability-scoring.md).

> Release status differs among these tools: **DeepMech** publishes code and weights; **ProPreT5** publishes MIT code without weights; **ChemDual** publishes code without a released model; **Reactron** is paper-only.

## DeepMech — *mechanism prediction with released weights*

> Graph-based framework that predicts elementary reaction steps with atom and
> bond attention guided by Templates of Mechanistic Operations.

- **Repository:** https://github.com/alhqlearn/DeepMech (IIT Bombay).
- **License:** **MIT** code. The Zenodo record lists separate **CC BY 4.0** and **MIT** terms for the released data and model files.
- **Paper:** *DeepMech: A Machine Learning Framework for Chemical Reaction Mechanism Prediction*, arXiv:2509.15872 (2025). Preprint.
- **Weights:** Zenodo DOI 10.5281/zenodo.20305780 (`DeepMech_Dataset_Model.zip`, ~45 MB: ReactMech splits + pretrained models). Reported 98.98% elementary-step / 95.94% full-CRM accuracy.
- **Install and run:** conda py3.6 + `rdkit-pypi` + PyTorch/**CUDA 11.3** + **DGL** (`dgl-cuda11.3`) + DGLLife; download Zenodo zip into `./models` and `./data`; `python NewCRM_Prediction.py`.
- **Dependencies and hardware:** RDKit, PyTorch, DGL, and DGLLife. A CUDA 11.3 GPU is required. The project pins Python 3.6 and CUDA 11.3, which may require compatibility work with newer drivers.
- **Use it when:** you need mechanism-level prediction with a published checkpoint and elementary-step outputs.

## ReaDISH — *reaction-property prediction (yield / selectivity), 2026 — code + weights*

> The model predicts yield, selectivity, and conversion under atom-order
> permutation. RXNGraphormer lists yield as a side task.

- **Repository:** `Meteor-han/ReaDISH` — **MIT**; ships a checkpoint (`checkpoint/last.ckpt`).
- **Paper:** *Reaction Prediction via Interaction Modeling of Symmetric Difference Shingle Sets*, arXiv:2511.06356 (v1 2025-11, v3 2026-02).
- **Maintenance:** The last recorded repository push was in December 2025.
- **Use it when:** you need a yield, selectivity, or conversion predictor rather than product prediction. The repository publishes MIT code and a checkpoint; training data terms are separate.

## ProPreT5 / BRS — *SMARTS-template product prediction (MIT code, no weights)*

> T5 chemistry language model for product prediction that applies SMARTS
> reaction templates in template-based and template-free settings. The Broad
> Reaction Set contains 20 hand-written generic SMARTS templates for evaluation.
> The work also introduces a SMARTS-augmentation strategy.

- **Repository:** https://github.com/DerinOzer/ProPreT5 (University of Angers).
- **License:** **MIT** code. No pretrained weights are released, so you must train the model. The `data/` directory is incomplete; assemble the BRS and USPTO-MIT splits before training.
- **Paper:** *A Transformer Model for Predicting Chemical Products from Generic SMARTS Templates with Data Augmentation*, arXiv:2503.05810 (v3 2025-09). Reported 85.8% on BRS.
- **Install and run:** `cd training && python main.py` (single-GPU) or SLURM/DDP multi-GPU; edit the configuration in code rather than with CLI flags.
- **Dependencies and hardware:** PyTorch (CUDA), HF transformers/datasets, sacrebleu, RDKit. GPU required.
- **Use it when:** you need SMARTS-template-aware forward prediction and can train from the public code. The paper introduces BRS as its evaluation dataset.

## ChemDual — *dual-task retro and forward LLM (code only; no released weights)*

> LLaMA-3.1-8B enhanced with a multi-scale tokenizer and **dual-task learning** treating forward prediction and retrosynthesis as coupled recombination/fragmentation, plus molecule/reaction understanding.

- **Repository:** https://github.com/JacklinGroup/ChemDual.
- **License:** **Apache-2.0** code. The README lists weights as pending and links
  only small evaluation JSON files in `dataset/`;
  the 4.4M instruction set is unreleased. The Llama-3.1-8B base model has
  Meta's Community License.
- **Paper:** *Enhancing Chemical Reaction and Retrosynthesis Prediction with LLM and Dual-task Learning*, IJCAI 2025 (arXiv:2505.02639).
- **Install and run:** conda py3.10; `llamafactory-cli train conf/train_ChemDual.yaml`.
  The repository does not include its training data, so the public files cannot
  reproduce training and full evaluation.
- **Use it when:** you are studying the dual-task architecture. The repository does not include a released checkpoint or training data.

## Reactron — *electron/arrow-pushing prediction* ⚠️ paper only, no code

> Claims to be the first **electron-based** ML model for general reaction prediction, sequentially predicting electron movement / arrow-pushing for 100%-valid products.

- **Repository:** No public code or data link is listed; the paper is the only release.
- **Paper:** *Predicting Chemical Reaction Outcomes Based on Electron Movements Using Machine Learning*, arXiv:2503.10197 (2025), Jung group (SNU).
- **Related projects:** MechFinder and FlowER are separate methods.

## Also do forward prediction (documented in single-step file)

- **ReactionT5v2** — `sagawa/ReactionT5v2-forward` (and `-forward-USPTO_MIT`), MIT, HF weights.
- **RXNGraphormer** — forward + retro + yield/selectivity in one pretrained model, MIT.

See [singlestep-retrosynthesis.md](singlestep-retrosynthesis.md) for both.

## Choosing

- **Forward validation of generated routes (round-trip):** ReactionT5v2-forward (MIT-labeled Hugging Face weights) or RXNGraphormer.
- **Mechanism-level prediction:** **DeepMech** (published checkpoint and data record).
- **SMARTS-template product prediction:** ProPreT5 (train from the public code).
- **Release status:** ChemDual has no released weights; Reactron has no public code.
