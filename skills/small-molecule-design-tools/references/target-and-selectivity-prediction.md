# Target, Off-Target & Selectivity Prediction

*"Will it bind — and what else will it hit?"* QSAR ([property-and-qsar-prediction.md](property-and-qsar-prediction.md)) tells you affinity at *your* target; this layer tells you the **off-target / selectivity** profile. The motivating case for a serotonin-receptor program: flagging that a tryptamine lead also lights up **5-HT2B** (agonism → cardiac valvulopathy — the fen-phen / pergolide lesson), or hERG, or MAO, *before* you synthesize it.

Two complementary strategies:

1. **Target / off-target prediction** — chemical-similarity statistics + ML over ChEMBL: given a structure, rank likely protein targets. (SEA, SwissTargetPrediction, PPB2/PPB3, ChEMBL multitask model.)
2. **Ligand-based 3D shape & pharmacophore overlay** — align a query to a *known anti-target ligand* and score steric/electrostatic/pharmacophoric overlap. High overlap with a known 5-HT2B agonist is a direct, interpretable liability signal that 2D fingerprints can miss. (ESP-Sim, Shape-it, Align-it, RDKit, OpenPharmacophore.)

**Licensing reality:** the *prediction* tools skew **web-only or no-license** (SEA, SwissTargetPrediction, PPB2/PPB3, SPiDER/TIGER). The genuinely commercial-safe assets are the **ChEMBL multitask model (MIT)**, **ESP-Sim (MIT)**, **Shape-it (MIT)**, and the **RDKit baseline (BSD-3)**; **Align-it is GPL-3.0** (copyleft). For every data-driven predictor the **data license** (ChEMBL = CC BY-SA 3.0) is a separate, real obligation. Verified **2026-06-13**.

---

## Target / off-target prediction

### SEA — Similarity Ensemble Approach — **WEB + COMMERCIAL**
- **What/method:** Predicts targets by **set-wise chemical similarity** of the query against each target's known-ligand set, with a BLAST-analogous E-value. The classic off-target tool (Shoichet lab).
- **Code:** ❌ **No canonical open Shoichet/BKSLab repo.** Web tool: `sea.bkslab.org`. Commercial engine **SEAware** is proprietary (SeaChange Pharmaceuticals). Only tangential community code: `momeara/DeepSEA` (**NO LICENSE**, 2016) and `momeara/SEAR` (R wrapper, NOASSERTION) — neither is the production tool. *(The GitHub org literally named "BKSLab" is unrelated.)*
- **Paper:** Keiser et al., *Nat. Biotechnol.* 2007 (DOI 10.1038/nbt1284); off-target application Lounkine et al., *Nature* 2012 (DOI 10.1038/nature11159).
- **Commercial:** ❌ No open license; SEAware needs a commercial license. Web usable but not embeddable.

### SwissTargetPrediction — **WEB-ONLY** (`swisstargetprediction.ch`)
- **What/method:** Most-probable targets via combined **2D + 3D similarity** to curated actives; per-target probability. SIB / Univ. Lausanne.
- **License/data:** No code. ChEMBL-derived library; outputs are **CC-BY 4.0**; terms permit "internal research, whether on a commercial or non-commercial basis."
- **Paper:** Daina, Michielin, Zoete, *NAR* 47(W1):W357, 2019. DOI 10.1093/nar/gkz382.
- **Commercial:** ⚠️ Free to *query* (incl. commercial internal research), outputs CC-BY 4.0 — but **no code to deploy/embed.**

### PPB2 — Polypharmacology Browser 2 — **WEB-ONLY** (`ppb2.gdb.tools`)
- **What/method:** Target/polypharmacology prediction over ChEMBL — nearest-neighbor (MQN/Xfp/ECfp4) + Naïve Bayes + DNN. Reymond group, Bern. *(No `reymond-group/PPB2` repo exists — web only.)*
- **Paper:** Awale & Reymond, *JCIM* 59(1):10, 2019. DOI 10.1021/acs.jcim.8b00524.
- **Commercial:** ⚠️ Free web query; no license/code to deploy. Superseded by PPB3.

### PPB3 — Polypharmacology Browser 3 — `reymond-group/PPB3` (web `ppb3.gdb.tools`)
- **What/method:** Deep-learning target prediction; SMILES → top-20 ranked targets; 7 DNNs over distinct fingerprints. Trained on **ChEMBL v34** (7,546 targets).
- **Code license:** ❌ **NO LICENSE** (public repo with training script + Flask app, but all rights reserved by default).
- **Paper:** Reymond group, 2024–25 (cite repo + PPB2 paper).
- **Commercial:** ❌ Code present but **no license** → not legally reusable without author contact. Web free to query.

