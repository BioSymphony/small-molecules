# ADMET Prediction

ADMET predictors estimate absorption, distribution, metabolism, excretion, and
toxicity. They also flag specific liabilities such as hERG blockade,
blood-brain-barrier penetration, CYP and MAO metabolism, Ames mutagenicity, and
drug-induced liver injury.

Use these predictors to rank candidates and identify follow-up tests. Confirm
important predictions experimentally. Also distinguish local packages from
hosted services. Most hosted entries do not publish local source code or
weights. ADMET-AI and OpenADMET publish local artifacts, but their code, weight,
and training-data terms remain separate.

ADMET-AI uses Chemprop models trained on TDC datasets. For general property
models, see [property-and-qsar-prediction.md](property-and-qsar-prediction.md).
For binding, see [docking-and-cofolding.md](docking-and-cofolding.md) and
[binding-affinity-and-fep.md](binding-affinity-and-fep.md). For off-target and
selectivity analysis, see
[target-and-selectivity-prediction.md](target-and-selectivity-prediction.md).

---

## ADMET-AI — `swansonk14/admet_ai` *(local package and web server)*
- **Method and output:** Predicts ADMET endpoints from SMILES with bundled Chemprop v2 GNNs trained on TDC datasets. Endpoints cover absorption, distribution, metabolism, excretion, and toxicity, including hERG, BBB, CYP, Ames, DILI, and LD50. It contextualizes predictions against 2,579 approved DrugBank drugs.
- **Code license:** **MIT** (`LICENSE.txt`, © 2026 Kyle Swanson).
- **Weights and data:** Weights ship with the package; training provenance is **TDC**. Version 2 uses Chemprop v2 rather than Chemprop-RDKit, and its predictions differ from version 1.
- **Paper:** *ADMET-AI*, *Bioinformatics* 40(7):btae416, 2024. DOI 10.1093/bioinformatics/btae416.
- **Installation and hardware:** `pip install admet-ai` (Python ≥3.11). Web: `admet.ai.greenstonebio.com` (≤1,000 molecules). **No GPU required** — CPU-fine.
- **Status:** On 2026-08-30, v2.0.1 was the most recent public release. It adds PAINS, BRENK, and NIH alerts.
- **Terms:** Code and bundled weights are MIT. The TDC datasets used for training have separate, dataset-specific terms.

## TDC (ADMET Benchmark Group) — `mims-harvard/TDC`
- **Method and output:** ADMET benchmark containing about 22 datasets, including Caco2, HIA, BBB_Martins, CYP, hERG, Ames, DILI, LD50, clearance, and half-life. It supports training and evaluation; see [property-and-qsar-prediction.md](property-and-qsar-prediction.md).
- **Code license:** **MIT.** Datasets are separately licensed; examples include ChEMBL CC BY-SA and non-commercial datasets.
- **Terms:** Code and data terms are separate.

## DeepPK (Deep-PK) — **WEB / API-ONLY** (`biosig.lab.uq.edu.au/deeppk`)
- **Method and output:** Deep-learning PK/tox across **73 endpoints** (incl. hERG, BBB, CYP); D-MPNN backbone. Ascher lab, UQ. No source repository exists.
- **License and access:** No local code or weights are published. The web service has a public REST API. The paper is **NAR CC BY-NC**; its training data partly derive from ADMETlab-2.0.
- **Paper:** *Deep-PK*, *NAR* 52(W1):W469, 2024. DOI 10.1093/nar/gkae254.
- **Terms:** This is a hosted service, not a published local package. Consult the site's terms before submitting sensitive structures or automating requests.

## ADMETlab 3.0 — **WEB / API-ONLY** (`admetlab3.scbdd.com`)
- **Method and output:** Online predictions for **119 endpoints**, including physicochemical and medicinal-chemistry properties, absorption, distribution, CYP metabolism, excretion, hERG and other toxicity endpoints, and toxicophore rules. The method uses a multitask D-MPNN with uncertainty estimates. No official v3 code repository is public.
- **License and access:** No local code or weights are published. The web/API documentation states a ≤5 request/s rate. The paper is NAR CC BY-NC and states that commercial use or bulk data downloads require author permission.
- **Paper:** *ADMETlab 3.0*, *NAR* 52(W1):W422, 2024. DOI 10.1093/nar/gkae236.
- **Terms:** Hosted service; no local software license is published. The site and paper terms govern use and bulk-data access.

## SwissADME — **WEB-ONLY** (`swissadme.ch`)
- **Method and output:** Physchem, lipophilicity (consensus LogP), solubility, PK (GI absorption + **BBB** via BOILED-Egg, P-gp, **CYP** 1A2/2C19/2C9/2D6/3A4 inhibition), druglikeness (Lipinski/Veber/…), med-chem alerts (PAINS/Brenk). **No toxicity/hERG.** SIB / Univ. Lausanne.
- **License and access:** Web-only and no login. The site states that results are **CC BY 4.0** and restricts competing services and bulk scraping (more than 20% automated requests).
- **Paper:** Daina, Michielin, Zoete, *Sci. Rep.* 7:42717, 2017. DOI 10.1038/srep42717.
- **Terms:** Results are CC BY 4.0 under the site's stated conditions. No local source code or weights are published.

