# Synthesizable Generation & Analog Projection

Tools that **produce molecules together with a synthetic route**, or that **project an arbitrary molecule into synthesizable space** (returning the nearest make-able analog plus how to make it). Contrast with [retrosynthesis-planning.md](retrosynthesis-planning.md), which plans a route for a target you already have.

The shared idea: instead of generating SMILES that may be unmakeable, these models generate over a space of **building blocks + reaction templates**, so every output carries a forward synthesis by construction.

---

## PrexSyn — *current pick for projection over synthesizable space*

> Decoder-only transformer that autoregressively generates a **postfix notation** of a synthesis (reactions + purchasable building blocks), conditioned on molecular descriptors. Fast molecule→pathway projection and programmable generation.

- **Repo:** https://github.com/luost26/prexsyn · **Docs:** https://prexsyn.readthedocs.io
- **Author:** Shitong Luo, Connor W. Coley (MIT / Coley group)
- **License:** **MIT** (code and weights). No research-only clause in the repo — but the bundled chemical space is Enamine-derived, so Enamine's catalog terms still govern commercial use of that data. See [licensing-and-data.md](licensing-and-data.md).
- **Paper:** *Efficient and Programmable Exploration of Synthesizable Chemical Space*, arXiv:2512.00384 (2025). Reports 94.06% reconstruction on the Enamine test set (Tanimoto 0.9859).
- **Weights:** HuggingFace dataset `luost26/prexsyn-data` — checkpoints + precomputed `enamine2310_rxn115` chemical space. **Auto-downloads on first run**; nothing to configure manually.
- **Inputs → outputs:** SMILES / fingerprint (e.g. ECFP4) → synthesis pathway (postfix notation), rendered synthesis-tree PNGs, structured tree dict.
- **Install:**
  ```bash
  pip install git+https://github.com/luost26/prexsyn.git
  # example projection (uv-based; data/checkpoints auto-download)
  uv run python scripts/examples/projection.py \
    --smiles "COc1ccc(-c2ccnc(Nc3ccccc3)n2)cc1" --draw-output-dir ./draw
  ```
- **Deps / hardware:** PyTorch (configurable CUDA), RDKit, the C++ *PrexSyn Engine* (on PyPI) for high-throughput data pipelines. GPU recommended; the model itself was trained on just 2 GPUs in ~2 days.
- **Maintenance:** Very active — last push 2026-06-08, latest tag v1.1.2, ~53 stars.
- **Use it when:** you want the most current, MIT-licensed, easy-to-install tool for projecting molecules into synthesizable space or for programmable exploration. This is the natural first thing to try in the Coley lineage.

---

## SynFormer — *published (PNAS), stable, two variants*

> Generative framework that always emits a viable synthetic pathway for every molecule. **SynFormer-ED** (encoder–decoder) does projection/reconstruction; **SynFormer-D** (decoder-only) does property-goal generation and fine-tuning.

- **Repo:** https://github.com/wenhao-gao/synformer — **use this one, not the unrelated `devalab/SynFormer`** (a name collision with a different retrosynthesis project). Also on PyPI as `synformer`.
- **Author:** Wenhao Gao (MIT / Coley group)
- **License:** **Apache-2.0** (code). ⚠️ **Data caveat (verbatim):** *"The preprocessed data is for research purposes only, and any commercial use requires appropriate permissions."* This is the most explicit research-only restriction among these tools.
- **Paper:** *Generative AI for Navigating Synthesizable Chemical Space*, **PNAS 2025, 122(41), e2415665122**, DOI 10.1073/pnas.2415665122 (preprint arXiv:2410.03494). Gao, Luo, Coley. The most cited / peer-reviewed of the lineage.
- **Weights:** HuggingFace `whgao/synformer` — `sf_ed_default.ckpt` plus required `fpindex.pkl` and `matrix.pkl` into `data/trained_weights/`.
- **Data:** 115 reaction templates + 223,244 commercially available building blocks derived from **Enamine US Stock** (gated — request from Enamine).
- **Inputs → outputs:** CSV of SMILES → CSV of molecules projected into synthesizable space, with pathways.
- **Install:**
  ```bash
  conda env create -f env.yml -n synformer && conda activate synformer
  pip install --no-deps -e .            # or: pip install synformer
  python sample.py --model-path data/trained_weights/sf_ed_default.ckpt \
    --input data/example.csv --output results/example.csv
  ```