### ChEMBL Multitask Target-Prediction Model — `chembl/chembl_multitask_model` ⭐
- **What/method:** Multitask **neural network** predicting active/inactive across thousands of ChEMBL targets from one molecule — built for off-target screening over large collections. Exported to **ONNX** (Python/C++/Julia/JS). Morgan/ECFP input.
- **Code license:** ✅ **MIT.**
- **Data:** trained on **ChEMBL** (CC BY-SA 3.0 — attribute + share-alike on redistributed derived data). Targets need ≥100 active + ≥100 inactive compounds.
- **Paper:** EMBL-EBI ChEMBL group (model card `chembl.github.io/chembl_multitask_model`; cf. Bosc et al., *J. Cheminform.* 2019, DOI 10.1186/s13321-018-0325-4).
- **Install / GPU:** `pip install onnxruntime rdkit numpy`; **CPU**-fine. Active (tracks ChEMBL releases).
- **Commercial:** ✅ **The open, embeddable anti-target screen.** Code MIT; mind the ChEMBL CC BY-SA data obligation if you redistribute derived datasets.

### SPiDER / TIGER (Schneider lab) — **NO OPEN CODE**
- **What/method:** Target prediction via consensus **self-organizing maps** over pharmacophore (CATS) + physchem descriptors; built to de-orphan de-novo molecules and probe off-targets. Was ETH-webserver-only (now defunct).
- **Paper:** Reker et al., *PNAS* 111(11):4067, 2014. DOI 10.1073/pnas.1320001111.
- **Commercial:** ❌ No usable code — methodological reference only.

---

## Ligand-based shape & pharmacophore screening

### ESP-Sim — `hesther/espsim`
- **What/method:** Scores **3D shape + electrostatic-potential similarity** (Tanimoto/Carbo over Coulomb-overlap integrals); embeds, aligns (core-constrained or free), scores. Directly answers "does my molecule overlay the known 5-HT2B agonist's shape **and** charge?"
- **Code license:** ✅ **MIT.**
- **Paper:** Bolcato, Heid, Boström, *JCIM* 62(6):1388, 2022. DOI 10.1021/acs.jcim.1c01535.
- **Install / GPU:** conda + `pip install -e .` (RDKit/NumPy/SciPy/sklearn; optional PyTorch/Psi4 charges). **CPU** sufficient.
- **Status:** Active (2025).
- **Commercial:** ✅ MIT. (Default RDKit/ML charge path avoids the LGPL Psi4 option.)

