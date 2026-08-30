# Reaction-Template and Rule Infrastructure

This layer extracts, curates, and applies reaction templates and graph rules
with stereochemistry handling. It accepts custom templates, building-block
definitions, and reaction datasets used by planning and generation tools. Core
extraction and application workflows run on CPU; optional learned mappers can
use a GPU.

Some package names differ from their Python import names. Install
`reaction-utils` and import `rxnutils`. Install `rdchiral-plus` and import
`rdchiral`. The `syntemp` and `rdchiral` package and import names match.

## RDChiral — *template extraction and application*

> A Coley-group RDKit wrapper that handles the introduction, destruction,
> retention, and inversion of tetrahedral stereocenters, plus cis-trans
> stereochemistry, during template extraction and application. ASKCOS and many
> computer-aided synthesis-planning workflows use it.

- **Repository:** https://github.com/connorcoley/rdchiral.
- **License:** **MIT.**
- **Paper:** *RDChiral: An RDKit Wrapper for Handling Stereochemistry in Retrosynthetic Template Extraction and Application*, JCIM 2019, 59(6):2529 (DOI 10.1021/acs.jcim.9b00286).
- **Install:** `pip install rdchiral` (v1.1.0). Fast C++ build: `conda install -c conda-forge -c ljn917 rdchiral_cpp`.
- **Inputs and outputs:** atom-mapped reaction SMILES → SMARTS template (`extract`); template + target SMILES → precursor sets (`rdchiralRun`), chirality preserved.
- **Maintenance:** The last recorded repository push was 2023-09-18. RDKit ≥2019, Python ≥3.5, CPU.
- **Use it when:** you need an established template extractor and applicator with stereochemistry handling. `reaction-utils` depends on it.

## rdchiral_plus — *stereo and speed-focused RDChiral fork (2026)*

> A denovochem fork and extension of RDChiral with the same interface and return
> structures. It reports changes to stereochemistry handling and deterministic
> behavior.

- **Repository:** https://github.com/denovochem/rdchiral_plus. The project carries the original MIT copyright forward.
- **License:** **MIT.**
- **Paper:** none (software-only).
- **Install:** `pip install rdchiral-plus` (imports as `rdchiral`).
- **Improvements described in the README:** Fixes include single-bond directions in conjugated systems, tetrahedral centers with lone pairs, one-pot and multi-reaction templates, recursive application, deterministic parity, stereochemical inversion, and spectator tracking. The README reports successful round trips of **99.84%** for rdchiral_plus, **98.41%** for rdchiral, and **97.36%** for rdchiral_cpp. These results are self-reported and not peer-reviewed.
- **Maintenance:** Release [**v0.5.0**](https://github.com/denovochem/rdchiral_plus/releases/tag/v0.5.0) was published on **2026-08-14**; the repository was updated on 2026-08-28. RDKit ≥2019, loguru, Python ≥3.10, CPU.
- **Use it when:** you need the fork's stereochemistry and determinism changes with an RDChiral-compatible interface.

## rxnutils (reaction-utils) — *reaction data curation pipelines*

> AstraZeneca's library for reaction-data curation, atom mapping, template
> extraction, and reproducible pipelines, including a USPTO preparation
> pipeline. It converts raw reaction records into atom-mapped data and extracted
> templates.

- **Repository:** https://github.com/MolecularAI/reaction_utils.
- **License:** **Apache-2.0.**
- **Paper:** *rxnutils – A Cheminformatics Python Library for Manipulating Chemical Reaction Data*, ChemRxiv 2022 (DOI 10.26434/chemrxiv-2022-wt440-v2). The cited 2024 J. Cheminform. paper describes AiZynthFinder.
- **Install:** `pip install reaction-utils` (imports `rxnutils`). Atom-mapping via rxnmapper needs a separate env/extra.
- **Inputs and outputs:** reaction SMILES/datasets → cleaned reactions, extracted SMARTS templates, processed routes (route module uses APTED tree-edit-distance for route comparison).
- **Dependencies:** RDKit (pinned `>=2023.9.1,<2024`), **rdchiral**, pandas, dask, metaflow, cgrtools-plus, optional onnxruntime. Python 3.9–3.12, CPU.
- **Maintenance:** The latest listed release is v1.9.3 from December 2025.
- **Use it when:** you are building or curating reaction datasets or route corpora for model training.

## SynTemp — *graph-based (ITS/DPO) rule extraction*

> Extracts reaction rules as partial **Imaginary Transition State (ITS)** graphs ≈ Double-Pushout (DPO) graph-rewriting rules, with hierarchical template clustering and an **ensemble** atom-mapper (RXNMapper + GraphormerMapper + LocalMapper) for consensus mapping.

- **Repository:** https://github.com/TieuLongPhan/SynTemp (Leipzig).
- **License:** **MIT.**
- **Paper:** *SynTemp: Efficient Extraction of Graph-Based Reaction Rules from Large-Scale Reaction Databases*, JCIM 2025 (DOI 10.1021/acs.jcim.4c01795).
- **Install:** `pip install syntemp` (core) or `syntemp[all]` (pulls PyTorch/DGL/mappers).
- **Inputs and outputs:** reaction SMILES (CSV) → atom-mapped reactions + templates in **GML** (graph-rule files) + hierarchical clusters.
- **Dependencies:** RDKit ≥2024.3.5, NetworkX, synrbl, synkit; `[all]` adds DGL/DGLLife/localmapper/rxnmapper/chytorch/PyTorch. Python ≥3.11. CPU core; learned mappers can use GPU.
- **Caveats:** The `[all]` extra installs many dependencies. GML and DPO outputs target graph-rewriting engines such as MØD; they do not directly replace an RDKit SMARTS pipeline.
- **Use it when:** you need mechanism-aware graph-rewriting rules and consensus atom mapping for datasets beyond SMARTS templates.

## Choosing

- **Extract and apply SMARTS templates with stereochemistry:** Use **RDChiral** or evaluate the **rdchiral_plus** fork for its stereochemistry and determinism changes.
- **Curate a reaction dataset or build a route corpus:** Use **rxnutils**. It uses Apache-2.0 terms and depends on rdchiral.
- **Extract graph-rewriting rules with ensemble atom mapping:** Use **SynTemp**.

`reaction-utils` depends on `rdchiral`. Install RDChiral first when you build the AstraZeneca reaction-template stack.
