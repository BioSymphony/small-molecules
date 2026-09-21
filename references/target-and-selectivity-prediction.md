# Target, Off-Target, and Selectivity Prediction

These tools estimate likely targets, off-targets, and selectivity from a
molecular structure. Use QSAR models in
[property-and-qsar-prediction.md](property-and-qsar-prediction.md) when you have
data for a defined target. Use the tools in this file to screen for activity at
other targets.

Two strategies are common:

1. **Target and off-target prediction** uses chemical similarity or models
   trained on sources such as ChEMBL to rank likely protein targets. Examples
   include SEA, SwissTargetPrediction, PPB2, PPB3, and the ChEMBL multitask
   model.
2. **Ligand-based three-dimensional shape and pharmacophore overlay** aligns a
   query with a known ligand and scores steric, electrostatic, or pharmacophore
   overlap. Examples include ESP-Sim, Shape-it, Align-it, RDKit, and
   OpenPharmacophore.

Several options are web-only or lack a stated code license, including SEA,
SwissTargetPrediction, PPB2, PPB3, SPiDER, and TIGER. The ChEMBL multitask
model, ESP-Sim, and Shape-it use MIT source-code terms. RDKit uses BSD-3-Clause,
and Align-it uses GPL-3.0. Review training-data terms separately; ChEMBL data use
CC BY-SA 3.0.

---

## Database Search Results

Record the query structure, database, search date, identity settings, similarity
threshold, and result limit. [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)
documents the identity modes, search limits, and response codes.

- Label `same_connectivity` results as connectivity matches. For matching
  stereochemistry and isotopes, request `same_stereo_isotope`.
- Report HTTP 503 responses and timeouts as unresolved queries. Inspect the
  response body before treating a not-found response as a search with no matches.
- If the result count reaches `MaxRecords`, mark the list as potentially
  truncated. The returned count is not a database-wide total.
- Keep the requested similarity threshold separate from per-hit scores. A CID
  list alone does not supply those scores.

Report results from different databases separately, with their search settings.
Use compound-level assay records to assess target activity.

## Target and Off-Target Prediction

### SEA — Similarity Ensemble Approach — **WEB-ONLY; PROPRIETARY ENGINE**
- **Method and output:** Predicts targets by **set-wise chemical similarity** of the query against each target's known-ligand set, with a BLAST-analogous E-value. The classic off-target tool (Shoichet lab).
- **Code:** No open Shoichet-lab repository was located for the production SEA
  service. The `momeara/DeepSEA` repository has no license file, and
  `momeara/SEAR` is a community R wrapper. SEAware is a separate proprietary
  product from SeaChange Pharmaceuticals.
- **Paper:** Keiser et al., *Nat. Biotechnol.* 2007 (DOI 10.1038/nbt1284); off-target application Lounkine et al., *Nature* 2012 (DOI 10.1038/nature11159).
- **Access:** SEA is a hosted query tool. SEAware is proprietary; no open source license is published for it.

### SwissTargetPrediction — **WEB-ONLY** (`swisstargetprediction.ch`)
- **Method and output:** Ranks probable targets from combined two-dimensional and three-dimensional similarity to selected active compounds. It returns a probability for each target.
- **License and data:** No code. The library is ChEMBL-derived; outputs are **CC BY 4.0**. Consult the site's current terms for permitted queries and automation.
- **Paper:** Daina, Michielin, Zoete, *NAR* 47(W1):W357, 2019. DOI 10.1093/nar/gkz382.
- **Access:** Hosted query service; no local code or weights are published.

### PPB2 — Polypharmacology Browser 2 — **WEB-ONLY** (`ppb2.gdb.tools`)
- **Method and output:** Target/polypharmacology prediction over ChEMBL — nearest-neighbor (MQN/Xfp/ECfp4) + Naïve Bayes + DNN. Reymond group, Bern. *(No `reymond-group/PPB2` repository exists — web only.)*
- **Paper:** Awale & Reymond, *JCIM* 59(1):10, 2019. DOI 10.1021/acs.jcim.8b00524.
- **Access:** Hosted query service; no local code or weights are published. Superseded by PPB3.

