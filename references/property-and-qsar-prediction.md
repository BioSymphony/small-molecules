# QSAR, Bioactivity & Property Prediction

The **ligand-based** half of *"will it bind?"* — and the broadest. Given enough labeled data for a target (e.g. ChEMBL IC50/Ki for 5-HT2A), a QSAR model predicts activity from structure alone, no protein structure required. It also covers physchem/property prediction and the molecular representations that feed everything downstream.

**Read this distinction first — it's the #1 source of confusion here:**

- **Frameworks / toolkits** — you bring your own data + targets; they ship *methods*, not validated predictors: **Chemprop, DeepChem, molfeat, scikit-mol, QSARtuna, MolPAL.**
- **Dataset / benchmark hubs:** **Therapeutics Data Commons (PyTDC).**
- **Pretrained representation models** — embeddings/fine-tuning, not turnkey predictors: **MoLFormer-XL, ChemBERTa, Uni-Mol.**

**The load-bearing caveat:** for every framework, **QSAR quality is a function of the training data you supply**, not the code. An MIT license on Chemprop doesn't make its predictions reliable, nor does it launder your data's license (**ChEMBL is CC BY-SA 3.0** — attribution + share-alike). Pretrained models give you *features*; you still fine-tune on your own labeled endpoint. Licenses verified **2026-06-13**.

> Closely related: **[admet-prediction.md](admet-prediction.md)** (ADMET endpoints — many built on the same Chemprop/TDC stack) and **[target-and-selectivity-prediction.md](target-and-selectivity-prediction.md)** (off-target/selectivity from chemical similarity). For physics-based and ML *binding* affinity see [binding-affinity-and-fep.md](binding-affinity-and-fep.md) and [Boltz-2](docking-and-cofolding.md).

---

## Chemprop — `chemprop/chemprop` ⭐
- **What/method:** Molecular property prediction via a **Directed Message-Passing Neural Network (D-MPNN)** over the molecular graph. The de-facto open QSAR workhorse.
- **Code license:** **MIT.** Authored by the **Coley/Barzilay (MIT)** group — same ecosystem as the ASKCOS retrosynthesis stack (see [retrosynthesis-planning.md](retrosynthesis-planning.md)).
- **Weights/data:** none shipped — you train on your data.
- **Paper:** *Chemprop: A Machine Learning Package for Chemical Property Prediction*, *JCIM* 2024. DOI 10.1021/acs.jcim.3c01250 (v2: 10.1021/acs.jcim.5c02332; foundational D-MPNN: Yang et al., *JCIM* 2019).
- **Install / GPU:** `pip install chemprop` / conda. GPU optional but recommended for training.
- **Status:** Very active — v2.2.x (2026).
- **Commercial:** ✅ MIT. (Reliability still depends on your training data.) **The default for a target-specific affinity/property model.**

