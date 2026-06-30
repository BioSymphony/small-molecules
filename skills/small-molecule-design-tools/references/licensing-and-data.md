# Licensing & Data Terms

The single biggest gotcha across this space: **the code license, the weights license, and the building-block/data license are often three different things.** A permissive code badge does not mean you can use the model or its data commercially. With the LLM-based tools, a fourth layer — the **base-model license** (Llama, Qwen, Chameleon) — stacks on top. This page is the checklist to run before building anything on these tools.

> Not legal advice. Licenses change; verify against the live repo/catalog terms for your actual use case. Facts below verified 2026-06-11.

## The four layers to check, every time

1. **Code license** — the repository source. Read the LICENSE file, not the README badge.
2. **Weights / model license** — often separate from the code, and sometimes more restrictive (copyleft, non-commercial, vendor-specific). **This is the #1 trap for co-folding/docking models** (Chai-1, AF3, NeuralPLexer) just as Enamine is for synthesizability tools.
3. **Data license** — for synthesizable-space tools this traces to **Enamine**; for docking/co-folding it traces to **structural data (PDB / PDBBind)**; for LLMs, to the training corpus.
4. **Base-model license** — for fine-tuned LLMs, the upstream base (Llama/Qwen/Chameleon) carries its own terms that survive into derivatives. (Co-folding models are trained from scratch, so this layer is usually N/A for them.)

## License types you'll encounter here (and what they mean)

- **MIT / Apache-2.0** — permissive; commercial use fine. (AiZynthFinder, PrexSyn, RDChiral, rxnutils, DeepMech, ReactionT5v2, SyntheMol code, …)
- **No LICENSE file = all rights reserved** — public ≠ open. You have *no* granted right to use/modify/redistribute. Surprisingly common here: **SynTwins, SynCoGen (code), InterRetro, ConRetroBert, LARC, Mol-LLaMA (code), ChemMLLM (code), GVT, SmiSelf.**
- **GPL-3.0 / AGPL-3.0 (copyleft)** — using/distributing obligates you to release source under the same license. **AGPL** extends this to *network/SaaS* use (serving the model triggers disclosure). **RetroDFM-R weights = GPL-3.0; ChemDFM-R weights = AGPL-3.0.**
- **CC BY-NC / CC BY-NC-SA / CC BY-NC-ND (non-commercial)** — no commercial use; **-SA** adds share-alike (derivatives under the same license). Unusual on *code*: **APEX code = CC BY-NC 4.0.** Common on **co-folding weights**: **NeuralPLexer weights = CC BY-NC-SA 4.0.** Also several *papers* (SynTwins, RetroScore, SynLlama, Chai-1, Boltz) are CC BY-NC / CC BY — that binds the manuscript, not the code/weights, but signals intent.
- **CC BY 4.0** — permissive, **commercial OK with attribution.** **AlphaFold2/ColabFold/OpenFold parameters = CC BY 4.0**; **Umol weights** too; SyntheMol & SynCoGen weights too.
- **CC0 / public domain** — no restrictions at all. **B3DB (BBB dataset) = CC0**; the PDB itself is effectively public-domain.
- **LGPL (2.1 / 3.0)** — weak copyleft: use/link freely (incl. commercially), but **modifications to the library itself must be shared**. Here: **OpenMM** GPU platforms, **RxDock**, **Meeko**, **GROMACS**, **scikit-mol**.
- **Web-only / academic-service "license"** — many ADMET and target-prediction tools (DeepPK, ADMETlab 3.0, pkCSM, SEA, SwissTargetPrediction, PPB2/3, DoGSiteScorer) ship **no code** — only a free academic web server. You can query them but **cannot embed them** in a commercial pipeline, and querying sends your structures to a third party. Not an open license.
- **BSD 3-Clause *Clear*** — like BSD-3 (permissive, commercial OK) **but explicitly grants NO patent rights** — a real consideration for a patentable method. **NeuralPLexer code** uses it.
- **Gated / request-only model terms** — **AlphaFold3 weights**: access by Google form, **non-commercial only**, no redistribution, outputs can't train competing models. The code is Apache-2.0 but the gated weights block commercial pipelines.
- **Vendor model licenses** — **NVIDIA Open Model License** (ReaSyn weights, GenMol weights): commercially usable *with conditions* (attribution, revocation clauses, no life-critical use). **Meta Chameleon Research License** (ChemMLLM base): **noncommercial research only**, plus an Illinois/Texas user bar.
- **University licenses** — **UC Berkeley Regents non-commercial** (SynLlama): educational/research/not-for-profit only; commercial use needs a signed UC OTL agreement. ⚠️ SynLlama's *paper* says "MIT" — that is wrong; the LICENSE file governs.
- **Meta Llama Community License** (Llama-2/3 bases) — commercial *allowed* with "Built with Llama" attribution, name-prefixing, and a **>700M-MAU** carve-out (very large products need a separate Meta license).

