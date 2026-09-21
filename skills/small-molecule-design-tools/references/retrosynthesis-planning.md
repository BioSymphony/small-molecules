# Retrosynthesis and Route Planning

These tools search for synthetic routes from a target molecule to purchasable
starting materials. ASKCOS can also predict reaction conditions and forward
feasibility. In contrast, the tools in
[synthesizable-generation.md](synthesizable-generation.md) generate a molecule
and its route together.

Use these tools as route-planning baselines, route scorers, and makeability
checks. This file covers multi-step planners and RetroDFM-R. For one-step
prediction models, see
[singlestep-retrosynthesis.md](singlestep-retrosynthesis.md). For LLM-assisted
planners, see [agentic-retrosynthesis.md](agentic-retrosynthesis.md). For
round-trip and route-aware scoring, see
[synthesizability-scoring.md](synthesizability-scoring.md).

---

## AiZynthFinder — *the default open retrosynthesis baseline*

> MIT-licensed retrosynthetic route planner. Its default engine uses a neural
> network to guide Monte Carlo tree search and recursively decompose a target
> into purchasable precursors.

- **Repository:** https://github.com/MolecularAI/aizynthfinder (AstraZeneca and MolecularAI).
- **License:** **MIT**. The README separately states that use is not limited by academic status.
- **Papers:** *AiZynthFinder: a fast, robust and flexible open-source software for retrosynthetic planning*, J. Cheminform. 2020, 12:70 (DOI 10.1186/s13321-020-00472-1); v4 update J. Cheminform. 2024, 16:57 (DOI 10.1186/s13321-024-00860-x).
- **Weights:** public **USPTO** expansion/policy model (~45,500 templates) plus a filter policy and stock, fetched with `download_public_data <folder>` from Figshare. Extra models are available through the ModelZoo plugin (`PTorrenPeraire/modelsmatter_modelzoo`).
- **Inputs and outputs:** target SMILES → ranked retrosynthetic routes/trees ending in purchasable building blocks, each with scores (state score, #steps, fraction-in-stock). Template-based **and** template-free expansion, plus a filter policy to prune unrealistic reactions.
- **Install:**
  ```bash
  conda create "python>=3.10,<3.13" -n aizynth-env && conda activate aizynth-env
  python -m pip install aizynthfinder[all]
  download_public_data my_folder          # fetch public model + stock
  ```
  Interfaces: `aizynthcli` (batch) and `aizynthapp` (Jupyter GUI). Linux/Windows/macOS.
- **Dependencies:** RDKit, NN frameworks (TF/Keras historically, PyTorch/ONNX in later versions). Stock benchmarked on **eMolecules** (~80% coverage) and **ZINC** (~60%). GPU optional.
- **Maintenance:** Release **v4.4.1** was published in December 2025.
- **Use it when:** you need an open baseline or a route-derived makeability score. The public USPTO model and stock package provide the documented starting configuration.

## RENKIN — *route planning and route auditing (MIT; v0.47.0)*

> Rust-based retrosynthesis engine that searches reaction-template routes and audits route exports from RENKIN, AiZynthFinder, Syntheseus, and SynPlanner.

- **Repository:** https://github.com/kent-tokyo/renkin — the project also publishes Rust, Python, and WebAssembly packages.
- **License:** **MIT** (repository `LICENSE`).
- **Release:** On 2026-08-30, [**v0.47.0**](https://github.com/kent-tokyo/renkin/releases/tag/v0.47.0) was the most recent public tag.
- **Inputs and outputs:** target SMILES plus reaction templates → candidate routes; an existing planner route → an audit report covering structural integrity, stock coverage, and declared-reaction forward replay.
- **Weights:** no neural model weights are required for the core engine or audit path.
- **Limits:** the README says RENKIN does not predict yields, calibrated experimental success probabilities, or side reactions, and does not search the literature automatically.
- **Use it when:** you need a lightweight route engine or a tool-neutral audit pass alongside a neural planner.

---

## ASKCOS — *synthesis-planning suite*

> Open-source computer-aided synthesis-planning suite that includes one-step
> retrosynthesis, multi-step route search, forward reaction-outcome prediction,
> condition recommendation, and feasibility scoring.

- **Repository:** **v2** https://gitlab.com/mlpds_mit/askcosv2 (entry repository `askcos2_core`); **v1 (legacy, archived)** https://github.com/ASKCOS/ASKCOS (frozen at v0.4.1, Feb 2021).
- **Org:** MIT (Coley, Jensen, Green groups), maintained by the **MLPDS consortium**; originated under DARPA Make-It.
- **License:** ⚠️ **mixed** — v2 code is MIT; the Reaxys template-relevance model is labeled **CC BY-NC 4.0**; CAS models are limited to MLPDS members. Legacy v1 code is MPL-2.0 with CC BY-NC-SA data. Check the selected model and data record separately.
- **Paper:** *ASKCOS: Open-Source, Data-Driven Synthesis Planning*, Acc. Chem. Res. 2025, 58(11):1764–1775 (DOI 10.1021/acs.accounts.5c00155); preprint arXiv:2501.01835.
- **Models:** four one-step retro models run side by side — **Template-relevance** (template-based), **Transformer** and **Graph2SMILES** (template-free), **RetroSim** (retrieval) — plus enzymatic (BKMS) and ring-breaker variants. Bundled and seeded during deployment.
- **Inputs and outputs:** target SMILES → ranked routes/trees to purchasable blocks, with per-step condition recommendations and forward-feasibility scores. Two UIs: Interactive Path Planner (IPP) and automated Tree Builder.
- **Deploy:**
  ```bash
  # Local (intended path): clone askcos2_core, then
  bash deploy.sh deploy        # multi-container Docker; seed databases after
  ```
  **Hardware:** ≥8 cores (16 preferred), 64 GB RAM (128 GB preferred). Hosted public service: https://askcos.mit.edu.
- **Dependencies:** RDKit, PyTorch, Docker/Compose (microservices), reaction-template libraries (USPTO/Pistachio/Reaxys/CAS), building-block stock sets.
- **Maintenance:** v2 is developed on GitLab; v1 has been frozen since 2021.
- **Use it when:** you need condition recommendation, forward prediction, and feasibility scoring in one planning suite. For route search without those components, use AiZynthFinder.

---

## Syntheseus — *benchmarking/search framework (pluggable models)*

> Microsoft Research library that combines pluggable single-step models with
> multi-step search algorithms for benchmark comparisons. It is a framework,
> not a standalone model.

- **Repository:** https://github.com/microsoft/syntheseus (MIT). [RetroChimera](singlestep-retrosynthesis.md#retrochimera) supplies a compatible single-step model; Syntheseus supplies multi-step search and evaluation.
- **License:** **MIT** code. Ships no first-party weights — it wraps external single-step models, whose licenses vary; benchmark data (USPTO/PaRoutes) carries upstream terms.
- **Paper:** *Re-evaluating retrosynthesis algorithms with Syntheseus*, Faraday Discuss. 2025, 256:568 (DOI 10.1039/D4FD00093E); arXiv:2310.19796.
- **Install and run:** `pip install "syntheseus[all]"` or the full conda environment. Library/CLI; no hosted service. The project environment file pins PyTorch 2.2.2; neural models can use a GPU.
- **Maintenance:** active — release [**v0.8.0**](https://github.com/microsoft/syntheseus/releases/tag/v0.8.0) was published on **2026-08-03**. The release adds a RetroChimera model class, forward-model filtering in the search CLI, resumable single-step evaluations, product/reactant filtering, and stereo removal.
- **Inputs and outputs:** target SMILES + a single-step model + a stock set → routes/search trees + benchmarking metrics.
- **Use it when:** you need to compare single-step models and search algorithms within one framework. LLM-Syn-Planner uses Syntheseus.

## SynPlanner — *CASP pipeline with curation, rules, MCTS, and GUI*

> CASP pipeline covering reaction-data curation, atom mapping, reaction-rule
> extraction, retro-model training, and MCTS planning guided by GNNs.

- **Repository:** https://github.com/Laboratoire-de-Chemoinformatique/SynPlanner (MIT).
- **License:** **MIT** code; pretrained presets are downloaded from the project's separate data record.
- **Paper:** *SynPlanner: An End-to-End Tool for Synthesis Planning*, JCIM 2025, 65(1):15 (DOI 10.1021/acs.jcim.4c02004).
- **Install and run:** `pip install SynPlanner`; `synplan download_preset --preset synplanner-gps --save_to synplan_data`. The project also publishes an HF Spaces GUI and Colab tutorials. CLI + GUI.
- **Maintenance:** active — release [**v1.7.0**](https://github.com/Laboratoire-de-Chemoinformatique/SynPlanner/releases/tag/v1.7.0) was published on **2026-08-25**. The linked data record is `Laboratoire-De-Chemoinformatique/SynPlanner-data`. RDKit, PyTorch, and GNNs are used; planning runs on CPU, while training benefits from GPU.
- **Inputs and outputs:** target SMILES (+ rules/blocks/checkpoints) → routes, HTML route reports, clustered/scored plans.
- **Use it when:** you need reaction-data curation, custom rules, MCTS planning, and a GUI in one toolkit.

## InterRetro — *search-free multi-step planner (RL)* ⚠️ no license

> InterRetro learns a worst-path value function in a tree-structured MDP
> through weighted self-imitation. A single-step model then emits full routes
> without inference-time tree search.

- **Repository:** https://github.com/MianchuWang/InterRetro (Warwick). ⚠️ The repository has no `LICENSE` file; the dataset is linked from Google Drive.
- **Paper:** *Retrosynthesis Planning via Worst-path Policy Optimisation in Tree-structured MDPs*, NeurIPS 2025 (arXiv:2509.10504).
- **Notes:** uses **Graph2Edits** as the single-step backbone; eMolecules stock; benchmarks Retro*-190 / ChEMBL-1000 / GDB17-1000. No pretrained checkpoints (training code only).
- **Use it when:** you are studying search-free route generation; the repository's license status is incomplete.

---

## RetroDFM-R — *reasoning LLM for single-step retrosynthesis*

> Reasoning-driven LLM for single-step retrosynthesis that can chain across
> steps. It was trained with reinforcement learning (DAPO) using chemically
> verifiable rewards and emits a reasoning trace with predicted reactant SMILES.

- **Repository:** https://github.com/OpenDFM/RetroDFM-R (X-LANCE Lab, Shanghai Jiao Tong University).
- **License:** ⚠️ The repository code is **MIT**. The Hugging Face `OpenDFM/RetroDFM-R-8B` model card labels the checkpoint **Apache-2.0** and identifies **Qwen/Qwen3-8B** as its base model. The base-model terms and the separate inference dataset record must be reviewed independently.
- **Paper:** *Reasoning-Driven Retrosynthesis Prediction with LLMs via Reinforcement Learning*, arXiv:2507.17448 (2025). Preprint. The repository reports top-1 **60.4%** on USPTO-50K without augmentation.
- **Weights:** HF `OpenDFM/RetroDFM-R-8B` (8B) and `OpenDFM/RetroDFM-R-v0-8B`; test data `OpenDFM/retrodfm-R-inference`.
- **Inputs and outputs:** product SMILES → chain-of-thought reasoning + predicted reactant SMILES (single-step; chain for multi-step).
- **Install:**
  ```bash
  conda create -n retrodfmR python=3.10 && pip install -r requirements.txt   # vLLM + CUDA
  cd inference && bash eval.sh        # beam search + test-time augmentation
  # or load via transformers: AutoModelForCausalLM.from_pretrained("OpenDFM/RetroDFM-R-8B", ...)
  ```
  Recommended generation: temperature 0.6, top-k 20, top-p 0.9. **No hosted service** — self-hosted GPU inference only.
- **Dependencies:** PyTorch, HF transformers, **vLLM** (CUDA GPU), RDKit. Training data: PubChem, USPTO-FULL/50K, distilled DeepSeek-R1 traces.
- **Maintenance:** The repository was updated on **2026-08-25**; the public release is the 8B Qwen3-based model.
- **Use it when:** you want reasoning-style single-step predictions or to study an LLM/RL approach. The model card warns that outputs can be incorrect or misleading and calls for domain-expert review. Pair it with AiZynthFinder or ASKCOS for full multi-step trees.

---

## RetroCast & SynthArena — *route benchmarking & validation (2026)*

> Standardizes outputs from more than 10 planners into one schema for
> stratified route comparisons with bootstrap confidence intervals. It also
> provides a web app for route inspection. The paper reports that solvability
> scores can miss chemical invalidity and that search and sequence models
> perform differently on short and long routes.

- **Repository:** `ischemist/project-procrustes` (RetroCast core) + `ischemist/syntharena` (web platform) — both **MIT**.
- **Weights:** None; the software evaluates outputs from other models.
- **Paper:** *Procrustean Bed for AI-Driven Retrosynthesis*, arXiv:2512.07079 (Morgunov & Batista, Yale, 2025-12).
- **Maintenance:** The repository received commits in June 2026.
- **Use it when:** you need validity-aware route comparisons alongside Syntheseus.

## Choosing a multi-step planner

For output checks, see [Validate Routes](#validate-routes).

- **Open baseline:** **AiZynthFinder** (MIT code, public USPTO model, pip install).
- **Route planning plus audit reports:** **RENKIN** (MIT; v0.47.0).
- **Synthesis planning with conditions, forward prediction, and feasibility scoring:** **ASKCOS**.
- **Compare single-step models and search algorithms:** **Syntheseus**.
- **Compare route validity and solvability:** **RetroCast / SynthArena** (MIT,
  2026).
- **Train a custom CASP pipeline with custom rules, building blocks, and a GUI:** **SynPlanner**.
- **LLM-assisted / constraint-steerable planning:** see [agentic-retrosynthesis.md](agentic-retrosynthesis.md) (DeepRetro, Synthelite).
- **Repository without a listed license:** InterRetro.

Each planner calls a single-step model at each node. Select that model from [singlestep-retrosynthesis.md](singlestep-retrosynthesis.md) and validate route outputs with a round-trip check ([synthesizability-scoring.md](synthesizability-scoring.md)).

## Validate Routes

Record the planner version, single-step model, stock snapshot, search limits,
and molecule-standardization settings with each result. Use the same target
structures and stock when comparing planners, and report differences in models
or search budgets.

Classify the result after inspecting the exported route:

| Result | Check |
|---|---|
| Target in stock | The target itself matches the selected stock; no reaction is required. |
| Complete route to stock | At least one reaction connects the target to terminal compounds that all match the selected stock. |
| Partial route | The exported route contains reactions but has unresolved terminal compounds. |
| No route within budget | Search completed within its limits without exporting a route. |
| Execution or export failure | Model loading, search, or route serialization failed; record the failed step. |

Check terminal compounds against the stock independently of the planner's
success flag. In [SynPlanner 1.7.0](https://github.com/Laboratoire-de-Chemoinformatique/SynPlanner/blob/v1.7.0/synplan/chem/precursor.py),
`is_building_block` accepts molecules at or below `min_mol_size` without a stock
lookup; its default threshold is six atoms. Specify whether stock matching
preserves stereochemistry, isotopes, and salt forms.

Review each reaction for bond changes, reagents, and stereochemical requirements.
Use [forward prediction and round-trip checks](synthesizability-scoring.md)
alongside that review. A complete route to stock establishes graph connectivity
and stock coverage; reaction feasibility requires separate checks.
