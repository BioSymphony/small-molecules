# Single-Step Retrosynthesis Models

Models that predict the **immediate precursors of one reaction**: product SMILES → ranked reactant SMILES. They are the per-node engine that multi-step planners ([multistep-retrosynthesis.md](retrosynthesis-planning.md)) call repeatedly. Benchmarked mostly on **USPTO-50K top-k accuracy**.

Three families appear here: **template-based** (retrieve/rank a reaction template, then apply it), **template-free** (generate reactants directly), and **semi-template** (find the reaction center, then complete synthons).

> Benchmark numbers below are **author-claimed** unless noted. Several 2026 entries are brand-new with unproven results.

---

## ReactionT5v2 — *easiest to run; HF, MIT, multi-task*

> T5 text-to-text transformer pretrained on the Open Reaction Database, served as task-specific checkpoints for forward prediction, **retrosynthesis**, and yield. The retro checkpoint is the single-step model.

- **Repo:** https://github.com/sagawatatsuya/ReactionT5v2 (Sagawa & Kojima). Predecessor `ReactionT5` (v1) also exists — use v2.
- **License:** **MIT** (code + HF weights). Training data is ORD (CC-BY-SA 4.0 — matters only if you redistribute the data). Commercial use OK.
- **Paper:** *ReactionT5: a pre-trained transformer model for accurate chemical reaction prediction with limited data*, J. Cheminform. 2025, DOI 10.1186/s13321-025-01075-4.
- **Weights:** HuggingFace — `sagawa/ReactionT5v2-retrosynthesis` (ORD) and `sagawa/ReactionT5v2-retrosynthesis-USPTO_50k` (fine-tuned); also `-forward`, `-forward-USPTO_MIT`, `-yield`; base `sagawa/CompoundT5`.
- **Benchmark:** USPTO-50K fine-tuned **top-1 71.2%, top-5 88.2%** (the ORD-only model is weak on USPTO-50K, top-1 13.8% — use the fine-tuned variant).
- **Install / run:** `pip install rdkit torch transformers==4.40.2 tokenizers==0.19.1 datasets accelerate sentencepiece`; load with `AutoModelForSeq2SeqLM`, beam search; repo has `prediction.py` for batch CSV. HF Spaces demo exists.
- **Deps / hardware:** RDKit, PyTorch, transformers (pinned). Pure transformers — no DGL/PyG. CPU or GPU.
- **Maintenance:** Lightly active (last push 2025-12; ~45 stars).
- **Use it when:** you want a drop-in, permissively licensed single-step retro model with published HF weights and no graph-library setup.

## RXNGraphormer — *unified GNN+Transformer, forward & retro*

> Pretrained framework (GNN + Transformer over ~13M reactions) for cross-task reaction performance prediction (yield, selectivity) **and** synthesis planning, covering both forward and retrosynthesis.

- **Repo:** https://github.com/licheng-xu-echo/RXNGraphormer.
- **License:** **MIT** (code). Weights+data bundled on **Figshare** (DOI 10.6084/m9.figshare.28356077) — check the Figshare record's license before redistributing weights.
- **Paper:** *A unified pre-trained deep learning framework for cross-task reaction performance prediction and synthesis planning*, Nature Machine Intelligence 2025, 7:1561 (s42256-025-01098-4). A 2026 Nature MI Reusability Report independently assessed it.
- **Install / run:** `conda create -n rxngraphormer python=3.8`; `pip install rxngraphormer -f https://data.pyg.org/whl/torch-1.12.0+cu113.html`. Pip-installable; notebooks provided.
- **Deps / hardware:** Python 3.8, PyTorch 1.12.1+cu113, **PyTorch Geometric 2.3.1**, RDKit. GPU (CUDA 11.3) expected.
- **Maintenance:** Very active (pushed 2026-06; ~48 stars). Exact USPTO-50K top-1 is in the paper/SI.
- **Use it when:** you want one model spanning forward + retro + yield/selectivity, and don't mind a PyG/CUDA-pinned environment.

## GDiffRetro — *semi-template, 3D diffusion*

> Two-stage **semi-template** method: identify the reaction center using a molecular graph plus its **dual graph**, then complete synthons → reactants with a conditional **3D diffusion** model.

- **Repo:** https://github.com/sunshy-1/GDiffRetro.
- **License:** **MIT** (code). Checkpoints via a SharePoint link in the README (no explicit weights license). USPTO-50K data.
- **Paper:** *GDiffRetro: Retrosynthesis Prediction with Dual Graph Enhanced Molecular Representation and Diffusion Generation*, AAAI 2025 (arXiv:2501.08001).
- **Install / run:** conda + RDKit + `torch==1.11.0+cu113`, `torch-cluster`/`torch-scatter`, OpenBabel, a **modified torchdrug** bundled in `./stage1`. Multi-stage training scripts.
- **Deps / hardware:** RDKit, PyTorch 1.11+cu113, PyG, OpenBabel, wandb. GPU (CUDA 11.3) required. Heavier env to set up.
- **Maintenance:** Published but dormant (last push ~2025-06; ~24 stars). Beats prior semi-template SOTA on USPTO-50K (numbers in paper).
- **Use it when:** you specifically want a semi-template/3D-diffusion approach. Otherwise ReactionT5v2/RXNGraphormer are easier.

