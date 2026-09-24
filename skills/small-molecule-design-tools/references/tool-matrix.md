# Tool Matrix

This matrix indexes tools by task category. Broad source checks were recorded
on **2026-06-11** for synthesizability entries and **2026-06-13** for
target-based entries. Changed cards were checked against primary sources on
**2026-08-30**; LDDM and RetroChimera were checked separately on **2026-09-21**.
These dates do not mean that every unchanged row was rechecked.
Check primary repository, model-card, and data terms before use;
[Licensing and Data Terms](licensing-and-data.md) explains the separate layers.

The **License signal** column summarizes the reviewed artifacts. ✅ marks MIT,
Apache-2.0, BSD, CC BY 4.0, or CC0 labels; ⚠️ marks LGPL, other copyleft
licenses, additional terms, or unverified terms; and ❌ marks non-commercial
terms, a missing license grant, or no open release. The signal does not
say whether a specific use is permitted.
The matrix first covers synthesizability and route planning, then target-based
design.

Status legend: ✅ active · ⚠️ limited or uncertain · ❌ archived, superseded, or
unreleased · — not applicable

## Synthesizable Generation, Projection, and Analogs

See [synthesizable-generation.md](synthesizable-generation.md).

Output = molecule **with a synthesis route**, or a makeable analog + how to make it. Many depend on vendor building blocks.

| Tool | Repository | Code | Weights | License signal | Status |
|---|---|---|---|---|---|
| **PrexSyn** | `luost26/prexsyn` | MIT | MIT-labeled data/model records | ⚠️ Enamine-derived data | ✅ v1.1.3 (2026-08-08) |
| **SynFormer** | `wenhao-gao/synformer` | Apache-2.0 | Apache-2.0 | ⚠️ data "research only" | ⚠️ Quiet; author-deprecated |
| **ChemProjector** | `luost26/ChemProjector` | MIT | (Google Drive) | ⚠️ Enamine, archived | ❌ Archived → PrexSyn |
| **ReaSyn** | `NVIDIA-BioNeMo/ReaSyn` | Apache-2.0 | **NVIDIA Open Model** | ⚠️ weights+Enamine | ✅ Active |
| **SynCoGen** | `andreirekesh/SynCoGen` | **none** | HF MIT | ⚠️ code unlicensed | ✅ Active (3D) |
| **SynTwins** | `snu-micc/SynTwins` | **none** | — | ❌ no license | ⚠️ Minimal (training-free) |
| **SynLlama** | `THGLab/SynLlama` | **UC non-commercial** | Figshare | ❌ non-commercial | ✅ Maintained (research) |
| **LDDM** | `LPDI-EPFL/lddm` | MIT | MIT `CDBB` / CC BY-NC paper checkpoint | ⚠️ checkpoint and reaction-space terms | ⚠️ Early research release |
| **SyntheMol** | `swansonk14/SyntheMol` | MIT | Zenodo terms not stated | ⚠️ artifact + vendor terms | ✅ v_2.0.0 (2025-05-12) |
| **APEX** | `NumerionLabs/apex` | **no `LICENSE` file** | Zenodo terms not stated | ❌ no license grant | ⚠️ 2025 preprint |

## General Molecular Generation

These tools address validity rather than synthesizability. See
[molecular-generation.md](molecular-generation.md).

| Tool | Repository | Code | Weights | License signal | Status |
|---|---|---|---|---|---|
| **GenMol** | `NVIDIA-BioNeMo/genmol` | Apache-2.0 | **NVIDIA Open Model** | ⚠️ separate weight terms | ✅ V2 dated 2025-10-15 |
| **MolReactGen** | `hogru/MolReactGen` | MIT | HF (MIT) | ✅ | ⚠️ Dormant (thesis) |
| **SmiSelf** | `wentao228/SmiSelf` | **none** | — (rule-based) | ❌ no license | ⚠️ Utility (EMNLP 2025) |
| **GVT** | `zzccppp/GVT` | **none** | README links | ❌ no license | ⚠️ 2025 preprint |

## Multi-Step Retrosynthesis and Route Planning

