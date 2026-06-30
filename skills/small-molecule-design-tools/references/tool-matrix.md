# Tool Matrix

Master index of every tool in this compilation, by category. All facts verified against live repos, papers, and HuggingFace cards on **2026-06-11** (target-based layer **2026-06-13**). **Verify licenses and data terms yourself before commercial use** — see [licensing-and-data.md](licensing-and-data.md). "Commercial?" below is a quick read of the *most restrictive* layer (code/weights/data), not legal advice. The compilation has **two layers**: **"can-I-make-it?" (synthesizability / route planning)** — the categories above the divider below — and **"will-it-work-on-the-target?" (target-based design)** — receptor structure, docking & co-folding, binding affinity, QSAR/property, ADMET, off-target/selectivity, and structure-based generation.

Legend: ✅ yes · ⚠️ conditional/caution · ❌ no / blocked · — n/a

## Synthesizable generation, projection & analogs → [synthesizable-generation.md](synthesizable-generation.md)

Output = molecule **with a synthesis route**, or a makeable analog + how to make it. All depend on Enamine building blocks.

| Tool | Repo | Code | Weights | Commercial? | Status |
|---|---|---|---|---|---|
| **PrexSyn** | `luost26/prexsyn` | MIT | MIT (auto-DL) | ⚠️ Enamine data terms | ✅ Active (current pick) |
| **SynFormer** | `wenhao-gao/synformer` | Apache-2.0 | Apache-2.0 | ⚠️ data "research only" | ⚠️ Quiet; author-deprecated |
| **ChemProjector** | `luost26/ChemProjector` | MIT | (Google Drive) | ⚠️ Enamine, archived | ❌ Archived → PrexSyn |
| **ReaSyn** | `NVIDIA-BioNeMo/ReaSyn` | Apache-2.0 | **NVIDIA Open Model** | ⚠️ weights+Enamine | ✅ Active |
| **SynCoGen** | `andreirekesh/SynCoGen` | **none** | HF MIT | ⚠️ code unlicensed | ✅ Active (3D) |
| **SynTwins** | `snu-micc/SynTwins` | **none** | — | ❌ no license | ⚠️ Minimal (training-free) |
| **SynLlama** | `THGLab/SynLlama` | **UC non-commercial** | Figshare | ❌ non-commercial | ✅ Maintained (research) |
| **SyntheMol** | `swansonk14/SyntheMol` | MIT | CC BY 4.0 | ✅ (+vendor catalog) | ✅ Active (make-on-demand) |
| **APEX** | `NumerionLabs/apex` | **CC BY-NC 4.0** | Zenodo | ❌ non-commercial | ✅ New (billions-scale search) |

## General molecular generation (validity, not synthesizability) → [molecular-generation.md](molecular-generation.md)

| Tool | Repo | Code | Weights | Commercial? | Status |
|---|---|---|---|---|---|
| **GenMol** | `NVIDIA-Digital-Bio/genmol` | Apache-2.0 | **NVIDIA Open Model** | ⚠️ usable w/ conditions | ✅ Active (SAFE diffusion) |
| **MolReactGen** | `hogru/MolReactGen` | MIT | HF (MIT) | ✅ | ⚠️ Dormant (thesis) |
| **SmiSelf** | `wentao228/SmiSelf` | **none** | — (rule-based) | ❌ no license | ⚠️ Utility (EMNLP 2025) |
| **GVT** | `zzccppp/GVT` | **none** | README links | ❌ no license | ⚠️ Brand-new preprint |

## Multi-step retrosynthesis / route planning → [retrosynthesis-planning.md](retrosynthesis-planning.md)

| Tool | Repo | Code | Weights/model | Commercial? | Status |
|---|---|---|---|---|---|
| **AiZynthFinder** | `MolecularAI/aizynthfinder` | MIT | USPTO model (free) | ✅ cleanest | ✅ Very active (v4.4.1) |
| **ASKCOS** | `gitlab…/askcosv2` | MIT (v2) | mostly MIT; Reaxys NC; CAS gated | ⚠️ avoid gated models | ✅ Active (heavy deploy) |
| **Syntheseus** | `microsoft/syntheseus` | MIT | wraps others | ✅ (code) | ✅ Active (benchmark fwk) |
| **SynPlanner** | `Laboratoire-de-Chemoinformatique/SynPlanner` | MIT | presets (MIT) | ✅ | ✅ Active (CASP + GUI) |
| **InterRetro** | `MianchuWang/InterRetro` | **none** | — | ❌ no license | ⚠️ New (NeurIPS 2025) |
| **RetroCast / SynthArena** | `ischemist/project-procrustes` (+`/syntharena`) | MIT | wraps others | ✅ | ✅ Active (2026; route validation) |

