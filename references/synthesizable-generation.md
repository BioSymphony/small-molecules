# Synthesizable Generation and Analog Projection

These tools generate molecules with a synthetic route or project an input
molecule into synthesizable space. A projection returns a nearby makeable
analog and a proposed route. In contrast,
[retrosynthesis-planning.md](retrosynthesis-planning.md) plans a route for a
fixed target molecule.

Most tools here generate from building blocks and reaction templates, returning
a construction route under explicit rules and stock assumptions. SynCraft-Core
instead proposes structural edits and needs a separate planner to assess the
resulting analogue. S3-GFN applies soft synthesis constraints during SMILES
post-training.

After projection changes a molecule, repeat its pose and property calculations
before comparing it with the input. Record both structures so each score is
associated with the molecule that produced it. Check the proposed route against
the selected stock using [route validation](retrosynthesis-planning.md#validate-routes).

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

## SyntheFluor-RL

SyntheFluor-RL extends [SyntheMol](https://github.com/swansonk14/SyntheMol/tree/60302339148339355fc3e568ce200ed06207f99c)
with fluorescence objectives and an expanded reaction space. The
[January 2026 paper](https://arxiv.org/abs/2601.07145) describes candidate
fluorophores generated with construction provenance. Checked on 2026-11-15 (UTC).

- **Inputs and outputs:** allowed building blocks, reaction templates and
  optical rewards → candidate SMILES with their construction steps. The
  expanded collection has 70 reactions.
- **Prediction contract:** the [fluorescence guide](https://github.com/swansonk14/SyntheMol/blob/60302339148339355fc3e568ce200ed06207f99c/docs/rl/fluorescence.md)
  uses Chemprop 1.6.1 graph/MLP models with molecular features and four solvent
  descriptors. Absorption and emission are regressions; PLQY is a classifier
  for **PLQY >0.5**. Its output is a class probability rather than a numerical
  quantum-yield estimate.
- **Assets and terms:** MIT source; [Zenodo 18203970](https://zenodo.org/records/18203970)
  provides property models, processed data and generation inputs under
  CC BY 4.0. Check vendor building-block rights separately. Restore the matching
  feature files, solvent descriptors and model ensemble before scoring.

## RxnFlow 2.1.1

[RxnFlow](https://github.com/SeonghwanSeo/RxnFlow/tree/8f7c9975a4f8f12e79c9753428a4c0d71de3563a)
trains a GFlowNet over a prepared building-block library, reaction definitions
and a user-defined reward. Sampling returns molecules and construction routes.
MIT source; stock and scoring-model terms are separate. Checked on 2026-11-15 (UTC).

- **Setup:** Python ≥3.10, PyTorch and RDKit. `scripts/prepare.py` builds the
  synthesis environment; examples train rewards or external conditioning;
  `scripts/sample.py` consumes a trained checkpoint. The supplied example stock
  contains 5,000 ZINC blocks. Default `explore` rules include 26 bimolecular
  reactions, four unimolecular transformations and compatibility constraints.
- **Breaking change:** the [November 11 v2.1.1 release](https://github.com/SeonghwanSeo/RxnFlow/releases/tag/v2.1.1)
  changes graph features and model weights. Checkpoints from v2.1.0 and earlier
  cannot load; train a new model. Prepared v2.0/v2.1 environments remain
  supported, except those with unsupported bond types need rebuilding.
- **Selection:** earlier RxnFlow checkpoints and results refer to their own
  model version. The v2.1.1 README documents training before sampling and
  supplies no replacement pretrained policy link.

## S3-GFN

[S3-GFN](https://github.com/hyeonahkimm/s3gfn/tree/43aa7b310e9e03ef71ea0bd0cce501a48b6e2d52)
post-trains a SMILES generator with a soft synthesis constraint and separate
accepted/rejected replay buffers. It produces candidate SMILES; synthesis
acceptance depends on the configured evaluator. The source snapshot is dated
June 2, 2026. Checked on 2026-11-15 (UTC).

- **Setup:** the tested environment uses Python 3.10 and PyTorch 2.5.1/CUDA 12.1.
  `python -m s3gfn.train` accepts `seh` or `vina:<receptor>` objectives.
  `--use_retrosynthesis` requires a prepared reaction/stock environment;
  otherwise acceptance uses an SA threshold, default 4.0. Docking additionally
  needs Uni-Dock and prepared receptor files.
- **Assets and terms:** [MIT source](https://github.com/hyeonahkimm/s3gfn/blob/43aa7b310e9e03ef71ea0bd0cce501a48b6e2d52/LICENSE)
  initializes from the [Apache-2.0-tagged GP-MoLFormer-Uniq](https://huggingface.co/ibm-research/GP-MoLFormer-Uniq).
  The repository supplies training code without a trained S3-GFN checkpoint
  download. Its [data guide](https://github.com/hyeonahkimm/s3gfn/blob/43aa7b310e9e03ef71ea0bd0cce501a48b6e2d52/data/README.md)
  documents ZINCFrag inputs and separate Enamine catalog access. Preserve
  inherited-code and data terms.
- **Use:** compare soft synthesis constraints with unconstrained molecular
  optimization. Record the stock, route-check limits or SA threshold; generated
  SMILES alone provide no construction route.

## SynCraft-Core

[SynCraft-Core](https://github.com/catalystforyou/SynCraft-Core/tree/557703e110b26a354afed2955ded5217837f6692)
uses an external LLM to propose explicit atom and bond edits for an input
molecule. RDKit applies the edit JSON; a separate planner evaluates the edited
analogue. MIT source, checked on 2026-11-15 (UTC).

- **Inputs and outputs:** molecule SMILES and retrieved example pairs → edit
  operations and revised molecular structures. Interaction-aware mode adds
  receptor/ligand information through Vina and PLIP.
- **Setup:** Python ≥3.10, RDKit and OpenBabel; configure an external model and
  the planner/stock separately. The repository publishes no bespoke LLM weights.
  Backend service, model and planner assets retain their own terms.
- **Use:** retain an explicit structural edit record when improving an
  analogue's predicted makeability. Check scaffold retention, stereochemistry
  and the revised route. Editing changes the target identity; evaluate the
  resulting analogue's properties again.

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

## LDDM — *Pocket-Conditioned Reaction-Space Generation*

> Three-dimensional pocket generation over supplied building blocks and
> reaction templates, with a proposed construction trace for each accepted
> search path.

- **Repository:** https://github.com/LPDI-EPFL/lddm · **Paper:** bioRxiv [10.64898/2026.09.15.751537](https://doi.org/10.64898/2026.09.15.751537).
- **License:** MIT code with split checkpoint terms. `lddm_CDBB.ckpt` is MIT; the paper checkpoint, `lddm.ckpt`, is CC BY-NC 4.0 because it includes BindingNet training data.
- **Inputs and outputs:** Prepared pocket structure, reference ligand, building blocks, and two-reactant, one-product templates produce three-dimensional SDF candidates and proposed construction traces.
- **Public example:** 44,944 SynSpace-derived building blocks and three reactions. This is much smaller than the separately licensed Enamine REAL setup used in the paper.
- **Status:** Early research release. The locked environment is Linux and CUDA specific, and the supplied synthesis-space workflow is designed for GPU execution.
- **Use it when:** pocket geometry must guide a reaction-space search. Confirm reaction applicability, conditions, selectivity, stock availability, and route feasibility independently. See the [focused LDDM review](lddm.md).

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

- **Train over custom reactions and rewards:** **RxnFlow 2.1.1**; earlier
  checkpoints require retraining.
- **Reaction-constrained fluorophore design:** **SyntheFluor-RL**.
- **Explicit structural edits with an external model:** **SynCraft-Core**;
  evaluate the edited analogue with a separate planner.

- **Project a molecule into synthesizable space:** **PrexSyn** (repository and Hugging Face data record labeled MIT; Enamine-derived data is separate).
- **Makeable analogs, no GPU/training, research:** **SynTwins**.
- **3D structures + route:** **SynCoGen**.
- **Pathway-level generation/editing:** **ReaSyn** (NVIDIA weights license).
- **Target-conditioned make-on-demand hit generation:** **SyntheMol** (MIT code; Zenodo artifact terms are separate).
- **Search billions-scale libraries:** **APEX** (repository and Zenodo records require separate term review).
- **LLM-based route generation:** **SynLlama** (UC Berkeley Regents non-commercial repository license).
- **Pocket-conditioned three-dimensional candidate and reaction trace:** **LDDM** (MIT checkpoint available; paper checkpoint is non-commercial).
- **Validity-focused rather than synthesis-aware:** See [molecular-generation.md](molecular-generation.md) for GenMol, MolReactGen, and related tools.