## Per-tool license stack

Grouped by how clean they are for **commercial** use.

### ✅ Cleanest (permissive code + permissive/usable weights)
| Tool | Code | Weights | Data | Notes |
|---|---|---|---|---|
| AiZynthFinder | MIT | MIT (USPTO model) | USPTO, eMolecules/ZINC | **Best.** No Enamine. |
| ASKCOS v2 | MIT | mostly MIT | USPTO/Pistachio/Reaxys/CAS | Use MIT/USPTO models; avoid Reaxys (CC BY-NC) & CAS (member-only). |
| SyntheMol | MIT | CC BY 4.0 | Enamine REAL / WuXi (vendor) | Permissive; catalog sourcing is vendor-governed. |
| DeepMech | MIT | CC-BY-4.0/MIT (Zenodo) | ReactMech | Fully usable. |
| ReactionT5v2 | MIT | MIT (HF) | ORD (CC-BY-SA, data only) | Easy single-step/forward. |
| RXNGraphormer | MIT | Figshare (check) | 13M reactions | Confirm Figshare weights license. |
| GDiffRetro / RetroDiT | MIT | SharePoint / none-yet | USPTO-50K | RetroDiT has no weights yet. |
| MolReactGen | MIT | HF (MIT) | GuacaMol/USPTO | Dormant but clean. |
| RDChiral, rdchiral_plus, SynTemp | MIT | — | — | Template infra. |
| rxnutils | Apache-2.0 | — | — | Curation infra. |
| DeepRetro, Synthelite, LLM-Syn-Planner | MIT | — | — | **But require a paid LLM API** (+ DeepRetro: Pistachio models restricted). |
| Syntheseus, SynPlanner | MIT | wraps/MIT presets | — | Frameworks. |
| **Boltz-2** | MIT | **MIT** (HF) | PDB-derived (MIT-released) | **Rare fully-open flagship** — code+weights MIT, **and** predicts binding affinity. |
| **Boltz-1** | MIT | **MIT** (HF) | PDB-derived (MIT-released) | Fully open AF3-class co-folder (structure only). |
| **Chai-1** | Apache-2.0 | **Apache-2.0** | PDB-derived | Weights **relaxed Nov-2024** from a non-commercial Community License — use the current release; ignore stale "NC" web results. |
| **DiffDock / DiffDock-L** | MIT | MIT | PDBBind (redistribution caveat) | Weights MIT (stated). ESM2 base = MIT. |
| **Uni-Mol Docking v2** | MIT | MIT (Dropbox) | PDBBind-style | Confirm the **Bohrium** hosted-service ToS if using DP's API vs self-host. |
| **Umol** | Apache-2.0 (README) | **CC BY 4.0** (Zenodo) | PDB-derived | Cleanest pure co-folder; attribution required; **no LICENSE file** (README-stated only). |
| **EquiBind, TankBind** | MIT | MIT (in-repo) | PDBBind | Legacy. TankBind also has an affinity head; "latest version" = commercial Galixir (separate terms). |
| AutoDock Vina / QuickVina / Vina-GPU | Apache-2.0 | — (empirical) | — | Classical docking; RTMScore (MIT code+weights) for ML rescoring. |
| AF2 / ColabFold / OpenFold | Apache-2.0 / MIT | **CC BY 4.0** params | PDB/MSA | Receptor structure; commercial OK w/ attribution. |
| ESMFold / ESM-2 | MIT | MIT | UniRef/MGnify | Single-sequence; archived but clean. |
| RoseTTAFold All-Atom | BSD-3 | BSD-3 (code+weights) | PDB | ⚠️ only the pdb100 template DB is CC BY-NC-SA — supply your own. |
| OpenFE / OpenMM / alchemlyb / BAT2 | MIT / BSD | — (physics) | — | Open FEP stack (OpenMM GPU platforms = LGPL). |
| Chemprop / DeepChem / molfeat / Uni-Mol | MIT / Apache | MIT/Apache | your data | QSAR frameworks; quality = your data. |
| MoLFormer-XL | Apache-2.0 | Apache-2.0 | ZINC/PubChem | Embeddings, not generation. |
| ADMET-AI | MIT | MIT (bundled) | TDC-derived | Deployable ADMET (hERG/BBB/CYP). |
| B3DB | CC0 | — (dataset) | — | BBB data, public domain. |
| ChEMBL multitask | MIT | MIT (ONNX) | **ChEMBL CC BY-SA** | Embeddable off-target screen. |
| ESP-Sim / Shape-it / RDKit / OpenPharmacophore | MIT / BSD-3 | — | your mols | Shape/pharmacophore overlay. |
| fpocket / P2Rank | MIT | MIT | — | Pocket detection. |
| DiffSBDD / Pocket2Mol / TargetDiff / PocketFlow / ResGen / Apo2Mol | MIT | MIT | PDBBind | Pocket generators (TargetDiff/PocketFlow = MIT in *misspelled* files). **Outputs not synthesizable.** |
| REINVENT 4 / PILOT (e3moldiffusion) | Apache-2.0 | Apache-2.0 | — | Generative frameworks; REINVENT can add a synthesizability reward. |