## TempRe — *templates as sequence generation* ⚠️ no public code

> Reframes reaction templates as **sequence generation** (generate the template token-by-token, can produce novel templates), evaluated on single-step **and** direct multi-step retrosynthesis with MCTS.

- **Repo:** ⚠️ **None located** (not in the Schwaller/LIAC org; no code/data link in the paper). Treat as **preprint-only** — see [watchlist.md](watchlist.md).
- **License:** code none (no repo); the manuscript is CC BY-SA 4.0.
- **Paper:** *TempRe: Template generation for single and direct multi-step retrosynthesis*, Nguyen-Xuan-Vu, Armstrong, Jončev, Schwaller (EPFL), arXiv:2507.21762 (2025).
- **Notes:** seq2seq Transformer on OpenNMT (4 layers, 8 heads, emb 384). Benchmarks use **PaRoutes**, not USPTO-50K (so its top-k aren't comparable to the others here). No weights.
- **Use it when:** conceptually interesting for novel-template generation; not runnable today.

---

## Brand-new (2026) — verified real, but unproven

## RetroDiT — *order-aware discrete flow matching* (weights pending)

> Template-free model using **reaction-center-guided atom ordering** as a positional inductive bias plus **discrete flow matching** (generates in 20–50 steps vs ~500 for diffusion).

- **Repo:** https://github.com/zzhnomorebugs/RetroDiT (created 2026-05; repo claims ICML 2026).
- **License:** **MIT** (code). ⚠️ **Weights not released yet** (docs are a placeholder) — you must train from scratch.
- **Paper:** *Order Matters in Retrosynthesis: Structure-aware Generation via Reaction-Center-Guided Discrete Flow Matching*, arXiv:2602.13136 (2026).
- **Benchmark (claimed):** USPTO-50K top-1 **61.2%** (predicted centers) / **71.1%** (oracle); USPTO-Full top-1 51.3% / 63.4%. Claims a 280K-param ordered model matches a 65M unordered one.
- **Deps / hardware:** PyTorch, RDKit; distributed/multi-GPU training env. Python 3.11.
- **Use it when:** research interest in atom-ordering / flow-matching. Not production-ready (no weights, numbers unreproduced).

## ConRetroBert — *template retrieval + listwise re-ranking* ⚠️ no license

> Template-based model reframed as **dense product↔template retrieval** then **listwise re-ranking**: dual-encoder, contrastive pretraining, multi-positive ranking with hard negatives, EMA-stabilized template encoder.

- **Repo:** https://github.com/JahidBasher/ConRetroBert (created 2026-05). ⚠️ **No LICENSE file — all rights reserved**, despite the paper saying "code available." Weights/data via Google Drive (also unlicensed).
- **Paper:** *ConRetroBert: EMA Stabilized Dual Encoders for Template-Based Single-Step Retrosynthesis*, arXiv:2605.12736 (2026); states "Submitted to NeurIPS 2026" (under review).
- **Benchmark (claimed):** USPTO-50K top-1 **62.4%** (75.4% when fine-tuned from a USPTO-Full checkpoint).
- **Deps / hardware:** PyTorch 2.7.1 (CUDA 12.8), RDKit, **FAISS-GPU**, PyTorch Lightning. GPU required.
- **Use it when:** only after a license appears. Real code, but not legally reusable as-is.

---

## RxnNano — *compact 0.5B dual-task LLM (forward + single-step retro)* (weights pending)

> A 0.5B model claiming to beat fine-tuned >7B LLMs and domain baselines (+23.5% top-1, no test-time augmentation) via latent chemical-consistency + atom-map permutation invariance — a tiny, cheap counterpoint to the 8B RetroDFM-R.

- **Repo:** `rlisml/RxnNano` — **MIT**. ⚠️ **weights NOT released** (training/eval code only — you must train it).
- **Paper:** *Training Compact LLMs … via Hierarchical Curriculum Learning*, arXiv:2603.02215 (2026-02).
- **Maintenance:** pushed May 2026.
- **Commercial:** ✅ MIT code; ⚠️ no checkpoints yet (train-your-own). Attractive if a tiny/cheap dual-task model matters.

## Also single-step, documented elsewhere

- **RetroDFM-R** — 8B reasoning LLM for single-step retro (CoT + reactants), top-1 65.0% USPTO-50K. Code Apache-2.0, **weights GPL-3.0** + Llama-3 base. See its card in [retrosynthesis-planning.md](retrosynthesis-planning.md) / [chemical-language-models.md](chemical-language-models.md).
- **ReactionT5v2 / RXNGraphormer** also do forward prediction — see [forward-and-reaction-modeling.md](forward-and-reaction-modeling.md).

## Picking one

- **Just want it to work, permissive license:** ReactionT5v2 (HF, MIT, fine-tuned USPTO-50K weights).
- **Want forward + retro + yield in one model:** RXNGraphormer.
- **Want interpretable reasoning:** RetroDFM-R (mind the GPL-3.0 weights).
- **Research into newest methods:** RetroDiT / GDiffRetro (semi-template / flow / diffusion) — expect to train.
- **Avoid for reuse until licensed:** ConRetroBert, TempRe (no usable/licensed code).