See [retrosynthesis-planning.md](retrosynthesis-planning.md).

| Tool | Repository | Code | Weights/model | License signal | Status |
|---|---|---|---|---|---|
| **AiZynthFinder** | `MolecularAI/aizynthfinder` | MIT | USPTO model (free) | ✅ MIT stack | ✅ v4.4.1 |
| **RENKIN** | `kent-tokyo/renkin` | MIT | — | ✅ MIT | ✅ v0.47.0 (2026-08-28) |
| **ASKCOS** | `mlpds_mit/askcosv2` (GitLab) | MIT (v2) | mostly MIT; Reaxys NC; CAS gated | ⚠️ model-specific terms | ✅ Active (heavy deployment) |
| **Syntheseus** | `microsoft/syntheseus` | MIT | wraps others | ✅ code | ✅ [v0.9.0](https://github.com/microsoft/syntheseus/releases/tag/v0.9.0) (2026-09-23) |
| **Tango\*** | `schwallergroup/TangoStar` | MIT | separate DESP model/data record | ⚠️ artifact terms | ✅ 2025 constrained search method |
| **SynPlanner** | `Laboratoire-de-Chemoinformatique/SynPlanner` | MIT | separate data record | ⚠️ data terms | ✅ v1.7.0 (2026-08-25) |
| **InterRetro** | `MianchuWang/InterRetro` | **none** | — | ❌ no stated license | ⚠️ NeurIPS 2025 |
| **RetroCast / SynthArena** | `ischemist/project-procrustes` (+`/syntharena`) | MIT | wraps others | ✅ | ✅ Active (2026; route validation) |

## Single-Step Retrosynthesis Models

See [singlestep-retrosynthesis.md](singlestep-retrosynthesis.md).

| Tool | Repository | Code | Weights | USPTO-50K top-1 | Status |
|---|---|---|---|---|---|
| **ReactionT5v2** | `sagawatatsuya/ReactionT5v2` | MIT | HF (MIT) | 71.2% (ft) | ✅ Maintained |
| **RetroChimera** | `microsoft/retrochimera` | MIT | Figshare (MIT) | See checkpoint-specific paper settings | v1.3.0 (2026-09-21) |
| **RXNGraphormer** | `licheng-xu-echo/RXNGraphormer` | MIT | Figshare | (in paper) | ✅ Active |
| **GDiffRetro** | `sunshy-1/GDiffRetro` | MIT | SharePoint | (in paper) | ⚠️ Dormant (AAAI 2025) |
| **RetroDFM-R** | `OpenDFM/RetroDFM-R` | MIT | Apache-2.0-tagged Qwen3 checkpoint | 60.4% (claim) | ⚠️ base/data terms |
| **RetroDiT** | `LOGO-CUHKSZ/RetroDiT` | MIT | ❌ not released | 61.2/71.1% (claim) | ⚠️ 2026 preprint |
| **RxnNano** | `rlisml/RxnNano` | MIT | ❌ not released | (reported in paper) | ⚠️ 2026; no weights |
| **ConRetroBert** | `JahidBasher/ConRetroBert` | **none** | Google Drive | 62.4% (claim) | ⚠️ No stated license |
| **TempRe** | — (no repository) | — | — | (PaRoutes only) | ❌ Preprint only |

## Agentic and LLM-Assisted Retrosynthesis

See [agentic-retrosynthesis.md](agentic-retrosynthesis.md).

The reviewed workflows use external LLM backends. Check the selected provider's
terms and require chemistry review of generated routes.

| Tool | Repository | Code | LLM backend | License signal | Status |
|---|---|---|---|---|---|
| **DeepRetro** | `deepforestsci/DeepRetro` | MIT | Configurable external backend | ⚠️ backend terms vary | ✅ Peer-reviewed; GUI |
| **Synthelite** | `schwallergroup/synthelite` | MIT | Configurable external backend | ⚠️ backend terms vary | ✅ Active preprint |
| **LLM-Syn-Planner** | `zoom-wang112358/LLM-Syn-Planner` | MIT | Configurable external backend | ⚠️ backend terms vary | ⚠️ Limited maintenance |
| **LARC** | `ninglab/LARC` | **none** | Configurable external backend | ❌ no stated license | ⚠️ Watchlist |
| **RetroAgent** | `SXKDZ/RetroAgent` | MIT | Apache-2.0-tagged Qwen3 checkpoint | ⚠️ base/data terms | ✅ COLM 2026 |
| **Retro-Expert** | — (no repository) | — | Qwen2.5-7B | ❌ no code | ❌ Preprint only |
| **ReTriP** | — (no repository) | — | Qwen3-8B | ❌ no code | ❌ Preprint only |

## Forward Reaction and Mechanism Prediction

See [forward-and-reaction-modeling.md](forward-and-reaction-modeling.md).

| Tool | Repository | Code | Weights | License signal | Status |
|---|---|---|---|---|---|
| **DeepMech** | `alhqlearn/DeepMech` | MIT | Zenodo (CC-BY/MIT) | ✅ | ✅ Released (mechanism) |
| **ReaDISH** | `Meteor-han/ReaDISH` | MIT | in-repository checkpoint | ✅ | ✅ 2026 (yield and selectivity) |
| **ProPreT5** | `DerinOzer/ProPreT5` | MIT | ❌ train yourself | ✅ (code) | ⚠️ No weights |
| **ChemDual** | `JacklinGroup/ChemDual` | Apache-2.0 | ❌ pending | ⚠️ no model released | ⚠️ Watchlist |
| **Reactron** | — (no repository) | — | — | ❌ no code | ❌ Paper only |
| *ReactionT5v2 and RXNGraphormer* | *(see single-step section)* | MIT | See the one-step rows | ✅ | Cross-reference |
| **ForwardChimeraDeNovo** | `microsoft/retrochimera` | MIT | Figshare (MIT) | MIT code and checkpoint; separate data terms | v1.3.0 (2026-09-21) |

## Reaction-Template and Rule Infrastructure

See [template-and-rule-infrastructure.md](template-and-rule-infrastructure.md).

These CPU tools state MIT or Apache-2.0 terms. The detailed reference records
cases where the package name differs from the import name.

| Tool | Repository | Code | pip name | Status |
|---|---|---|---|---|
| **RDChiral** | `connorcoley/rdchiral` | MIT | `rdchiral` | ✅ Stable |
| **rdchiral_plus** | `denovochem/rdchiral_plus` | MIT | `rdchiral-plus` | ✅ v0.5.0 (2026-08-14) |
| **rxnutils** | `MolecularAI/reaction_utils` | Apache-2.0 | `reaction-utils` | ✅ Active (curation pipelines) |
| **SynTemp** | `TieuLongPhan/SynTemp` | MIT | `syntemp` | ✅ Moderate (ITS/DPO rules) |

## Synthesizability Scoring

See [synthesizability-scoring.md](synthesizability-scoring.md).

| Tool | Repository | Code | Notes |
|---|---|---|---|
| **RetroScore** | `Snowgao320/RetroScore` | MIT (weights unspecified) | route-aware SA score + GED |
| **shallow-tree** | `Arhs99/shallow-tree` | **GPL-3.0** | fast depth-limited AiZynthFinder screen (2026) |
| **round-trip score** | — (concept) | — | retro→forward recovery check; cheapest validation |
| **RetroTrim** | — (no repository) | — | hallucination-ensemble; preprint only |

---

The remaining sections cover receptor structure, docking, affinity, QSAR,
ADMET, selectivity, and structure-based generation.

## Protein Structure Prediction and Receptor Preparation

See [protein-structure-prediction.md](protein-structure-prediction.md).

Docking requires a target structure. Check the code and model-weight terms
separately.

| Tool | Repository | Code | Weights | License signal | Status |
|---|---|---|---|---|---|
| **ColabFold** | `sokrypton/ColabFold` | MIT | AF2 params CC BY 4.0 | ✅ (attribution) | ✅ Active (fast AF2) |
| **AlphaFold2** | `google-deepmind/alphafold` | Apache-2.0 | CC BY 4.0 | ✅ (attribution) | ✅ Stable |
| **ESMFold / ESM-2** | `facebookresearch/esm` | MIT | MIT | ✅ | ⚠️ Archived (read-only) |
| **OpenFold** | `aqlaboratory/openfold` | Apache-2.0 | CC BY 4.0 | ✅ (trainable) | ✅ Active |
| **RoseTTAFold All-Atom** | `baker-laboratory/RoseTTAFold-All-Atom` | BSD-3 (code+weights) | BSD-3 | ✅ (pdb100 DB is NC) | ✅ Maintained |
| **RoseTTAFold** | `RosettaCommons/RoseTTAFold` | MIT | **non-commercial** (Rosetta-DL) | ❌ non-commercial weights | ❌ Superseded |
| **ESM3 / ESM-C** | `Biohub/esm` | MIT | MIT for listed Biohub releases | ✅ MIT stack | ✅ Active; check exact checkpoint |
| **AlphaFold3** | `google-deepmind/alphafold3` | Apache-2.0 | **gated non-commercial** | ❌ | ✅ v3.0.2 (2026-04-20) |
| **OpenFold3 / OpenBind-0** | `aqlaboratory/openfold-3` | Apache-2.0 | **Apache-2.0** + released data/recipes | ✅ Apache-2.0 stack | ⚠️ Preview; OpenBind-0 released 2026-08-21 |
| **Protenix** | `bytedance/Protenix` | Apache-2.0 | **Apache-2.0** | ✅ Apache-2.0 stack | ✅ v2 (2026-04-08) |

## Docking and Co-Folding

See [docking-and-cofolding.md](docking-and-cofolding.md).

Most entries return a pose and confidence score rather than binding affinity.
Boltz-2, TankBind, and FlowDock also predict affinity. Check model-weight terms
separately from code terms.

**Classical and physics-based docking:**

| Tool | Repository | Code | License signal | Status |
|---|---|---|---|---|
| **AutoDock Vina** | `ccsb-scripps/AutoDock-Vina` | Apache-2.0 | ✅ Apache-2.0 | ✅ Active (CPU; default engine) |
| **AutoDock-GPU** | `ccsb-scripps/AutoDock-GPU` | GPL-2.0 | ⚠️ copyleft | ✅ Active (GPU; AD4) |
| **smina** | `mwojcikowski/smina` | Apache+GPL | ⚠️ copyleft | ⚠️ Dormant → gnina |
| **gnina** | `gnina/gnina` (+`/models`) | Apache+GPL code; **weights no-license** | ❌ weights lack a stated license | ✅ Active (CNN rescoring) |
| **QuickVina 2 / -W** | `QVina/qvina` | Apache-2.0 | ✅ | ⚠️ Stable (CPU) |
| **Vina-GPU 2.1** | `DeltaGroupNJUPT/Vina-GPU-2.1` | Apache-2.0 | ✅ | ✅ Stable (GPU/OpenCL) |
| **RxDock** | `rxdock/rxdock` (GitLab) | LGPL-3.0 | ✅ weak copyleft | ⚠️ Semi-dormant (RNA+protein) |
| **DOCK6** | `docking-org/dock6` | BSD-3 (GitHub) / academic EULA (UCSF) | ⚠️ provenance-dependent | ✅ Active |
| **Meeko** | `forlilab/Meeko` | LGPL-2.1 | ✅ | ✅ Active (preparation) |
| **RTMScore** | `sc8668/RTMScore` | MIT (+MIT weights) | ✅ | ⚠️ Dormant (ML rescoring) |

**Deep-learning docking & co-folding** (read weights separately from code):

| Tool | Repository | Code | Weights | Output | License signal | Status |
|---|---|---|---|---|---|---|
| **Boltz-2** | `jwohlwend/boltz` | MIT | **MIT** (HF) | **structure + affinity estimate** | ✅ MIT stack | ✅ Active |
| **Boltz-1** | `jwohlwend/boltz` | MIT | **MIT** (HF) | structure only | ✅ MIT stack | ✅ Active (AF3-class) |
| **Chai-1** | `chaidiscovery/chai-lab` | Apache-2.0 | **Apache-2.0** (relaxed Nov-24) | structure only | ✅ (post-Nov-24 release) | ✅ Active |
| **DiffDock / DiffDock-L** | `gcorso/DiffDock` | MIT | MIT | pose + confidence | ✅ | ✅ Active (diffusion docking) |
| **Uni-Mol Docking v2** | `deepmodeling/Uni-Mol` | MIT | MIT (Dropbox) | pose | ✅ | ✅ Active; PoseBusters benchmark |
| **Umol** | `patrickbryant1/Umol` | Apache-2.0 (README) | **CC BY 4.0** (Zenodo) | structure (from seq) | ✅ (attribution) | ⚠️ Moderate; no LICENSE file |
| **NeuralPLexer** | `zrqiao/NeuralPLexer` | BSD-3-Clear | **CC BY-NC-SA 4.0** (Zenodo) | structure from sequence | ❌ weights non-commercial | ⚠️ Limited; NeuralPLexer3 is closed |
| **EquiBind** | `HannesStark/EquiBind` | MIT | MIT (in-repository) | pose | ✅ | ❌ Legacy → DiffDock |
| **TankBind** | `luwei0917/TankBind` | MIT | MIT (in-repository) | **structure + AFFINITY** | ✅ (repository) | ❌ Legacy (dated deps) → Galixir |
| **AlphaFold3** | `google-deepmind/alphafold3` | Apache-2.0 | **gated non-commercial** | structure + confidence | ❌ non-commercial weights | ✅ Active (covered elsewhere) |
| **SigmaDock** | `alvaroprat97/sigmadock` | BSD-3 | BSD-3 | pose | ✅ | ⚠️ 2026 beta |
| **FlowDock** | `BioinfoMachineLearning/FlowDock` | MIT | MIT (Zenodo) | **structure + AFFINITY** | ✅ | ⚠️ Quiet (ISMB 2025) |

## Binding Affinity and Free Energy

See [binding-affinity-and-fep.md](binding-affinity-and-fep.md).

These tools estimate affinity with molecular dynamics and free-energy methods.
The docking table lists ML affinity predictors. Free-energy workflows require
specialized setup and compute.

| Tool | Repository | Code | Method | License signal | Status |
|---|---|---|---|---|---|
| **OpenFE** | `OpenFreeEnergy/openfe` | MIT | RBFE (OpenMM) | ✅ | ✅ Active |
| **Perses** | `choderalab/perses` | MIT | RBFE/ABFE/mutation | ✅ (pre-alpha) | ✅ Active |
| **alchemlyb** | `alchemistry/alchemlyb` | BSD-3 | FEP analysis (MBAR/BAR/TI) | ✅ | ✅ Active |
| **OpenMM** | `openmm/openmm` | MIT/LGPL (GPU=LGPL) | MD engine | ✅ | ✅ Active |
| **BAT.py / BAT2** | `GHeinzelmann/BAT.py` | MIT | ABFE (AMBER/OpenMM) | ✅ | ✅ Active |
| **gmx_MMPBSA** | `Valdes-Tresanco-MS/gmx_MMPBSA` | GPL-3.0 | MM-PBSA/GBSA | ⚠️ copyleft | ✅ Active |
| **BioSimSpace** | `OpenBioSim/BioSimSpace` | GPL-3.0 | FEP workflow layer | ⚠️ copyleft | ✅ Active |
| **GROMACS** | `gromacs/gromacs` | LGPL-2.1 | MD engine + FEP | ✅ | ✅ Active |
| **Yank** | `choderalab/yank` | MIT | ABFE (legacy) | ✅ | ❌ Unmaintained |
| **LigUnity** | `IDEA-XL/LigUnity` | Apache-2.0 (data NC) | ML ranking and active learning | ⚠️ data terms | ✅ Patterns 2025 |
| **AQAffinity** | `SandboxAQ/AQAffinity` | Apache-2.0 | ML affinity (Boltz-2 head on OpenFold3) | ✅ | ✅ 2026 release |
| **LamNet** | `RenlingHu/LamNet` | MIT | ML-accelerated FEP (λ-path GNN) | ✅ | ⚠️ Light (NSR 2026) |

## QSAR, Bioactivity, and Property Prediction

See [property-and-qsar-prediction.md](property-and-qsar-prediction.md).

This category includes modeling frameworks, dataset hubs, and pretrained
representations. Model quality depends on the selected training data. ChEMBL
states CC BY-SA 3.0 terms.

| Tool | Repository | Code | Type | License signal | Status |
|---|---|---|---|---|---|
| **Chemprop** | `chemprop/chemprop` | MIT | D-MPNN framework | ✅ | ✅ Active |
| **DeepChem** | `deepchem/deepchem` | MIT | toolkit | ✅ (check datasets) | ✅ Active |
| **PyTDC (TDC)** | `mims-harvard/TDC` | MIT | data/benchmark hub | ⚠️ data per-dataset | ✅ Active |
| **molfeat** | `datamol-io/molfeat` | Apache-2.0 | featurizers | ✅ | ✅ Active |
| **scikit-mol** | `EBjerrum/scikit-mol` | **LGPL-3.0** | sklearn transformers | ⚠️ LGPL-3.0 terms | ✅ Active |
| **MolPAL** | `coleygroup/molpal` | MIT | active-learning VS | ✅ | ⚠️ Stale (2021) |
| **QSARtuna** | `MolecularAI/QSARtuna` | Apache (no LICENSE file) | AutoML QSAR | ⚠️ | ✅ Active |
| **MoLFormer-XL** | `IBM/molformer` | Apache-2.0 (+weights) | pretrained LM (embeddings) | ✅ | ⚠️ Frozen artifact |
| **ChemBERTa** | `seyonechithrananda/bert-loves-chemistry` | MIT / weights unstated | pretrained LM | ⚠️ weights | ⚠️ Quiet |
| **Uni-Mol** | `deepmodeling/Uni-Mol` | MIT | 3D representation | ✅ | ✅ Active |
| **CheMeleon** | `JacksonBurns/chemeleon` | MIT | foundation encoder (Chemprop plug-in) | ✅ | ✅ Active (2026) |

## ADMET Prediction

See [admet-prediction.md](admet-prediction.md).

Use these tools for triage rather than experimental conclusions. The table
separates local models from hosted services with separate terms.

| Tool | Repository / access | Code | License signal | Notes |
|---|---|---|---|---|
| **ADMET-AI** | `swansonk14/admet_ai` | MIT | ✅ local, CPU | Chemprop+TDC; hERG/BBB/CYP |
| **OpenADMET** | `OpenADMET/openadmet-models` | Apache-2.0 | ✅ local, weights Apache | 2026 consortium; Caco-2/LogD/PPB/CL/CYP/PXR |
| **B3DB** | `theochem/B3DB` | **CC0** | ✅ | BBB dataset under CC0 |
| **TDC** | `mims-harvard/TDC` | MIT | ✅ code / ⚠️ data | ADMET benchmark backbone |
| **BayeshERG** | `GIST-CSBL/BayeshERG` | MIT code / **NC weights** | ⚠️ split terms | hERG + uncertainty |
| **CardioTox** | `Abdulk084/CardioTox` | **no license** | ❌ | hERG ensemble |
| **CYP (Ersilia)** | `ersilia-os/eos44zp` | GPL-3.0 | ⚠️ copyleft, archived | or train on TDC data |
| **SwissADME** | web `swissadme.ch` | web-only | ⚠️ hosted; CC BY results | physchem/druglikeness |
| **DeepPK / ADMETlab 3.0 / pkCSM** | web | web-only | ⚠️ hosted; separate terms | no local artifacts published |

## Target, Off-Target, and Selectivity Prediction

See [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md).

This category covers off-target screening and ligand-based shape or
pharmacophore comparisons.

| Tool | Repository / access | Code | License signal | Notes |
|---|---|---|---|---|
| **ChEMBL multitask** | `chembl/chembl_multitask_model` | MIT | ⚠️ data CC BY-SA | local ONNX off-target screen |
| **ESP-Sim** | `hesther/espsim` | MIT | ✅ | 3D shape + electrostatic overlay |
| **Shape-it** | `silicos-it/shape-it` | MIT | ✅ | Gaussian shape overlay (ROCS-like) |
| **Align-it** | `OliverBScott/align-it` | **GPL-3.0** | ⚠️ copyleft | pharmacophore alignment |
| **RDKit (shape/pharm)** | `rdkit/rdkit` | BSD-3 | ✅ BSD-3 | shape/pharmacophore baseline |
| **OpenPharmacophore** | `uibcdf/OpenPharmacophore` | MIT | ✅ | pharmacophore modeling (stale) |
| **ROSHAMBO2** | `molecularinformatics/roshambo2` | MIT | ✅ | GPU shape screening (2026) |
| **DiffPhore** | `VicFisher/DiffPhore` | MIT | ✅ | ML ligand-pharmacophore mapping (Nat Commun 2025) |
| **SwissTargetPrediction** | web | web-only | ⚠️ query-only | target fishing |
| **SEA / PPB2 / PPB3** | web / `reymond-group/PPB3` | none / no-license | ❌ | SEAware proprietary; PPB3 no license |

## Structure-Based Generation

See [structure-based-generation.md](structure-based-generation.md).

These tools generate ligands for a pocket or detect pockets. Most generators do
not guarantee a synthesis route, so follow generation with a makeability or
route-planning step. TargetDiff and PocketFlow store MIT terms in misspelled
license filenames.

| Tool | Repository | Code | Method | License signal | Synth? |
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
| **PocketXMol** | `pengxingang/PocketXMol` | MIT | multi-task (SBDD+frag/linker+PROTAC+dock) | ✅ (CC-BY-4.0 weights) | ❌ (2026, Cell) |
| **LDDM** | `LPDI-EPFL/lddm` | MIT | generation + docking + reaction-space mode | ⚠️ checkpoint terms differ | ✅ reaction-space mode |
| **OMTRA** | `gnina/OMTRA` | Apache-2.0 | multi-task flow-matching | ✅ | ❌ (2026, gnina lab) |
| **Saturn** | `schwallergroup/saturn` | Apache-2.0 (detector false-neg) | sample-efficient RL | ✅ | ⚠️ synth-control feature |
| **RxnFlow** | `SeonghwanSeo/RxnFlow` | MIT | synthesis GFlowNet | ✅ | ✅ **synthesizable by construction** |
| **CGFlow** | `tsa87/cgflow` | MIT | synthesis pathway + 3D pose | ✅ | ✅ **synthesizable by construction** |
| **ShEPhERD** | `coleygroup/shepherd` | MIT | shape/ESP/pharmacophore-conditioned gen | ✅ | ❌ |

## Agentic and LLM-Orchestrated Drug Design

See [agentic-drug-design.md](agentic-drug-design.md).

These LLM and multi-agent systems combine generation, docking, ADMET, and
retrosynthesis tools. Most entries depend on external model APIs and remain
early research releases.

| Tool | Repository | Code | Backend | License signal | Status |
|---|---|---|---|---|---|
| **AgentD** | `hoon-ock/AgentD` | MIT | Configurable external model backend | ⚠️ backend terms vary | ✅ Active |
| **CLADD** | `Genentech/CLADD` | Apache-2.0 | Model-agnostic | ⚠️ backend terms vary | ✅ AAAI 2026 (RAG QA) |
| **delta** | `deltawave-tech/delta` | MIT | Configurable external model backend | ⚠️ backend terms vary | ⚠️ Reference architecture |
| **DrugPilot** | `wzn99/DrugPilot` | MIT | Configurable external model backend | ⚠️ backend terms vary | ⚠️ Notebook implementation |
| **Mozi** | — (no public code) | — | Qwen3 and DeepSeek in paper | — | ⚠️ Paper only |

## Chemical Language Models

See [chemical-language-models.md](chemical-language-models.md).

Each entry has an unresolved or additional license layer.

| Tool | Repository | Recorded terms | Base | Status |
|---|---|---|---|---|
| **SynLlama** | `THGLab/SynLlama` | UC **non-commercial** | Llama-3.1/3.2 | Non-commercial repository terms |
| **ChemDFM-R** | (HF only) `OpenDFM/ChemDFM-R-14B` | weights **AGPL-3.0** | Qwen2.5-14B | Check AGPL-3.0 weight terms |
| **Mol-LLaMA** | `DongkiKim95/Mol-LLaMA` | **no stated code license** plus Llama terms | Llama-3.1/2 | No stated code license |
| **ChemMLLM** | `bbsbz/ChemMLLM` | no stated license; **no weights**; Chameleon NC | Chameleon-7B | No released weights |
| *ChemDual, RetroDFM-R* | *(see above)* | separate code, checkpoint, and base terms | LLaMA-3.1 / Qwen3 | — |

## Watchlist

See [watchlist.md](watchlist.md).

Paper-only or code-pending entries include **Reactron, Retro-Expert, ReTriP,
TempRe, RetroTrim**, and **SynthEx**. Repositories without an observed license
include **InterRetro, ConRetroBert, SynCoGen code, SynTwins code, Mol-LLaMA
code, ChemMLLM code, GVT, SmiSelf, CardioTox,** and **PPB3**. TargetDiff and
PocketFlow store MIT terms in misspelled license filenames. The detailed
[watchlist](watchlist.md) records non-commercial releases, hosted services,
proprietary reference tools, and other 2026 additions.

## Lineage Notes

- **Coley-group synthesizable generation:** ChemProjector, SynFormer, and
  PrexSyn share a 115-reaction-template set. ChemProjector is archived, and its
  repository names PrexSyn as the successor.
- **NVIDIA generation:** ReaSyn reuses SynFormer templates. GenMol is a general
  molecular generator under NVIDIA BioNeMo.
- **OpenDFM:** ChemDFM-R covers chemistry reasoning, while RetroDFM-R targets
  retrosynthesis.
- **Schwaller group:** Synthelite, LLM-Syn-Planner, TempRe, and SynthEx cover
  route planning, route evaluation, or synthesis strategy.
- **AstraZeneca tools:** AiZynthFinder performs route search. rxnutils prepares
  reaction data and depends on RDChiral for template operations.
- **MIT learned docking:** EquiBind preceded DiffDock and DiffDock-L. Boltz-1
  and Boltz-2 cover co-folding; Boltz-2 also returns an affinity estimate.
- **AlphaFold3-class co-folding:** Boltz-1/-2 state MIT terms, Chai-1 and
  Protenix state Apache-2.0 terms, and OpenFold3/OpenBind-0 states Apache-2.0
  terms for its released code, parameters, data, and recipes. AlphaFold 3 code
  is Apache-2.0, while its released parameters use separate non-commercial
  terms.
- **NeuralPLexer:** Open NeuralPLexer weights use CC BY-NC-SA terms.
  NeuralPLexer3 is proprietary.
- **AutoDock family:** AutoDock4, AutoDock Vina, smina, and gnina use empirical
  docking scores. QuickVina, Vina-GPU, and AutoDock-GPU provide accelerated
  variants, and Meeko prepares inputs.
- **Open free-energy tools:** OpenMM supplies the simulation engine. Perses and
  OpenFE build alchemical workflows, and alchemlyb analyzes free-energy output.
  Yank remains unmaintained.
- **AlphaFold receptor tools:** AlphaFold2 parameters use CC BY 4.0 terms.
  ColabFold and OpenFold provide alternative execution or training paths.
- **Chemprop and TDC:** Chemprop underlies ADMET-AI, CheMeleon, and OpenADMET.
  TDC provides benchmark datasets whose terms vary by source.
- **Agentic design:** AgentD, CLADD, delta, and Mozi coordinate generation,
  docking, ADMET, and retrosynthesis tools.