### ⚠️ Permissive code, but a restrictive weights/data/base layer
| Tool | Trap |
|---|---|
| PrexSyn | MIT code+weights, but bundled space is **Enamine-derived** — verify Enamine terms. |
| SynFormer | Apache-2.0 code, but data is **"research purposes only, commercial use requires permissions."** |
| ReaSyn | Apache-2.0 code, **weights = NVIDIA Open Model License**; + Enamine. |
| GenMol | Apache-2.0 code, **weights = NVIDIA Open Model License** (commercial OK *with conditions*). |
| RetroDFM-R | Apache-2.0 code, **weights GPL-3.0**, base Llama-3 (extra terms). |
| ChemDual | Apache-2.0 code, **weights unreleased**; base LLaMA-3.1 (Meta terms). |
| ProPreT5 | MIT code, **no weights** (train yourself). |
| NeuralPLexer | **BSD-3-*Clear*** code (permissive but **no patent grant**), **weights CC BY-NC-SA 4.0 (non-commercial)** — code is usable commercially, the released weights are not (retrain for commercial). |
| scikit-mol | **LGPL-3.0** — use/link freely; modifications to scikit-mol itself must be shared (copyleft). |
| QSARtuna | Apache-2.0 declared in `pyproject` but **no LICENSE file** — permissive intent, diligence gap. |
| ChemBERTa | MIT code, but **weights license unstated** on HF — confirm or retrain. |
| gnina | Apache/GPL code, but the **CNN weights (`gnina/models`) have NO LICENSE** (+ CrossDocked provenance) — empirical-only for commercial. |
| AutoDock-GPU / smina | **GPL-2.0** (smina effectively GPL via OpenBabel) — copyleft on redistribution. |
| RxDock / Meeko / GROMACS | **LGPL** — commercial use OK; modifications to the library shared under LGPL. |
| BioSimSpace / gmx_MMPBSA | **GPL-3.0** — internal use fine; distributing a derived product triggers copyleft. |
| Align-it / Lingo3DMol | **GPL-3.0** — copyleft; run Align-it as a standalone CLI to avoid linking. |
| Ersilia CYP (eos44zp) | **GPL-3.0** + archived — or DIY a CYP model on TDC (MIT). |
| BayeshERG | MIT **code**, but trained **weights + data = CC BY-NC-SA** — retrain for commercial. |
| ESM3 / ESM-C | weights term changed recently (NC→MIT, ~2026) — **re-verify the live model card**. |
| DOCK6 | **BSD-3 from GitHub** (clean) vs **academic EULA from the UCSF portal** — provenance decides. |
| SwissADME | web-only; **results are CC-BY 4.0 (usable), but the engine isn't embeddable**; no bulk scraping. |