## Single-step retrosynthesis models → [singlestep-retrosynthesis.md](singlestep-retrosynthesis.md)

| Tool | Repo | Code | Weights | USPTO-50K top-1 | Status |
|---|---|---|---|---|---|
| **ReactionT5v2** | `sagawatatsuya/ReactionT5v2` | MIT | HF (MIT) | 71.2% (ft) | ✅ Maintained |
| **RXNGraphormer** | `licheng-xu-echo/RXNGraphormer` | MIT | Figshare | (in paper) | ✅ Very active |
| **GDiffRetro** | `sunshy-1/GDiffRetro` | MIT | SharePoint | (in paper) | ⚠️ Dormant (AAAI 2025) |
| **RetroDFM-R** | `OpenDFM/RetroDFM-R` | Apache-2.0 | **GPL-3.0** (8B) | 65.0% | ⚠️ Single release |
| **RetroDiT** | `zzhnomorebugs/RetroDiT` | MIT | ❌ not yet | 61.2/71.1% (claim) | ⚠️ New, no weights |
| **RxnNano** | `rlisml/RxnNano` | MIT | ❌ not yet | (claims > 7B LLMs) | ⚠️ New 2026, 0.5B, no weights |
| **ConRetroBert** | `JahidBasher/ConRetroBert` | **none** | Google Drive | 62.4% (claim) | ⚠️ New, no license |
| **TempRe** | — (no repo) | — | — | (PaRoutes only) | ❌ Preprint only |

## Agentic / LLM retrosynthesis → [agentic-retrosynthesis.md](agentic-retrosynthesis.md)

All need a paid LLM API; treat as chemist-in-the-loop.

| Tool | Repo | Code | LLM backend | Commercial? | Status |
|---|---|---|---|---|---|
| **DeepRetro** | `deepforestsci/DeepRetro` | MIT | Claude + DeepSeek | ✅ (code; +API) | ✅ Peer-reviewed + GUI |
| **Synthelite** | `schwallergroup/synthelite` | MIT | Claude/Gemini/GPT | ✅ (code; +API) | ✅ Active (preprint) |
| **LLM-Syn-Planner** | `zoom-wang112358/LLM-Syn-Planner` | MIT | GPT-4o + DeepSeek | ✅ (code; +API) | ⚠️ Lightly maintained |
| **LARC** | `ninglab/LARC` | **none** | Claude / Mistral | ❌ no license | ⚠️ Watchlist |
| **Retro-Expert** | — (no repo) | — | Qwen2.5-7B | ❌ no code | ❌ Preprint only |
| **ReTriP** | — (no repo) | — | Qwen3-8B | ❌ no code | ❌ Preprint only |

## Forward reaction & mechanism prediction → [forward-and-reaction-modeling.md](forward-and-reaction-modeling.md)

| Tool | Repo | Code | Weights | Commercial? | Status |
|---|---|---|---|---|---|
| **DeepMech** | `alhqlearn/DeepMech` | MIT | Zenodo (CC-BY/MIT) | ✅ | ✅ Usable (mechanism) |
| **ReaDISH** | `Meteor-han/ReaDISH` | MIT | in-repo ckpt | ✅ | ✅ 2026 (yield/selectivity) |
| **ProPreT5** | `DerinOzer/ProPreT5` | MIT | ❌ train yourself | ✅ (code) | ⚠️ No weights |
| **ChemDual** | `JacklinGroup/ChemDual` | Apache-2.0 | ❌ "coming soon" | ⚠️ no model yet | ⚠️ Watchlist |
| **Reactron** | — (no repo) | — | — | ❌ no code | ❌ Paper only |
| *ReactionT5v2 / RXNGraphormer* | *(see single-step)* | MIT | yes | ✅ | also do forward |

## Reaction-template & rule infrastructure → [template-and-rule-infrastructure.md](template-and-rule-infrastructure.md)

CPU; permissively licensed. pip-name ≠ import-name traps noted in the file.

