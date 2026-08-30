# Watchlist for Public Artifact and License Gaps

Tools with a documented method but a missing public implementation, released checkpoint, or repository license. They remain here until the relevant public artifact appears or its terms become clear.

The watchlist records two distinct gaps:

- **No usable code or weights:** Only a paper or repository stub is public, so
  the method cannot run from the published artifacts.
- **No stated license:** A public repository exists, but no license grant is
  visible for the code or artifacts.

## No public code (paper only)

| Tool | What it is | Paper | Why watch / status |
|---|---|---|---|
| **Reactron** | Electron-movement / arrow-pushing reaction prediction (claims 100%-valid products) | arXiv:2503.10197 (2025), Jung group SNU | No repository in the group's organization or personal accounts; no code/data link in the paper. The public **MechFinder** project, **FlowER** (Nature 2025), the JACS polar-reaction model, and arrow-pushing LLM arXiv:2512.05722 are distinct methods. |
| **Retro-Expert** | LLM (Qwen2.5-7B + RL) + specialist models (T5Chem, GraphRetro) for interpretable single-step retro with natural-language explanations | arXiv:2508.10967 (2025) | No public repository found; the method remains a paper-only reference. |
| **ReTriP** | CoT retrosynthetic planning with RL and verifiable rewards, BioMedGPT-Mol (Qwen3-8B) base | arXiv:2603.29723 (2026) | No code or release statement was found. The paper studies long-route planning. |
| **TempRe** | Reaction templates as sequence generation (can generate novel templates); single- + multi-step | arXiv:2507.21762 (2025), Schwaller group | No repository located anywhere (not in the LIAC org); no weights. Built on OpenNMT, so reproducible in principle. Uses PaRoutes benchmarks. |
| **RetroTrim** | Hallucination filtering with an ensemble of reaction scorers; winner of the Standard Industries Retrosynthesis Challenge | arXiv:2510.10645 (2025) | No code-availability statement or repository was found. Until artifacts are released, use round-trip checks with multiple one-step scorers. See [synthesizability-scoring.md](synthesizability-scoring.md). |
| **NeuralPLexer3** | Physics-inspired **flow-matching** co-folding; AF3-class biomolecular complex prediction (Iambic Therapeutics) | arXiv:2412.10743 (2024); NeurIPS 2025 poster | **Proprietary / closed.** No model code or weights. Iambic's GitHub org has only `np-bench` (a *benchmark*, BSD-3-Clause); no `neuralplexer3` model repository exists. The open predecessor `zrqiao/NeuralPLexer` *is* runnable (⚠️ non-commercial weights). See [docking-and-cofolding.md](docking-and-cofolding.md). |
| **Chai-2 / Chai-3** | Chai-2: zero-shot antibody/protein *de novo design* (different task from Chai-1's structure prediction) | bioRxiv 2025 (DOI 10.1101/2025.07.05.663018) | **Proprietary.** No code or weights for these models are published in `chai-lab`. Chai-1 is the only **open** release in the family — see [docking-and-cofolding.md](docking-and-cofolding.md). |
| **LARC** | LLM-agent constrained retrosynthesis ("Agent-as-a-Judge" injects constraint feedback: avoid carcinogens and pyrophoric compounds) | arXiv:2508.11860 (2025) | The `ninglab/LARC` repository has no `LICENSE` file. It uses the MEEA* engine. See [agentic-retrosynthesis.md](agentic-retrosynthesis.md). |
| **SynthEx** | Strategy-first planning for complex natural products with editable reaction-graph actions | [arXiv:2608.07454](https://arxiv.org/abs/2608.07454) (2026) | The [repository](https://github.com/schwallergroup/synthex) says code is not yet published and shows an Apache-2.0 release as planned. Routes are browsable at [SynthAtlas](https://synthatlas.epfl.ch). |

## Code exists but no license is stated

These are real, sometimes runnable codebases, but no license grant is visible in the repository or its linked artifacts.

| Tool | Category | Repository | Note |
|---|---|---|---|
| **InterRetro** | Search-free multi-step planner (worst-path RL); NeurIPS 2025 | `MianchuWang/InterRetro` | No LICENSE; data on Google Drive only. "Interactive" (not "interpretable") Retrosynthesis. |
| **ConRetroBert** | Template retrieval/ranking single-step retro | `JahidBasher/ConRetroBert` | No LICENSE; weights/data on Google Drive. Under NeurIPS 2026 review. |
| **SynCoGen** (code) | 3D synthesizable co-generation | `andreirekesh/SynCoGen` | The code repository has no license; the HF weights and SynSpace dataset are labeled MIT. See [synthesizable-generation.md](synthesizable-generation.md). |
| **SynTwins** (code) | Training-free analog generation | `snu-micc/SynTwins` | No code license; paper CC BY-NC. Bundles 150K Enamine blocks. See [synthesizable-generation.md](synthesizable-generation.md). |
| **Mol-LLaMA** (code) | Molecular-understanding LLM | `DongkiKim95/Mol-LLaMA` | No code license; weights HF-tagged apache but Llama-based. See [chemical-language-models.md](chemical-language-models.md). |
| **ChemMLLM** (code) | Multimodal chemistry LLM | `bbsbz/ChemMLLM` | No code license; **no weights released**; Chameleon noncommercial base. See [chemical-language-models.md](chemical-language-models.md). |
| **GVT** (code) | Graph VQ-Transformer generation | `zzccppp/GVT` | On 2026-08-30, the repository had two commits and no `LICENSE` file. See [molecular-generation.md](molecular-generation.md). |
| **SmiSelf** (code) | SMILES validity correction | `wentao228/SmiSelf` | No license; EMNLP 2025. Useful utility once licensed. See [molecular-generation.md](molecular-generation.md). |
| **CardioTox** (code) | hERG blockade (DL ensemble) | `Abdulk084/CardioTox` | No LICENSE; pretrained weights bundled. See [admet-prediction.md](admet-prediction.md). |
| **PPB3** (code) | Target / polypharmacology prediction (ChEMBL v34) | `reymond-group/PPB3` | Public repository (training script + Flask app) but **no LICENSE**. Web tool free to query. See [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md). |

**License metadata check:** **TargetDiff** (`guanjq/targetdiff`) and **PocketFlow** (`Saoge123/PocketFlow`) show no license in GitHub metadata but include **MIT** text in repository files named `LICIENCE` and `Liscense`. See [structure-based-generation.md](structure-based-generation.md).

## Released artifacts with restrictive or incomplete terms

Code or weights exist, but at least one artifact has a non-commercial or copyleft term, or a required checkpoint is not released.

| Tool | Blocker |
|---|---|
| **SynLlama** | Repository `LICENSE` contains a UC Berkeley Regents **non-commercial** grant; the paper uses an MIT label. |
| **ChemDFM-R** | Released weights are tagged **AGPL-3.0**. Review the exact license text for the planned distribution and network use. |
| **APEX** | The repository has no `LICENSE` file; Zenodo data and weight records are separate and do not expose a license field in their metadata. |
| **ChemDual** | Apache-2.0 code; **weights are not released**, so the public repository cannot run model inference. |
| **NeuralPLexer** | Code BSD-3-Clause; weights CC BY-NC-SA 4.0. See [docking-and-cofolding.md](docking-and-cofolding.md). |
| **AlphaFold3** | Code Apache-2.0; weights are request-gated and carry non-commercial terms. See [docking-and-cofolding.md](docking-and-cofolding.md). |
| **DecompDiff** | Pocket-conditioned generator under **CC-BY-NC 4.0** (non-commercial) + archived (2025). See [structure-based-generation.md](structure-based-generation.md). |
| **BayeshERG** | MIT code; trained weights and data are CC BY-NC-SA. See [admet-prediction.md](admet-prediction.md). |
| **RoseTTAFold** (original) | MIT code; the original weights use the non-commercial Rosetta-DL terms. RoseTTAFold All-Atom uses BSD-3-Clause for its code and weights. See [protein-structure-prediction.md](protein-structure-prediction.md). |
| **ChemBERTa** (weights) | MIT code, but the popular HF checkpoints have **no stated license** — confirm or retrain. See [property-and-qsar-prediction.md](property-and-qsar-prediction.md). |
| **ESM3 / ESM-C** | On 2026-08-30, the `Biohub/esm` repository listed MIT terms for its code and models. Earlier EvolutionaryScale checkpoints used Cambrian terms, so verify the exact checkpoint. See [protein-structure-prediction.md](protein-structure-prediction.md). |

## Web-only or closed-binary (no source to deploy)

These services publish no local code or weights. A query sends the submitted
structure to the service operator.

| Tool | What it is | Access | Note |
|---|---|---|---|
| **SEA / SEAware** | Target / off-target prediction (similarity-ensemble) | web `sea.bkslab.org`; SEAware proprietary | No open Shoichet repository; community `momeara/DeepSEA` is no-license. See [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md). |
| **SwissTargetPrediction** | Target prediction (2D+3D similarity) | web | Outputs CC-BY 4.0; no code to deploy. |
| **PPB2** | Polypharmacology / target prediction | web `ppb2.gdb.tools` | No repository (PPB3 has a no-license repository, above). |
| **SPiDER / TIGER** | SOM-consensus target prediction (Schneider) | ETH webserver (defunct) | No open code; methodological reference only. |
| **DoGSiteScorer** | Binding-site detection + druggability | web (ProteinsPlus) | Academic-only; no open code. See [structure-based-generation.md](structure-based-generation.md). |
| **PLANTS** | Ant-colony docking | closed academic binary (site stale) | No public source. See [docking-and-cofolding.md](docking-and-cofolding.md). |
| **DeepPK, ADMETlab 3.0, pkCSM** | ADMET prediction | web | DeepPK and ADMETlab publish non-commercial terms; pkCSM is a hosted service. See [admet-prediction.md](admet-prediction.md). |
| **SwissADME** | Physchem / druglikeness | web | Results are CC BY 4.0; the engine is not published for local deployment, and the service does not provide a bulk-scraping interface. |

## Entries Added in the 2026 Review

The entries below were checked against public records on **2026-08-30**. Each
entry has a non-commercial or copyleft term, lacks a `LICENSE` file, or has no
public code.

**Released but non-commercial / copyleft / missing-license:**

| Tool | Category | Repository | Blocker |
|---|---|---|---|
| **MATCHA** | docking (flow-matching) | `LigandPro/Matcha` | Code and weights are **CC BY-NC 4.0**. |
| **FLOWR.root** | SBDD and affinity | `jule-c/flowr_root` | The README says MIT, but the repository has no `LICENSE` file; weights are linked from Google Drive. |
| **GatorAffinity** | affinity | `AIDD-LiLab/GatorAffinity` | code MIT but **checkpoints non-commercial** (CC-BY-NC-SA); preprint only. |
| **DiffSMol** | SBDD | `ninglab/DiffSMol` | **PolyForm Noncommercial** license (not permissive); 2023/24 vintage. |
| **Suiren-1.0** | 3D foundation model | `golab-ai/Suiren-Foundation-Model` | **Modified MIT** (UI-attribution clause if >1k MAU / >$10k/mo); organic-only; 1.8B 3D model, arXiv:2603.21942 (Mar 2026). |
| **JMM** | OOD and uncertainty QSAR | `molML/JointMolecularModel` | The README says MIT, but the repository has no `LICENSE` file; *Nat. Mach. Intel.* Mar 2026; introduces an "unfamiliarity" OOD metric. |
| **EDMolGPT** | SBDD (electron-density) | `JiahaoChen1/EDMolGPT` | The repository has no `LICENSE` file; ICML 2026; introduces a density-conditioned modality. |

**Code with pre-1.0 or incomplete artifact terms:** **FragNet** (`pnnl/FragNet`, custom Battelle/PNNL terms), **UQ4DD** (`MolecularAI/uq4dd`, Apache, UQ benchmark with censored-label focus), **GLACIER** (`eemokey/glacier`, MIT, distilled encoder, Jun 2026), **TerraMax** (`terraytherapeutics/terramax`, Apache, batch Bayesian optimization, single-commit), **MolMiner** (`raulorteg/molminer`, Apache, fragment-based generation), **ReACT-Drug** (`YadunandanRaman/ReACT-Drug`, MIT, template-RL generation), **MolFORM** (`daiheng-zhang/SBDD-MolFORM`, MIT, checkpoint terms to confirm), **SynthLadder** (`SergeiNikolenko/SynthLadder`, no license, agentic synthesis benchmark).

**Paper-only / no public code (concept worth tracking):**
- *Retrosynthesis:* **CREED / ChemCensor** (Insilico Medicine, ICML 2026 — LLM-retro benchmark rethink + ~6.4M validated reactions), **AOT\*** (LLM AND-OR tree search, Sep 2025), **Retro-R1** (RL agentic retro, NeurIPS 2025), **RetroReasoner** (round-trip-reward reasoning LLM, Mar 2026), **SCR** (margin-calibrated classifier guidance, May 2026), **MolReAct** (RL+LLM template actions, Apr 2026).
- *Selectivity and DTI:* **OmniBind** predicts promiscuity across 15,405 human
  proteins from SMILES; its paper is CC BY-NC, and no code is public. **PIGLET**
  studies proteome-wide knowledge-graph DTI; its February 2026 bioRxiv paper
  links no public code.
- *Agentic:* **Mozi, ToolMol, OrchestRA, FROGENT, PharmAgents** — see [agentic-drug-design.md](agentic-drug-design.md).

**Not added:** NovoExpert-1/-2 (cited GitHub 404s), TITAN-BBB, SMILES-Mamba, EvoEGF-Mol, S3-GFN, FragmentGPT (no code); ChemFM / MAMMAL / EPT (2026 journal dates but 2024–25 models, some with NC weights); mCLM (May-2025, no code); SyntheFluor-RL (fluorophore-specific).

## How to use this list

- For redistribution or deployment, compare the code, weights, and data terms in [tool-matrix.md](tool-matrix.md) and [licensing-and-data.md](licensing-and-data.md).
- For research, use the status labels to distinguish released artifacts, missing-license repositories, and paper-only methods.
- Re-check each upstream record before relying on its status; licenses change, weights appear, and repositories move.
