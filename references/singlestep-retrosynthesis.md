# Single-Step Retrosynthesis Models

These models predict the immediate precursors of one reaction. They accept a
product SMILES string and return ranked reactant SMILES strings. Multi-step
planners call them at each search node. Most published benchmarks report
USPTO-50K top-k accuracy.

Three families appear here: **template-based** (retrieve/rank a reaction template, then apply it), **template-free** (generate reactants directly), and **semi-template** (find the reaction center, then complete synthons).

> Unless noted, the benchmark numbers in this reference are author claims. Several 2026 entries have limited independent evaluation.

---

## ReactionT5v2 — *HF multi-task model*

> T5 text-to-text transformer pretrained on the Open Reaction Database, served as task-specific checkpoints for forward prediction, **retrosynthesis**, and yield. The retro checkpoint is the single-step model.

- **Repository:** https://github.com/sagawatatsuya/ReactionT5v2 (Sagawa & Kojima). Predecessor `ReactionT5` (v1) also exists — use v2.
- **License:** **MIT** repository code and Hugging Face weight records. Training data is the Open Reaction Database (ORD), whose record carries **CC BY-SA 4.0** terms; data terms are separate from the code and weights.
- **Paper:** *ReactionT5: a pre-trained transformer model for accurate chemical reaction prediction with limited data*, J. Cheminform. 2025, DOI 10.1186/s13321-025-01075-4.
- **Weights:** HuggingFace — `sagawa/ReactionT5v2-retrosynthesis` (ORD) and `sagawa/ReactionT5v2-retrosynthesis-USPTO_50k` (fine-tuned); also `-forward`, `-forward-USPTO_MIT`, `-yield`; base `sagawa/CompoundT5`.
- **Benchmark:** USPTO-50K fine-tuned **top-1 71.2%, top-5 88.2%**; the ORD-only model reports **13.8% top-1** on USPTO-50K.
- **Install and run:** `pip install rdkit torch transformers==4.40.2 tokenizers==0.19.1 datasets accelerate sentencepiece`; load with `AutoModelForSeq2SeqLM`, beam search; repository has `prediction.py` for batch CSV. HF Spaces demo exists.
- **Dependencies and hardware:** RDKit, PyTorch, transformers (pinned). Pure transformers — no DGL/PyG. CPU or GPU.
- **Maintenance:** The last recorded repository push was 2025-12-02.
- **Use it when:** you need a single-step retro model with published Hugging Face weights and no graph-library setup.

## RetroChimera