## pkCSM — **WEB-ONLY** (`biosig.lab.uq.edu.au/pkcsm`)
- **Method and output:** ADMET across all five classes via **graph-based signatures** (Caco-2, HIA, BBB logBB, CNS logPS, CYP inhibitors/substrates, clearance, Ames, **hERG I/II**, LD50, hepatotoxicity…). Ascher group.
- **License and access:** Web-only and free for academic use. The site states that non-academic use requires a separate license from the lab.
- **Paper:** Pires, Blundell, Ascher, *J. Med. Chem.* 58(9):4066, 2015. DOI 10.1021/acs.jmedchem.5b00104.
- **Terms:** No local source code or weights are published; consult the site's license terms for non-academic use.

## CardioTox net (hERG) — `Abdulk084/CardioTox`
- **Method and output:** Deep-learning meta-feature **ensemble** for hERG blockade (binary). Pretrained weights included.
- **Code license:** No license file is present in the repository.
- **Paper:** Karim et al., *J. Cheminform.* 13:60, 2021. DOI 10.1186/s13321-021-00541-z.
- **Terms:** The repository does not state code or weights terms.

## BayeshERG (hERG) — `GIST-CSBL/BayeshERG`
- **Method and output:** **Bayesian GNN** for hERG blockade with **calibrated uncertainty** (MC-dropout) + atom-level attention.
- **Licenses (split):** ✅ **code MIT** / ⚠️ **trained models + data CC-BY-NC-SA-4.0 (non-commercial)** — the repository ships both files.
- **Paper:** Kim et al., *Brief. Bioinform.* 23(4):bbac211, 2022. DOI 10.1093/bib/bbac211.
- **Terms:** Code is MIT; released trained models and data are CC BY-NC-SA-4.0.

## B3DB (BBB dataset) — `theochem/B3DB`
- **Method and output:** An open BBB-permeability benchmark with 1,058 numeric logBB records and 7,982 BBB labels from 50 sources, plus descriptors and notebooks. This is a dataset rather than a packaged model; pair it with a classifier such as Chemprop.
- **License:** **CC0-1.0** (public domain). The companion model code, `theochem/B3clf`, is **GPL-3.0** and is distinct from the dataset.
- **Paper:** Meng et al., *Sci. Data* 8:289, 2021. DOI 10.1038/s41597-021-01069-5.
- **Terms:** Dataset is CC0-1.0; companion code has separate GPL-3.0 terms.

## CYP Inhibition — `ersilia-os/eos44zp` and TDC Training Data
- **Method and output:** Ersilia Model Hub package wrapping NCATS **CYP2C9/2D6/3A4** models.
- **Code license:** ✅ **GPL-3.0** (copyleft). Weights included but **large** (~5.6 GB pkg / ~19 GB Docker).
- **Status:** ⚠️ **Archived (read-only) since 2025-12** — frozen but functional.
- **Terms:** Source code is GPL-3.0; the repository is archived. TDC provides the `CYP2C9/2D6/3A4_Veith` datasets under their own terms.

---

## OpenADMET — `OpenADMET/openadmet-models` and `openadmet-toolkit` *(2026 consortium release)*
- **Method and output:** Open-science ADMET consortium shipping local models with downloadable Apache-2.0 weights. Endpoints include Caco-2 permeability (A→B / B→A), LogD, human and mouse plasma-protein binding, microsomal clearance, multitask **CYP** (1A2/2D6/3A4/2C9), and **PXR activation**. The encoder is **CheMeleon** (see [property-and-qsar-prediction.md](property-and-qsar-prediction.md)).
- **Code and weights:** **Apache-2.0** for the models repository, toolkit, and listed weights. The permeability model v2 was available in June 2026.
- **Context:** ASAP–Polaris–OpenADMET blind challenge (*JCIM* 2026, 10.1021/acs.jcim.5c02030).
- **Status:** Public code activity continued through June 2026. The toolkit is pre-1.0 and uses conda rather than pip.
- **Terms:** Check the underlying data and CheMeleon checkpoint terms separately.

## Choosing

| Need | Pick | Terms |
|---|---|---|
| Local, broad ADMET (hERG/BBB/CYP) | **ADMET-AI** | MIT code and bundled weights; TDC data terms |
| Second local ADMET source (2026) | **OpenADMET** (+ CheMeleon encoder) | Apache-2.0 code and weights |
| BBB data for a custom model | **B3DB** | CC0-1.0 dataset |
| Benchmark backbone / training data | **TDC** | MIT code; per-dataset data terms |
| Physchem + drug-likeness lookup | **SwissADME** | Hosted service; CC BY 4.0 results under site terms |
| Broad hosted endpoints | **ADMETlab 3.0 / DeepPK** | Hosted services; no local artifacts published |
| hERG with uncertainty | **BayeshERG** | MIT code; CC BY-NC-SA models and data |
