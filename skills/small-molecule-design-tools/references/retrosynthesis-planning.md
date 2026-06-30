# Retrosynthesis & Route Planning

Tools that take a **target you already have** and find a synthetic route back to purchasable starting materials (and, for ASKCOS, predict conditions and forward feasibility). Contrast with [synthesizable-generation.md](synthesizable-generation.md), where the molecule and its route are generated together.

Use these as **route-planning baselines and scorers**, and to validate that a generated analog is actually makeable.

This file covers **multi-step planners / frameworks** (and RetroDFM-R, a reasoning LLM). Related files:
- **[singlestep-retrosynthesis.md](singlestep-retrosynthesis.md)** — the single-step prediction models that planners call per node (ReactionT5v2, RXNGraphormer, GDiffRetro, RetroDiT, ConRetroBert, TempRe).
- **[agentic-retrosynthesis.md](agentic-retrosynthesis.md)** — LLM/agentic planners (DeepRetro, Synthelite, LLM-Syn-Planner).
- **[synthesizability-scoring.md](synthesizability-scoring.md)** — round-trip / RetroScore to validate routes.

---

## AiZynthFinder — *the default open retrosynthesis baseline*

> Fast, robust, MIT-licensed retrosynthetic route planner. Default engine is neural-network-guided **Monte Carlo Tree Search (MCTS)** that recursively decomposes a target into purchasable precursors.