### Shape-it — `silicos-it/shape-it`
- **What/method:** **Gaussian-volume shape-only overlay** + Tanimoto shape scoring (Grant–Pickup) — the open analogue to ROCS shape mode.
- **Code license:** ✅ **MIT** on the modern `silicos-it/shape-it`. ⚠️ The original 2008 Silicos *Pharao* (`silicos-it/pharao`) is **LGPL-3.0** — use the MIT `shape-it` repo to stay permissive.
- **Paper:** Grant et al., *JCC* 1996; tool lineage Taminau et al., *JMGM* 27(2):161, 2008 (DOI 10.1016/j.jmgm.2008.04.003).
- **Install / GPU:** C++/CMake (OpenBabel3 + optional RDKit/Boost). **CPU.**
- **Status:** Lightly maintained (stable).
- **Commercial:** ✅ MIT (confirm you're on `silicos-it/shape-it`, not the LGPL Pharao).

### Align-it — `OliverBScott/align-it`
- **What/method:** **Pharmacophore-based alignment** — extracts pharmacophore points (donor/acceptor/aromatic/hydrophobe/charge) and overlays/scores. Pairs with Shape-it for shape+pharmacophore. *(No `silicos-it/align-it` repo exists — the maintained fork is `OliverBScott/align-it`; engine in `silicos-it/pharao`.)*
- **Code license:** ⚠️ **GPL-3.0** (original Pharao core LGPL-3.0). Copyleft.
- **Paper:** Taminau et al., *JMGM* 27(2):161, 2008. DOI 10.1016/j.jmgm.2008.04.003.
- **Install / GPU:** C++/CMake (OpenBabel3). **CPU.**
- **Commercial:** ⚠️ **GPL-3.0** — internal use fine; distributing a product that links it triggers copyleft. Run it as a standalone CLI to avoid linking concerns (or use the LGPL `pharao` core if you must redistribute).

### RDKit — built-in shape & pharmacophore — `rdkit/rdkit` *(permissive baseline)*
- **What/method:** **Shape similarity** (`rdShapeHelpers.ShapeTanimotoDist`, `Open3DAlign`) + **pharmacophore features/fingerprints** (`ChemicalFeatures`, 2D/3D pharmacophore FPs, pharmacophore-constrained embedding). No statistical target model — but the substrate everything else builds on.
- **Code license:** ✅✅ **BSD-3-Clause** — the safest baseline; build your own shape/pharmacophore anti-target screen with zero copyleft exposure.
- **Citation:** Landrum, *RDKit: Open-source cheminformatics*, rdkit.org. (Pharmacophore-FP: Gobbi & Lee, 2003.)
- **Install / GPU:** `pip install rdkit` / conda. **CPU.**
- **Status:** Very active (the de-facto standard).
- **Commercial:** ✅✅ BSD-3.

### OpenPharmacophore — `uibcdf/OpenPharmacophore`
- **What/method:** Python library to derive pharmacophores from ligand / ligand-receptor / receptor inputs **and from MD trajectories**, plus virtual screening. A viable open pharmacophore-modeling complement to Align-it.
- **Code license:** ✅ **MIT.**
- **Install / GPU:** RDKit + scientific Python. **CPU.**
- **Status:** ⚠️ Somewhat stale (authors mark it "in progress"; quiet since 2023).
- **Commercial:** ✅ MIT.

### ROSHAMBO2 — `molecularinformatics/roshambo2` ⭐ *(2026 — fast open ROCS)*
- **What/method:** **GPU-accelerated ROCS-style** Gaussian shape + color (pharmacophore-feature) overlay; claims >200× speedup over the original ROSHAMBO, built for large-library screening. The strongest open FastROCS-class tool — a drop-in upgrade over CPU **Shape-it**.
- **Code license:** ✅ **MIT** (no weights — it's an algorithm).
- **Paper:** *JCIM* 2025, DOI 10.1021/acs.jcim.5c01322.
- **Status:** Pushed Jan 2026, ~55★ (no tagged release yet).
- **Commercial:** ✅ MIT — the fast, permissive ROCS replacement for anti-target shape screening.

### DiffPhore — `VicFisher/DiffPhore` *(2026 — ML ligand-pharmacophore mapping)*
- **What/method:** Knowledge-guided **diffusion model for 3D ligand-pharmacophore mapping** — predicts a ligand's bound conformation against a pharmacophore with calibrated sampling; beats classical pharmacophore tools and some docking on pose/conformer prediction. Fills an ML-pharmacophore gap none of ESP-Sim / Shape-it / Align-it / OpenPharmacophore cover. Bundles the AncPhore engine.
- **Code + weights:** ✅ **MIT** (weights in-repo; datasets on Zenodo 14819917).
- **Paper:** *Nature Communications* 16:2269 (2025), DOI 10.1038/s41467-025-57485-3.
- **Status:** Very active (pushed Jun 2026, ~51★).
- **Commercial:** ✅ MIT — bundled weights, peer-reviewed, maintained.

> **Commercial reference points (proprietary, not open):** **ROCS** (OpenEye/Cadence) — industry-standard Gaussian shape + color (pharmacophore) overlay, the benchmark Shape-it/ESP-Sim/ROSHAMBO2 are measured against; **Phase** (Schrödinger) — pharmacophore modeling + 3D database screening.

---

## Choosing (for a selectivity / anti-target screen)

| Need | Pick | License |
|---|---|---|
| Embeddable off-target prediction over ChEMBL | **ChEMBL multitask model** | ✅ MIT (data CC BY-SA) |
| Quick free target-fishing (manual) | **SwissTargetPrediction** / SEA web | ⚠️ query-only |
| "Does it overlay a known anti-target ligand?" (shape + charge) | **ESP-Sim** | ✅ MIT |
| Shape-only overlay (ROCS-style) | **Shape-it** (CPU) / **ROSHAMBO2** (GPU, faster) | ✅ MIT |
| Pharmacophore overlay | **Align-it** (GPL) / **OpenPharmacophore** (MIT) | ⚠️ / ✅ |
| ML ligand-pharmacophore mapping | **DiffPhore** | ✅ MIT |
| Roll-your-own, fully permissive | **RDKit** shape + pharmacophore | ✅✅ BSD-3 |

**Anti-target workflow for a tryptamine 5-HT program:** run candidates through the **ChEMBL multitask model** (broad off-target scan) + an **ESP-Sim** overlay against known **5-HT2B** agonists (focused liability check), gate the series on 2A-over-2B, then feed survivors to the synthesizability layer. **Commercial-clean set:** ChEMBL multitask, ESP-Sim, Shape-it, RDKit, OpenPharmacophore. **Flags:** Align-it (GPL copyleft), all the web/no-license predictors (SEA, SwissTarget, PPB2/3, SPiDER/TIGER). See [licensing-and-data.md](licensing-and-data.md).
