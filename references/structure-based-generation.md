# Structure-Based Generation and Pocket Detection

Pocket-conditioned generators sample ligands directly in a target's three-
dimensional binding site. They condition generation on pocket atoms or a pocket
surface. In contrast, the tools in
[molecular-generation.md](molecular-generation.md) do not use a target pocket.

Most pocket-conditioned generators do not constrain output to synthesizable
chemical space. Their generated structures can be strained or impractical.
Follow generation with a synthesis-aware projection tool, such as PrexSyn,
SynFormer, or ChemProjector, or with a retrosynthesis tool such as
AiZynthFinder. See
[synthesizable-generation.md](synthesizable-generation.md) and
[retrosynthesis-planning.md](retrosynthesis-planning.md).

Get the pocket from a binding-site detector such as fpocket, P2Rank, or
DoGSiteScorer. Use a structure from the PDB or from a method in
[protein-structure-prediction.md](protein-structure-prediction.md).

These generators are usually trained on drug-like small molecules in single,
well-defined pockets from CrossDocked or PDBBind. Performance can decline for
macrocycles, natural-product scaffolds, molecular glues, and other
induced-proximity binders. These binders can occupy a composite surface across
two proteins. For daraxonrasib, use scaffold-constrained enumeration around the
known ligand and score the ternary structure. See the
[KRAS(ON) glue worked example](worked-example-kras-glue.md).

TargetDiff and PocketFlow place MIT text in files named `LICIENCE` and
`Liscense`, so GitHub might not detect their licenses. DecompDiff uses CC BY-NC
4.0, and Lingo3DMol uses GPL-3.0. Check the exact file at the cited revision.

---

## Pocket-conditioned generators

### Pocket2Mol — `pengxingang/Pocket2Mol`
- **Method:** **Autoregressive** (E(3)-equivariant; sequential atom/bond sampling in the pocket).
- **License:** **MIT.** Weights are hosted on Google Drive.
- **Paper:** *Pocket2Mol*, **ICML 2022**, arXiv:2205.07249.
- **Hardware and status:** GPU (CUDA 11.3); dormant (2023) but a standard baseline.
- **Terms:** Source code is MIT. **Synth-constrained:** no SA or retrosynthesis filter at generation.

### TargetDiff — `guanjq/targetdiff`
- **Method:** **Diffusion** (SE(3)-equivariant, non-autoregressive); also outputs a binding-affinity *ranking*.
- **License:** **MIT** in the misspelled `LICIENCE` file. Weights are hosted on Google Drive.
- **Paper:** *3D Equivariant Diffusion for Target-Aware Molecule Generation and Affinity Prediction*, **ICLR 2023**, arXiv:2303.03543.
- **Hardware and status:** GPU (CUDA 11.6); dormant (2023); standard SBDD benchmark.
- **Terms:** Source code is MIT. **Synth-constrained:** no.

### DiffSBDD — `arneschneuing/DiffSBDD`
- **Method:** **Diffusion** (E(3)-equivariant EGNN); de novo + inpainting/scaffold tasks.
- **License:** **MIT.** Eight checkpoints are on Zenodo (record 8183747).
- **Paper:** *Structure-based drug design with equivariant diffusion models*, **Nature Computational Science** 2024. DOI 10.1038/s43588-024-00737-x.
- **Hardware and status:** GPU; public code activity continued through 2025.
- **Terms:** Source code is MIT. **Synth-constrained:** no at base generation; `optimize.py` can apply a post-hoc SA objective.

### DecompDiff — `bytedance/DecompDiff`
- **Method:** **Diffusion** with **decomposed priors** (arms/scaffold via reference ligand or subpockets) + optional bond diffusion.
- **License:** **CC BY-NC 4.0.** This is a content license rather than an open-source software license. The repository is archived (read-only) as of December 2025.
- **Paper:** *DecompDiff*, **ICML 2023**, arXiv:2403.07902.
- **Terms:** The repository states CC BY-NC 4.0. **Synth-constrained:** no.

### ResGen — `HaotianZhangAI4Science/ResGen`
- **Method:** **Autoregressive** parallel multi-scale (global pocket + local atomic context).
- **License:** ✅ **MIT.** Weights on Google Drive; data on Zenodo (DOI 10.5281/zenodo.7759114).
- **Paper:** *ResGen*, **Nature Machine Intelligence** 2023. DOI 10.1038/s42256-023-00712-7.
- **Hardware and status:** GPU (CUDA 11.3); mostly dormant (2024).
- **Terms:** Source code is MIT. **Synth-constrained:** no.

### Lingo3DMol — `stonewiseAIDrugDesign/Lingo3DMol`
- **Method:** **Language model + 3D coords** (fragment-based SMILES with local/global geometry). StoneWise AI.
- **License:** ⚠️ **GPL-3.0 (strong copyleft).** Checkpoints on AWS S3.
- **Paper:** *Generation of 3D molecules in pockets via a language model*, **Nature Machine Intelligence** 2023. DOI 10.1038/s42256-023-00775-6.
- **Hardware and status:** GPU **≥5 GB VRAM** (lighter than diffusion); dormant (2023).
- **Terms:** Source code is GPL-3.0. **Synth-constrained:** no hard filter; the authors report synthetic-accessibility metrics.

