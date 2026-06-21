# Reaction-Template & Rule Infrastructure

The unglamorous-but-load-bearing layer: **extract, curate, and apply reaction templates / rules** with correct stereochemistry. You need this if you want custom templates, your own building-block chemistry, internal route rules, or clean reaction datasets to train any of the models elsewhere in this compilation. All CPU; all permissively licensed.

> **pip-name traps** (the package name ≠ the import name in several cases): `reaction-utils` (imports `rxnutils`), `syntemp`, `rdchiral`, `rdchiral-plus` (imports `rdchiral`). Get these wrong and the install silently fails.

## RDChiral — *the foundational template extractor/applicator*

> The Coley-group RDKit wrapper that adds **consistent stereochemistry** (introduction/destruction/retention/inversion of tetrahedral centers; cis/trans) to retrosynthetic template **extraction** and **application**. The de-facto standard underneath ASKCOS and much of CASP.

- **Repo:** https://github.com/connorcoley/rdchiral (185 stars).
- **License:** **MIT.**
- **Paper:** *RDChiral: An RDKit Wrapper for Handling Stereochemistry in Retrosynthetic Template Extraction and Application*, JCIM 2019, 59(6):2529 (DOI 10.1021/acs.jcim.9b00286).
- **Install:** `pip install rdchiral` (v1.1.0). Fast C++ build: `conda install -c conda-forge -c ljn917 rdchiral_cpp`.
- **I/O:** atom-mapped reaction SMILES → SMARTS template (`extract`); template + target SMILES → precursor sets (`rdchiralRun`), chirality preserved.
- **Maintenance:** Stable/mature (last push 2023; not under active feature dev — which is the gap `rdchiral_plus` targets). RDKit ≥2019, Python ≥3.5, CPU.
- **Use it when:** the proven default for template extraction/application. `reaction-utils` depends on it.

## rdchiral_plus — *2026 stereo/speed-focused drop-in fork*

> A `denovochem` fork/extension of RDChiral; same interface and return structures (drop-in), with better stereochemistry and determinism.

- **Repo:** https://github.com/denovochem/rdchiral_plus (new, created 2026-02; authors include Connor Coley + Carson Britt; carries the original MIT copyright forward).
- **License:** **MIT.**
- **Paper:** none (software-only).
- **Install:** `pip install rdchiral-plus` (imports as `rdchiral`).
- **Improvements (README):** fixes corrupted single-bond directions in conjugated systems; tetrahedral centers with lone pairs; one-pot/multi-reaction templates; recursive application with configurable depth/radius; **deterministic** parity (no random shuffling); stereo-inversion counted as changed atoms; spectator tracking; auto-installs RDKit. Claimed **99.84% successful round-trips** vs 98.41% (rdchiral) / 97.36% (rdchiral_cpp) — *self-reported, not peer-reviewed*.
- **Maintenance:** New but active (v0.4.0, 2026-04; ~117 commits; 0 stars — longevity unproven; small org). RDKit ≥2019, loguru, Python ≥3.10, CPU.
- **Use it when:** you want better stereochemistry/determinism and can accept a young, unpublished fork. Easy to A/B against `rdchiral` since it's drop-in.

## rxnutils (reaction-utils) — *reaction data curation pipelines*

> AstraZeneca's library for cleaning/curating reaction datasets, atom-mapping, template extraction, and reproducible pipelines (including an end-to-end USPTO prep pipeline). The "messy reactions → clean, atom-mapped, template-ready dataset" tool.

- **Repo:** https://github.com/MolecularAI/reaction_utils (96 stars).
- **License:** **Apache-2.0.**
- **Paper:** *rxnutils – A Cheminformatics Python Library for Manipulating Chemical Reaction Data*, ChemRxiv 2022 (DOI 10.26434/chemrxiv-2022-wt440-v2). (Don't confuse with the 2024 J. Cheminform. paper, which is AiZynthFinder.)
- **Install:** `pip install reaction-utils` (imports `rxnutils`). Atom-mapping via rxnmapper needs a separate env/extra.
- **I/O:** reaction SMILES/datasets → cleaned reactions, extracted SMARTS templates, processed routes (route module uses APTED tree-edit-distance for route comparison).
- **Deps:** RDKit (pinned `>=2023.9.1,<2024`), **rdchiral**, pandas, dask, metaflow, cgrtools-plus, optional onnxruntime. Python 3.9–3.12, CPU.
- **Maintenance:** Actively maintained (v1.9.3, 2025-12).
- **Use it when:** you're building/curating a reaction dataset or route corpus to train models — the standard pipeline layer.

## SynTemp — *graph-based (ITS/DPO) rule extraction*

> Extracts reaction rules as partial **Imaginary Transition State (ITS)** graphs ≈ Double-Pushout (DPO) graph-rewriting rules, with hierarchical template clustering and an **ensemble** atom-mapper (RXNMapper + GraphormerMapper + LocalMapper) for consensus mapping.

- **Repo:** https://github.com/TieuLongPhan/SynTemp (Leipzig; 36 stars).
- **License:** **MIT.**
- **Paper:** *SynTemp: Efficient Extraction of Graph-Based Reaction Rules from Large-Scale Reaction Databases*, JCIM 2025 (DOI 10.1021/acs.jcim.4c01795).
- **Install:** `pip install syntemp` (core) or `syntemp[all]` (pulls PyTorch/DGL/mappers).
- **I/O:** reaction SMILES (CSV) → atom-mapped reactions + templates in **GML** (graph-rule files) + hierarchical clusters.
- **Deps:** RDKit ≥2024.3.5, NetworkX, synrbl, synkit; `[all]` adds DGL/DGLLife/localmapper/rxnmapper/chytorch/PyTorch. Python ≥3.11. CPU core; learned mappers can use GPU.
- **Caveats:** heavy `[all]` dependency tree; GML/DPO output targets graph-rewriting engines (e.g., MØD), **not** a drop-in for RDKit SMARTS pipelines.
- **Use it when:** you want mechanism-aware, graph-rewriting-style rules and consensus atom-mapping at scale — beyond what SMARTS templates capture.

## Choosing

- **Extract/apply SMARTS templates with correct stereo:** **RDChiral** (proven) or **rdchiral_plus** (newer, drop-in, better stereo/determinism).
- **Curate a reaction dataset / build a route corpus:** **rxnutils** (Apache-2.0, depends on rdchiral).
- **Graph-rewriting (ITS/DPO) rules + ensemble mapping:** **SynTemp**.

Dependency reality: `reaction-utils` → `rdchiral`, so RDChiral sits at the base of the AstraZeneca stack. Start there.