| Tool | Repo | Code | pip name | Status |
|---|---|---|---|---|
| **RDChiral** | `connorcoley/rdchiral` | MIT | `rdchiral` | ✅ Stable/mature (foundation) |
| **rdchiral_plus** | `denovochem/rdchiral_plus` | MIT | `rdchiral-plus` | ✅ New, active (drop-in) |
| **rxnutils** | `MolecularAI/reaction_utils` | Apache-2.0 | `reaction-utils` | ✅ Active (curation pipelines) |
| **SynTemp** | `TieuLongPhan/SynTemp` | MIT | `syntemp` | ✅ Moderate (ITS/DPO rules) |

## Synthesizability scoring → [synthesizability-scoring.md](synthesizability-scoring.md)

| Tool | Repo | Code | Notes |
|---|---|---|---|
| **RetroScore** | `Snowgao320/RetroScore` | MIT (weights unspecified) | route-aware SA score + GED |
| **shallow-tree** | `Arhs99/shallow-tree` | **GPL-3.0** | fast depth-limited AiZynthFinder screen (2026) |
| **round-trip score** | — (concept) | — | retro→forward recovery check; cheapest validation |
| **RetroTrim** | — (no repo) | — | hallucination-ensemble; preprint only |

---

> **▼ TARGET-BASED DESIGN LAYER ("will it work on the target?")** — everything from here down: receptor structure → docking/affinity → QSAR/ADMET/selectivity → structure-based generation. Verified 2026-06-13.

## Protein structure prediction (receptor prep) → [protein-structure-prediction.md](protein-structure-prediction.md)

You need the target's 3D structure before docking. Code and weights diverge constantly here.

| Tool | Repo | Code | Weights | Commercial? | Status |
|---|---|---|---|---|---|
| **ColabFold** | `sokrypton/ColabFold` | MIT | AF2 params CC BY 4.0 | ✅ (attribution) | ✅ Active (fast AF2) |
| **AlphaFold2** | `google-deepmind/alphafold` | Apache-2.0 | CC BY 4.0 | ✅ (attribution) | ✅ Stable |
| **ESMFold / ESM-2** | `facebookresearch/esm` | MIT | MIT | ✅ | ⚠️ Archived (read-only) |
| **OpenFold** | `aqlaboratory/openfold` | Apache-2.0 | CC BY 4.0 | ✅ (trainable) | ✅ Active |
| **RoseTTAFold All-Atom** | `baker-laboratory/RoseTTAFold-All-Atom` | BSD-3 (code+weights) | BSD-3 | ✅ (pdb100 DB is NC) | ✅ Maintained |
| **RoseTTAFold** | `RosettaCommons/RoseTTAFold` | MIT | **non-commercial** (Rosetta-DL) | ⚠️→❌ | ❌ Superseded |
| **ESM3 / ESM-C** | `evolutionaryscale/esm` | MIT | ⚠️ **re-verify** (NC→MIT, recent) | ⚠️ | ✅ Active |
| **AlphaFold3** | `google-deepmind/alphafold3` | Apache-2.0 | **gated non-commercial** | ❌ | ✅ Active (also co-folds ligands) |
| **OpenFold3** | `aqlaboratory/openfold-3` | Apache-2.0 | **Apache-2.0** + open data | ✅ fully open | ✅ Active (2026; fully-open AF3) ⭐ |
| **Protenix** | `bytedance/Protenix` | Apache-2.0 | **Apache-2.0** | ✅ fully open | ✅ Active (v2, 2026) |
| **IntelliFold-2** | `IntelliGen-AI/IntelliFold` | Apache-2.0 | **Apache-2.0** | ✅ fully open | ✅ Active (2026; +affinity adapters) |

## Docking & co-folding (structure ± affinity) → [docking-and-cofolding.md](docking-and-cofolding.md)

The pose/affinity layer. Output is **STRUCTURE-ONLY** (pose + a confidence score) unless noted — **confidence ≠ affinity**. Only **Boltz-2** and **TankBind** predict binding affinity. License trap (DL/co-folding): **weights diverging from code** (the mirror of the Enamine trap).