### ❌ Blocked for commercial use (non-commercial / copyleft-SaaS / no license)
| Tool | Blocker |
|---|---|
| SynLlama | **UC Berkeley non-commercial** (paper's "MIT" is wrong). |
| ChemDFM-R | **AGPL-3.0 weights** (network copyleft). |
| APEX | **CC BY-NC 4.0 code.** |
| ChemMLLM | **No code license; no weights; Chameleon noncommercial base** (+ IL/TX bar). |
| Mol-LLaMA | **No code license** (+ Llama base). |
| SynTwins, SynCoGen (code), InterRetro, ConRetroBert, LARC, GVT, SmiSelf | **No LICENSE file = all rights reserved.** (SynCoGen's HF weights/dataset *are* MIT — the artifacts are usable, the code isn't.) |
| ChemProjector | MIT but **archived/deprecated**; Enamine-gated. |
| AlphaFold3 | Apache-2.0 *code*, but **weights are request-gated + non-commercial** (no redistribution; outputs can't train competing models) → whole pipeline blocked for commercial use. Use Boltz/Chai instead. |
| NeuralPLexer (weights) | **CC BY-NC-SA 4.0** weights (code is permissive BSD-3-Clear — see ⚠️ above). |
| NeuralPLexer3, Chai-2/Chai-3 | **Proprietary — no open code/weights** (Iambic; Chai Discovery). Not licensable as software. |
| RoseTTAFold (original) | **Non-commercial weights** (Rosetta-DL); RFAA relaxed to BSD but the original did not. |
| DecompDiff | **CC-BY-NC 4.0** (non-commercial) + archived. |
| CardioTox | **No LICENSE = all rights reserved** (hERG model). |
| DeepPK / ADMETlab 3.0 / pkCSM | **Web-only** — non-commercial (DeepPK/ADMETlab) or paid-license (pkCSM); not embeddable. |
| SEA / SEAware | No open code; **SEAware is proprietary** (commercial license). |
| PPB3 / SPiDER / TIGER | PPB3 = public repo but **NO LICENSE**; SPiDER/TIGER = **no open code**. |
| DoGSiteScorer / PLANTS | DoGSiteScorer = **academic-only web service**; PLANTS = **closed academic binary** — neither embeddable. |

## The Enamine dependency

Every synthesizable-generation tool is built on **Enamine building blocks** (+ a shared ~115-reaction-template set). The catalog (US Stock / Global Stock / REAL Space) is **free to request** but carries Enamine's **own usage terms** distinguishing research from commercial use. No repo restates those terms — you are responsible for licensing the catalog appropriately.

- **Request from Enamine** (not redistributed): SynFormer, ReaSyn, ChemProjector.
- **Bundled in-repo** (redistribution of Enamine-derived structures): PrexSyn (precomputed space), SynTwins (150,560 Global Stock blocks), SynCoGen (93 blocks via RGFN — small), SynLlama (~230K blocks, train).
- **Make-on-demand vendor space:** SyntheMol & APEX design over Enamine **REAL** (and WuXi GalaXi) — sourcing/synthesis is governed by the vendor, separate from the tool's license.
- Even with MIT/Apache code, the **outputs** are drawn from Enamine's space. For commercial work, confirm with Enamine that your use of their building-block data is covered.

## The structural-data layer (docking / co-folding)

The docking/co-folding tools don't touch Enamine — their data layer is **protein-ligand structural data**, almost always **PDB-derived** (the PDB itself is public-domain / CC0).

- **PDBBind** (the standard training/benchmark set for docking — DiffDock, Uni-Mol Docking v2, EquiBind, TankBind) carries its own **redistribution terms** that lean academic. The trained *model* is governed by its own weights license (above); the caveat only bites if you **redistribute the PDBBind dataset itself**, not if you run the model.
- **Co-folding training data** (Boltz, Chai) is PDB/MSA-derived; Boltz explicitly MIT-releases its datasets/benchmarks. Boltz-2 used Recursion's proprietary affinity data for training but the **release** is MIT with no rider found.
- **MSA generation:** Chai-1, Boltz, Umol default to **public ColabFold / MMseqs2 servers** for MSAs. For a closed commercial pipeline, **self-host MSA generation** rather than sending sequences to a public server (data-egress concern, not a license one).
- The weights-vs-code split is the real trap here, not the data: see Chai-1 (weights relaxed Nov-2024), NeuralPLexer (NC weights), AlphaFold3 (gated NC weights).

## The bioactivity-data layer (QSAR / ADMET / target prediction)

The ligand-based predictors don't depend on Enamine or PDB — their data layer is **bioactivity databases**, and two issues recur:

- **ChEMBL = CC BY-SA 3.0 (attribution + share-alike).** Most QSAR/target models train on ChEMBL (Chemprop on your extract, the ChEMBL multitask model, ADMET-AI via TDC). The MIT/Apache code does not launder this: if you **redistribute derived datasets**, attribution + share-alike apply. Running a model you trained is generally fine; redistributing the data/derivatives is the trigger.
- **TDC datasets are per-dataset licensed** — some non-commercial; vet each before commercial training (see [property-and-qsar-prediction.md](property-and-qsar-prediction.md)).
- **Web-only tools you can't embed:** the most-used ADMET (DeepPK, ADMETlab 3.0, pkCSM) and target-prediction (SEA, SwissTargetPrediction, PPB2/3) tools are free **academic web servers** — you may query them, but their terms forbid embedding in a commercial pipeline, and you'd be sending proprietary structures to a third-party host (IP/egress risk). Deployable-local exceptions: **ADMET-AI** (MIT), the **ChEMBL multitask model** (MIT), **B3DB** (CC0 data).

## Decision shortcuts

- **Need clean commercial licensing today?**
  - Retrosynthesis: **AiZynthFinder** (MIT + USPTO); **ASKCOS v2** with MIT/USPTO models; **Syntheseus/SynPlanner** frameworks.
  - Single-step / forward: **ReactionT5v2**, **RXNGraphormer**, **DeepMech** (all MIT, weights released).
  - Make-on-demand generation: **SyntheMol** (MIT + CC BY) — clear the Enamine REAL catalog with the vendor.
  - Synthesizable projection: **PrexSyn** (MIT code+weights) — lightest-friction learned generator, still inherits Enamine data terms.
  - Templates/curation: **RDChiral / rdchiral_plus / rxnutils / SynTemp** (all permissive).
  - Docking / co-folding (structure): **Boltz-1** (MIT/MIT), **Chai-1** (Apache/Apache, post-Nov-24 release), **Umol** (Apache/CC BY 4.0), **DiffDock-L** & **Uni-Mol Docking v2** (MIT/MIT). **Avoid AlphaFold3** (gated NC weights) and **NeuralPLexer weights** (CC BY-NC-SA) for commercial use.
  - Binding **affinity** (not just a pose): **Boltz-2** (MIT/MIT — the only fully-open affinity predictor); TankBind has an affinity head but is legacy MIT.
  - Receptor **structure**: **ColabFold / AF2 / OpenFold** (CC BY 4.0 params), **ESMFold** (MIT), **RoseTTAFold All-Atom** (BSD; swap the NC pdb100 templates). **Avoid AlphaFold3 weights** (gated NC) and **RoseTTAFold-original weights** (NC).
  - Binding **free energy** (physics): **OpenFE / OpenMM / alchemlyb / BAT2** (MIT/BSD); GPL tools (BioSimSpace, gmx_MMPBSA) are usable but copyleft on redistribution.
  - **QSAR / property**: **Chemprop, DeepChem, molfeat, MoLFormer-XL, Uni-Mol** (permissive) — clear the **ChEMBL (CC BY-SA)** data terms on what you train/redistribute.
  - **ADMET**: **ADMET-AI** (MIT, deployable) + **B3DB** (CC0). Web tools (DeepPK/ADMETlab/pkCSM) aren't embeddable.
  - **Off-target / selectivity**: **ChEMBL multitask model** (MIT) + **ESP-Sim / Shape-it / RDKit** (MIT/BSD). **Align-it** is GPL-3.
  - **Structure-based generation**: **REINVENT 4 / PILOT** (Apache), **DiffSBDD** (MIT). **Avoid DecompDiff** (CC-BY-NC); **Lingo3DMol** is GPL-3. Outputs aren't makeable → project with PrexSyn.
- **Doing research / non-commercial?** Almost everything is fair game; pick by capability. The "no license" set still technically needs author contact. For docking/co-folding, **AlphaFold3** (best accuracy) and **NeuralPLexer** weights are fine for non-commercial research.
- **Building a commercial product on generative design?** Expect to (a) clear **Enamine** terms, (b) check the **weights** license separately (NVIDIA for ReaSyn/GenMol, GPL for RetroDFM-R, AGPL for ChemDFM-R), and (c) for LLM fine-tunes, satisfy the **base-model** license (Llama/Qwen/Chameleon).
- **Using an LLM/agentic planner?** The code may be MIT, but you'll **pay for a commercial LLM API** (Anthropic/OpenAI/Gemini) and send structures to it — factor in cost and data egress.

## "Verify before commercial use" — minimal checklist

- [ ] Code license read from the **LICENSE file** (not the README badge or the paper's claim — see SynLlama).
- [ ] Weights/model license checked **separately** from the code.
- [ ] No **non-commercial** (CC BY-NC*) or **copyleft** (GPL/AGPL) artifact in your dependency path unless you accept its terms (AGPL = disclose your SaaS source).
- [ ] If Enamine building blocks are involved, your Enamine catalog license covers commercial use.
- [ ] For fine-tuned LLMs, the **base-model** license (Llama/Qwen/Chameleon) is satisfied, including Llama's >700M-MAU clause.
- [ ] For LLM/agentic tools, the **commercial API** terms (Anthropic/OpenAI/Gemini) and data-egress are acceptable.
- [ ] No "all rights reserved" (no-license) repo in your shipped path without written author permission.
- [ ] For QSAR / target / ADMET models, the **training-data license** (ChEMBL CC BY-SA; TDC per-dataset) is satisfied for your use (especially redistribution).
- [ ] No **web-only academic tool** (DeepPK, ADMETlab, pkCSM, SEA, SwissTargetPrediction) embedded in a commercial pipeline — and no proprietary structures sent to a third-party server.
- [ ] For receptor structure, the **parameters** license is clear (AF2/ColabFold/OpenFold = CC BY 4.0 OK; AF3 = gated NC; RoseTTAFold-orig = NC; ESM3/ESM-C = re-verify).
- [ ] For docking, the **scoring weights** are clear (gnina's CNN weights are unlicensed → use empirical Vina scoring for commercial).
