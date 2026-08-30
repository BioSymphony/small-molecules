# QSAR, Bioactivity, and Property Prediction

QSAR models predict activity or molecular properties from structure. They do
not require a protein structure, but they do require labeled data for the
selected endpoint and chemical domain.

Distinguish three types of resource:

- **Frameworks and toolkits** provide methods that you train on your own data.
  Examples include Chemprop, DeepChem, molfeat, scikit-mol, QSARtuna, and
  MolPAL.
- **Dataset and benchmark hubs** provide evaluation data and task definitions.
  Therapeutics Data Commons is the main example in this file.
- **Pretrained representation models** — embeddings and fine-tuning components,
  rather than endpoint predictors: **MoLFormer-XL, ChemBERTa, Uni-Mol.**

QSAR quality depends on the labeled data and evaluation protocol. Source-code
terms do not replace training-data terms; ChEMBL data use CC BY-SA 3.0.
Pretrained models provide features, but they still require endpoint-specific
fine-tuning and validation.

> Closely related: **[admet-prediction.md](admet-prediction.md)** (ADMET endpoints — many built on the same Chemprop/TDC stack) and **[target-and-selectivity-prediction.md](target-and-selectivity-prediction.md)** (off-target/selectivity from chemical similarity). For physics-based and ML *binding* affinity see [binding-affinity-and-fep.md](binding-affinity-and-fep.md) and [Boltz-2](docking-and-cofolding.md).

---

## Chemprop — `chemprop/chemprop`
- **Method and output:** Molecular property predictor based on a directed message-passing neural network.
- **Code license:** **MIT.**
- **Weights and data:** The package ships no weights or data; train it on endpoint-specific labeled data.
- **Paper:** *Chemprop: A Machine Learning Package for Chemical Property Prediction*, *JCIM* 2024. DOI 10.1021/acs.jcim.3c01250 (v2: 10.1021/acs.jcim.5c02332; foundational D-MPNN: Yang et al., *JCIM* 2019).
- **Installation and hardware:** `pip install chemprop` / conda. GPU optional but recommended for training.
- **Status:** On 2026-08-30, v2.2.0 was the most recent public release. It adds atom and bond targets plus foundation-model fine-tuning.
- **Terms:** Source code is MIT. Reliability depends on the training data and validation design.

