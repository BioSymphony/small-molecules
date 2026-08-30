# Synthesizable Generation and Analog Projection

These tools generate molecules with a synthetic route or project an input
molecule into synthesizable space. A projection returns a nearby makeable
analog and a proposed route. In contrast,
[retrosynthesis-planning.md](retrosynthesis-planning.md) plans a route for a
fixed target molecule.

These models generate from building blocks and reaction templates. Each output
therefore includes a forward synthesis under the model's reaction rules and
stock assumptions.

---

## PrexSyn — *projection over synthesizable space*

> Decoder-only transformer that autoregressively generates postfix synthesis
> notation from molecular descriptors, including reactions and purchasable
> building blocks. It maps molecules to synthesis pathways and accepts
> programmable generation settings.

- **Repository:** https://github.com/luost26/prexsyn · **Docs:** https://prexsyn.readthedocs.io
- **Author:** Shitong Luo, Connor W. Coley (MIT / Coley group)
- **License:** The repository and the Hugging Face `luost26/prexsyn-data` record are labeled **MIT**. The dataset includes an Enamine-derived chemical space, so the catalog's terms are a separate consideration. See [licensing-and-data.md](licensing-and-data.md).
- **Paper:** *Efficient and Programmable Exploration of Synthesizable Chemical Space*, arXiv:2512.00384 (2025). Reports 94.06% reconstruction on the Enamine test set (Tanimoto 0.9859).
- **Weights:** Hugging Face dataset `luost26/prexsyn-data` — checkpoints plus the precomputed `enamine2310_rxn115` chemical space. The v1 checkpoint and chemical-space assets are published in that record.
- **Inputs and outputs:** A SMILES string or molecular fingerprint, such as ECFP4, produces a synthesis pathway in postfix notation, rendered synthesis-tree images, and a structured tree dictionary.
- **Install:**
  ```bash
  python -m pip install prexsyn
  # example projection (uv-based; data/checkpoints auto-download)
  uv run python scripts/examples/projection.py \
    --smiles "COc1ccc(-c2ccnc(Nc3ccccc3)n2)cc1" --draw-output-dir ./draw
  ```