- **Deps / hardware:** Python ≥3.10, PyTorch, RDKit. GPU optional — CPU ~30s–2min/molecule, RTX 4090 seconds–30s/molecule.
- **Maintenance:** ⚠️ Quiet — last push 2025-01-11; the author describes the lineage as deprecated in favor of PrexSyn. Still fully usable and the only **peer-reviewed** option here.
- **Use it when:** you want a citable, published method, or specifically need the **SynFormer-D** property-optimization variant. For pure projection, PrexSyn is newer and MIT.

---

## ChemProjector — *archived; historical predecessor*

> Transformer that translates an arbitrary molecular graph into a postfix synthetic pathway, yielding structurally similar **synthesizable analogs** for molecules that may not be makeable themselves.

- **Repo:** https://github.com/luost26/ChemProjector — ⚠️ **Archived / read-only since 2026-02-24.** The authors state ChemProjector and its derivatives (e.g. SynFormer) are deprecated; recommended replacement is **PrexSyn**.
- **License:** **MIT.**
- **Paper:** *Projecting Molecules into Synthesizable Chemical Spaces*, **ICML 2024** (PMLR v235), arXiv:2406.04628. Luo, Gao, Wu, Peng, Coley, Ma.
- **Weights:** Google Drive (`original_default.ckpt`, `original_split.ckpt`) → `data/trained_weights/`.
- **Data:** Enamine US Stock required; preprocessed blocks/templates are **password-protected** (you must already hold the Enamine catalog to unarchive).
- **Install:** `git clone --recurse-submodules …; conda env create -f env.yml -n chemprojector; pip install -e .`
- **Use it when:** essentially only if you need to reproduce the ICML 2024 result. **Otherwise use PrexSyn.** Listed here for lineage completeness.

---

## ReaSyn — *pathway-level refinement and analog generation*

> Encoder–decoder transformer that predicts a molecule's full synthesis pathway and obtains synthesizable analogs by **iteratively refining whole pathways** — bottom-up decoding, top-down decoding, and holistic editing (insert/delete/substitute) via a discrete flow model. Uses a **Chain-of-Reaction (CoR)** notation.

- **Repo:** https://github.com/NVIDIA-BioNeMo/ReaSyn — the older `NVIDIA-Digital-Bio/ReaSyn` URL 301-redirects here (org was renamed). Cite the BioNeMo URL.
- **Org:** NVIDIA. Lee, Kreis, Veccham, Liu, Reidenbach, Paliwal, Nie, Vahdat.
- **License:** ⚠️ **Split** — code is **Apache-2.0**, but **model weights are under the NVIDIA Open Model License** (not Apache). Verbatim: *"The source code is made available under Apache-2.0. The model weights are made available under the NVIDIA Open Model License."*
- **Paper:** *Exploring Synthesizable Chemical Space with Iterative Pathway Refinements* (a.k.a. *Rethinking Molecule Synthesizability with Chain-of-Reaction*), arXiv:2509.16084 (2025/26).
- **Weights:** NGC + HuggingFace `nvidia/NV-ReaSyn-AR-166M-v2` and `nvidia/NV-ReaSyn-EB-174M-v2` (~166M/174M params) → `data/trained_model/`.
- **Data:** reuses **SynFormer's 115 reaction templates** (`data/rxn_templates/comprehensive.txt`). Building blocks are **Enamine US Stock**, available upon request from Enamine → `data/building_blocks/building_blocks.txt`. ZINC250k blocks bundled for the reconstruction benchmark.
- **Inputs → outputs:** SMILES → synthesizable analogs with full CoR pathways; also supports goal-directed molecular optimization.
- **Install:** `conda env create -f env.yml && conda activate reasyn`
- **Deps / hardware:** PyTorch (`torchrun`), RDKit, scikit-learn (pinned). **Heavy GPU for training** (2 nodes × 8× A100, ~5–6 days). Multi-GPU recommended for inference. Repo is **not accepting external contributions**.
- **Maintenance:** Active — last push 2026-01-11, ~100 stars.
- **Use it when:** you care about **pathway-level** generation and editing (refining or projecting whole routes, not just endpoint molecules), and the NVIDIA Open Model License on weights is acceptable for your use.

---

## SynCoGen — *3D-aware co-generation (blocks + templates + coordinates)*

> Jointly models building blocks + reaction templates (absorbing-state masked **discrete graph diffusion**) and atomic **3D coordinates** (**flow matching**), sampling from the joint distribution to return a 3D structure *and* its synthetic route together. Supports pharmacophore / linker conditioning from a reference ligand.