### PPB3 — Polypharmacology Browser 3 — `reymond-group/PPB3` (web `ppb3.gdb.tools`)
- **Method and output:** Deep-learning target prediction; SMILES → top-20 ranked targets; 7 DNNs over distinct fingerprints. Trained on **ChEMBL v34** (7,546 targets).
- **Code license:** No license file is stated in the public repository, which includes a training script and Flask application.
- **Reference:** See the `reymond-group/PPB3` repository and the PPB2 paper cited above.
- **Terms:** The repository does not include a code license. The web application is separately available for queries.

### ChEMBL Multitask Target-Prediction Model — `chembl/chembl_multitask_model`
- **Method and output:** Multitask **neural network** predicting active/inactive across thousands of ChEMBL targets from one molecule — built for off-target screening over large collections. Exported to **ONNX** (Python/C++/Julia/JS). Morgan/ECFP input.
- **Code license:** ✅ **MIT.**
- **Data:** trained on **ChEMBL** (CC BY-SA 3.0 — attribute + share-alike on redistributed derived data). Targets need ≥100 active + ≥100 inactive compounds.
- **Paper:** EMBL-EBI ChEMBL group (model card `chembl.github.io/chembl_multitask_model`; cf. Bosc et al., *J. Cheminform.* 2019, DOI 10.1186/s13321-018-0325-4).
- **Installation and hardware:** `pip install onnxruntime rdkit numpy`; **CPU**-fine. Active (tracks ChEMBL releases).
- **Terms:** Source code is MIT. The model is trained on ChEMBL data, whose CC BY-SA 3.0 terms remain relevant to redistributed data and derivatives.

### SPiDER / TIGER (Schneider lab) — **NO OPEN CODE**
- **Method and output:** Target prediction via consensus **self-organizing maps** over pharmacophore (CATS) + physchem descriptors; built to de-orphan de-novo molecules and probe off-targets. Was ETH-webserver-only (now defunct).
- **Paper:** Reker et al., *PNAS* 111(11):4067, 2014. DOI 10.1073/pnas.1320001111.
- **Access:** No local code or weights are published; use this as a methodological reference.

---

## Ligand-Based Shape and Pharmacophore Screening

### ESP-Sim — `hesther/espsim`
- **Method and output:** Scores three-dimensional shape and electrostatic-potential similarity. It can compare a query with a known 5-HT2B agonist.
- **Code license:** ✅ **MIT.**
- **Paper:** Bolcato, Heid, Boström, *JCIM* 62(6):1388, 2022. DOI 10.1021/acs.jcim.1c01535.
- **Installation and hardware:** conda + `pip install -e .` (RDKit/NumPy/SciPy/sklearn; optional PyTorch/Psi4 charges). **CPU** sufficient.
- **Status:** Active (2025).
- **Terms:** Source code is MIT. The optional Psi4 charge path has separate LGPL-3.0 terms.

### Shape-it — `silicos-it/shape-it`
- **Method and output:** **Gaussian-volume shape-only overlay** + Tanimoto shape scoring (Grant–Pickup) — the open analogue to ROCS shape mode.
- **Code license:** **MIT** on the modern `silicos-it/shape-it`. The original 2008 Silicos *Pharao* (`silicos-it/pharao`) is **LGPL-3.0**.
- **Paper:** Grant et al., *JCC* 1996; tool lineage Taminau et al., *JMGM* 27(2):161, 2008 (DOI 10.1016/j.jmgm.2008.04.003).
- **Installation and hardware:** C++/CMake (OpenBabel3 + optional RDKit/Boost). **CPU.**
- **Status:** Lightly maintained (stable).
- **Terms:** `silicos-it/shape-it` is MIT; `silicos-it/pharao` is LGPL-3.0.

### Align-it — `OliverBScott/align-it`
- **Method and output:** **Pharmacophore-based alignment** — extracts donor, acceptor, aromatic, hydrophobic, and charged pharmacophore points, then overlays and scores them. Pair it with Shape-it for shape and pharmacophore comparison. The maintained fork is `OliverBScott/align-it`; the engine is in `silicos-it/pharao`.
- **Code license:** ⚠️ **GPL-3.0** (original Pharao core LGPL-3.0). Copyleft.
- **Paper:** Taminau et al., *JMGM* 27(2):161, 2008. DOI 10.1016/j.jmgm.2008.04.003.
- **Installation and hardware:** C++/CMake (OpenBabel3). **CPU.**
- **Terms:** Source code is GPL-3.0. The original Pharao core is LGPL-3.0; review the applicable license text for a particular distribution.