## DeepChem — `deepchem/deepchem`
- **Method and output:** Broad deep-learning toolkit for drug discovery/materials/quantum — featurizers, **MoleculeNet** datasets, many model classes (GNNs, classical ML, transformers).
- **Code license:** **MIT.**
- **Paper:** *Deep Learning for the Life Sciences* (O'Reilly 2019); MoleculeNet: Wu et al., *Chem. Sci.* 2018, DOI 10.1039/C7SC02664A.
- **Installation and hardware:** `pip install deepchem[torch]` / conda. GPU optional.
- **Status:** Active codebase but **last tag v2.8.0 (2024)** — leans on nightly/`master`.
- **Terms:** The library is MIT. Each MoleculeNet dataset or downloaded model has separate terms.

## Therapeutics Data Commons (PyTDC) — `mims-harvard/TDC`
- **Method and output:** AI-ready **datasets + benchmarks** (bioactivity/DTI, ADMET, tox…); the backbone many open models train against. Dataset hub, not a model. (Also central to [admet-prediction.md](admet-prediction.md).)
- **Code license:** **MIT.**
- **Data terms:** Per-dataset and heterogeneous. Bioactivity/DTI sets derive from **ChEMBL → CC BY-SA 3.0**; some oracle or benchmark sets are non-commercial. The MIT code license does not extend to those datasets.
- **Paper:** Huang et al., *NeurIPS* 2021 (Datasets); *Nat. Chem. Biol.* 2022, DOI 10.1038/s41589-022-01131-2.
- **Installation and hardware:** `pip install PyTDC`. No GPU.
- **Status:** Active.
- **Terms:** Source code is MIT; use the named dataset's terms for data access and redistribution.

## molfeat — `datamol-io/molfeat`
- **Method and output:** A **hub of molecular featurizers** — descriptors/fingerprints + wrappers around pretrained embeddings, with caching.
- **Code license:** **Apache-2.0.** (Wrapped pretrained featurizers keep their own upstream licenses.)
- **Citation:** Zenodo DOI 10.5281/zenodo.6135486.
- **Installation and hardware:** `mamba install -c conda-forge molfeat` / pip. GPU only for transformer/GNN featurizers.
- **Status:** Active — v0.11.0 (2025).
- **Terms:** molfeat is Apache-2.0. Plug-ins and pretrained featurizers keep their upstream terms.

## scikit-mol — `EBjerrum/scikit-mol`
- **Method and output:** **scikit-learn-compatible transformers** for molecular vectorization (RDKit fingerprints/descriptors) — drop molecules/SMILES straight into sklearn `Pipeline`s.
- **Code license:** **LGPL-3.0.** Review its license text for the terms that apply to a modified or redistributed version.
- **Citation:** ChemRxiv DOI 10.26434/chemrxiv-2023-fzqwd.
- **Installation and hardware:** `pip install scikit-mol`. CPU.
- **Status:** Active — v0.6.x (2025).
- **Terms:** Source code is LGPL-3.0.

## MolPAL — `coleygroup/molpal`
- **Method and output:** **Active-learning, pool-based virtual screening** — iteratively trains a surrogate + uses acquisition functions to pick which library compounds to dock/score next, avoiding brute-force enumeration. (Coley group; pairs naturally with the docking layer as the scoring oracle.)
- **Code license:** **MIT.**
- **Paper:** Graff, Shakhnovich, Coley, *Chem. Sci.* 2021, 12(22):7866. DOI 10.1039/D0SC06805E.
- **Installation and hardware:** conda env + `pip install -e .` (no PyPI). GPU optional.
- **Status:** ⚠️ **Stale** — last release v0.2 (2021); aging deps.
- **Terms:** Source code is MIT. The dependency stack is aging.

## QSARtuna — `MolecularAI/QSARtuna`
- **Method and output:** **AutoML for QSAR** (AstraZeneca) — Optuna search over descriptors × ML algorithms (sklearn + optional ChemProp/D-MPNN), with uncertainty + explainability.
- **Code license:** `pyproject.toml` declares **Apache-2.0**, but the repository has no standalone `LICENSE` file.
- **Paper:** Mervin et al., *JCIM* 64(14):5365, 2024. DOI 10.1021/acs.jcim.4c00457.
- **Installation and hardware:** conda + `poetry install` (**not on PyPI**). GPU only for the ChemProp backend.
- **Status:** Active (pushed 2025); no tagged releases.

## MoLFormer-XL — code `IBM/molformer`, weights `ibm-research/MoLFormer-XL-both-10pct` (HF)
- **Method and output:** Transformer **chemical language model** (SMILES) for **representations/embeddings + fine-tuning**; linear-attention transformer pretrained on ~1.1B molecules.
- **Code and weights license:** ✅ **Apache-2.0** (both; verified on the HF card). **Intended for feature extraction / fine-tuning / similarity — explicitly NOT molecule generation.**
- **Data:** ZINC15 + PubChem (PubChem public-domain; ZINC has its own access terms).
- **Paper:** Ross et al., *Nature Machine Intelligence* 2022. DOI 10.1038/s42256-022-00580-7 (arXiv:2106.09553).
- **Installation and hardware:** Hugging Face `transformers` supports
  `trust_remote_code=True`; the source repository also requires NVIDIA Apex.
- **Status:** The source repository has limited recent activity.
- **Terms:** Code and weights are Apache-2.0. The model card describes feature extraction and fine-tuning rather than generation.

## ChemBERTa / ChemBERTa-2 — `seyonechithrananda/bert-loves-chemistry` (weights on HF under `DeepChem/`)
- **Method and output:** **RoBERTa on SMILES** for property prediction / embeddings (MLM and multi-task-regression variants).
- **Code license:** **MIT.** The popular HF cards (for example, `DeepChem/ChemBERTa-77M-MLM`) do not state a weights license. The model-card owner must provide applicable checkpoint terms.
- **Data:** PubChem (public-domain source).
- **Paper:** Ahmad et al., arXiv:2209.01712 (2022); orig. arXiv:2010.09885.
- **Terms:** Source code is MIT; the listed checkpoints do not state a weights license.

## Uni-Mol — `deepmodeling/Uni-Mol`
- **Method and output:** **3D molecular representation learning** that uses conformers
  rather than only SMILES for property prediction, docking, and QSAR. Uni-Mol
  Docking v2 is documented in
  [docking-and-cofolding.md](docking-and-cofolding.md).
- **Code and weights license:** **MIT** (verify per-checkpoint for the largest models).
- **Paper:** Zhou et al., *ICLR* 2023; Uni-Mol2: *NeurIPS* 2024.
- **Installation and hardware:** `pip install unimol-tools`. GPU recommended (3D models are heavier); needs conformer generation.
- **Status:** Active.
- **Terms:** Source code and the documented checkpoint terms are MIT; check an individual checkpoint before use.

---

## CheMeleon — `JacksonBurns/chemeleon` *(2026 foundation encoder)*
- **Method and output:** Descriptor-based molecular **foundation model** — a D-MPNN
  pretrained to predict Mordred descriptors from about 1 million PubChem
  molecules. It integrates with Chemprop through `--from-foundation CheMeleon`
  or emits fingerprints. The authors report wins on about 79% of Polaris tasks
  against Chemprop and random-forest baselines. The model supports fine-tuning
  and supplies the encoder used by **OpenADMET**; see
  [admet-prediction.md](admet-prediction.md).
- **Code license:** **MIT** (© 2025 Jackson Burns).
- **Weights:** Available from Zenodo (DOI 10.5281/zenodo.15426600); the record lists separate terms.
- **Paper:** arXiv:2506.15792 (Jun 2025, **revised Feb 2026**).
- **Status:** The repository received commits in June 2026.

## Choosing

| Need | Pick | License |
|---|---|---|
| Target-specific affinity/property model (you have ChEMBL data) | **Chemprop** (D-MPNN) | MIT ✅ |
| AutoML over many descriptors/algos | **QSARtuna** | Apache (no LICENSE file ⚠️) |
| Broad toolkit / many model classes / MoleculeNet | **DeepChem** | MIT ✅ |
| Datasets + benchmarks to train/evaluate on | **PyTDC** | MIT code / ⚠️ data per-dataset |
| Featurization into sklearn or your own NN | **molfeat** (Apache) / **scikit-mol** (LGPL) | ✅ / ⚠️ copyleft |
| Pretrained embeddings (no generation) | **MoLFormer-XL** (Apache) / **Uni-Mol** (MIT, 3D) | ✅ |
| Foundation encoder to fine-tune (2026) | **CheMeleon** (Chemprop plug-in) | MIT code; check weights record |
| Active-learning virtual screening | **MolPAL** | MIT ✅ (stale) |

See [licensing-and-data.md](licensing-and-data.md) for the code, weight, and data terms.