- **Repo:** https://github.com/andreirekesh/SynCoGen (canonical — lead author's repo).
- **Authors:** Rekesh, Cretu, Shevchuk, Somnath, Liò, Batey, Tyers, Koziarski, Liu (U. Toronto / SickKids / Vector / Cambridge / ETH / Mila).
- **License:** ⚠️ **Split** — the **GitHub code has NO LICENSE file (all rights reserved by default)**, but the released **HuggingFace weights + dataset are MIT-tagged**. Treat the *code* as unlicensed until the authors clarify; the *artifacts* are MIT.
- **Paper:** *SynCoGen: Synthesizable 3D Molecule Generation via Joint Reaction and Coordinate Modeling*, arXiv:2507.11818 (2025), ICML 2025.
- **Weights / data:** HF `DreiSSB/SynCoGen-SynSpace-Unconditional`, `DreiSSB/SynCoGen-SynSpace-Conditional`; dataset **SynSpace** `DreiSSB/SynSpace` (~622,766 block/reaction graphs).
- **Data:** vocabulary of **93 building blocks + 19 reaction templates**, adapted from RGFN (Koziarski et al., 2024) — Enamine-sourced but **bundled and small** (no Enamine catalog request needed). Lightest Enamine dependency here.
- **Inputs → outputs:** molecular graphs (+ optional reference-ligand **SDF**) → generated molecules as **SDF with 3D coordinates** + explicit reaction route.
- **Install:** `conda env create -f requirements.yaml && conda activate syncogen` (needs **GFN2-xTB** for conformers, CUDA 12.4).
- **Maintenance:** Active — last push 2026-06-03, ~30 stars.
- **Use it when:** you need **3D structures** (docking, shape/pharmacophore work, linker design) *and* synthesizability in one shot. The only 3D-native generator in this set.

---

## SynTwins — *training-free analog generation by search*

> A **search algorithm** (no neural generator) for synthetically accessible analogs, in three steps: (1) multi-step retrosynthesis via retro-templates, (2) kNN search over **ECFP** fingerprints for similar building blocks, (3) virtual forward synthesis. "Twins" = close, makeable analogs of a query.

- **Repo:** https://github.com/snu-micc/SynTwins (MICC group, Seoul National University — Yousung Jung lab).
- **License:** ⚠️ **No LICENSE file — all rights reserved by default.** The *paper* is CC BY-NC 3.0 (non-commercial), but that does not license the code. Not safe to reuse commercially without contacting the authors.
- **Paper:** *SynTwins: a retrosynthesis-guided framework for synthesizable molecular analog generation*, **RSC Chemical Science 2026, 17(4):2255–2262**, DOI 10.1039/D5SC05225D (preprint arXiv:2507.02752). Chen, Nam, Aspuru-Guzik, Jung.
- **Weights:** none — nothing is trained.
- **Data:** bundles **150,560 building blocks from the Enamine Building Blocks Catalog (Global Stock)** directly in `data/`. That redistribution sits under Enamine's catalog terms — flag given the absent code license.
- **Inputs → outputs:** target SMILES → set of synthesizable analogs. See `Demo.ipynb`.
- **Install:**
  ```bash
  conda create -c conda-forge -n rdenv python=3.6 -y && conda activate rdenv
  pip install PyTDC      # only needed for the MPO/optimization experiments
  ```
- **Deps / hardware:** Python ≥3.6, NumPy, RDKit, optional PyTDC. **CPU-only — no GPU**, since it's search, not a neural net.
- **Maintenance:** ⚠️ Minimal — last push 2025-04-11, ~9 stars. Research artifact.
- **Use it when:** you want a **dependency-light, GPU-free, training-free** way to generate makeable analogs and you're in a research (non-commercial) context. Good baseline / sanity check against the learned generators above.

---

## SynLlama — *LLM that emits synthesizable routes* ⚠️ UC non-commercial

> Fine-tuned Llama-3 that generates synthesizable molecules and analogs by producing full synthetic pathways (building blocks + reaction templates) — a constrained-retrosynthesis-style generator. UC Berkeley (Head-Gordon lab).