### PocketFlow — `Saoge123/PocketFlow`
- **Method:** Autoregressive flow with valence-rule priors. The authors report 100% chemical validity and experimental validation for HAT1 and YTHDC1.
- **License:** **MIT** in the misspelled `Liscense` file on the `master` branch. A checkpoint is committed in the repository.
- **Paper:** *PocketFlow*, **Nature Machine Intelligence** 2024. DOI 10.1038/s42256-024-00808-8.
- **Hardware and status:** GPU (CPU fallback); lightly maintained (2025).
- **Terms:** Source code is MIT. **Synth-constrained:** it enforces chemical validity, not synthetic accessibility.

### REINVENT 4 — `MolecularAI/REINVENT4` *(maintained framework)*
- **Method:** Production molecular-design framework — de novo, scaffold hopping, R-group, **linker design (LinkInvent)**, library/R-group **(LibInvent)**, Mol2Mol — via **RL** over a multi-component scoring function. AstraZeneca.
- **Pocket-conditioning:** REINVENT uses ligands and SMILES rather than a three-dimensional pocket as model input. You can add docking scores from a tool such as AutoDock Vina through DockStream to its reinforcement-learning reward. The reward provides the pocket signal; the generator itself is not pocket-conditioned.
- **License:** **Apache-2.0.** Priors ship with the framework.
- **Paper:** *Reinvent 4: Modern AI-driven generative molecule design*, **J. Cheminform.** 2024. DOI 10.1186/s13321-024-00812-5.
- **Hardware and status:** GPU helps; CPU is adequate for RL scoring. Public v4.x releases continued through 2025.
- **Terms:** Source code is Apache-2.0. **Synth-constrained:** configurable rather than default; the reward can include SA-score, reaction filters, or AiZynthFinder retrosynthesis.

### Apo2Mol — `AIDD-LiLab/Apo2Mol` *(2026)*
- **Method:** **Diffusion** (full-atom) — de novo design from **apo (unbound) pockets**, jointly generating ligand **and** holo-like pocket conformation (models pocket flexibility).
- **License:** ✅ **MIT** (verify the HF dataset license separately before training).
- **Paper:** *Apo2Mol*, **AAAI 2026**, arXiv:2511.14559.
- **Hardware and status:** GPU; full-atom diffusion has substantial memory and compute requirements. The 2026 release is early-stage; confirm checkpoint availability.
- **Terms:** Source code is MIT. **Synth-constrained:** no.

### PILOT / e3moldiffusion — `pfizer-opensource/e3moldiffusion` *(2025)*
- **Method:** **Diffusion** (E(3)-equivariant) — pocket-conditioned de novo with **multi-objective guidance via importance sampling** (steer toward docking score / SA at sampling time). Pfizer open-source.
- **License:** **Apache-2.0** for the code. The journal article is CC BY-NC, which is separate from the repository terms.
- **Paper:** *PILOT*, **Chemical Science (RSC)** 2024. DOI 10.1039/D4SC03523B (arXiv:2405.14925).
- **Hardware and status:** GPU (heavy); reasonably maintained (2025).
- **Terms:** Source code is Apache-2.0. **Synth-constrained:** guidance can steer toward SA/QED but does not impose a hard synthetic-accessibility constraint.

---

## Binding-site / pocket detection (the upstream input)

### fpocket — `Discngine/fpocket`
- **Method:** Geometry-based pocket detection + druggability scoring (**Voronoi / alpha-spheres**; no ML). Bundles `mdpocket` (trajectories), `dpocket`, `tpocket`.
- **License:** ✅ **MIT.** Runs on CPU.
- **Paper:** Le Guilloux et al., *BMC Bioinformatics* 2009. DOI 10.1186/1471-2105-10-168.
- **Status:** Active — v4.2.3 (2026).
- **Terms:** Source code is MIT.

### P2Rank — `rdk/p2rank`
- **Method:** **Machine-learning** ligand-binding-site prediction (random-forest over surface points → ranked pockets); no external feature deps. (`prankweb` is the web frontend.)
- **License:** ✅ **MIT.** **CPU only**, multi-threaded; needs **Java 17+**.
- **Paper:** Krivák & Hoksza, *J. Cheminform.* 2018. DOI 10.1186/s13321-018-0285-8.
- **Status:** Active — v2.5.1 (2025).
- **Terms:** Source code is MIT.

### DoGSiteScorer — **WEB-ONLY** (ProteinsPlus, `proteins.plus`)
- **Method:** **Difference-of-Gaussians** grid pocket detection + descriptor-based druggability. ZBH, Univ. Hamburg.
- **License:** ❌ **No open source — proprietary web service, free for *academic* use only** (REST API via ProteinsPlus).
- **Paper:** Volkamer et al., *Bioinformatics* 28(15):2074, 2012. DOI 10.1093/bioinformatics/bts310.
- **Terms:** Hosted academic service; no local source code or weights are published. Consult the service terms for non-academic use.