- **Repo:** https://github.com/MolecularAI/aizynthfinder (AstraZeneca / MolecularAI). ~848 stars, very active.
- **License:** **MIT** — README explicitly states "restrictions to use by non-academics: none." Cleanest license in this whole compilation.
- **Papers:** *AiZynthFinder: a fast, robust and flexible open-source software for retrosynthetic planning*, J. Cheminform. 2020, 12:70 (DOI 10.1186/s13321-020-00472-1); v4 update J. Cheminform. 2024, 16:57 (DOI 10.1186/s13321-024-00860-x).
- **Weights:** public **USPTO** expansion/policy model (~45,500 templates) + filter policy + stock, fetched via `download_public_data <folder>` (hosted on Figshare; writes a `config.yml`). AstraZeneca's internal ~180k-template model (Reaxys/Pistachio/ELN) is **not** released. Extra models via the ModelZoo plugin (`PTorrenPeraire/modelsmatter_modelzoo`).
- **Inputs → outputs:** target SMILES → ranked retrosynthetic routes/trees ending in purchasable building blocks, each with scores (state score, #steps, fraction-in-stock). Template-based **and** template-free expansion, plus a filter policy to prune unrealistic reactions.
- **Install:**
  ```bash
  conda create "python>=3.10,<3.13" -n aizynth-env && conda activate aizynth-env
  python -m pip install aizynthfinder[all]
  download_public_data my_folder          # fetch public model + stock
  ```
  Interfaces: `aizynthcli` (batch) and `aizynthapp` (Jupyter GUI). Linux/Windows/macOS.
- **Deps:** RDKit, NN frameworks (TF/Keras historically, PyTorch/ONNX in later versions). Stock benchmarked on **eMolecules** (~80% coverage) and **ZINC** (~60%). GPU optional.
- **Maintenance:** Very active — **v4.4.1, Dec 2025**.
- **Use it when:** you need a dependable, commercial-friendly route-planning baseline or a scorer for "is this makeable, and how?" The public USPTO model is freely usable. **Start here for retrosynthesis.**

---

## ASKCOS — *full synthesis-planning suite*

> Open-source computer-aided synthesis planning suite covering one-step retrosynthesis, multi-step route search, forward reaction-outcome prediction, condition recommendation, and feasibility scoring. More than a route finder — an end-to-end planning system.

- **Repo:** **v2 (current)** https://gitlab.com/mlpds_mit/askcosv2 (entry repo `askcos2_core`); **v1 (legacy, archived)** https://github.com/ASKCOS/ASKCOS (frozen at v0.4.1, Feb 2021).
- **Org:** MIT (Coley, Jensen, Green groups), maintained by the **MLPDS consortium**; originated under DARPA Make-It.
- **License:** ⚠️ **mixed** — **v2 code MIT**, most v2 models MIT, but the **Reaxys template-relevance model is CC BY-NC 4.0 (non-commercial)** and **CAS models are MLPDS-member-only**. Legacy v1 code is MPL-2.0 with CC BY-NC-SA data. For commercial use, stay on v2 and the USPTO/MIT-licensed models.
- **Paper:** *ASKCOS: Open-Source, Data-Driven Synthesis Planning*, Acc. Chem. Res. 2025, 58(11):1764–1775 (DOI 10.1021/acs.accounts.5c00155); preprint arXiv:2501.01835.
- **Models:** four one-step retro models run side by side — **Template-relevance** (template-based), **Transformer** and **Graph2SMILES** (template-free), **RetroSim** (retrieval) — plus enzymatic (BKMS) and ring-breaker variants. Bundled and seeded during deployment.
- **Inputs → outputs:** target SMILES → ranked routes/trees to purchasable blocks, with per-step condition recommendations and forward-feasibility scores. Two UIs: Interactive Path Planner (IPP) and automated Tree Builder.
- **Deploy:**
  ```bash
  # Local (intended path): clone askcos2_core, then
  bash deploy.sh deploy        # multi-container Docker; seed databases after
  ```
  **Heavy:** ≥8 cores (16 preferred), 64 GB RAM (128 GB preferred). Hosted public service: https://askcos.mit.edu (free; the Tree Builder caps search effort per job — no published per-user quota found, so batch use favors local deployment).
- **Deps:** RDKit, PyTorch, Docker/Compose (microservices), reaction-template libraries (USPTO/Pistachio/Reaxys/CAS), building-block stock sets.
- **Maintenance:** v2 actively developed on GitLab; v1 frozen since 2021.
- **Use it when:** you need **more than routes** — condition recommendation, forward-prediction, feasibility — or a richer multi-model planner. For simple batch route-finding, AiZynthFinder is lighter to stand up.

---

## Syntheseus — *benchmarking/search framework (pluggable models)*

> Microsoft Research library that standardizes **pluggable single-step models + multi-step search algorithms** so they can be compared fairly. A platform, not a single model — the right tool for evaluating "which retro setup works best for my targets."

- **Repo:** https://github.com/microsoft/syntheseus (MIT, ~198 stars). Sibling `microsoft/retrochimera` is a separate model.
- **License:** **MIT** code. Ships no first-party weights — it wraps external single-step models, whose licenses vary; benchmark data (USPTO/PaRoutes) carries upstream terms.
- **Paper:** *Re-evaluating retrosynthesis algorithms with Syntheseus*, Faraday Discuss. 2025, 256:568 (DOI 10.1039/D4FD00093E); arXiv:2310.19796.
- **Install / run:** `pip install "syntheseus[all]"` or the full conda env. Library/CLI; no hosted service. PyTorch (pinned torch 2.2.2 in current env), RDKit; GPU for neural models.
- **Maintenance:** active (v0.7.2, 2026-01).
- **I/O:** target SMILES + a single-step model + a stock set → routes/search trees + benchmarking metrics.
- **Use it when:** you want to **benchmark / mix-and-match** single-step models and search algorithms rather than commit to one planner. Used under LLM-Syn-Planner.

## SynPlanner — *end-to-end CASP (curation → rules → MCTS), with GUI*

> Full CASP pipeline: reaction-data curation, atom-mapping, reaction-rule extraction, retro-model training, and **MCTS planning** guided by GNNs (rule prediction + synthesizability scoring). Lab. de Chémoinformatique, Strasbourg.

- **Repo:** https://github.com/Laboratoire-de-Chemoinformatique/SynPlanner (MIT, ~54 stars).
- **License:** **MIT** code; pretrained presets via the CLI downloader (no separate restrictive license observed).
- **Paper:** *SynPlanner: An End-to-End Tool for Synthesis Planning*, JCIM 2025, 65(1):15 (DOI 10.1021/acs.jcim.4c02004).
- **Install / run:** `pip install SynPlanner`; `synplan download_preset --preset synplanner-gps …`. **Hosted GUI** on HF Spaces (`Laboratoire-De-Chemoinformatique/SynPlanner`) + Colab tutorials. CLI + GUI.
- **Maintenance:** active (v1.5.0, 2026-05). RDKit, PyTorch, GNNs; planning runs on CPU, GPU helps for training.
- **I/O:** target SMILES (+ rules/blocks/checkpoints) → routes, HTML route reports, clustered/scored plans.
- **Use it when:** you want a **train-your-own**, end-to-end CASP toolkit (custom rules + building blocks) with a ready GUI — more configurable than AiZynthFinder, lighter than ASKCOS.

## InterRetro — *search-free multi-step planner (RL)* ⚠️ no license

> "Interactive" (not interpretable) Retrosynthesis: learns a worst-path value function in a tree-structured MDP via weighted self-imitation, so a single-step model can emit **full routes without inference-time tree search**.

- **Repo:** https://github.com/MianchuWang/InterRetro (Warwick). ⚠️ **No LICENSE file — all rights reserved**; dataset is Google-Drive-only. Not safely reusable until licensed — see [watchlist.md](watchlist.md).
- **Paper:** *Retrosynthesis Planning via Worst-path Policy Optimisation in Tree-structured MDPs*, NeurIPS 2025 (arXiv:2509.10504).
- **Notes:** uses **Graph2Edits** as the single-step backbone; eMolecules stock; benchmarks Retro*-190 / ChEMBL-1000 / GDB17-1000. No pretrained checkpoints (training code only).
- **Use it when:** research interest in search-free route generation. Blocked for reuse by the missing license.

---

## RetroDFM-R — *reasoning LLM for single-step retrosynthesis*

> Reasoning-driven LLM for single-step (chainable to multi-step) retrosynthesis, trained with large-scale **reinforcement learning** (DAPO) using chemically verifiable rewards. Emits explicit chain-of-thought alongside predicted reactant SMILES.

- **Repo:** https://github.com/OpenDFM/RetroDFM-R (X-LANCE Lab, Shanghai Jiao Tong University).
- **License:** ⚠️ **three different licenses across artifacts** — **code Apache-2.0**, **weights `OpenDFM/RetroDFM-R-8B` are GPL-3.0** (copyleft), inference **dataset MIT**. The base model is **ChemDFM-v1.5-8B → Llama3-8B**, which adds the **Llama 3 Community License** on top. Reconcile the full GPL-3.0 + Llama-3 stack before any commercial deployment — this is *not* a clean permissive model despite the Apache-2.0 code.
- **Paper:** *Reasoning-Driven Retrosynthesis Prediction with LLMs via Reinforcement Learning*, arXiv:2507.17448 (2025). Preprint only. Reports top-1 65.0% on USPTO-50K.
- **Weights:** HF `OpenDFM/RetroDFM-R-8B` (primary, 8B) and `OpenDFM/RetroDFM-R-v0-8B`; test data `OpenDFM/retrodfm-R-inference`.
- **Inputs → outputs:** product SMILES → chain-of-thought reasoning + predicted reactant SMILES (single-step; chain for multi-step).
- **Install:**
  ```bash
  conda create -n retrodfmR python=3.10 && pip install -r requirements.txt   # vLLM + CUDA
  cd inference && bash eval.sh        # beam search + test-time augmentation
  # or load via transformers: AutoModelForCausalLM.from_pretrained("OpenDFM/RetroDFM-R-8B", ...)
  ```
  Recommended generation: temperature 0.6, top-k 20, top-p 0.9. **No hosted service** — self-hosted GPU inference only.
- **Deps:** PyTorch, HF transformers, **vLLM** (CUDA GPU), RDKit. Training data: PubChem, USPTO-FULL/50K, distilled DeepSeek-R1 traces.
- **Maintenance:** ⚠️ Single research release — weights Nov 2025, ~23 stars.
- **Use it when:** you want **interpretable, reasoning-style single-step predictions** or to experiment with an LLM/RL approach, and you can host an 8B model and accept the GPL-3.0 + Llama-3 license stack. More prediction-oriented than route-search-oriented; pair with AiZynthFinder/ASKCOS for full multi-step trees.

---

## RetroCast & SynthArena — *route benchmarking & validation (2026)*

> Standardizes the outputs of 10+ planners into one schema for statistically rigorous (bootstrapped-CI, stratified) **route comparison**, plus an interactive web app for inspecting routes. Complements **Syntheseus** (single-step + search benchmarking) with a focus on **route quality/validity** — it shows that "solvability" scores can mask chemical invalidity, and surfaces a "complexity cliff" where search beats sequence models on short routes but loses on long ones.

- **Repo:** `ischemist/project-procrustes` (RetroCast core) + `ischemist/syntharena` (web platform) — both **MIT**.
- **Weights:** none (it's infrastructure; wraps others' models).
- **Paper:** *Procrustean Bed for AI-Driven Retrosynthesis*, arXiv:2512.07079 (Morgunov & Batista, Yale, 2025-12).
- **Maintenance:** very active (pushed Jun 2026).
- **Use it when:** you want rigorous, validity-aware route comparison/validation alongside Syntheseus — directly relevant to the "is this route real?" layer ([synthesizability-scoring.md](synthesizability-scoring.md)).

## Choosing a multi-step planner

- **Fastest to stand up, cleanest license:** **AiZynthFinder** (MIT, USPTO model, pip install). Default baseline.
- **Full suite (conditions, forward, feasibility):** **ASKCOS** (heavy Docker deploy, or use the hosted service).
- **Benchmark/compare many single-step models + search algos:** **Syntheseus**.
- **Rigorously compare/validate *route quality* (validity, not just solvability):** **RetroCast / SynthArena** (MIT, 2026).
- **Train your own end-to-end CASP (custom rules/blocks) with a GUI:** **SynPlanner**.
- **LLM-assisted / constraint-steerable planning:** see [agentic-retrosynthesis.md](agentic-retrosynthesis.md) (DeepRetro, Synthelite).
- **Research-only / blocked:** InterRetro (no license).

All of these consume a **single-step model** per node — pick that separately from [singlestep-retrosynthesis.md](singlestep-retrosynthesis.md), and validate output routes with a round-trip check ([synthesizability-scoring.md](synthesizability-scoring.md)).
