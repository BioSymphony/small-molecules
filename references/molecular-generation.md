# General Molecular Generation

Generators that produce **valid** molecules (de novo, scaffold/linker, or via SMILES correction) but — unlike the [synthesizable-generation.md](synthesizable-generation.md) tools — **do not enforce synthesizability**. Their outputs are chemically valid, not guaranteed-makeable; pair them with a retrosynthesis check or SA score ([synthesizability-scoring.md](synthesizability-scoring.md)) if make-ability matters.

## GenMol — *drug-discovery generalist (NVIDIA); commercial-usable weights*

> Masked **discrete diffusion** over **SAFE** fragment sequences with parallel bidirectional decoding; one model for de novo generation, fragment-constrained design (linkers, scaffold/motif decoration), goal-directed hit generation, and lead optimization.

- **Repo:** https://github.com/NVIDIA-Digital-Bio/genmol (ships V1 and V2). Part of NVIDIA **BioNeMo**.
- **License — split, both usable:** **code Apache-2.0**; **weights under the NVIDIA Open Model License** — explicitly **"commercially usable"** and redistributable, but with attribution requirements, a revocation clause (if you bypass safety guardrails or sue NVIDIA over IP), and a no-life-critical-use term. Cleanest *commercial* posture among the general generators, with conditions.
- **Paper:** *GenMol: A Drug Discovery Generalist with Discrete Diffusion*, ICML 2025 (arXiv:2501.06158), NVIDIA.
- **Weights:** HF `nvidia/NV-GenMol-89M-v2` (89M); checkpoints on NGC; hosted **NVIDIA NIM** endpoint (`build.nvidia.com/nvidia/genmol-generate`).
- **Install / run:** `git clone …/genmol; bash env/setup.sh`; scripts for de novo / fragment / goal-directed (`pmo`) / lead-opt. RDKit, PyTorch, transformers. Train 8×A100 (~5h); inference 1×A100.
- **Representation:** **SAFE** (fragment-based → biased toward assemblable chemistries) but reports **validity, not enforced synthesizability**.
- **Maintenance:** active, well-backed (~184 stars; V2 added 2025-07).
- **Use it when:** broad lead-optimization / scaffold / linker work where you want a maintained, **commercially licensable** generalist. Add an SA/retro filter if you need make-ability.

## MolReactGen — *small autoregressive SMILES/SMARTS generator (MIT)*

> GPT-2-style decoder that generates either **molecules (SMILES)** or **reaction templates (SMARTS)** — two separate trained checkpoints.

- **Repo:** https://github.com/hogru/MolReactGen.
- **License:** **MIT** (code); HF weights inherit project terms. Public GuacaMol / USPTO-50K data.
- **Paper:** none peer-reviewed — a **Master's thesis** (Jan 2024). Cite as a thesis/software release.
- **Weights:** HF `hogru/MolReactGen-GuacaMol-Molecules`, `hogru/MolReactGen-USPTO50K-Reaction-Templates`.
- **Install / run:** `git clone --recurse-submodules …; pip install -e .`; `prepare_data.py`, `train.py`, `generate.py smiles|smarts …`. Also usable via HF `text-generation` pipeline.
- **Deps / hardware:** RDKit, PyTorch ≥2.1, transformers ≥4.35, Python ≥3.9. GPU for training.
- **Maintenance:** ⚠️ **dormant** (last push 2024-06; v1.0.0). Functional but ~2 years stale.
- **Use it when:** you want a small, MIT-licensed, hackable autoregressive generator (or a simple SMARTS-template generator) and don't need active support.

## SmiSelf — *force 100%-valid SMILES (post-processor)* ⚠️ no license

> Not a generator — a **validity correction layer**. Parses an invalid SMILES to a graph, routes through **SELFIES** (robust by construction), and converts back to a guaranteed-valid SMILES. Bolts onto any SMILES-emitting LLM/model.

- **Repo:** https://github.com/wentao228/SmiSelf.
- **License:** ⚠️ **No license file (all rights reserved)** — despite the "compatible with all SMILES generators" framing. Contact authors before commercial/derivative use.
- **Paper:** *How to Make Large Language Models Generate 100% Valid Molecules?*, EMNLP 2025 Main (DOI 10.18653/v1/2025.emnlp-main.1350; arXiv:2509.23099). Peer-reviewed.
- **Run:** no weights — rule/grammar-based. `selfies = smiself.encoder(smiles); valid = smiself.decoder(selfies)`. Built on the `selfies` library; CPU, no GPU.
- **Use it when:** you have a SMILES-generating model that emits invalid strings and want a validity guarantee that preserves molecular characteristics. Useful utility — but resolve the licensing before depending on it.

## GVT — *Graph VQ-Transformer (fast graph generation)* ⚠️ no license, brand-new

> Two-stage: a **Graph VQ-VAE** compresses molecular **graphs** into discrete latent tokens, then an autoregressive Transformer models them. Claims competitive distribution metrics (FCD/KL) with up to ~2 orders-of-magnitude faster sampling than diffusion.

- **Repo:** https://github.com/zzccppp/GVT (created 2025-11; 2 commits; ~8 stars).
- **License:** ⚠️ **No license file (all rights reserved).** (An automated check falsely reported an "MIT badge" — there is none.)
- **Paper:** *Graph VQ-Transformer (GVT): Fast and Accurate Molecular Generation via High-Fidelity Discrete Latents*, arXiv:2512.02667 (2025). Preprint, no venue/DOI yet.
- **Weights:** README lists downloadable VQVAE + AR checkpoints (host/permanence unverified).
- **Run:** `uv sync; uv run src/train_vqvae.py …`; trains on ZINC250k / MOSES / GuacaMol. PyTorch + PyG, RDKit for eval. GPU for training. Outputs **graphs**; validity-focused, not synthesizability-constrained.
- **Maintenance:** ⚠️ bleeding-edge, single-team, 2 commits — unproven.
- **Use it when:** research interest in fast VQ-latent graph generation. Not reusable until a license appears.

## Choosing

- **Maintained, commercially licensable, broad design (de novo / linker / scaffold / lead-opt):** **GenMol** (NVIDIA Open Model License on weights). Add a synthesizability filter.
- **Small MIT autoregressive generator (SMILES or SMARTS):** **MolReactGen** (dormant but usable).
- **Make any SMILES generator output 100% valid:** **SmiSelf** (resolve license first).
- **Fast graph generation, research only:** **GVT** (no license yet).

If you actually need **synthesizable** molecules (with routes), use the constrained generators in [synthesizable-generation.md](synthesizable-generation.md) instead — these four optimize validity, not make-ability.
