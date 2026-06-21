# ADMET Prediction

*"Will it survive as a drug?"* — absorption, distribution, metabolism, excretion, toxicity, plus the specific liabilities that sink CNS programs: **hERG** cardiotoxicity, **blood-brain-barrier** penetration (for a CNS target like a 5-HT receptor you *want* it; for a peripheral target you don't), **CYP**/MAO metabolism, Ames, DILI.

**Two things to keep straight:**
1. **ADMET predictors are triage/flagging tools, not ground truth.** Use them to rank and de-prioritize; confirm anything that matters experimentally.
2. **Open local model you can deploy** vs. **academic web tool you cannot legally embed.** This is the dominant licensing split below — most ADMET "tools" are free web servers whose terms forbid commercial embedding, even though anyone can query them. Only **ADMET-AI** is a clean, deployable, permissively-licensed local model. Licenses verified **2026-06-13**.

> Built on the same backbone as [property-and-qsar-prediction.md](property-and-qsar-prediction.md) — ADMET-AI = Chemprop + TDC. For target *binding* (not ADMET) see [docking-and-cofolding.md](docking-and-cofolding.md) / [binding-affinity-and-fep.md](binding-affinity-and-fep.md); for off-target/selectivity see [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md).

---

## ADMET-AI — `swansonk14/admet_ai` ⭐ *(open local package + web server)*
- **What/method:** Full ADMET profile from SMILES — absorption (HIA, Caco-2, PAMPA, P-gp), distribution (**BBB**, PPB, VDss), metabolism (**CYP** inhibition/substrate), excretion (half-life, clearance), toxicity (**hERG**, Ames, DILI, LD50) — contextualized vs. 2,579 approved DrugBank drugs. Bundled **Chemprop v2** GNN weights trained on **TDC** datasets. **Same author as SyntheMol** (Kyle Swanson — see [synthesizable-generation.md](synthesizable-generation.md)).
- **Code license:** **MIT** (`LICENSE.txt`, © 2026 Kyle Swanson).
- **Weights/data:** weights ship with the package; training provenance is **TDC** (so the TDC data caveat applies transitively — see [property-and-qsar-prediction.md](property-and-qsar-prediction.md)).
- **Paper:** *ADMET-AI*, *Bioinformatics* 40(7):btae416, 2024. DOI 10.1093/bioinformatics/btae416.
- **Install / GPU:** `pip install admet-ai` (Python ≥3.11). Web: `admet.ai.greenstonebio.com` (≤1,000 molecules). **No GPU required** — CPU-fine.
- **Status:** Active — v2.0.1 (2026-02).
- **Commercial:** ✅ **Green — deployable locally.** MIT code + bundled weights. Only light check: comfort with TDC-derived training provenance. **The clean anchor for an embeddable ADMET layer.**

## TDC (ADMET Benchmark Group) — `mims-harvard/TDC`
- **What/method:** The standard ~22-dataset **ADMET benchmark** (Caco2, HIA, BBB_Martins, CYP2C9/2D6/3A4_Veith, hERG, Ames, DILI, LD50, clearance, half-life) — the leaderboard ADMET-AI tops, and a DIY training source. (Full card in [property-and-qsar-prediction.md](property-and-qsar-prediction.md).)
- **Code license:** **MIT.** ⚠️ **Datasets separately licensed** (ChEMBL CC BY-SA, some non-commercial) — vet each before commercial training/redistribution.
- **Commercial:** ✅ code / ⚠️ data.

## DeepPK (Deep-PK) — **WEB / API-ONLY** (`biosig.lab.uq.edu.au/deeppk`)
- **What/method:** Deep-learning PK/tox across **73 endpoints** (incl. hERG, BBB, CYP); D-MPNN backbone. Ascher lab, UQ. No source repo exists.
- **License/access:** No code → no code license. Web free, no login, public REST API (no key). Paper is **NAR CC BY-NC** (non-commercial); training data partly ADMETlab-2.0-derived (non-commercial provenance).
- **Paper:** *Deep-PK*, *NAR* 52(W1):W469, 2024. DOI 10.1093/nar/gkae254.
- **Commercial:** ❌ **Cannot be embedded** — academic host, no redistribution license, NC provenance. Routing proprietary structures to it = IP/ToS risk.

## ADMETlab 3.0 — **WEB / API-ONLY** (`admetlab3.scbdd.com`)
- **What/method:** Comprehensive online ADMET — **119 endpoints** (physchem, med-chem, absorption, distribution, metabolism incl. CYP, excretion, toxicity incl. hERG, toxicophore rules). Multi-task DMPNN with uncertainty. No official v3 code repo.
- **License/access:** No code. Web/API free (≤5 req/s). **Binding restriction: paper is NAR CC BY-NC, and commercial use / bulk data download "requires explicit permission of the authors."**
- **Paper:** *ADMETlab 3.0*, *NAR* 52(W1):W422, 2024. DOI 10.1093/nar/gkae236.
- **Commercial:** ❌ **Cannot be embedded; commercial use gated behind author permission.** Free public access ≠ commercial license.

## SwissADME — **WEB-ONLY** (`swissadme.ch`)
- **What/method:** Physchem, lipophilicity (consensus LogP), solubility, PK (GI absorption + **BBB** via BOILED-Egg, P-gp, **CYP** 1A2/2C19/2C9/2D6/3A4 inhibition), druglikeness (Lipinski/Veber/…), med-chem alerts (PAINS/Brenk). **No toxicity/hERG.** SIB / Univ. Lausanne.
- **License/access:** Web-only, free, no login. **Notably commercial-friendly terms:** permitted use explicitly includes "internal research, **whether on a commercial or non-commercial basis**," and **results are CC-BY 4.0** (redistributable with attribution). Restrictions: no competing service, no bulk scraping (>20% automated).
- **Paper:** Daina, Michielin, Zoete, *Sci. Rep.* 7:42717, 2017. DOI 10.1038/srep42717.
- **Commercial:** ⚠️ **Results usable commercially (CC-BY 4.0), but the engine can't be deployed/embedded** (no source/weights) and bulk scraping is barred. The most commercial-friendly of the web tools — treat as a manual/scriptable lookup.

## pkCSM — **WEB-ONLY** (`biosig.lab.uq.edu.au/pkcsm`)
- **What/method:** ADMET across all five classes via **graph-based signatures** (Caco-2, HIA, BBB logBB, CNS logPS, CYP inhibitors/substrates, clearance, Ames, **hERG I/II**, LD50, hepatotoxicity…). Ascher group.
- **License/access:** Web-only, free for academic use. **Non-academic/commercial use requires a separate paid license** negotiated with the lab.
- **Paper:** Pires, Blundell, Ascher, *J. Med. Chem.* 58(9):4066, 2015. DOI 10.1021/acs.jmedchem.5b00104.
- **Commercial:** ❌ **Cannot be embedded; commercial use needs a paid non-academic license.**

## CardioTox net (hERG) — `Abdulk084/CardioTox`
- **What/method:** Deep-learning meta-feature **ensemble** for hERG blockade (binary). Pretrained weights included.
- **Code license:** 🔴 **NO LICENSE FILE = all rights reserved** (verified: GitHub `license: null`, no LICENSE anywhere). Critical commercial red flag.
- **Paper:** Karim et al., *J. Cheminform.* 13:60, 2021. DOI 10.1186/s13321-021-00541-z.
- **Commercial:** ❌ **No license** — no granted right to use/redistribute without an explicit author grant.

## BayeshERG (hERG) — `GIST-CSBL/BayeshERG`
- **What/method:** **Bayesian GNN** for hERG blockade with **calibrated uncertainty** (MC-dropout) + atom-level attention.
- **Licenses (split):** ✅ **code MIT** / ⚠️ **trained models + data CC-BY-NC-SA-4.0 (non-commercial)** — the repo ships both files.
- **Paper:** Kim et al., *Brief. Bioinform.* 23(4):bbac211, 2022. DOI 10.1093/bib/bbac211.
- **Commercial:** ⚠️ **Mixed** — MIT code, NC weights. For commercial deployment, **retrain on permissive data using the MIT code**, or license the weights.

## B3DB (BBB dataset) — `theochem/B3DB`
- **What/method:** Largest open **BBB-permeability benchmark** (1,058 numeric logBB + 7,982 BBB±), 50 sources, with descriptors + notebooks. A **dataset**, not a packaged model — pair with your own classifier (e.g. Chemprop).
- **License:** ✅ **CC0-1.0 (public domain)** — the cleanest license in this whole layer. (The companion model code `theochem/B3clf` is **GPL-3.0** — copyleft — distinct from the CC0 data.)
- **Paper:** Meng et al., *Sci. Data* 8:289, 2021. DOI 10.1038/s41597-021-01069-5.
- **Commercial:** ✅ **Green — CC0, no restrictions.**

## CYP inhibition — `ersilia-os/eos44zp` (+ DIY-on-TDC)
- **What/method:** Ersilia Model Hub package wrapping NCATS **CYP2C9/2D6/3A4** models.
- **Code license:** ✅ **GPL-3.0** (copyleft). Weights included but **large** (~5.6 GB pkg / ~19 GB Docker).
- **Status:** ⚠️ **Archived (read-only) since 2025-12** — frozen but functional.
- **Commercial:** ⚠️ GPL-3 copyleft (SaaS generally OK; bundling into shipped software triggers copyleft) + archived. **Cleaner alternative:** train your own CYP classifier on **TDC** (`CYP2C9/2D6/3A4_Veith`) — PyTDC is MIT, actively maintained, fully permissive path.

---

## OpenADMET — `OpenADMET/openadmet-models` + `openadmet-toolkit` ⭐ *(2026 — the open-ADMET consortium)*
- **What/method:** Open-science ADMET consortium (OMSF / UCSF / Octant / MSKCC; ARPA-H + Gates funded) shipping **deployable models with downloadable Apache-2.0 weights** — exactly the embeddable-vs-web-only gap. Endpoints: Caco-2 permeability (A→B / B→A), LogD, human + mouse plasma-protein binding, microsomal clearance, multitask **CYP** (1A2/2D6/3A4/2C9), and **PXR activation** (a rarer endpoint). Encoder is **CheMeleon** (see [property-and-qsar-prediction.md](property-and-qsar-prediction.md)).
- **Code + weights:** **Apache-2.0** (models repo + toolkit; HF weights Apache-2.0). Permeability model on **v2** (~Jun 2026, improved ChEMBL curation).
- **Context:** ASAP–Polaris–OpenADMET blind challenge (*JCIM* 2026, 10.1021/acs.jcim.5c02030).
- **Status:** Actively shipping (pushed Jun 2026). ⚠️ Models still "baseline"-grade; toolkit pre-1.0 (conda, not pip yet).
- **Commercial:** ✅ **Apache code + weights — deployable.** A fresher, fully-open complement to ADMET-AI; pull it with CheMeleon (the encoder).

## Choosing

| Need | Pick | Commercial |
|---|---|---|
| **Embeddable, broad ADMET (hERG/BBB/CYP)** | **ADMET-AI** | ✅ MIT, local, CPU |
| Second deployable open ADMET source (2026) | **OpenADMET** (+ CheMeleon encoder) | ✅ Apache |
| BBB data to train your own | **B3DB** | ✅ CC0 |
| Benchmark backbone / DIY training data | **TDC** | ✅ code / ⚠️ data |
| Quick manual physchem + druglikeness | **SwissADME** | ⚠️ results CC-BY; not embeddable |
| Most endpoints, manual triage only | **ADMETlab 3.0 / DeepPK** | ❌ web-only, NC |
| hERG with uncertainty | **BayeshERG** (retrain weights) | ⚠️ MIT code / NC weights |

**Bottom line:** for a commercial, embeddable ADMET layer, **ADMET-AI is the clean anchor** (MIT, CPU, hERG+BBB+CYP); add **B3DB (CC0)** for BBB and **TDC (MIT code)** as the benchmark/DIY backbone. Treat **CardioTox** (no license) and **BayeshERG weights** (CC-BY-NC-SA) as legal flags, and **all four web tools** (DeepPK, ADMETlab, SwissADME, pkCSM) as non-embeddable — manual triage only. See [licensing-and-data.md](licensing-and-data.md).