**Classical / physics-based docking** (mature, mostly permissive; the one weights trap is gnina's CNN):

| Tool | Repo | Code | Commercial? | Status |
|---|---|---|---|---|
| **AutoDock Vina** | `ccsb-scripps/AutoDock-Vina` | Apache-2.0 | ✅ clean | ✅ Active (CPU; default engine) |
| **AutoDock-GPU** | `ccsb-scripps/AutoDock-GPU` | GPL-2.0 | ⚠️ copyleft | ✅ Active (GPU; AD4) |
| **smina** | `mwojcikowski/smina` | Apache+GPL | ⚠️ copyleft | ⚠️ Dormant → gnina |
| **gnina** | `gnina/gnina` (+`/models`) | Apache+GPL code; **weights no-license** | ⚠️→❌ CNN weights unlicensed | ✅ Active (CNN rescoring) |
| **QuickVina 2 / -W** | `QVina/qvina` | Apache-2.0 | ✅ | ⚠️ Stable (CPU) |
| **Vina-GPU 2.1** | `DeltaGroupNJUPT/Vina-GPU-2.1` | Apache-2.0 | ✅ | ✅ Stable (GPU/OpenCL) |
| **RxDock** | `rxdock/rxdock` (GitLab) | LGPL-3.0 | ✅ weak copyleft | ⚠️ Semi-dormant (RNA+protein) |
| **DOCK6** | `docking-org/dock6` | BSD-3 (GitHub) / academic EULA (UCSF) | ⚠️ provenance-dependent | ✅ Active |
| **Meeko** | `forlilab/Meeko` | LGPL-2.1 | ✅ | ✅ Very active (prep) |
| **RTMScore** | `sc8668/RTMScore` | MIT (+MIT weights) | ✅ | ⚠️ Dormant (ML rescoring) |

**Deep-learning docking & co-folding** (read weights separately from code):

| Tool | Repo | Code | Weights | Output | Commercial? | Status |
|---|---|---|---|---|---|---|
| **Boltz-2** | `jwohlwend/boltz` | MIT | **MIT** (HF) | **structure + AFFINITY** | ✅ fully open | ✅ Active (FEP-approaching) ⭐ |
| **Boltz-1** | `jwohlwend/boltz` | MIT | **MIT** (HF) | structure only | ✅ fully open | ✅ Active (AF3-class) |
| **Chai-1** | `chaidiscovery/chai-lab` | Apache-2.0 | **Apache-2.0** (relaxed Nov-24) | structure only | ✅ (post-Nov-24 release) | ✅ Active |
| **DiffDock / DiffDock-L** | `gcorso/DiffDock` | MIT | MIT | pose + confidence | ✅ | ✅ Active (diffusion docking) |
| **Uni-Mol Docking v2** | `deepmodeling/Uni-Mol` | MIT | MIT (Dropbox) | pose | ✅ | ✅ Active (PoseBusters-strong) |
| **Umol** | `patrickbryant1/Umol` | Apache-2.0 (README) | **CC BY 4.0** (Zenodo) | structure (from seq) | ✅ (attribution) | ⚠️ Moderate; no LICENSE file |
| **NeuralPLexer** | `zrqiao/NeuralPLexer` | BSD-3-Clear | **CC BY-NC-SA 4.0** (Zenodo) | structure (from seq) | ❌ weights non-commercial | ⚠️ Active-ish → NP3 closed |
| **EquiBind** | `HannesStark/EquiBind` | MIT | MIT (in-repo) | pose | ✅ | ❌ Legacy → DiffDock |
| **TankBind** | `luwei0917/TankBind` | MIT | MIT (in-repo) | **structure + AFFINITY** | ✅ (repo) | ❌ Legacy (dated deps) → Galixir |
| **AlphaFold3** | `google-deepmind/alphafold3` | Apache-2.0 | **gated non-commercial** | structure + confidence | ❌ non-commercial weights | ✅ Active (covered elsewhere) |
| **SigmaDock** | `alvaroprat97/sigmadock` | BSD-3 | BSD-3 | pose (PoseBusters-leading) | ✅ | ⚠️ New 2026, beta |
| **FlowDock** | `BioinfoMachineLearning/FlowDock` | MIT | MIT (Zenodo) | **structure + AFFINITY** | ✅ | ⚠️ Quiet (ISMB 2025) |

## Binding affinity & free energy (physics) → [binding-affinity-and-fep.md](binding-affinity-and-fep.md)

Rigorous affinity from MD. For cheap/fast **ML** affinity, see **Boltz-2** (docking table). FEP is GPU- and expertise-heavy.

| Tool | Repo | Code | Method | Commercial? | Status |
|---|---|---|---|---|---|
| **OpenFE** | `OpenFreeEnergy/openfe` | MIT | RBFE (OpenMM) | ✅ | ✅ Very active ⭐ |
| **Perses** | `choderalab/perses` | MIT | RBFE/ABFE/mutation | ✅ (pre-alpha) | ✅ Active |
| **alchemlyb** | `alchemistry/alchemlyb` | BSD-3 | FEP analysis (MBAR/BAR/TI) | ✅ | ✅ Active |
| **OpenMM** | `openmm/openmm` | MIT/LGPL (GPU=LGPL) | MD engine | ✅ | ✅ Very active |
| **BAT.py / BAT2** | `GHeinzelmann/BAT.py` | MIT | ABFE (AMBER/OpenMM) | ✅ | ✅ Active |
| **gmx_MMPBSA** | `Valdes-Tresanco-MS/gmx_MMPBSA` | GPL-3.0 | MM-PBSA/GBSA | ⚠️ copyleft | ✅ Active |
| **BioSimSpace** | `OpenBioSim/BioSimSpace` | GPL-3.0 | FEP workflow layer | ⚠️ copyleft | ✅ Active |
| **GROMACS** | `gromacs/gromacs` | LGPL-2.1 | MD engine + FEP | ✅ | ✅ Active |
| **Yank** | `choderalab/yank` | MIT | ABFE (legacy) | ✅ | ❌ Unmaintained |
| **LigUnity** | `IDEA-XL/LigUnity` | Apache-2.0 (data NC) | ML ranking (FEP-alt) + active learning | ✅ | ✅ Active (Patterns 2025) ⭐ |
| **AQAffinity** | `SandboxAQ/AQAffinity` | Apache-2.0 | ML affinity (Boltz-2 head on OpenFold3) | ✅ | ✅ New 2026 |
| **LamNet** | `RenlingHu/LamNet` | MIT | ML-accelerated FEP (λ-path GNN) | ✅ | ⚠️ Light (NSR 2026) |

## QSAR, bioactivity & property prediction → [property-and-qsar-prediction.md](property-and-qsar-prediction.md)

Frameworks (bring your own data) + dataset hubs + pretrained representations. Quality depends on YOUR training data; ChEMBL = CC BY-SA 3.0.

| Tool | Repo | Code | Type | Commercial? | Status |
|---|---|---|---|---|---|
| **Chemprop** | `chemprop/chemprop` | MIT | D-MPNN framework | ✅ | ✅ Very active ⭐ |
| **DeepChem** | `deepchem/deepchem` | MIT | toolkit | ✅ (check datasets) | ✅ Active |
| **PyTDC (TDC)** | `mims-harvard/TDC` | MIT | data/benchmark hub | ⚠️ data per-dataset | ✅ Active |
| **molfeat** | `datamol-io/molfeat` | Apache-2.0 | featurizers | ✅ | ✅ Active |
| **scikit-mol** | `EBjerrum/scikit-mol` | **LGPL-3.0** | sklearn transformers | ✅ (copyleft if modified) | ✅ Active |
| **MolPAL** | `coleygroup/molpal` | MIT | active-learning VS | ✅ | ⚠️ Stale (2021) |
| **QSARtuna** | `MolecularAI/QSARtuna` | Apache (no LICENSE file) | AutoML QSAR | ⚠️ | ✅ Active |
| **MoLFormer-XL** | `IBM/molformer` | Apache-2.0 (+weights) | pretrained LM (embeddings) | ✅ | ⚠️ Frozen artifact |
| **ChemBERTa** | `seyonechithrananda/bert-loves-chemistry` | MIT / weights unstated | pretrained LM | ⚠️ weights | ⚠️ Quiet |
| **Uni-Mol** | `deepmodeling/Uni-Mol` | MIT | 3D representation | ✅ | ✅ Active |
| **CheMeleon** | `JacksonBurns/chemeleon` | MIT | foundation encoder (Chemprop plug-in) | ✅ | ✅ Active (2026) ⭐ |

## ADMET prediction → [admet-prediction.md](admet-prediction.md)

Triage/flagging, not ground truth. Key split: **deployable local model** vs **web-only (can't embed)**.

| Tool | Repo / access | Code | Commercial? | Notes |
|---|---|---|---|---|
| **ADMET-AI** | `swansonk14/admet_ai` | MIT | ✅ local, CPU | Chemprop+TDC; hERG/BBB/CYP ⭐ |
| **OpenADMET** | `OpenADMET/openadmet-models` | Apache-2.0 | ✅ local, weights Apache | 2026 consortium; Caco-2/LogD/PPB/CL/CYP/PXR ⭐ |
| **B3DB** | `theochem/B3DB` | **CC0** | ✅ | BBB dataset (cleanest license) |
| **TDC** | `mims-harvard/TDC` | MIT | ✅ code / ⚠️ data | ADMET benchmark backbone |
| **BayeshERG** | `GIST-CSBL/BayeshERG` | MIT code / **NC weights** | ⚠️ retrain | hERG + uncertainty |
| **CardioTox** | `Abdulk084/CardioTox` | **no license** | ❌ | hERG ensemble |
| **CYP (Ersilia)** | `ersilia-os/eos44zp` | GPL-3.0 | ⚠️ copyleft, archived | or DIY on TDC |
| **SwissADME** | web `swissadme.ch` | web-only | ⚠️ results CC-BY; not embeddable | physchem/druglikeness |
| **DeepPK / ADMETlab 3.0 / pkCSM** | web | web-only | ❌ embed (NC / paid) | manual triage only |

## Target, off-target & selectivity prediction → [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md)

Off-target / anti-target screening (e.g. catch a 5-HT2B liability) + ligand-based shape/pharmacophore overlay.

| Tool | Repo / access | Code | Commercial? | Notes |
|---|---|---|---|---|
| **ChEMBL multitask** | `chembl/chembl_multitask_model` | MIT | ✅ (data CC BY-SA) | embeddable off-target screen ⭐ |
| **ESP-Sim** | `hesther/espsim` | MIT | ✅ | 3D shape + electrostatic overlay |
| **Shape-it** | `silicos-it/shape-it` | MIT | ✅ | Gaussian shape overlay (ROCS-like) |
| **Align-it** | `OliverBScott/align-it` | **GPL-3.0** | ⚠️ copyleft | pharmacophore alignment |
| **RDKit (shape/pharm)** | `rdkit/rdkit` | BSD-3 | ✅✅ | permissive baseline |
| **OpenPharmacophore** | `uibcdf/OpenPharmacophore` | MIT | ✅ | pharmacophore modeling (stale) |
| **ROSHAMBO2** | `molecularinformatics/roshambo2` | MIT | ✅ | GPU ROCS-style shape (2026; faster than Shape-it) ⭐ |
| **DiffPhore** | `VicFisher/DiffPhore` | MIT | ✅ | ML ligand-pharmacophore mapping (Nat Commun 2025) |
| **SwissTargetPrediction** | web | web-only | ⚠️ query-only | target fishing |
| **SEA / PPB2 / PPB3** | web / `reymond-group/PPB3` | none / no-license | ❌ | SEAware proprietary; PPB3 no license |

## Structure-based (pocket-conditioned) generation → [structure-based-generation.md](structure-based-generation.md)

Generate ligands INTO a pocket; outputs almost never synthesizable → project downstream (PrexSyn) / score (AiZynthFinder). Includes pocket detection. Two no-license traps read wrong on GitHub — **TargetDiff, PocketFlow are genuine MIT** (misspelled LICENSE files).

| Tool | Repo | Code | Method | Commercial? | Synth? |
|---|---|---|---|---|---|
| **PILOT / e3moldiffusion** | `pfizer-opensource/e3moldiffusion` | Apache-2.0 | diffusion + guidance | ✅ | ⚠️ guidance |
| **REINVENT 4** | `MolecularAI/REINVENT4` | Apache-2.0 | RL (Lib/LinkInvent) | ✅ | ⚠️ configurable |
| **DiffSBDD** | `arneschneuing/DiffSBDD` | MIT | diffusion | ✅ | ❌ (SA post-hoc) |
| **PocketFlow** | `Saoge123/PocketFlow` | MIT (misspelled) | knowledge-guided flow | ✅ | ⚠️ valid-only |
| **Pocket2Mol** | `pengxingang/Pocket2Mol` | MIT | autoregressive | ✅ | ❌ |
| **TargetDiff** | `guanjq/targetdiff` | MIT (misspelled) | diffusion + affinity rank | ✅ | ❌ |
| **ResGen** | `HaotianZhangAI4Science/ResGen` | MIT | autoregressive | ✅ | ❌ |
| **Apo2Mol** | `AIDD-LiLab/Apo2Mol` | MIT | diffusion (apo pocket) | ✅ | ❌ |
| **Lingo3DMol** | `stonewiseAIDrugDesign/Lingo3DMol` | **GPL-3.0** | LM + 3D | ⚠️ copyleft | ❌ |
| **DecompDiff** | `bytedance/DecompDiff` | **CC-BY-NC** | diffusion | ❌ NC | ❌ |
| **fpocket** | `Discngine/fpocket` | MIT | pocket detection | ✅ | — |
| **P2Rank** | `rdk/p2rank` | MIT | ML pocket detection | ✅ | — |
| **DoGSiteScorer** | web (ProteinsPlus) | web-only | pocket detection | ❌ | — |
| **PocketXMol** | `pengxingang/PocketXMol` | MIT | multi-task (SBDD+frag/linker+PROTAC+dock) | ✅ (CC-BY-4.0 weights) | ❌ (2026, Cell) ⭐ |
| **OMTRA** | `gnina/OMTRA` | Apache-2.0 | multi-task flow-matching | ✅ | ❌ (2026, gnina lab) |
| **Saturn** | `schwallergroup/saturn` | Apache-2.0 (detector false-neg) | sample-efficient RL | ✅ | ⚠️ synth-control feature |
| **RxnFlow** | `SeonghwanSeo/RxnFlow` | MIT | synthesis GFlowNet | ✅ | ✅ **synthesizable by construction** |
| **CGFlow** | `tsa87/cgflow` | MIT | synthesis pathway + 3D pose | ✅ | ✅ **synthesizable by construction** |
| **ShEPhERD** | `coleygroup/shepherd` | MIT | shape/ESP/pharmacophore-conditioned gen | ✅ | ❌ |

## Agentic / LLM-orchestrated drug design → [agentic-drug-design.md](agentic-drug-design.md)

LLM / multi-agent systems that orchestrate the other tools (generate → dock → ADMET → retro). API-dependent; young; treat as reference architectures + runnable starting points, not turnkey.

| Tool | Repo | Code | Backend | Commercial? | Status |
|---|---|---|---|---|---|
| **AgentD** | `hoon-ock/AgentD` | MIT | GPT-4o (+Claude/DeepSeek) | ✅ (code; +API) | ✅ Most active ⭐ |
| **CLADD** | `Genentech/CLADD` | Apache-2.0 | model-agnostic | ✅ (code; +API) | ✅ AAAI 2026 (RAG QA) |
| **delta** | `deltawave-tech/delta` | MIT | Claude/o3/Gemini/GPT | ✅ (code; +API) | ⚠️ One-shot drop (blueprint) |
| **DrugPilot** | `wzn99/DrugPilot` | MIT | API-driven | ✅ (code; +API) | ⚠️ Notebook-grade |
| **Mozi** | — (no code yet) | — | open Qwen3/DeepSeek | — | ⚠️ Paper only (watchlist) |

## Chemical language models → [chemical-language-models.md](chemical-language-models.md)

⚠️ Every one has a license trap; none cleanly commercial.

| Tool | Repo | Binding license | Base | Status |
|---|---|---|---|---|
| **SynLlama** | `THGLab/SynLlama` | UC **non-commercial** | Llama-3.1/3.2 | research-only |
| **ChemDFM-R** | (HF only) `OpenDFM/ChemDFM-R-14B` | weights **AGPL-3.0** | Qwen2.5-14B | research |
| **Mol-LLaMA** | `DongkiKim95/Mol-LLaMA` | **no code license** + Llama | Llama-3.1/2 | research |
| **ChemMLLM** | `bbsbz/ChemMLLM` | no license; **no weights**; Chameleon NC | Chameleon-7B | research |
| *ChemDual, RetroDFM-R* | *(see above)* | Apache code / restricted weights | LLaMA-3.1 / Llama-3 | — |

## Not ready — watchlist → [watchlist.md](watchlist.md)

Paper-only (no code): **Reactron, Retro-Expert, ReTriP, TempRe, RetroTrim**. Code-but-no-license: **InterRetro, ConRetroBert, SynCoGen-code, SynTwins-code, Mol-LLaMA-code, ChemMLLM-code, GVT, SmiSelf, CardioTox, PPB3** (note: **TargetDiff & PocketFlow look no-license on GitHub but are genuine MIT** — misspelled files). Released-but-non-commercial: **SynLlama, ChemDFM-R, APEX, NeuralPLexer-weights, AlphaFold3-weights, RoseTTAFold-weights, DecompDiff, BayeshERG-weights** (and **ChemDual/RetroDiT** = no weights yet; ESM3/ESM-C weights = re-verify). Proprietary / web-only / no open release: **NeuralPLexer3** (Iambic), **Chai-2/Chai-3**, **PLANTS, SEA/SEAware, SPiDER/TIGER, DoGSiteScorer**, the ADMET web tools (**DeepPK, ADMETlab, pkCSM**), and commercial reference points (**Schrödinger FEP+/Glide/Phase, OpenEye ROCS, Cresset Flare**). **2026 arrivals on the watchlist** (non-commercial / missing-LICENSE / paper-only): **MATCHA, FLOWR.root, GatorAffinity, DiffSMol, Suiren, JMM, EDMolGPT** (license blockers); **OmniBind, PIGLET, CREED/ChemCensor, AOT\*, Retro-R1, RetroReasoner, Mozi** (no code) — see [watchlist.md](watchlist.md).

## Lineage notes

- **Coley-group synthesizable line:** ChemProjector (ICML 2024, archived) → SynFormer (PNAS 2025, quiet) → **PrexSyn** (2025, active). Shared 115-reaction-template set. Default to PrexSyn.
- **ReaSyn** (NVIDIA) reuses SynFormer's templates; **SynCoGen** uses RGFN's block vocabulary; **GenMol** is NVIDIA BioNeMo's general generator.
- **OpenDFM / SJTU line:** ChemDFM → ChemDFM-R (reasoning) and RetroDFM-R (retrosynthesis).
- **Schwaller group (EPFL):** Synthelite, LLM-Syn-Planner, TempRe; underpins much round-trip-score methodology.
- **AstraZeneca stack:** AiZynthFinder + rxnutils (which depends on **RDChiral**, the foundational template layer).
- **MIT docking line (Barzilay/Jaakkola lab):** EquiBind (ICML 2022, Stärk) → **DiffDock** (ICLR 2023, Corso) → **DiffDock-L** (ICLR 2024) for docking; same lab's **Boltz-1/-2** for co-folding (Wohlwend/Corso/Passaro), now also the Boltz PBC spinout. EquiBind is superseded by DiffDock.
- **AF3-class open co-folders:** **Boltz-1/-2** (MIT), **Chai-1** (Apache), plus Protenix/HelixFold3 — all reimplement/extend **AlphaFold3** (DeepMind, non-commercial) under permissive licenses. Boltz-2 adds the affinity head AF3 lacks.
- **NeuralPLexer line:** open **NeuralPLexer** (Caltech, Qiao; NMI 2024) → closed **NeuralPLexer3** (Iambic Therapeutics, 2024). Open weights are CC BY-NC-SA; NP3 is proprietary.
- **AutoDock lineage (Scripps / Forli):** AutoDock4 → **AutoDock Vina** → **smina** → **gnina** (CNN rescoring); GPU forks **QuickVina / Vina-GPU / AutoDock-GPU**; **Meeko** is the shared prep layer. All Vina-family scoring is empirical/physics-based.
- **Chodera / OpenFF free-energy stack:** **OpenMM** (engine) → **Perses** (research) → **OpenFE** (production RBFE); **Yank** is the legacy ancestor. alchemlyb analyzes any engine's output.
- **AlphaFold lineage (receptor):** **AlphaFold2** (CC BY 4.0 weights) → **ColabFold** / **OpenFold** reimplementations; **AlphaFold3** (Apache code, gated NC weights) → open co-folders **Boltz-1/-2**, **Chai-1** (cross-listed in docking).
- **Chemprop / TDC stack (Coley-Barzilay + Harvard Zitnik):** **Chemprop** (D-MPNN) underlies **ADMET-AI** (Swanson — also SyntheMol), **CheMeleon** (the foundation encoder), **OpenADMET**, and most QSAR/ADMET models here; **TDC** is the shared dataset/benchmark backbone (ChEMBL-derived → CC BY-SA data terms).
- **Open AF3-class co-folders (2026):** AlphaFold3 (DeepMind, NC weights) spawned the permissive reimplementations **Boltz-1/-2** (MIT), **Chai-1** (Apache), and now **OpenFold3 / Protenix / IntelliFold-2** (all Apache code *and* weights) — the commercial-clean AF3 alternatives.
- **Agentic-DD orchestration layer (2025–26):** **AgentD, CLADD, delta, Mozi** wire the generators / dockers / ADMET / retro tools together — open prototypes of a full design-make-test loop (the layer a `biosymphony`-style platform occupies).