- **Dependencies and hardware:** PyTorch (configurable CUDA), RDKit, and the C++ *PrexSyn Engine* for high-throughput data pipelines. GPU support is available.
- **Release and maintenance:** [**v1.1.3**](https://github.com/luost26/prexsyn/releases/tag/v1.1.3) was released on **2026-08-08**; the repository also received commits on 2026-08-30. The v1 README says property-based queries are not supported in v1; that feature belongs to the v0 branch.
- **Use it when:** you need descriptor-conditioned projection into a reaction-and-building-block space or programmable pathway generation.

---

## SynFormer — *published (PNAS), stable, two variants*

> Generative framework that combines molecule projection with synthetic
> pathways. **SynFormer-ED** performs projection and reconstruction;
> **SynFormer-D** performs property-goal generation and fine-tuning.

- **Repository:** https://github.com/wenhao-gao/synformer. The project is also published on PyPI as `synformer`; it is distinct from `devalab/SynFormer`.
- **Author:** Wenhao Gao (MIT / Coley group)
- **License:** **Apache-2.0** code. The project README says its preprocessed data is for research purposes and that commercial use requires appropriate permissions. The data and code terms are separate.
- **Paper:** *Generative AI for Navigating Synthesizable Chemical Space*, **PNAS 2025, 122(41), e2415665122**, DOI 10.1073/pnas.2415665122 (preprint arXiv:2410.03494). Gao, Luo, Coley.
- **Weights:** HuggingFace `whgao/synformer` — `sf_ed_default.ckpt` plus required `fpindex.pkl` and `matrix.pkl` into `data/trained_weights/`.
- **Data:** 115 reaction templates + 223,244 commercially available building blocks derived from **Enamine US Stock** (gated — request from Enamine).
- **Inputs and outputs:** CSV of SMILES → CSV of molecules projected into synthesizable space, with pathways.
- **Install:**
  ```bash
  conda env create -f env.yml -n synformer && conda activate synformer
  pip install --no-deps -e .            # or: pip install synformer
  python sample.py --model-path data/trained_weights/sf_ed_default.ckpt \
    --input data/example.csv --output results/example.csv
  ```
- **Dependencies and hardware:** Python ≥3.10, PyTorch, RDKit. GPU optional — CPU ~30s–2min/molecule, RTX 4090 seconds–30s/molecule.
- **Maintenance:** The last repository push was 2025-01-11; no 2026 release is listed.
- **Use it when:** you need a citable published method or specifically need the **SynFormer-D** property-optimization variant.

---

## ChemProjector — *archived; historical predecessor*

> Transformer that translates a molecular graph into a postfix synthetic
> pathway. It returns structurally similar synthesizable analogs when the input
> molecule is not makeable under the model's reaction rules and stock set.

- **Repository:** https://github.com/luost26/ChemProjector — GitHub marks the repository **archived / read-only on 2026-02-24**.
- **License:** **MIT.**
- **Paper:** *Projecting Molecules into Synthesizable Chemical Spaces*, **ICML 2024** (PMLR v235), arXiv:2406.04628. Luo, Gao, Wu, Peng, Coley, Ma.
- **Weights:** Google Drive (`original_default.ckpt`, `original_split.ckpt`) → `data/trained_weights/`.
- **Data:** Enamine US Stock is required; the preprocessed blocks and templates are distributed separately from the public repository, under the source catalog's terms.
- **Install:** `git clone --recurse-submodules …; conda env create -f env.yml -n chemprojector; pip install -e .`
- **Use it when:** you need to reproduce the ICML 2024 result or inspect the predecessor architecture.

---

## ReaSyn — *pathway-level refinement and analog generation*

> Encoder-decoder transformer that predicts a molecule's synthesis pathway and
> generates synthesizable analogs by refining whole pathways. It uses bottom-up
> decoding, top-down decoding, and insertion, deletion, and substitution edits
> through a discrete flow model. The output uses Chain-of-Reaction notation.

- **Repository:** https://github.com/NVIDIA-BioNeMo/ReaSyn; the public v2 release is in the `reasyn_v2` branch.
- **Org:** NVIDIA. Lee, Kreis, Veccham, Liu, Reidenbach, Paliwal, Nie, Vahdat.
- **License:** ⚠️ **Split** — code is **Apache-2.0**; model weights are under the **NVIDIA Open Model License**.
- **Paper:** *Exploring Synthesizable Chemical Space with Iterative Pathway Refinements* (also known as *Rethinking Molecule Synthesizability with Chain-of-Reaction*), arXiv:2509.16084 (2025/26).
- **Weights:** NGC + Hugging Face `nvidia/NV-ReaSyn-AR-166M-v2` and `nvidia/NV-ReaSyn-EB-174M-v2` (~166M/174M parameters). The model card dates ReaSyn v2 to 2026-01-08.
- **Data:** reuses **SynFormer's 115 reaction templates** (`data/rxn_templates/comprehensive.txt`). Building blocks are **Enamine US Stock**, available upon request from Enamine → `data/building_blocks/building_blocks.txt`. ZINC250k blocks bundled for the reconstruction benchmark.
- **Inputs and outputs:** SMILES → synthesizable analogs with full CoR pathways; also supports goal-directed molecular optimization.
- **Install:** `conda env create -f env.yml && conda activate reasyn`
- **Dependencies and hardware:** PyTorch (`torchrun`), RDKit, and pinned scikit-learn. Training and larger inference runs require GPU resources.
- **Maintenance:** The public repository tracks the v2 branch; its most recent GitHub update was dated 2026-07-18.
- **Use it when:** you need pathway-level generation and editing, and you have reviewed the NVIDIA Open Model License for the weights.

---

## SynCoGen — *3D-aware co-generation (blocks + templates + coordinates)*

> Jointly models building blocks, reaction templates, and atomic 3D coordinates
> with discrete graph diffusion and flow matching. It returns a 3D structure
> and synthetic route together and accepts pharmacophore or linker conditioning
> from a reference ligand.

- **Repository:** https://github.com/andreirekesh/SynCoGen (canonical — lead author's repository).
- **Authors:** Rekesh, Cretu, Shevchuk, Somnath, Liò, Batey, Tyers, Koziarski, Liu (U. Toronto / SickKids / Vector / Cambridge / ETH / Mila).
- **License:** ⚠️ **Split** — the GitHub repository has no `LICENSE` file, while the released Hugging Face weights and SynSpace dataset records are labeled **MIT**. Keep code and artifact terms separate.
- **Paper:** *SynCoGen: Synthesizable 3D Molecule Generation via Joint Reaction and Coordinate Modeling*, arXiv:2507.11818 (2025), ICML 2025.
- **Weights and data:** HF `DreiSSB/SynCoGen-SynSpace-Unconditional`, `DreiSSB/SynCoGen-SynSpace-Conditional`; dataset **SynSpace** `DreiSSB/SynSpace` (~622,766 block/reaction graphs).
- **Data:** the README describes a vocabulary of **93 building blocks and 19 reaction templates** adapted from RGFN (Koziarski et al., 2024). The released records identify SynSpace as the public dataset; catalog provenance and terms remain separate.
- **Inputs and outputs:** molecular graphs (+ optional reference-ligand **SDF**) → generated molecules as **SDF with 3D coordinates** + explicit reaction route.
- **Install:** `conda env create -f requirements.yaml && conda activate syncogen` (needs **GFN2-xTB** for conformers, CUDA 12.4).
- **Maintenance:** The last recorded repository push was on 2026-06-03.
- **Use it when:** you need **3D structures** (docking, shape/pharmacophore work, linker design) together with an explicit synthetic route.

---

## SynTwins — *training-free analog generation by search*

> A **search algorithm** (no neural generator) for synthetically accessible analogs, in three steps: (1) multi-step retrosynthesis via retro-templates, (2) kNN search over **ECFP** fingerprints for similar building blocks, (3) virtual forward synthesis. "Twins" = close, makeable analogs of a query.

- **Repository:** https://github.com/snu-micc/SynTwins (MICC group, Seoul National University — Yousung Jung lab).
- **License:** ⚠️ The repository has no `LICENSE` file. The paper is published under **CC BY-NC 3.0**; that publication license and the repository's code status are separate.
- **Paper:** *SynTwins: a retrosynthesis-guided framework for synthesizable molecular analog generation*, **RSC Chemical Science 2026, 17(4):2255–2262**, DOI 10.1039/D5SC05225D (preprint arXiv:2507.02752). Chen, Nam, Aspuru-Guzik, Jung.
- **Weights:** none — nothing is trained.
- **Data:** bundles **150,560 building blocks from the Enamine Building Blocks Catalog (Global Stock)** directly in `data/`. The catalog terms are separate from the repository's code status.
- **Inputs and outputs:** target SMILES → set of synthesizable analogs. See `Demo.ipynb`.
- **Install:**
  ```bash
  conda create -c conda-forge -n rdenv python=3.6 -y && conda activate rdenv
  pip install PyTDC      # only needed for the MPO/optimization experiments
  ```
- **Dependencies and hardware:** Python ≥3.6, NumPy, RDKit, optional PyTDC. **CPU-only — no GPU**, since it's search, not a neural net.
- **Maintenance:** Minimal. The last recorded repository push was on 2025-04-11; treat it as a research artifact.
- **Use it when:** you need a dependency-light, GPU-free, training-free search baseline for synthesizable analogs.

---

## SynLlama — *LLM that emits synthesizable routes* ⚠️ UC non-commercial

> Fine-tuned Llama-3 that generates synthesizable molecules and analogs by producing full synthetic pathways (building blocks + reaction templates) — a constrained-retrosynthesis-style generator. UC Berkeley (Head-Gordon lab).

- **Repository:** https://github.com/THGLab/SynLlama.
- **License:** ⚠️ The repository `LICENSE` grants a **UC Berkeley Regents non-commercial** license, while the paper describes the project as MIT. Llama-3.1/3.2 Community Licenses apply to the base models; the Figshare weight records do not show a separate license label.
- **Paper:** ACS Central Science 2025, 11:2108 (DOI 10.1021/acscentsci.5c01285); arXiv:2503.12602.
- **Weights:** Figshare — `SynLlama-1B-2M` (recommended), `-1B-500k`, `-8B-500k`. Bases Llama-3.1-8B / 3.2-1B. ~230K Enamine blocks (train).
- **Inputs and outputs:** target SMILES → JSON route (SMARTS steps + building-block SMILES + intermediates). Baselines: SynNet, ChemProjector, SynFormer.
- **Use it when:** you are evaluating LLM-based synthesizable generation under the repository and base-model terms. Full card in [chemical-language-models.md](chemical-language-models.md).

---

## Make-on-demand / combinatorial-library generation

These design over **vendor combinatorial spaces** (Enamine REAL / WuXi GalaXi — tens of billions of make-on-demand compounds) rather than a learned latent space.

## SyntheMol — *generative design over make-on-demand space*

> Generates molecules by navigating a combinatorial make-on-demand space with a
> bioactivity predictor. It documents SyntheMol-MCTS and SyntheMol-RL; the
> repository default was SyntheMol-RL on 2026-08-30. The papers apply the
> system to antibiotic discovery.

- **Repository:** https://github.com/swansonk14/SyntheMol (SyntheMol-RL is in the same repository).
- **License:** **MIT** code. The Zenodo record for the paper's data and models does not expose a license field in its metadata; its files include vendor-derived catalog data and ChEMBL-derived data. Review the record and source-catalog terms separately.
- **Papers:** *Generative AI for designing and validating easily synthesizable and structurally novel antibiotics*, Nature Machine Intelligence 2024 (DOI 10.1038/s42256-024-00809-7); *SyntheMol-RL: A flexible framework for molecular generation using reinforcement learning*, Molecular Systems Biology 2026 (DOI 10.1038/s44320-026-00206-9).
- **Install and run:** `conda create -n synthemol python=3.11`; `pip install synthemol`. Uses **Chemprop** (D-MPNN) bioactivity models.
- **Data:** Enamine REAL Space (~137,656 blocks / 70 reactions / ~30.3B molecules) and WuXi GalaXi.
- **Inputs and outputs:** bioactivity training data + building blocks + reactions → generated SMILES with predicted activity + synthesis recipe.
- **Maintenance:** The repository's default is SyntheMol-RL. Its most recent
  GitHub release was v_2.0.0 (2025-05-12), and the repository received updates
  in 2026. RDKit, Chemprop, and PyTorch are required; training uses a GPU.
- **Use it when:** you need target-conditioned generation over the Enamine REAL or WuXi GalaXi combinatorial spaces and can review the separate code, data, and catalog terms.

## APEX — *search ultra-large libraries without enumeration*

> "Approximate-but-exhaustive" search: a neural surrogate with an inductive library encoder enumerates a full combinatorial library on one consumer GPU in under a minute, giving exact retrieval of approximate top-k over tens-of-billions-scale spaces — no exhaustive per-compound scoring.

- **Repository:** https://github.com/NumerionLabs/apex (needs the `apex_topk` extension).
- **License:** ⚠️ The repository has no `LICENSE` file. The combinatorial-library data and model weights are published in separate Zenodo records ([10.5281/zenodo.17455955](https://doi.org/10.5281/zenodo.17455955) and [10.5281/zenodo.17456522](https://doi.org/10.5281/zenodo.17456522)); those records do not expose a license field in their metadata.
- **Paper:** *APEX: Approximate-but-exhaustive search for ultra-large combinatorial synthesis libraries*, arXiv:2510.24380 (2025), Numerion Labs + NVIDIA.
- **Install and run:** install `apex_topk`, then `pip install .`. Reported: top-1M over a 10B-compound library in ~30 s on a single T4.
- **Inputs and outputs:** A combinatorial library of synthons, R-groups, and reactions in Parquet format, plus a scoring objective such as docking, produces a ranked set of candidates. A GPU is required.
- **Use it when:** you need approximate top-k search over ultra-large combinatorial libraries and have reviewed the repository and Zenodo terms.

---

## Quick pick (generation side)

- **Project a molecule into synthesizable space:** **PrexSyn** (repository and Hugging Face data record labeled MIT; Enamine-derived data is separate).
- **Makeable analogs, no GPU/training, research:** **SynTwins**.
- **3D structures + route:** **SynCoGen**.
- **Pathway-level generation/editing:** **ReaSyn** (NVIDIA weights license).
- **Target-conditioned make-on-demand hit generation:** **SyntheMol** (MIT code; Zenodo artifact terms are separate).
- **Search billions-scale libraries:** **APEX** (repository and Zenodo records require separate term review).
- **LLM-based route generation:** **SynLlama** (UC Berkeley Regents non-commercial repository license).
- **Validity-focused rather than synthesis-aware:** See [molecular-generation.md](molecular-generation.md) for GenMol, MolReactGen, and related tools.