### RDKit — built-in shape & pharmacophore — `rdkit/rdkit` *(permissive baseline)*
- **Method and output:** **Shape similarity** (`rdShapeHelpers.ShapeTanimotoDist`, `Open3DAlign`) + **pharmacophore features/fingerprints** (`ChemicalFeatures`, 2D/3D pharmacophore FPs, pharmacophore-constrained embedding). No statistical target model — but the substrate everything else builds on.
- **Code license:** **BSD-3-Clause.**
- **Citation:** Landrum, *RDKit: Open-source cheminformatics*, rdkit.org. (Pharmacophore-FP: Gobbi & Lee, 2003.)
- **Installation and hardware:** `pip install rdkit` / conda. **CPU.**
- **Status:** Active.
- **Terms:** Source code is BSD-3-Clause.

### OpenPharmacophore — `uibcdf/OpenPharmacophore`
- **Method and output:** Python library to derive pharmacophores from ligand / ligand-receptor / receptor inputs **and from MD trajectories**, plus virtual screening. A viable open pharmacophore-modeling complement to Align-it.
- **Code license:** ✅ **MIT.**
- **Installation and hardware:** RDKit + scientific Python. **CPU.**
- **Status:** ⚠️ Somewhat stale (authors mark it "in progress"; quiet since 2023).
- **Terms:** Source code is MIT.

### ROSHAMBO2 — `molecularinformatics/roshambo2` *(2026 open shape screening)*
- **Method and output:** **GPU-accelerated ROCS-style** Gaussian shape + color (pharmacophore-feature) overlay. The authors report more than 200× speedup over the original ROSHAMBO for large-library screening.
- **Code license:** ✅ **MIT** (no weights — it's an algorithm).
- **Paper:** *JCIM* 2025, DOI 10.1021/acs.jcim.5c01322.
- **Status:** The repository received commits in January 2026 and had no tagged release on 2026-08-30.
- **Terms:** Source code is MIT.

### DiffPhore — `VicFisher/DiffPhore` *(2026 — ML ligand-pharmacophore mapping)*
- **Method and output:** Knowledge-guided diffusion model for three-dimensional ligand-pharmacophore mapping. It predicts bound conformations from a pharmacophore and bundles AncPhore.
- **Code and weights:** ✅ **MIT** (weights in-repository; datasets on Zenodo 14819917).
- **Paper:** *Nature Communications* 16:2269 (2025), DOI 10.1038/s41467-025-57485-3.
- **Status:** The repository received commits in June 2026.
- **Terms:** The repository and bundled weights are MIT; inspect the Zenodo dataset record separately.

> **Proprietary reference points:** **ROCS** (OpenEye/Cadence) provides Gaussian shape and color (pharmacophore) overlay; **Phase** (Schrödinger) provides pharmacophore modeling and 3D database screening.

---

## Choosing (for a selectivity / anti-target screen)

| Need | Pick | License |
|---|---|---|
| Local off-target prediction over ChEMBL | **ChEMBL multitask model** | MIT code; ChEMBL data CC BY-SA |
| Quick free target-fishing (manual) | **SwissTargetPrediction** / SEA web | ⚠️ query-only |
| "Does it overlay a known anti-target ligand?" (shape + charge) | **ESP-Sim** | ✅ MIT |
| Shape-only overlay (ROCS-style) | **Shape-it** (CPU) / **ROSHAMBO2** (GPU, faster) | ✅ MIT |
| Pharmacophore overlay | **Align-it** (GPL) / **OpenPharmacophore** (MIT) | ⚠️ / ✅ |
| ML ligand-pharmacophore mapping | **DiffPhore** | ✅ MIT |
| Custom shape/pharmacophore screen | **RDKit** shape + pharmacophore | BSD-3-Clause |

For a tryptamine 5-HT program, use the **ChEMBL multitask model** for broad
off-target screening. Then compare candidates with known **5-HT2B** agonists in
**ESP-Sim**. Gate the series on 2A-over-2B before synthesis planning. See
[licensing-and-data.md](licensing-and-data.md).