## DeepChem — `deepchem/deepchem`
- **What/method:** Broad deep-learning toolkit for drug discovery/materials/quantum — featurizers, **MoleculeNet** datasets, many model classes (GNNs, classical ML, transformers).
- **Code license:** **MIT.**
- **Paper:** *Deep Learning for the Life Sciences* (O'Reilly 2019); MoleculeNet: Wu et al., *Chem. Sci.* 2018, DOI 10.1039/C7SC02664A.
- **Install / GPU:** `pip install deepchem[torch]` / conda. GPU optional.
- **Status:** Active codebase but **last tag v2.8.0 (2024)** — leans on nightly/`master`.
- **Commercial:** ✅ MIT for the library. ⚠️ Verify the license of any specific MoleculeNet dataset or model you pull through it.

## Therapeutics Data Commons (PyTDC) — `mims-harvard/TDC`
- **What/method:** AI-ready **datasets + benchmarks** (bioactivity/DTI, ADMET, tox…); the backbone many open models train against. Dataset hub, not a model. (Also central to [admet-prediction.md](admet-prediction.md).)
- **Code license:** **MIT.**
- **Data license — the gate:** **per-dataset, heterogeneous.** Bioactivity/DTI sets derive from **ChEMBL → CC BY-SA 3.0**; some oracle/benchmark sets are **non-commercial**. The MIT code license does **not** cover the data — clear each dataset before commercial use.
- **Paper:** Huang et al., *NeurIPS* 2021 (Datasets); *Nat. Chem. Biol.* 2022, DOI 10.1038/s41589-022-01131-2.
- **Install / GPU:** `pip install PyTDC`. No GPU.
- **Status:** Active.
- **Commercial:** ⚠️ **Code ✅ MIT, data is the gate.** Vet each dataset's license.

## molfeat — `datamol-io/molfeat`
- **What/method:** A **hub of molecular featurizers** — descriptors/fingerprints + wrappers around pretrained embeddings, with caching.
- **Code license:** **Apache-2.0.** (Wrapped pretrained featurizers keep their own upstream licenses.)
- **Citation:** Zenodo DOI 10.5281/zenodo.6135486.
- **Install / GPU:** `mamba install -c conda-forge molfeat` / pip. GPU only for transformer/GNN featurizers.
- **Status:** Active — v0.11.0 (2025).
- **Commercial:** ✅ Apache-2.0 for molfeat; ⚠️ check the license of any plugin/pretrained featurizer you load.

## scikit-mol — `EBjerrum/scikit-mol`
- **What/method:** **scikit-learn-compatible transformers** for molecular vectorization (RDKit fingerprints/descriptors) — drop molecules/SMILES straight into sklearn `Pipeline`s.
- **Code license:** ⚠️ **LGPL-3.0** (weak copyleft) — the one non-MIT/Apache tool here. Use/link freely in commercial software; **modifications to scikit-mol itself must be shared** under LGPL.
- **Citation:** ChemRxiv DOI 10.26434/chemrxiv-2023-fzqwd.
- **Install / GPU:** `pip install scikit-mol`. CPU.
- **Status:** Active — v0.6.x (2025).
- **Commercial:** ✅ usable (LGPL permits use without relicensing your app); keep it an unmodified dependency to avoid copyleft obligations.

## MolPAL — `coleygroup/molpal`
- **What/method:** **Active-learning, pool-based virtual screening** — iteratively trains a surrogate + uses acquisition functions to pick which library compounds to dock/score next, avoiding brute-force enumeration. (Coley group; pairs naturally with the docking layer as the scoring oracle.)
- **Code license:** **MIT.**
- **Paper:** Graff, Shakhnovich, Coley, *Chem. Sci.* 2021, 12(22):7866. DOI 10.1039/D0SC06805E.
- **Install / GPU:** conda env + `pip install -e .` (no PyPI). GPU optional.
- **Status:** ⚠️ **Stale** — last release v0.2 (2021); aging deps.
- **Commercial:** ✅ MIT; ⚠️ budget integration/maintenance effort.

## QSARtuna — `MolecularAI/QSARtuna`
- **What/method:** **AutoML for QSAR** (AstraZeneca) — Optuna search over descriptors × ML algorithms (sklearn + optional ChemProp/D-MPNN), with uncertainty + explainability.
- **Code license:** ⚠️ **Apache-2.0 declared in `pyproject.toml` but NO standalone LICENSE file** — GitHub's detector misses it. Intent is clearly Apache-2.0; for legal certainty, ask AZ to add the file.
- **Paper:** Mervin et al., *JCIM* 64(14):5365, 2024. DOI 10.1021/acs.jcim.4c00457.
- **Install / GPU:** conda + `poetry install` (**not on PyPI**). GPU only for the ChemProp backend.
- **Status:** Active (pushed 2025); no tagged releases.
- **Commercial:** ⚠️ intended Apache-2.0 (permissive) with a **missing-LICENSE-file** diligence flag.

## MoLFormer-XL — code `IBM/molformer`, weights `ibm-research/MoLFormer-XL-both-10pct` (HF)
- **What/method:** Transformer **chemical language model** (SMILES) for **representations/embeddings + fine-tuning**; linear-attention transformer pretrained on ~1.1B molecules.
- **Code + weights license:** ✅ **Apache-2.0** (both; verified on the HF card). **Intended for feature extraction / fine-tuning / similarity — explicitly NOT molecule generation.**
- **Data:** ZINC15 + PubChem (PubChem public-domain; ZINC has its own access terms).
- **Paper:** Ross et al., *Nature Machine Intelligence* 2022. DOI 10.1038/s42256-022-00580-7 (arXiv:2106.09553).
- **Install / GPU:** easiest via HF `transformers` (`trust_remote_code=True`); the code repo needs NVIDIA Apex (fiddly).
- **Status:** ⚠️ Code repo near-dormant; **HF weights stable and heavily used** — treat as a frozen working artifact.
- **Commercial:** ✅ Apache-2.0 code + weights. Mind the "no generation" intended-use note.

## ChemBERTa / ChemBERTa-2 — `seyonechithrananda/bert-loves-chemistry` (weights on HF under `DeepChem/`)
- **What/method:** **RoBERTa on SMILES** for property prediction / embeddings (MLM and multi-task-regression variants).
- **Code license:** **MIT.** ⚠️ **Weights license unspecified** — the popular HF cards (e.g. `DeepChem/ChemBERTa-77M-MLM`) carry **no license tag**. Treat weights as license-ambiguous; for commercial use confirm with the authors or retrain on the MIT code.
- **Data:** PubChem (public-domain source).
- **Paper:** Ahmad et al., arXiv:2209.01712 (2022); orig. arXiv:2010.09885.
- **Commercial:** ⚠️ **Code ✅ MIT; weights license gap** — diligence flag on the checkpoints.

## Uni-Mol — `deepmodeling/Uni-Mol`
- **What/method:** **3D molecular representation learning** (uses conformers, not just SMILES) for property prediction, docking, QSAR. (Uni-Mol Docking v2 is the docking head — see [docking-and-cofolding.md](docking-and-cofolding.md).)
- **Code + weights license:** **MIT** (verify per-checkpoint for the largest models).
- **Paper:** Zhou et al., *ICLR* 2023; Uni-Mol2: *NeurIPS* 2024.
- **Install / GPU:** `pip install unimol-tools`. GPU recommended (3D models are heavier); needs conformer generation.
- **Status:** Active.
- **Commercial:** ✅ MIT.

---

## CheMeleon — `JacksonBurns/chemeleon` *(2026 — deployable foundation encoder)*
- **What/method:** Descriptor-based molecular **foundation model** — a D-MPNN pretrained to predict Mordred descriptors (~1M PubChem). Plugs straight into **Chemprop** (`--from-foundation CheMeleon`) or emits fingerprints; ~79% win rate on Polaris vs Chemprop/RF. A strong *fine-tuning base* for any property/ADMET endpoint (train-your-own, not just frozen) — and the encoder powering **OpenADMET** (see [admet-prediction.md](admet-prediction.md)).
- **Code license:** **MIT** (© 2025 Jackson Burns). Weights on Zenodo (DOI 10.5281/zenodo.15426600), openly downloadable (confirm the Zenodo license field before redistribution).
- **Paper:** arXiv:2506.15792 (Jun 2025, **revised Feb 2026**).
- **Status:** Very active (pushed Jun 2026, ~144★).
- **Commercial:** ✅ MIT code + openly-downloadable weights. The cleanest deployable foundation encoder here — pair with Chemprop.

## Choosing

| Need | Pick | License |
|---|---|---|
| Target-specific affinity/property model (you have ChEMBL data) | **Chemprop** (D-MPNN) | MIT ✅ |
| AutoML over many descriptors/algos | **QSARtuna** | Apache (no LICENSE file ⚠️) |
| Broad toolkit / many model classes / MoleculeNet | **DeepChem** | MIT ✅ |
| Datasets + benchmarks to train/evaluate on | **PyTDC** | MIT code / ⚠️ data per-dataset |
| Featurization into sklearn or your own NN | **molfeat** (Apache) / **scikit-mol** (LGPL) | ✅ / ⚠️ copyleft |
| Pretrained embeddings (no generation) | **MoLFormer-XL** (Apache) / **Uni-Mol** (MIT, 3D) | ✅ |
| Foundation encoder to fine-tune (deployable, 2026) | **CheMeleon** (Chemprop plug-in) | MIT ✅ |
| Active-learning virtual screening | **MolPAL** | MIT ✅ (stale) |

**Commercial-clean shortlist:** Chemprop, DeepChem, molfeat, MoLFormer-XL, Uni-Mol, MolPAL (all permissive). **Flags:** scikit-mol (LGPL copyleft if modified), QSARtuna (missing LICENSE file), ChemBERTa weights (unstated), and — across all of them — the **data license** (ChEMBL CC BY-SA 3.0; some TDC sets non-commercial). See [licensing-and-data.md](licensing-and-data.md).