- **Repo:** https://github.com/THGLab/SynLlama.
- **License:** ⚠️ **UC Berkeley Regents NON-COMMERCIAL** license (GitHub: NOASSERTION). **The paper's "MIT" claim is incorrect — the LICENSE file is binding.** Base adds Llama-3.1/3.2 Community Licenses; weights on Figshare (untagged).
- **Paper:** ACS Central Science 2025, 11:2108 (DOI 10.1021/acscentsci.5c01285); arXiv:2503.12602.
- **Weights:** Figshare — `SynLlama-1B-2M` (recommended), `-1B-500k`, `-8B-500k`. Bases Llama-3.1-8B / 3.2-1B. ~230K Enamine blocks (train).
- **I/O:** target SMILES → JSON route (SMARTS steps + building-block SMILES + intermediates). Baselines: SynNet, ChemProjector, SynFormer.
- **Use it when:** **research-only** LLM synthesizable generation. For commercial work use PrexSyn instead. Full card in [chemical-language-models.md](chemical-language-models.md).

---

## Make-on-demand / combinatorial-library generation

These design over **vendor combinatorial spaces** (Enamine REAL / WuXi GalaXi — tens of billions of make-on-demand compounds) rather than a learned latent space.

## SyntheMol — *generative design over make-on-demand space (MIT + CC BY)*

> Generates readily synthesizable molecules by navigating a combinatorial make-on-demand space, guided by a bioactivity predictor. Two variants: SyntheMol-MCTS (original) and **SyntheMol-RL** (current default). Built for antibiotic discovery.

- **Repo:** https://github.com/swansonk14/SyntheMol (SyntheMol-RL is in the same repo).
- **License:** **MIT** code; **weights + data CC BY 4.0** (Zenodo DOI 10.5281/zenodo.10257839). Fully permissive — **commercial-OK with attribution** (the cleanest license of the make-on-demand generators). Caveat: the Enamine REAL / WuXi GalaXi *catalogs* themselves are vendor-governed.
- **Paper:** *Generative AI for designing and validating easily synthesizable and structurally novel antibiotics*, Nature Machine Intelligence 2024 (DOI 10.1038/s42256-024-00809-7).
- **Install / run:** `conda create -n synthemol python=3.11`; `pip install synthemol`. Uses **Chemprop** (D-MPNN) bioactivity models.
- **Data:** Enamine REAL Space (~137,656 blocks / 70 reactions / ~30.3B molecules) and WuXi GalaXi.
- **I/O:** bioactivity training data + building blocks + reactions → generated SMILES with predicted activity + synthesis recipe.
- **Maintenance:** active (~220 stars; RL release 2025-05). RDKit, Chemprop, PyTorch; GPU for training.
- **Use it when:** target-conditioned generation over Enamine REAL with a permissive license — strong default for make-on-demand hit generation.

## APEX — *search ultra-large libraries without enumeration* ⚠️ non-commercial code

> "Approximate-but-exhaustive" search: a neural surrogate with an inductive library encoder enumerates a full combinatorial library on one consumer GPU in under a minute, giving exact retrieval of approximate top-k over tens-of-billions-scale spaces — no exhaustive per-compound scoring.

- **Repo:** https://github.com/NumerionLabs/apex (needs the `apex_topk` extension).
- **License:** ⚠️ **code CC BY-NC 4.0 (NON-COMMERCIAL)** — unusual for software, but it blocks commercial use. Datasets are CC BY 4.0 (Zenodo 10.5281/zenodo.17455955); weights on Zenodo 17456522 (license unconfirmed).
- **Paper:** *APEX: Approximate-but-exhaustive search for ultra-large combinatorial synthesis libraries*, arXiv:2510.24380 (2025), Numerion Labs + NVIDIA.
- **Install / run:** install `apex_topk`, then `pip install .`. Reported: top-1M over a 10B-compound library in ~30 s on a single T4.
- **I/O:** combinatorial library (synthons/R-groups/reactions as Parquet) + scoring objective (e.g., docking) → ranked top-k. GPU required.
- **Use it when:** screening Enamine-REAL-scale spaces in **research** (non-commercial). For commercial use you'd need a license from Numerion Labs.

---

## Quick pick (generation side)

- **Project a molecule into synthesizable space, commercial-friendly:** **PrexSyn** (MIT).
- **Makeable analogs, no GPU/training, research:** **SynTwins**.
- **3D structures + route:** **SynCoGen**.
- **Pathway-level generation/editing:** **ReaSyn** (NVIDIA weights license).
- **Target-conditioned make-on-demand hit generation, permissive:** **SyntheMol** (MIT + CC BY).
- **Search billions-scale libraries, research:** **APEX** (non-commercial).
- **LLM-based, research-only:** **SynLlama** (UC non-commercial).
- **Validity-focused (not synthesizability):** see [molecular-generation.md](molecular-generation.md) (GenMol, etc.).
