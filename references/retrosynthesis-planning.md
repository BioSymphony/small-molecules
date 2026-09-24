# Retrosynthesis and Route Planning

These tools search for synthetic routes from a target molecule to a declared
starting-material inventory. ASKCOS can also predict reaction conditions and
forward feasibility. In contrast, the tools in
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

### The ZINC stock is a selected snapshot

[ZINC](https://pmc.ncbi.nlm.nih.gov/articles/PMC1360656/) is a UCSF database for virtual
screening that includes purchasable compounds and supplier information.
[ZINC20](https://pubmed.ncbi.nlm.nih.gov/33118813/) and
[ZINC22](https://pubmed.ncbi.nlm.nih.gov/36790087/) expanded the searchable
space, including make-on-demand compounds. Neither name identifies the
starting-material list used by a particular route search.

ZINC22 includes both make-on-demand space and [in-stock informer
layers](https://wiki.docking.org/index.php?title=ZINC22:Layers). The layer guide
lists `22a` for Enamine in-stock compounds and `22g` for a ZINC20 in-stock
informer set. It reports a May 2023 last rebuild for `22g` but does not give
an actual last-refresh date for `22a`. Record the selected layer and its
verified snapshot or check date; confirm present availability with the supplier.

The [2020 AiZynthFinder paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7672904/)
reports an example stock of **17,422,831** ZINC compounds. Its authors selected
tranches with molecular weight up to 250 Da, logP up to 3.5, and ZINC reactivity
labels “standard” or “reactive.” The linked [data release](https://figshare.com/articles/dataset/AiZynthFinder_a_fast_robust_and_flexible_open-source_software_for_retrosynthetic_planning/12334577)
dates the stock to 17 April 2020; its [file metadata](https://api.figshare.com/v2/articles/12334577)
names `zinc_stock_17_04_20.hdf5`. That file is a filtered snapshot of ZINC,
separate from the full database and current supplier catalogs.
In the paper's 100-target illustration, adding Enamine building blocks enabled
routes for ten additional targets. Route closure depends on the chosen stock.

ZINC's [guidance for earlier releases](https://wiki.docking.org/index.php/ZINC) describes
screening-focused filters that can omit highly reactive building blocks, and its
[data terms](https://wiki.docking.org/index.php?title=UCSF_ZINC_License)
restrict redistribution of major portions. Check target-relevant ingredient
coverage and current supplier information before using a ZINC-derived stock as
a purchasing boundary.

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
- **Maintenance:** release [**v0.9.0**](https://github.com/microsoft/syntheseus/releases/tag/v0.9.0) was published on **2026-09-23**. Its [changelog](https://github.com/microsoft/syntheseus/blob/v0.9.0/CHANGELOG.md) records ForwardChimeraDeNovo integration and an update to RetroChimera 1.3.0. Version 0.8.0 added RetroChimera integration and proposal filtering.
- **Inputs and outputs:** target SMILES + a single-step model + a stock set → routes/search trees + benchmarking metrics.
- **Use it when:** you need to compare single-step models and search algorithms within one framework. LLM-Syn-Planner uses Syntheseus.

### Published RetroChimera benchmark setup

The [RetroChimera paper](https://arxiv.org/html/2412.05269) integrated its
single-step model with Syntheseus for multi-step evaluation. Its SimpRetro
comparison reused a setup with 23.1 million commercially available eMolecules
building blocks; its separate Pistachio hard-target experiment used Retro*
with the same building-block set. For the latter experiment, the authors tuned
Retro*'s policy temperature per model on 151 validation targets before testing
on 800 targets. These are study-specific search and stock choices, not default
settings for another target set or inventory. Record them when comparing
reported route results.

### Repeated intermediates in trees and graphs

Syntheseus 0.9.0's [RetroStar class](https://github.com/microsoft/syntheseus/blob/v0.9.0/syntheseus/search/algorithms/best_first/retro_star.py#L31-L35)
inherits a [tree requirement](https://github.com/microsoft/syntheseus/blob/v0.9.0/syntheseus/search/algorithms/best_first/base.py#L94-L96),
and the [search base](https://github.com/microsoft/syntheseus/blob/v0.9.0/syntheseus/search/algorithms/base.py#L69-L104)
rejects shared molecule nodes for algorithms that require a tree. The same
intermediate can therefore occupy separate nodes in different branches.
Syntheseus also has an [AND/OR graph class](https://github.com/microsoft/syntheseus/blob/v0.9.0/syntheseus/search/graph/and_or.py#L53-L67)
that can share molecule nodes for
algorithms that permit it; that option does not change RetroStar's tree rule.

[DreamRetroer's released code](https://github.com/osu-zxf/DreamRetroer/blob/ab3eab4c3547322b54e4deb3db66c887cfea2b8a/src/dreamretroer/algorithm/search_tree.py#L50-L68)
uses a molecule-string lookup to reuse a node when a predicted reactant string
has appeared earlier in its search graph. Its [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11695995/)
describes shared intermediates in group retrosynthesis. This code-level match
does not establish that differently written strings for the same chemical
structure will merge. Record the search representation and identity rule when
comparing route exports or joining saved predictions.

## Tango* — *search toward specified starting materials*

> A 2025 Retro*-based method for planning routes toward specified building
> blocks, guided by a cost that combines Tanimoto similarity and fuzzy maximum
> common substructure similarity.

- **Paper and code:** [Digital Discovery paper](https://doi.org/10.1039/D5DD00130G); [TangoStar](https://github.com/schwallergroup/TangoStar).
- **License and artifacts:** [MIT code](https://github.com/schwallergroup/TangoStar/blob/667fdd915bc94562139cbcdae25bb1b2ed423aaa/LICENSE); its README links separate pretrained models and data from a [DESP Figshare record](https://doi.org/10.6084/m9.figshare.25956076.v3) labeled CC BY 4.0. Check the specific artifacts before reuse.
- **Implementation:** the released code is based on DESP; it is not supplied as a Syntheseus plugin. Its [search structure](https://github.com/schwallergroup/TangoStar/blob/667fdd915bc94562139cbcdae25bb1b2ed423aaa/desp/search/data_structures/desp_tree.py#L120-L143) reuses nodes when precursor strings match. Verify molecular identity handling before relying on it to merge equivalent structures.
- **Use it when:** a route must include specified inputs. The paper's target/start-pair benchmarks do not establish current supplier availability or general route quality. Tango* is distinct from the separate [TANGO constrained-synthesizability reward](https://openreview.net/forum?id=Im90Ziq4M1).
- **Checked:** 2026-09-24.

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

Record the planner version, single-step model and checkpoint, prediction mode,
stock snapshot, search limits, and molecule-standardization settings with each
result. Use the same target structures and stock when comparing planners, and
report differences in models or search budgets.

Document where the stock came from, its release or snapshot date, selection
filters, and any added or excluded molecules. Check the exact identities of
expected starting materials and the target against the inventory before
interpreting a search result. If the model includes a reagent among reaction
reactants, check its inventory identity as well. Membership in a stock file
does not establish current supplier availability or price. For example,
[Syntheseus search](https://microsoft.github.io/syntheseus/dev/cli/search/)
accepts a separate SMILES inventory file; the selected file determines which
terminal molecules its search can accept.

Separate a single-step precursor query from a multi-step route search. For a
search, report the algorithm, iteration, model-call and time limits, whether
the target was solved in the saved graph, and the number of exported routes.
Count precursor predictions separately. The [Syntheseus custom-model example](https://microsoft.github.io/syntheseus/dev/tutorials/custom_model/#running-search)
returns a search graph and extracted routes as separate objects and measures
model calls separately.

Classify the planner output after inspecting its exported routes and saved
graph, when available:

| Result | Check |
|---|---|
| Target in stock | The target itself matches the selected stock; no reaction is required. |
| Complete route to stock | At least one reaction connects the target to terminal compounds that all match the selected stock. |
| Partial route | The exported route contains reactions but has unresolved terminal compounds. |
| No route within budget | Search ended without a stock-closed route in the planner output; inspect the saved graph if available. |
| Execution or export failure | Model loading, search, or route serialization failed; record the failed step. |

Record whether each reported route was exported by the planner or assembled
afterward from reactions in a saved search graph. For an assembled route,
preserve the original prediction identifiers and every added connection.
Verify that the connected nodes represent the same molecular structure under
the stated identity rules, then follow every reaction dependency from the
exact target to a stock leaf. Inspect the graph beyond the displayed route
limit when the exported routes do not answer the task. A graph assembly is a
postprocessed candidate, not a planner-exported route.

Check terminal compounds against the stock independently of the planner's
success flag. In [SynPlanner 1.7.0](https://github.com/Laboratoire-de-Chemoinformatique/SynPlanner/blob/v1.7.0/synplan/chem/precursor.py),
`is_building_block` accepts molecules at or below `min_mol_size` without a stock
lookup; its default threshold is six atoms. Specify whether stock matching
preserves stereochemistry, isotopes, and salt forms.

Review each reaction for bond changes, reagents, and stereochemical requirements.
Use [forward prediction and round-trip checks](synthesizability-scoring.md)
alongside that review. A complete route to stock establishes graph connectivity
and stock coverage; reaction feasibility requires separate checks.