RetroChimera combines template-localization and SMILES-generation models to
predict ranked precursors for a product molecule. Use it as a single-step
predictor or connect it to [Syntheseus](retrosynthesis-planning.md#syntheseus--benchmarkingsearch-framework-pluggable-models)
for multi-step search with a selected starting-material stock.

- **Repository and paper:** [Microsoft RetroChimera](https://github.com/microsoft/retrochimera);
  [Chemist-aligned retrosynthesis by ensembling diverse inductive bias models](https://www.nature.com/articles/s41586-026-11160-9)
  (Nature, 2026; [methods preprint](https://arxiv.org/abs/2412.05269)).
- **Code and checkpoints:** [MIT code](https://github.com/microsoft/retrochimera/blob/bf5ec59eec9ef32911d5167bf7528e3648622be1/LICENSE).
  The Figshare records for [Pistachio](https://figshare.com/articles/software/RetroChimera_Pistachio_/30591107),
  [USPTO-50K](https://figshare.com/articles/software/RetroChimera_USPTO-50K_/30601718),
  and [USPTO-FULL](https://figshare.com/articles/software/RetroChimera_USPTO-FULL_/30597563)
  checkpoints each state MIT. Check training-data access and redistribution
  terms separately.
- **Inputs and outputs:** product SMILES through a Syntheseus `Molecule`;
  ranked precursor sets with model probabilities. The Python entry point is
  `RetroChimeraModel`, with `model_dir` pointing to an extracted checkpoint.
- **Setup:** use the upstream [environment file](https://github.com/microsoft/retrochimera/blob/bf5ec59eec9ef32911d5167bf7528e3648622be1/environment.yml)
  before `pip install retrochimera==1.3.0`. It pins Python 3.9.7, PyTorch 2.2.2
  with CUDA 12.1, RDKit 2023.09.6, and PyG 2.5.2. For USPTO-50K, install
  `"retrochimera[graphium]==1.3.0"`. The package requires Syntheseus 0.8.0 or later.
- **Inference settings:** the defaults target the Pistachio checkpoint.
  For USPTO benchmark reproduction, use the paper's Extended Data Tables 3
  and 4. Upstream recommends at most 5 to 10 predictions per input unless
  stronger filtering is applied.
- **Inference and validation:** the [upstream usage notes](https://github.com/microsoft/retrochimera/tree/bf5ec59eec9ef32911d5167bf7528e3648622be1#checkpoints-for-retrochimera-1)
  recommend consensus mode and reaction-feasibility filtering. Record the
  ensemble mode, checkpoint, proposal limit, and filters actually used; these
  settings determine which predictions reach the planner. Review the reaction
  chemistry independently. After multi-step search, apply the separate
  [route and stock checks](retrosynthesis-planning.md#validate-routes).
- **Release:** checked on 2026-09-21 at commit
  [`bf5ec59`](https://github.com/microsoft/retrochimera/tree/bf5ec59eec9ef32911d5167bf7528e3648622be1).
  [Version 1.3.0](https://github.com/microsoft/retrochimera/blob/bf5ec59eec9ef32911d5167bf7528e3648622be1/CHANGELOG.md)
  adds consensus ensembling, fine-tuning, and the forward-model interface.

## RXNGraphormer — *unified GNN+Transformer, forward & retro*

> Pretrained framework (GNN + Transformer over ~13M reactions) for cross-task reaction performance prediction (yield, selectivity) **and** synthesis planning, covering both forward and retrosynthesis.

- **Repository:** https://github.com/licheng-xu-echo/RXNGraphormer.
- **License:** **MIT** (code). Weights+data bundled on **Figshare** (DOI 10.6084/m9.figshare.28356077) — check the Figshare record's license before redistributing weights.
- **Paper:** *A unified pre-trained deep learning framework for cross-task reaction performance prediction and synthesis planning*, Nature Machine Intelligence 2025, 7:1561 (s42256-025-01098-4). A 2026 Nature MI Reusability Report independently assessed it.
- **Install and run:** `conda create -n rxngraphormer python=3.8`; `pip install rxngraphormer -f https://data.pyg.org/whl/torch-1.12.0+cu113.html`. Pip-installable; notebooks provided.
- **Dependencies and hardware:** Python 3.8, PyTorch 1.12.1+cu113, **PyTorch Geometric 2.3.1**, RDKit. GPU (CUDA 11.3) expected.
- **Maintenance:** The repository was updated on 2026-08-24. Exact USPTO-50K top-1 results are reported in the paper and supplementary information.
- **Use it when:** you need one model spanning forward prediction, retrosynthesis, yield, and selectivity; the environment pins PyG and CUDA versions.

## GDiffRetro — *semi-template, 3D diffusion*

> Two-stage **semi-template** method: identify the reaction center using a molecular graph plus its **dual graph**, then complete synthons → reactants with a conditional **3D diffusion** model.

- **Repository:** https://github.com/sunshy-1/GDiffRetro.
- **License:** **MIT** (code). Checkpoints via a SharePoint link in the README (no explicit weights license). USPTO-50K data.
- **Paper:** *GDiffRetro: Retrosynthesis Prediction with Dual Graph Enhanced Molecular Representation and Diffusion Generation*, AAAI 2025 (arXiv:2501.08001).
- **Install and run:** conda + RDKit + `torch==1.11.0+cu113`, `torch-cluster`/`torch-scatter`, OpenBabel, a **modified torchdrug** bundled in `./stage1`. Multi-stage training scripts.
- **Dependencies and hardware:** RDKit, PyTorch 1.11+cu113, PyG, OpenBabel, wandb. GPU (CUDA 11.3) required. The environment has more dependencies than ReactionT5v2 or RXNGraphormer.
- **Maintenance:** The last recorded repository push was in June 2025; the paper reports higher results than prior semi-template methods on USPTO-50K.
- **Use it when:** you specifically want a semi-template and 3D-diffusion approach. For a transformer-based alternative, use ReactionT5v2 or RXNGraphormer.

## TempRe — *templates as sequence generation* ⚠️ no public code

> Reframes reaction templates as sequence generation: it generates templates
> token by token and can produce novel templates. The paper evaluates
> single-step and direct multi-step retrosynthesis with MCTS.

- **Repository:** ⚠️ **None located** (not in the Schwaller/LIAC org; no code/data link in the paper). It remains **preprint-only** — see [watchlist.md](watchlist.md).
- **License:** no repository or model license is available; the manuscript is CC BY-SA 4.0.
- **Paper:** *TempRe: Template generation for single and direct multi-step retrosynthesis*, Nguyen-Xuan-Vu, Armstrong, Jončev, Schwaller (EPFL), arXiv:2507.21762 (2025).
- **Notes:** seq2seq Transformer on OpenNMT (4 layers, 8 heads, emb 384). Benchmarks use **PaRoutes**, not USPTO-50K, so the top-k values are not directly comparable with USPTO-50K results in this reference. No weights.
- **Use it when:** you are studying novel-template generation. No public implementation or weights are listed.

---

## 2026 additions with limited independent evaluation

## RetroDiT — *order-aware discrete flow matching* (weights pending)

> Template-free model that combines reaction-center-guided atom ordering with
> discrete flow matching. The paper reports generation in 20 to 50 steps,
> compared with approximately 500 steps for diffusion.

- **Repository:** https://github.com/LOGO-CUHKSZ/RetroDiT — the former `zzhnomorebugs/RetroDiT` URL redirects to this repository.
- **License:** **MIT** code. The documentation does not list a released project checkpoint; the training code expects a supplied or newly trained model.
- **Paper:** *Order Matters in Retrosynthesis: Structure-aware Generation via Reaction-Center-Guided Discrete Flow Matching*, arXiv:2602.13136 (2026).
- **Benchmark (claimed):** USPTO-50K top-1 **61.2%** (predicted centers) / **71.1%** (oracle); USPTO-Full top-1 51.3% / 63.4%. Claims a 280K-param ordered model matches a 65M unordered one.
- **Dependencies and hardware:** PyTorch, RDKit; distributed/multi-GPU training env. Python 3.11.
- **Maintenance:** The repository was updated on 2026-08-19.
- **Use it when:** you are evaluating atom-ordering and discrete flow-matching ideas. The reported numbers remain author claims until independently reproduced.

## ConRetroBert — *template retrieval + listwise re-ranking* ⚠️ no license

> Template-based model reframed as **dense product↔template retrieval** then **listwise re-ranking**: dual-encoder, contrastive pretraining, multi-positive ranking with hard negatives, EMA-stabilized template encoder.

- **Repository:** https://github.com/JahidBasher/ConRetroBert (created 2026-05). ⚠️ The repository has no `LICENSE` file. The paper links code, while weights and data are linked from Google Drive without a separate license notice.
- **Paper:** *ConRetroBert: EMA Stabilized Dual Encoders for Template-Based Single-Step Retrosynthesis*, arXiv:2605.12736 (2026); states "Submitted to NeurIPS 2026" (under review).
- **Benchmark (claimed):** USPTO-50K top-1 **62.4%** (75.4% when fine-tuned from a USPTO-Full checkpoint).
- **Dependencies and hardware:** PyTorch 2.7.1 (CUDA 12.8), RDKit, **FAISS-GPU**, PyTorch Lightning. GPU required.
- **Use it when:** you are studying the retrieval and re-ranking method and have resolved the repository and artifact terms.

---

## RxnNano — *multi-task LLM for forward and single-step retro* (weights pending)

> Training and evaluation code for retrosynthesis, retrosynthesis with reaction class, and forward reaction prediction, with mapped and unmapped SMILES variants.

- **Repository:** https://github.com/rlisml/RxnNano — **MIT**. ⚠️ No pretrained checkpoint is shown in the repository; the README's example fine-tunes `Qwen/Qwen2.5-7B-Instruct`.
- **Paper:** *Training Compact LLMs … via Hierarchical Curriculum Learning*, arXiv:2603.02215 (2026-02).
- **Maintenance:** The repository was updated on 2026-05-25.
- **Use it when:** you want to inspect or extend a compact reaction-prediction training recipe and can provide the base model, datasets, and checkpoint.

## Also single-step, documented elsewhere

- **RetroDFM-R** — 8B reasoning LLM for single-step retro (reasoning trace + reactants); the README reports 60.4% top-1 on USPTO-50K without augmentation. MIT repository code, an Apache-2.0-tagged Qwen3-based checkpoint, and separate base and data terms. See its cards in [retrosynthesis-planning.md](retrosynthesis-planning.md) and [chemical-language-models.md](chemical-language-models.md).
- **ReactionT5v2 / RXNGraphormer** also do forward prediction — see [forward-and-reaction-modeling.md](forward-and-reaction-modeling.md).

## Picking one

- **Ensemble predictor with Syntheseus integration:** RetroChimera, with
  checkpoint-specific settings and reaction filtering.
- **Released single-step checkpoint:** ReactionT5v2 (Hugging Face, MIT labels, fine-tuned USPTO-50K weights).
- **Want forward + retro + yield in one model:** RXNGraphormer.
- **Want reasoning traces:** RetroDFM-R (review the checkpoint, base-model, and data terms).
- **2026 methods with limited evaluation:** RetroDiT and GDiffRetro; both require training from the public code.
- **License and repository gaps:** ConRetroBert has no listed repository license; TempRe has no public repository.
