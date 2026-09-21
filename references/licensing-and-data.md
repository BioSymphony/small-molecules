# Licensing and Data Terms

A tool can apply different terms to its code, model weights, training data, and
base model. Check each layer before you select or distribute the tool.

> This guide supports preliminary diligence; it is not legal advice. Check the
> primary terms that apply to your release and use case. The general license
> descriptions were reviewed on 2026-08-30; tool claims keep their source-check
> dates in the category references.

## Check four layers

1. **Code:** Read the repository's license file and notices.
2. **Model weights:** Read the model card, artifact license, and download terms.
3. **Data:** Check the terms for catalogs, structures, assays, and training sets.
4. **Base model:** For a fine-tuned model, check the original model's terms and
   the derivative's terms.

## Common license labels

- **MIT and Apache-2.0:** These licenses grant broad permissions subject to
  their stated conditions. Read the [MIT License](https://opensource.org/license/mit)
  or [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) before
  distribution.
- **No license file or grant:** GitHub explains that default copyright applies
  when a repository has no license. Contact the rights holder before reuse that
  requires permission. Examples in this guide include SynTwins, SynCoGen code,
  InterRetro, ConRetroBert, LARC, Mol-LLaMA code, ChemMLLM code, GVT, and
  SmiSelf. See [GitHub's repository licensing guide](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).
- **GPL and AGPL:** These copyleft licenses set conditions for covered copying,
  modification, and distribution. AGPLv3 also addresses a modified program that
  users interact with over a network. Read the applicable [GNU license
  text](https://www.gnu.org/licenses/).
- **CC BY-NC variants:** The NonCommercial condition restricts use that is
  primarily intended for commercial advantage or monetary compensation.
  ShareAlike adds conditions for adapted material. Check the exact
  [Creative Commons license](https://creativecommons.org/share-your-work/cclicenses/).
- **CC BY 4.0:** The license permits sharing and adaptation for any purpose,
  subject to attribution and its other conditions. See the [CC BY 4.0
  deed](https://creativecommons.org/licenses/by/4.0/).
- **CC0 1.0:** CC0 waives covered rights to the extent allowed by law and adds a
  fallback license. The PDB archive applies CC0 to its data files. See the
  [CC0 legal code](https://creativecommons.org/publicdomain/zero/1.0/legalcode)
  and [wwPDB usage policy](https://www.wwpdb.org/about/usage-policies).
- **LGPL:** LGPL terms distinguish the licensed library, modifications, and a
  larger work that uses the library. Check the applicable version before you
  distribute software that includes an LGPL component.
- **Web-only service:** A public website does not grant a software license.
  Check the service terms, automation policy, and data-handling policy before
  you submit structures or integrate the service.
- **BSD 3-Clause Clear:** This license states that it grants no express or
  implied patent license. NeuralPLexer uses this license for its code.
- **Gated, vendor, university, and base-model terms:** Read the terms attached
  to the exact artifact and version. Repository code terms do not replace model
  download terms or a base-model license.

## Per-tool license stack

The groups provide preliminary routing signals. They do not say whether a
license permits a specific use.

### ✅ Artifacts labeled MIT, Apache-2.0, BSD, or CC BY
| Tool | Code | Weights | Data | Notes |
|---|---|---|---|---|
| AiZynthFinder | MIT | MIT (USPTO model) | USPTO, eMolecules/ZINC | No Enamine layer listed. |
| ASKCOS v2 | MIT | mostly MIT | USPTO/Pistachio/Reaxys/CAS | Reaxys data states CC BY-NC terms; CAS access is member-only. |
| DeepMech | MIT | CC-BY-4.0/MIT (Zenodo) | ReactMech | Check the ReactMech data terms. |
| ReactionT5v2 | MIT | MIT (HF) | ORD (CC-BY-SA, data only) | Supports single-step and forward prediction. |
| RXNGraphormer | MIT | Figshare (check) | 13M reactions | Confirm Figshare weights license. |
| GDiffRetro / RetroDiT | MIT | SharePoint / none-yet | USPTO-50K | RetroDiT has no weights yet. |
| MolReactGen | MIT | HF (MIT) | GuacaMol/USPTO | Repository activity is limited. |
| RDChiral, rdchiral_plus, SynTemp | MIT | — | — | Template infra. |
| rxnutils | Apache-2.0 | — | — | Curation infra. |
| DeepRetro, Synthelite, LLM-Syn-Planner | MIT | — | — | Selected model-provider terms apply; DeepRetro also offers Pistachio-based models. |
| RENKIN | MIT | — | user-supplied templates and stock | Route planner and route validator. |
| Syntheseus | MIT | wraps external models | benchmark datasets | Model and dataset terms vary. |
| [RetroChimera](singlestep-retrosynthesis.md#retrochimera) | MIT | MIT-labeled Figshare checkpoints | Pistachio / USPTO | Three retro checkpoint records checked on 2026-09-21; data terms are separate. |
| [ForwardChimeraDeNovo](forward-and-reaction-modeling.md#also-do-forward-prediction-documented-in-single-step-file) | MIT | MIT-labeled Figshare checkpoint | Pistachio | Forward checkpoint record checked on 2026-09-21; data terms are separate. |
| **Boltz-2** | MIT | **MIT** (HF) | PDB-derived (MIT-released) | Predicts structure and binding affinity. |
| **Boltz-1** | MIT | **MIT** (HF) | PDB-derived (MIT-released) | Predicts structure. |
| **Chai-1** | Apache-2.0 | **Apache-2.0** | PDB-derived | Chai changed the weights from its Community License to Apache-2.0 in November 2024. |
| **DiffDock / DiffDock-L** | MIT | MIT | PDBBind (redistribution caveat) | Weights MIT (stated). ESM2 base = MIT. |
| **Uni-Mol Docking v2** | MIT | MIT (Dropbox) | PDBBind-style | Bohrium hosted-service terms apply to its API separately. |
| **Umol** | Apache-2.0 (README) | **CC BY 4.0** (Zenodo) | PDB-derived | The repository has no license file; the README states Apache-2.0. |
| **EquiBind, TankBind** | MIT | MIT (in-repository) | PDBBind | Legacy. TankBind also has an affinity head; the commercial Galixir offering uses its own terms. |
| AutoDock Vina / QuickVina / Vina-GPU | Apache-2.0 | — (empirical) | — | Classical docking; RTMScore (MIT code+weights) for ML rescoring. |
| AF2 / ColabFold / OpenFold | Apache-2.0 / MIT | **CC BY 4.0** params | PDB/MSA | CC BY 4.0 attribution conditions apply to the parameters. |
| ESMFold / ESM-2 | MIT | MIT | UniRef/MGnify | Single-sequence; repository archived. |
| RoseTTAFold All-Atom | BSD-3 | BSD-3 (code+weights) | PDB | The optional pdb100 template database states CC BY-NC-SA terms. |
| OpenFE / OpenMM / alchemlyb / BAT2 | MIT / BSD | — (physics) | — | Open FEP stack (OpenMM GPU platforms = LGPL). |
| Chemprop / DeepChem / molfeat / Uni-Mol | MIT / Apache | MIT/Apache | your data | QSAR frameworks; model quality depends on the training data and validation design. |
| MoLFormer-XL | Apache-2.0 | Apache-2.0 | ZINC/PubChem | Embeddings, not generation. |
| ADMET-AI | MIT | MIT (bundled) | TDC-derived | Local ADMET package (hERG/BBB/CYP). |
| B3DB | CC0 | — (dataset) | — | BBB dataset under CC0. |
| ChEMBL multitask | MIT | MIT (ONNX) | **ChEMBL CC BY-SA** | ONNX off-target model. |
| ESP-Sim / Shape-it / RDKit / OpenPharmacophore | MIT / BSD-3 | — | your mols | Shape/pharmacophore overlay. |
| fpocket / P2Rank | MIT | MIT | — | Pocket detection. |
| DiffSBDD / Pocket2Mol / TargetDiff / PocketFlow / ResGen / Apo2Mol | MIT | MIT | PDBBind | Pocket generators; TargetDiff and PocketFlow use misspelled license filenames. These tools do not provide synthesis routes. |
| REINVENT 4 / PILOT (e3moldiffusion) | Apache-2.0 | Apache-2.0 | — | Generative frameworks; REINVENT can add a synthesizability reward. |

### ⚠️ Additional or unverified weights, data, or base-model terms
| Tool | Additional term |
|---|---|
| PrexSyn | MIT-labeled repository and data/model records; Enamine-derived data. |
| LDDM | MIT code and `lddm_CDBB.ckpt`; the paper checkpoint, `lddm.ckpt`, is CC BY-NC 4.0. Enamine REAL assets require separate permission. |
| SynFormer | Apache-2.0 code, but data is **"research purposes only, commercial use requires permissions."** |
| ReaSyn | Apache-2.0 code, **weights = NVIDIA Open Model License**; + Enamine. |
| GenMol | Apache-2.0 code; the **NVIDIA Open Model License** applies to the weights. Review its conditions. |
| SyntheMol | MIT code; the reviewed Zenodo data/model record does not state a license; vendor-derived data. |
| APEX | The reviewed repository and Zenodo records do not state license terms. |
| SynPlanner | MIT code; separate model/data record. |
| RetroDFM-R | MIT code; Apache-2.0-tagged checkpoint; Qwen3 base and separate inference data. |
| RetroAgent | MIT code; Apache-2.0-tagged checkpoint; Qwen3 base and separate search assets. |
| ChemDual | Apache-2.0 code, **weights unreleased**; base LLaMA-3.1 (Meta terms). |
| ProPreT5 | MIT code; no released weights. |
| NeuralPLexer | **BSD-3-Clause-Clear** code; **CC BY-NC-SA 4.0** weights. The code license states that it grants no patent license. |
| scikit-mol | **LGPL-3.0**. Review the license before distributing the library, a modified version, or a larger work that includes it. |
| QSARtuna | `pyproject` declares Apache-2.0; the reviewed repository has no license file. |
| ChemBERTa | MIT code; the reviewed Hugging Face weights do not state a license. |
| gnina | Apache/GPL code; the reviewed CNN-weights repository has no license file. |
| AutoDock-GPU / smina | **GPL-2.0** code. |
| RxDock / Meeko / GROMACS | **LGPL**. Check the version-specific distribution conditions. |
| BioSimSpace / gmx_MMPBSA | **GPL-3.0**. Check the GPL conditions before distributing covered code or modifications. |
| Align-it / Lingo3DMol | **GPL-3.0** code. |
| Ersilia CYP (eos44zp) | **GPL-3.0** code; archived repository. |
| BayeshERG | MIT code; **CC BY-NC-SA** weights and data. |
| ESM3 / ESM-C | The reviewed weight terms changed from non-commercial to MIT in 2026. Check the exact model card and version. |
| DOCK6 | The GitHub source states BSD-3; the UCSF download portal uses an academic EULA. |
| SwissADME | Hosted service; results state CC BY 4.0 terms. The service prohibits bulk access. |

### ❌ Non-commercial, no-license, or no-open-release status
| Tool | Reviewed status |
|---|---|
| SynLlama | The repository license states UC Berkeley non-commercial terms; the paper states MIT. Use the repository's primary license file for diligence. |
| ChemDFM-R | **AGPL-3.0 weights**. |
| ChemMLLM | No code license or released weights; the Chameleon base has separate research terms. |
| Mol-LLaMA | **No code license** (+ Llama base). |
| SynTwins, SynCoGen (code), InterRetro, ConRetroBert, LARC, GVT, SmiSelf | No license file. SynCoGen's Hugging Face weights and dataset state MIT terms separately. |
| ChemProjector | MIT but **archived/deprecated**; Enamine-gated. |
| AlphaFold3 | Apache-2.0 code; the reviewed weights terms are request-gated and non-commercial. |
| NeuralPLexer (weights) | **CC BY-NC-SA 4.0** weights; BSD-3-Clause-Clear code. |
| NeuralPLexer3, Chai-2/Chai-3 | No public code or weights release was available for review. |
| RoseTTAFold (original) | The original weights state non-commercial terms; RoseTTAFold All-Atom code and weights state BSD-3-Clause terms. |
| DecompDiff | **CC-BY-NC 4.0** (non-commercial) + archived. |
| CardioTox | The reviewed repository has no license file. |
| DeepPK / ADMETlab 3.0 / pkCSM | Hosted services; DeepPK and ADMETlab state non-commercial terms, and pkCSM offers separate paid terms. |
| SEA / SEAware | No open code; **SEAware is proprietary** (commercial license). |
| PPB3 / SPiDER / TIGER | PPB3 has a public repository with no stated license. SPiDER and TIGER have no public code. |
| DoGSiteScorer / PLANTS | DoGSiteScorer is an academic-use service; PLANTS is an academic-use binary. |

## The Enamine dependency

Several tools in the synthesizable-generation table use **Enamine building
blocks** and related reaction templates. Enamine sets separate terms for its
catalogs. Check the terms for the specific catalog and access method that your
workflow uses.

- **Request from Enamine** (not redistributed): SynFormer, ReaSyn, ChemProjector.
- **Bundled in-repository** (redistribution of Enamine-derived structures): PrexSyn (precomputed space), SynTwins (150,560 Global Stock blocks), SynCoGen (93 blocks via RGFN — small), SynLlama (~230K blocks, train).
- **Make-on-demand vendor space:** SyntheMol and APEX design over Enamine REAL
  and WuXi GalaXi. Vendor terms apply separately from the tool's license.
- **LDDM:** The public example uses a small SynSpace-derived reaction space.
  The paper's Enamine REAL workflow requires separately licensed reactions and
  building blocks that are not redistributed upstream.
- For product-facing work, confirm that the applicable catalog terms cover your
  use of the building-block data and resulting candidate space.

## The Structural-Data Layer for Docking and Co-Folding

Docking and co-folding tools usually rely on protein-ligand structural data.
The [wwPDB usage policy](https://www.wwpdb.org/about/usage-policies) applies
CC0 1.0 to PDB archive data files and asks users to attribute the original
structure authors where possible.

- **PDBbind:** DiffDock, Uni-Mol Docking v2, EquiBind, and TankBind use PDBbind
  data. Check the PDBbind download and redistribution terms separately from the
  model-weights license.
- **Co-folding training data:** Boltz and Chai use PDB- and MSA-derived data.
  The Boltz repository states MIT terms for its released datasets and
  benchmarks. The Boltz-2 paper describes additional Recursion affinity data
  used during training.
- **MSA generation:** Chai-1, Boltz, and Umol can use public ColabFold or
  MMseqs2 servers. Check the service's data policy before submitting a non-public
  sequence.
- **Weights:** Chai-1 states Apache-2.0 terms, NeuralPLexer states CC BY-NC-SA
  terms, and AlphaFold3 states gated non-commercial terms for the reviewed
  weights.

## The Bioactivity-Data Layer for QSAR, ADMET, and Target Prediction

Ligand-based predictors commonly use bioactivity databases. Check the database
terms separately from the training code and weights.

- **ChEMBL:** The ChEMBL download from 2026-08-30 includes a
  [CC BY-SA 3.0 license](https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/LICENSE).
  Review its attribution and ShareAlike conditions before you distribute ChEMBL
  data or adaptations.
- **TDC datasets are per-dataset licensed**; some state non-commercial terms. See [property-and-qsar-prediction.md](property-and-qsar-prediction.md).
- **Web-only tools:** DeepPK, ADMETlab 3.0, pkCSM, SEA,
  SwissTargetPrediction, and PPB2/3 require service-specific review. Before you
  submit a structure, check the service terms and data-handling policy. Local
  alternatives in this guide include ADMET-AI, the ChEMBL multitask model, and
  B3DB.

## Selected artifact labels by task

| Task | Reviewed artifact labels | Separate terms recorded in this guide |
|---|---|---|
| Retrosynthesis | AiZynthFinder, RENKIN, Syntheseus, and SynPlanner: MIT code | ASKCOS, Syntheseus, and SynPlanner model/data terms vary |
| Single-step and forward prediction | ReactionT5v2, RXNGraphormer, and DeepMech: MIT code | Dataset and weights terms remain separate |
| Make-on-demand generation | SyntheMol: MIT code | Reviewed Zenodo record does not state a license; Enamine REAL and WuXi GalaXi vendor terms |
| Synthesizable projection | PrexSyn: MIT code and weights | Enamine-derived candidate space |
| Template tools | RDChiral, rdchiral_plus, and SynTemp: MIT; rxnutils: Apache-2.0 | Input reaction-data terms |
| Docking and co-folding | Boltz-1: MIT; Chai-1 and OpenBind-0: Apache-2.0; DiffDock-L and Uni-Mol Docking v2: MIT | Umol repository lacks a license file; its README states Apache-2.0 |
| Binding affinity | Boltz-2: MIT code and weights | Training-data provenance described in the tool card |
| Receptor structure | AlphaFold2 and OpenFold code: Apache-2.0; ColabFold code: MIT; reviewed parameters: CC BY 4.0 | AlphaFold3 and original RoseTTAFold weights state non-commercial terms |
| Free-energy methods | OpenFE: MIT; OpenMM: MIT/LGPL; alchemlyb: BSD-3; BAT2: MIT | BioSimSpace and gmx_MMPBSA: GPL-3.0 |
| QSAR and property prediction | Chemprop and DeepChem: MIT; molfeat and MoLFormer-XL: Apache-2.0; Uni-Mol: MIT | ChEMBL: CC BY-SA 3.0; TDC terms vary by dataset |
| ADMET | ADMET-AI: MIT; B3DB: CC0 | Hosted-service terms for DeepPK, ADMETlab, and pkCSM |
| Off-target and selectivity | ChEMBL multitask model and ESP-Sim: MIT; RDKit: BSD-3 | ChEMBL data: CC BY-SA 3.0; Align-it: GPL-3.0 |
| Structure-based generation | REINVENT 4 and PILOT: Apache-2.0; DiffSBDD and LDDM code: MIT | LDDM paper checkpoint and DecompDiff: CC BY-NC; Lingo3DMol: GPL-3.0 |
| LLM and agentic planning | RetroAgent: MIT code and Apache-2.0-tagged checkpoint; project code terms vary by tool | Provider, base-model, training-data, retention, and data-handling terms |

## Terms review checklist

- [ ] Record the code license, primary source URL, and verification date.
- [ ] Record the model-weights terms and download conditions separately.
- [ ] Record each training, benchmark, catalog, and structure dataset license.
- [ ] Record the exact base model and version for each fine-tuned model.
- [ ] Record any non-commercial, copyleft, gated-access, or field-of-use terms.
- [ ] Record any permission grant that covers planned reuse when a repository
      has no license.
- [ ] Review hosted-service terms, retention, and data-handling policies before
      submitting non-public data.
- [ ] Record attribution, notice, source-offer, and redistribution requirements
      that apply to the planned release.