---

## New 2026 — multi-task generators & the synthesis-aware exception

### PocketXMol — `pengxingang/PocketXMol` *(2026, multi-task)*
- **Method:** Single atom-level generative **foundation** model for pocket-conditioned 3D SBDD, fragment linking/growing, PROTAC design, small-molecule and peptide docking, and conformer generation without task-specific fine-tuning.
- **License:** **MIT** code + **CC BY 4.0** weights (Zenodo 17801271). Each license has its own notice and attribution conditions.
- **Paper:** *Cell*, February 2026.
- **Terms:** Code is MIT and weights are CC BY 4.0. **Synth-constrained:** no.

### OMTRA — `gnina/OMTRA` *(2026, multi-task flow-matching)*
- **Method:** Multimodal flow matching from the gnina and Koes teams. It supports pocket-conditioned de novo generation, docking, and conformer generation, and conditions on pockets and pharmacophores. Training used a dataset of approximately 500 million conformers.
- **License:** **Apache-2.0** (code + trained models + dataset).
- **Paper:** arXiv:2512.05080 (Dec 2025).
- **Status:** Public code activity continued through June 2026.
- **Terms:** Code, trained models, and dataset are Apache-2.0.
- **Synthesizability:** No hard synthesis constraint is stated.

### Saturn — `schwallergroup/saturn` *(2026, sample-efficient RL — a REINVENT alternative)*
- **Method:** Schwaller-group RL generative framework built for **sample efficiency** (far fewer oracle/docking calls than REINVENT) with a 2025 extension giving **steerable synthesizability control** (specify allowed/forbidden reactions; >90% exact-match to specified routes).
- **License:** **Apache-2.0**. GitHub might report `NOASSERTION`; the repository includes an Apache-2.0 license file.
- **Paper:** synthesizability-control arXiv:2505.08774 (2025-05); core Saturn 2024.
- **Status:** Active as of June 2026. **Terms:** Source code is Apache-2.0. **Synth-constrained:** configurable via its built-in synthesizability control.

## Synthesis-Aware Pocket Generators

These methods combine pocket conditioning with reaction templates and building
blocks.

- **RxnFlow — `SeonghwanSeo/RxnFlow`** — synthesis-oriented GFlowNet over reaction templates and building blocks. The paper reports 34.8% synthesizable-by-construction output on CrossDocked. Code is MIT; the work appeared at ICLR 2025, and public code activity continued through April 2026.
- **CGFlow / 3DSynthFlow — `tsa87/cgflow`** — compositional flows that jointly design a synthesis pathway and three-dimensional pose. The paper reports approximately 62% AiZynthFinder success and results on 15 LIT-PCBA targets. Code is MIT; the work appeared at ICML 2025.
- **ShEPhERD — `coleygroup/shepherd`** — equivariant diffusion that generates three-dimensional molecules conditioned on shape, electrostatics, and pharmacophores for bioisostere and scaffold-hopping tasks. Code is MIT; the Hugging Face weights do not state separate terms. The work appeared as an ICLR 2025 oral, and the repository received commits in 2026. It complements the shape and pharmacophore overlay tools in [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md). It does not constrain generation to synthesizable molecules.

## Choosing

| Need | Pick | License |
|---|---|---|
| 3D pocket generator | **PILOT / e3moldiffusion** (Apache), **OMTRA** (Apache), or **DiffSBDD** (MIT) | Source-code terms listed in card |
| Multi-task model (SBDD + fragment/linker/PROTAC/docking) | **PocketXMol** | MIT code; CC BY 4.0 weights |
| Synthesizable-by-construction pocket generation | **RxnFlow**, CGFlow | MIT source code |
| Configurable synthesis-aware reward | **REINVENT 4** (+ AiZynthFinder) or **Saturn** | Apache-2.0 source code |
| Validity-focused pocket generation | **PocketFlow** | MIT source code in misspelled file |
| Pocket flexibility / apo pockets | **Apo2Mol** | MIT source code |
| Pocket detection | **fpocket** / **P2Rank** | MIT source code |
| Distinct restrictive terms | **DecompDiff** (CC BY-NC), **Lingo3DMol** (GPL-3.0) | Check individual license texts |

1. Detect the pocket with fpocket or P2Rank.
2. Generate candidates with PILOT, DiffSBDD, OMTRA, or PocketXMol.
3. Assess synthesis feasibility with PrexSyn or SynFormer plus AiZynthFinder.
4. Score poses with DiffDock-L, Boltz-1, or SigmaDock.
5. Use Boltz-2 only as a model-based affinity estimate.

See [synthesizable-generation.md](synthesizable-generation.md) and
[licensing-and-data.md](licensing-and-data.md) for related terms and methods.
