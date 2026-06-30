# Watchlist — Interesting but Not Ready-to-Use

Tools whose ideas are relevant but which you **cannot run or safely reuse today** — either no public code, no released weights, or no usable license. Kept here (out of the main category files) so the rest of the compilation stays "things you can actually pick up." Re-check periodically; several may graduate.

Two distinct failure modes:
- **No usable code/weights** — paper only, or repo is a stub. Not runnable.
- **Code exists but no license** — public repo, but no license = *all rights reserved*, so not legally reusable/redistributable despite being visible.

## No public code (paper only)

| Tool | What it is | Paper | Why watch / status |
|---|---|---|---|
| **Reactron** | Electron-movement / arrow-pushing reaction prediction (claims 100%-valid products) | arXiv:2503.10197 (2025), Jung group SNU | No repo in the group's org or personal accounts; no code/data link in paper. The group's **MechFinder** *is* public (different tool). Don't confuse with **FlowER** (Nature 2025), the JACS polar-reaction model, or arrow-pushing LLM arXiv:2512.05722. |
| **Retro-Expert** | LLM (Qwen2.5-7B + RL) + specialist models (T5Chem, GraphRetro) for interpretable single-step retro with NL explanations | arXiv:2508.10967 (2025) | No public repo found. Attractive because it targets an open-weight backbone (no commercial API), but unrealized until code drops. |
| **ReTriP** | End-to-end CoT retrosynthetic planning, RL with verifiable rewards, BioMedGPT-Mol (Qwen3-8B) base | arXiv:2603.29723 (2026) | No code, no "will release" statement. Strong concept (long-route robustness) on the watchlist. |
| **TempRe** | Reaction templates as sequence generation (can generate novel templates); single- + multi-step | arXiv:2507.21762 (2025), Schwaller group | No repo located anywhere (not in the LIAC org); no weights. Built on OpenNMT, so reproducible in principle. Uses PaRoutes benchmarks. |
| **RetroTrim** | Hallucination-filtering via a diverse ensemble of reaction scorers; won the Standard Industries Retrosynthesis Challenge | arXiv:2510.10645 (2025) | No code-availability statement / repo. Very relevant to route validation — emulate with round-trip + multiple single-step scorers until released. See [synthesizability-scoring.md](synthesizability-scoring.md). |
| **NeuralPLexer3** | Physics-inspired **flow-matching** co-folding; AF3-class biomolecular complex prediction (Iambic Therapeutics) | arXiv:2412.10743 (2024); NeurIPS 2025 poster | **Proprietary / closed.** No model code or weights. Iambic's GitHub org has only `np-bench` (a *benchmark*, BSD-3-Clause); no `neuralplexer3` model repo exists. The open predecessor `zrqiao/NeuralPLexer` *is* runnable (⚠️ non-commercial weights). See [docking-and-cofolding.md](docking-and-cofolding.md). |
| **Chai-2 / Chai-3** | Chai-2: zero-shot antibody/protein *de novo design* (different task from Chai-1's structure prediction) | bioRxiv 2025 (DOI 10.1101/2025.07.05.663018) | **Proprietary.** No code/weights in `chai-lab` (only cited); commercialized via partnerships (Pfizer, Lilly). Chai-1 is the only **open** release in the family — see [docking-and-cofolding.md](docking-and-cofolding.md). |
| **LARC** | LLM-agent constrained retrosynthesis ("Agent-as-a-Judge" injects constraint feedback: avoid carcinogens/pyrophorics/…) | arXiv:2508.11860 (2025) | Code **does** exist (`ninglab/LARC`) but ⚠️ **no LICENSE file (all rights reserved)** — listed here for the license blocker, not absence of code. Claude-3.5 / Mistral-Nemo backends; MEEA* engine. See [agentic-retrosynthesis.md](agentic-retrosynthesis.md). |

## Code exists but no usable license (all rights reserved)

These are real, sometimes runnable codebases — but with **no license**, you have no granted right to use, modify, or redistribute them. Treat as look-only / contact-the-authors until a license appears.

| Tool | Category | Repo | Note |
|---|---|---|---|
| **InterRetro** | Search-free multi-step planner (worst-path RL); NeurIPS 2025 | `MianchuWang/InterRetro` | No LICENSE; data on Google Drive only. "Interactive" (not "interpretable") Retrosynthesis. |
| **ConRetroBert** | Template retrieval/ranking single-step retro | `JahidBasher/ConRetroBert` | No LICENSE; weights/data on Google Drive. Under NeurIPS 2026 review. |
| **SynCoGen** (code) | 3D synthesizable co-generation | `andreirekesh/SynCoGen` | Code has no license, **but the HF weights + SynSpace dataset are MIT** — so the *artifacts* are usable; only the training/inference *code* is unlicensed. See [synthesizable-generation.md](synthesizable-generation.md). |
| **SynTwins** (code) | Training-free analog generation | `snu-micc/SynTwins` | No code license; paper CC BY-NC. Bundles 150K Enamine blocks. See [synthesizable-generation.md](synthesizable-generation.md). |
| **Mol-LLaMA** (code) | Molecular-understanding LLM | `DongkiKim95/Mol-LLaMA` | No code license; weights HF-tagged apache but Llama-based. See [chemical-language-models.md](chemical-language-models.md). |
| **ChemMLLM** (code) | Multimodal chemistry LLM | `bbsbz/ChemMLLM` | No code license; **no weights released**; Chameleon noncommercial base. See [chemical-language-models.md](chemical-language-models.md). |
| **GVT** (code) | Graph VQ-Transformer generation | `zzccppp/GVT` | No license; brand-new (2 commits). See [molecular-generation.md](molecular-generation.md). |
| **SmiSelf** (code) | SMILES validity correction | `wentao228/SmiSelf` | No license; EMNLP 2025. Useful utility once licensed. See [molecular-generation.md](molecular-generation.md). |
| **CardioTox** (code) | hERG blockade (DL ensemble) | `Abdulk084/CardioTox` | No LICENSE; pretrained weights bundled. See [admet-prediction.md](admet-prediction.md). |
| **PPB3** (code) | Target / polypharmacology prediction (ChEMBL v34) | `reymond-group/PPB3` | Public repo (training script + Flask app) but **no LICENSE**. Web tool free to query. See [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md). |

**Looks no-license but isn't:** **TargetDiff** (`guanjq/targetdiff`) and **PocketFlow** (`Saoge123/PocketFlow`) show "no license" on GitHub but ship genuine **MIT** in misspelled files (`LICIENCE`, `Liscense`) — they are usable; keep a copy of the file. See [structure-based-generation.md](structure-based-generation.md).

## Released but commercially blocked (usable for research only)

Not "watchlist" exactly, but flagged so they aren't mistaken for open: code/weights exist and run, but a **non-permissive license** blocks commercial use.

| Tool | Blocker |
|---|---|
| **SynLlama** | UC Berkeley Regents **non-commercial** license (the paper's "MIT" claim is wrong). |
| **ChemDFM-R** | Weights **AGPL-3.0** (network copyleft) — SaaS triggers source-disclosure. |
| **APEX** | Code **CC BY-NC 4.0** (non-commercial); datasets are CC BY 4.0. |
| **ChemDual** | Apache-2.0 code, but **weights unreleased** ("coming soon") — not usable as a model yet. |
| **RetroDiT** | MIT code, but **weights not yet released** — train from scratch. |
| **NeuralPLexer** | Code BSD-3-Clear, but **weights CC BY-NC-SA 4.0 (non-commercial)** — runnable for research; retrain for commercial. See [docking-and-cofolding.md](docking-and-cofolding.md). |
| **AlphaFold3** | Code Apache-2.0, but **weights request-gated + non-commercial** (no redistribution) — research-only; use Boltz/Chai to ship. See [docking-and-cofolding.md](docking-and-cofolding.md). |
| **DecompDiff** | Pocket-conditioned generator under **CC-BY-NC 4.0** (non-commercial) + archived (2025). See [structure-based-generation.md](structure-based-generation.md). |
| **BayeshERG** | MIT *code*, but trained **weights + data = CC-BY-NC-SA** — retrain on permissive data for commercial. See [admet-prediction.md](admet-prediction.md). |
| **RoseTTAFold** (original) | MIT code, **weights non-commercial** (Rosetta-DL). RFAA relaxed to BSD; the original didn't. See [protein-structure-prediction.md](protein-structure-prediction.md). |
| **ChemBERTa** (weights) | MIT code, but the popular HF checkpoints have **no stated license** — confirm or retrain. See [property-and-qsar-prediction.md](property-and-qsar-prediction.md). |
| **ESM3 / ESM-C** | Historically Cambrian **non-commercial**; reportedly **relicensed to MIT (~2026)** — re-verify the live model card. See [protein-structure-prediction.md](protein-structure-prediction.md). |

## Web-only or closed-binary (no source to deploy)

Useful to *query*, but there is **no open code/weights to run or embed** — and querying often sends your structures to a third-party academic host (IP/egress risk).

| Tool | What it is | Access | Note |
|---|---|---|---|
| **SEA / SEAware** | Target / off-target prediction (similarity-ensemble) | web `sea.bkslab.org`; SEAware proprietary | No open Shoichet repo; community `momeara/DeepSEA` is no-license. See [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md). |
| **SwissTargetPrediction** | Target prediction (2D+3D similarity) | web | Outputs CC-BY 4.0; no code to deploy. |
| **PPB2** | Polypharmacology / target prediction | web `ppb2.gdb.tools` | No repo (PPB3 has a no-license repo, above). |
| **SPiDER / TIGER** | SOM-consensus target prediction (Schneider) | ETH webserver (defunct) | No open code; methodological reference only. |
| **DoGSiteScorer** | Binding-site detection + druggability | web (ProteinsPlus) | Academic-only; no open code. See [structure-based-generation.md](structure-based-generation.md). |
| **PLANTS** | Ant-colony docking | closed academic binary (site stale) | No public source. See [docking-and-cofolding.md](docking-and-cofolding.md). |
| **DeepPK, ADMETlab 3.0, pkCSM** | ADMET prediction | web | Non-commercial (DeepPK/ADMETlab) or paid (pkCSM); not embeddable. See [admet-prediction.md](admet-prediction.md). |
| **SwissADME** | Physchem / druglikeness | web | Results CC-BY 4.0 (usable); engine not deployable; no bulk scraping. |

**Commercial reference points (proprietary, paid — orientation only):** Schrödinger **FEP+ / Glide / Phase**, OpenEye/Cadence **ROCS / Szybki**, Cresset **Flare**, **SEAware**. The open tools in this compilation are benchmarked against these.

## 2026 new arrivals on the watchlist

From the 2026 literature/repo sweep (verified 2026-06-13). The clearly-usable permissive ones were brought into the category files; these are the rest — recent and relevant, but blocked by a non-commercial/copyleft license, a *missing* LICENSE file, or no public code.

**Released but non-commercial / copyleft / missing-license:**

| Tool | Category | Repo | Blocker |
|---|---|---|---|
| **MATCHA** | docking (flow-matching) | `LigandPro/Matcha` | code + weights **CC-BY-NC-4.0** (non-commercial); strong/recent — track for relicense. |
| **FLOWR.root** | SBDD + affinity | `jule-c/flowr_root` | README says MIT but **no LICENSE file exists** (all-rights-reserved in practice); weights pre-final on Google Drive. |
| **GatorAffinity** | affinity | `AIDD-LiLab/GatorAffinity` | code MIT but **checkpoints non-commercial** (CC-BY-NC-SA); preprint only. |
| **DiffSMol** | SBDD | `ninglab/DiffSMol` | **PolyForm Noncommercial** license (not permissive); 2023/24 vintage. |
| **Suiren-1.0** | 3D foundation model | `golab-ai/Suiren-Foundation-Model` | **Modified MIT** (UI-attribution clause if >1k MAU / >$10k/mo); organic-only; 1.8B 3D model, arXiv:2603.21942 (Mar 2026). |
| **JMM** | OOD/uncertainty QSAR | `molML/JointMolecularModel` | README says MIT, **no LICENSE file**; *Nat. Mach. Intel.* Mar 2026; novel "unfamiliarity" OOD metric. |
| **EDMolGPT** | SBDD (electron-density) | `JiahaoChen1/EDMolGPT` | **no LICENSE** (all rights reserved); ICML 2026; novel density-conditioned modality. |

**Code-but-pre-license / pre-1.0 (track):** **FragNet** (`pnnl/FragNet`, custom Battelle/PNNL permissive — legal review), **UQ4DD** (`MolecularAI/uq4dd`, Apache, UQ benchmark w/ censored-label focus), **GLACIER** (`eemokey/glacier`, MIT, distilled encoder, Jun 2026), **TerraMax** (`terraytherapeutics/terramax`, Apache, batch Bayesian-opt, single-commit), **MolMiner** (`raulorteg/molminer`, Apache, fragment-based gen), **ReACT-Drug** (`YadunandanRaman/ReACT-Drug`, MIT, template-RL gen — overlaps SyntheMol), **MolFORM** (`daiheng-zhang/SBDD-MolFORM`, MIT, confirm weights), **SynthLadder** (`SergeiNikolenko/SynthLadder`, no license, agentic synth benchmark).

**Paper-only / no public code (concept worth tracking):**
- *Retrosynthesis:* **CREED / ChemCensor** (Insilico Medicine, ICML 2026 — LLM-retro benchmark rethink + ~6.4M validated reactions), **AOT\*** (LLM AND-OR tree search, Sep 2025), **Retro-R1** (RL agentic retro, NeurIPS 2025), **RetroReasoner** (round-trip-reward reasoning LLM, Mar 2026), **SCR** (margin-calibrated classifier guidance, May 2026), **MolReAct** (RL+LLM template actions, Apr 2026).
- *Selectivity / DTI:* **OmniBind** (promiscuity across 15,405 human proteins from SMILES; Vendruscolo lab, bioRxiv Mar 2026 — the single most on-target *selectivity* concept; CC-BY-NC paper, **no code**), **PIGLET** (proteome-wide knowledge-graph DTI; Stanford, bioRxiv Feb 2026, no code).
- *Agentic:* **Mozi, ToolMol, OrchestRA, FROGENT, PharmAgents** — see [agentic-drug-design.md](agentic-drug-design.md).

**Checked → SKIP (no verifiable repo, or out of scope):** NovoExpert-1/-2 (cited GitHub 404s), TITAN-BBB, SMILES-Mamba, EvoEGF-Mol, S3-GFN, FragmentGPT (no code); ChemFM / MAMMAL / EPT (2026 journal dates but 2024–25 models, some with NC weights); mCLM (May-2025, no code); SyntheFluor-RL (fluorophore-specific). **No open "Boltz-3 / Chai-3" exists** as of 2026-06-13.

## How to use this list

- Building something you'll **ship**: avoid everything here. Use the permissively-licensed, weights-released tools highlighted in [tool-matrix.md](tool-matrix.md) and [licensing-and-data.md](licensing-and-data.md).
- Doing **research**: the "released but commercially blocked" set is fair game; the "no license" set needs author contact; the "paper only" set isn't runnable.
- Re-verify before relying on any status — licenses get added, weights get released, repos appear. Synthesizability-layer entries checked **2026-06-11**; target-based-layer entries (structure, docking, affinity, QSAR, ADMET, selectivity, structure-based generation) checked **2026-06-13**.
