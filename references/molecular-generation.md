# General Molecular Generation

These generators produce valid molecules through de novo generation,
scaffold-based or linker-based generation, or SMILES correction. They do not
enforce synthesizability. When makeability matters, follow generation with a
retrosynthesis check or a synthetic-accessibility score from
[synthesizability-scoring.md](synthesizability-scoring.md).

## GenMol — *drug-discovery generalist (NVIDIA)*

> Masked **discrete diffusion** over **SAFE** fragment sequences with parallel bidirectional decoding; one model for de novo generation, fragment-constrained design (linkers, scaffold/motif decoration), goal-directed hit generation, and lead optimization.

- **Repository:** https://github.com/NVIDIA-BioNeMo/genmol (ships V1 and V2). The former `NVIDIA-Digital-Bio/genmol` URL redirects to this repository.
- **License:** **Apache-2.0** code. The weights use the **NVIDIA Open Model License**, which has terms separate from the source license; read the model license and model card before redistribution or deployment.
- **Paper:** *GenMol: A Drug Discovery Generalist with Discrete Diffusion*, ICML 2025 (arXiv:2501.06158), NVIDIA.
- **Weights:** Hugging Face `nvidia/NV-GenMol-89M-v2` (89M parameters) and NVIDIA-hosted checkpoints. The model card and weight terms are separate from the repository license.
- **Install and run:** clone the repository and run its environment setup; scripts cover de novo, fragment, goal-directed (`pmo`), and lead-optimization workflows. RDKit, PyTorch, and Transformers are required.
- **Representation:** **SAFE** (fragment-based → biased toward assemblable chemistries) but reports **validity, not enforced synthesizability**.
- **Maintenance:** The repository README dates GenMol V2 to **2025-10-15**. The repository was updated on 2026-08-24.
- **Use it when:** you need one model for de novo, scaffold, linker, or lead-optimization experiments. Add an SA or retrosynthesis filter when makeability matters.

## MolReactGen — *small autoregressive SMILES/SMARTS generator (MIT)*

> GPT-2-style decoder that generates either **molecules (SMILES)** or **reaction templates (SMARTS)** — two separate trained checkpoints.

- **Repository:** https://github.com/hogru/MolReactGen.
- **License:** **MIT** (code); HF weights inherit project terms. Public GuacaMol / USPTO-50K data.
- **Paper:** No peer-reviewed paper is listed; the project is documented in a Master's thesis from January 2024.
- **Weights:** HF `hogru/MolReactGen-GuacaMol-Molecules`, `hogru/MolReactGen-USPTO50K-Reaction-Templates`.
- **Install and run:** `git clone --recurse-submodules …; pip install -e .`; `prepare_data.py`, `train.py`, `generate.py smiles|smarts …`. Also usable via HF `text-generation` pipeline.
- **Dependencies and hardware:** RDKit, PyTorch ≥2.1, transformers ≥4.35, Python ≥3.9. GPU for training.
- **Maintenance:** The last repository push was in June 2024; release v1.0.0 is listed.
- **Use it when:** you need a small autoregressive molecule or SMARTS-template generator for experiments that do not depend on recent maintenance.

## SmiSelf — *force 100%-valid SMILES (post-processor)* ⚠️ no license

> A validity-correction layer rather than a generator. It parses an invalid
> SMILES string into a graph, converts the graph through SELFIES, and returns a
> valid SMILES string. It can post-process output from any model that emits
> SMILES.

- **Repository:** https://github.com/wentao228/SmiSelf.
- **License:** ⚠️ The repository has no `LICENSE` file. The repository's code and the paper's publication terms are separate.
- **Paper:** *How to Make Large Language Models Generate 100% Valid Molecules?*, EMNLP 2025 Main (DOI 10.18653/v1/2025.emnlp-main.1350; arXiv:2509.23099). Peer-reviewed.
- **Run:** no weights — rule/grammar-based. `selfies = smiself.encoder(smiles); valid = smiself.decoder(selfies)`. Built on the `selfies` library; CPU, no GPU.
- **Use it when:** you have a SMILES-generating model that emits invalid strings and need a validity-correction layer. Resolve the repository's code terms before making it a dependency.

## GVT — *Graph VQ-Transformer (fast graph generation)* ⚠️ no license file; 2025 preprint

> Two-stage: a **Graph VQ-VAE** compresses molecular **graphs** into discrete latent tokens, then an autoregressive Transformer models them. Claims competitive distribution metrics (FCD/KL) with up to ~2 orders-of-magnitude faster sampling than diffusion.

- **Repository:** https://github.com/zzccppp/GVT (created November 2025; two commits).
- **License:** ⚠️ The README displays an MIT badge, but no `LICENSE` file is present and the repository API reports no license.
- **Paper:** *Graph VQ-Transformer (GVT): Fast and Accurate Molecular Generation via High-Fidelity Discrete Latents*, arXiv:2512.02667 (2025). Preprint, no venue/DOI yet.
- **Weights:** README lists downloadable VQVAE + AR checkpoints (host/permanence unverified).
- **Run:** `uv sync; uv run src/train_vqvae.py …`; trains on ZINC250k / MOSES / GuacaMol. PyTorch + PyG, RDKit for eval. GPU for training. Outputs **graphs**; validity-focused, not synthesizability-constrained.
- **Maintenance:** The repository has two commits; no independent evaluation is listed.
- **Use it when:** you are studying fast VQ-latent graph generation; the repository's code license remains unstated.

## Choosing

| Need | Start with | Limit |
|---|---|---|
| De novo, linker, scaffold, or lead optimization | **GenMol** | Add a synthesizability filter; weight terms differ from code terms |
| Small autoregressive SMILES or SMARTS model | **MolReactGen** | Dormant repository |
| SMILES validity correction | **SmiSelf** | The repository has no `LICENSE` file |
| Graph generation | **GVT** | The repository has no `LICENSE` file |

For **synthesizable** molecules with routes, use the constrained generators in [synthesizable-generation.md](synthesizable-generation.md). GenMol, MolReactGen, SmiSelf, and GVT focus on general generation or SMILES validity.
