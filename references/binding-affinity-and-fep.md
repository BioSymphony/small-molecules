# Binding Affinity and Free-Energy Calculation

Free-energy methods estimate binding affinity from molecular dynamics. These
methods include alchemical free-energy perturbation and thermodynamic
integration, plus lower-cost endpoint methods such as MM-PBSA and MM-GBSA.
Their accuracy depends on system setup, sampling, force-field choice, and
convergence. Each alchemical transformation can require substantial GPU time
and specialist review.

Use machine-learning and docking scores to screen large sets, then use a
free-energy method to rank a short list. Machine-learning scores are less
expensive but can be unreliable outside their training domain. Relevant tools
include [Boltz-2](docking-and-cofolding.md), the gnina and RTMScore pose
rescorers, and the trainable models in
[property-and-qsar-prediction.md](property-and-qsar-prediction.md). Validate each
model for the selected endpoint and chemical domain.

> **Proprietary reference points:** Schrödinger **FEP+** (RBFE/ABFE, OPLS), Cresset **Flare** (FEP + SBDD GUI), **Amber** TI/MMPBSA, and **OpenEye/Cadence**. The license sections below describe only the cited public repositories and do not cover their dependencies.

---

## OpenFE (Open Free Energy) — `OpenFreeEnergy/openfe`
- **Method and output:** Open RBFE via an **OpenMM** hybrid-topology protocol (built on the Perses implementation), plus solvation/ABFE protocols. Default force fields are OpenFF Sage 2.x (ligand) and ff14SB (protein); atom mapping uses Kartograf or LOMAP.
- **Code license:** **MIT** (© 2022 OpenFreeEnergy).
- **Data and weights:** n/a (physics). Force fields and dependencies have separate terms.
- **Citation:** Zenodo DOI 10.5281/zenodo.17258732 (versioned); methods cite Perses + Kartograf (*JCTC* 2024, 10.1021/acs.jctc.3c01206).
- **Installation and hardware:** `mamba env create -f environment.yml` + `pip install --no-deps .` (conda/Docker/single-file installer). **GPU strongly recommended** (OpenMM CUDA/OpenCL); campaigns are GPU-heavy.
- **Status:** On 2026-08-30, v1.12.0 was the most recent public release.
- **Terms:** Source code is MIT. Force fields and other dependencies have their own terms.

## Perses — `choderalab/perses`
- **Method and output:** Alchemical free energy via expanded-ensemble / nonequilibrium switching — **RBFE, ABFE, and protein point-mutation** free energies. **OpenMM**-based (the research engine OpenFE's RBFE protocol derives from).
- **Code license:** **MIT.**
- **Citation:** Zenodo DOI 10.5281/zenodo.8350218.
- **Installation and hardware:** `conda install -c conda-forge perses`. GPU (CUDA) for production.
- **Status:** Active but explicitly **pre-alpha** ("API can change at any time"); last tag v0.10.3 (2023).
- **Terms:** Source code is MIT. Some setup paths use an optional OpenEye dependency with separate terms; the API is explicitly pre-alpha.

## Alchemlyb — `alchemistry/alchemlyb`
- **Method and output:** **FEP *analysis*, not simulation.** Parsers for GROMACS/AMBER/NAMD dHdl output + best-practice estimators (**MBAR, BAR, TI**) + an automated ABFE analysis workflow. Engine-agnostic post-processing.
- **Code license:** **BSD-3-Clause.**
- **Citation:** Wu et al., *JOSS* 9(101):6934, 2024. DOI 10.21105/joss.06934.
- **Installation and hardware:** `pip install alchemlyb` / conda. **No GPU** (pandas/numpy/pymbar).
- **Status:** Active — v2.5.0 (2025).
- **Terms:** Source code is BSD-3-Clause.

## OpenMM — `openmm/openmm`
- **Method and output:** The high-performance, GPU-accelerated **MD engine** underneath most of this stack (custom forces/integrators → the alchemical machinery Perses/OpenFE build on). Not an FEP tool itself.
- **Code license:** **Dual MIT / LGPL.** The API, Reference, and CPU platforms are MIT; CUDA and OpenCL platforms are LGPL.
- **Citation:** Eastman et al., *PLoS Comput. Biol.* 13(7):e1005659, 2017. DOI 10.1371/journal.pcbi.1005659.
- **Installation and hardware:** `conda install -c conda-forge openmm`. **GPU** (CUDA primary; OpenCL).
- **Status:** The project published v8.x releases in 2026.
- **Terms:** See the component-specific MIT and LGPL license texts in the OpenMM distribution.

## BioSimSpace — `OpenBioSim/BioSimSpace`
- **Method and output:** Interoperable Python **FEP workflow layer** — write a perturbation pipeline once, run it across **GROMACS, AMBER, SOMD, OpenMM** back-ends (RBFE + solvation FE). Built on Sire.
- **Code license:** **GPL-3.0.**
- **Citation:** Hedges et al., *JOSS* 4(43):1831, 2019. DOI 10.21105/joss.01831.
- **Installation and hardware:** `conda create -n openbiosim -c conda-forge -c openbiosim biosimspace`. GPU via the chosen back-end.
- **Status:** Active — 2025.x.
- **Terms:** Source code is GPL-3.0. Each selected back end and force field, including AMBER `pmemd`, has separate terms.

## gmx_MMPBSA — `Valdes-Tresanco-MS/gmx_MMPBSA`
- **Method and output:** **Endpoint** binding free energy from **GROMACS** trajectories — **MM-PBSA / MM-GBSA** (a GROMACS-native re-implementation of AMBER's `MMPBSA.py`; needs AmberTools ≥20). Lower accuracy than alchemical FEP, but far cheaper — good for **ranking/triage**.
- **Code license:** **GPL-3.0.**
- **Citation:** Valdés-Tresanco et al., *JCTC* 17(10):6281, 2021. DOI 10.1021/acs.jctc.1c00645.
- **Installation and hardware:** `pip install gmx_MMPBSA` (+ AmberTools + GROMACS). **CPU-bound** post-processing (only the upstream MD needs GPU).
- **Status:** Active — v1.6.x (2026).
- **Terms:** Source code is GPL-3.0.

## BAT.py / BAT2 — `GHeinzelmann/BAT.py`
- **Method and output:** Fully automated **absolute binding free energy (ABFE)** workflow (also RBFE). Double-decoupling / SDR for ABFE; common-core or SepTop for RBFE. **AMBER (`pmemd.cuda`) + OpenMM** engines.
- **Code license:** **MIT.**
- **Citation:** Heinzelmann, Huggins, Gilson, *JCTC* 20:6518, 2024.
- **Installation and hardware:** Anaconda; dependency-heavy (VMD, OpenBabel, USalign, AmberTools20+). **GPU-intensive** (ABFE = many λ windows × decoupling legs).
- **Status:** Active — v2.4 (2026).
- **Terms:** BAT source code is MIT. The AMBER (`pmemd`) and OpenMM back ends have separate terms.

## GROMACS *(engine note)* — GitLab `gromacs/gromacs`
- Mainstream high-performance **MD engine** with built-in alchemical FEP (soft-core λ, TI, `gmx bar`; dH/dλ consumable by alchemlyb). Back-end for BioSimSpace, gmx_MMPBSA, and many ABFE workflows. Source code is **LGPL-2.1** and supports CUDA, HIP, and SYCL acceleration.

## Yank *(legacy)* — `choderalab/yank`
- Early ABFE framework based on Hamiltonian replica exchange in OpenMM. Source
  code is MIT. Its last release was in 2019; OpenFE and Perses provide maintained
  successors for related workflows.

> **Other open ABFE workflows:** **BindFlow** supports MM(PB/GB)SA and
> FEP-level ABFE with GROMACS (bioRxiv 2025,
> 10.1101/2025.09.25.678545). **FEP-SPell-ABFE** provides an automated workflow
> (*JCIM* 2024, 10.1021/acs.jcim.4c01986).

---

## 2026 ML Affinity and ML-Accelerated FEP Additions

### LigUnity — `IDEA-XL/LigUnity`
- **Method and output:** Foundation model for virtual screening and hit-to-lead ranking with active learning. It produces relative, assay-specific rankings rather than Boltz-2-style co-folded affinity estimates.
- **Code license:** **Apache-2.0** (data CC-BY-NC-4.0; weights HF `fengb/LigUnity_VS`).
- **Paper:** bioRxiv 2025.02 → peer-reviewed in **Patterns** (Cell Press), Oct 2025.
- **Status:** The repository received commits in March 2026.
- **Terms:** Source code is Apache-2.0; the training data are CC BY-NC-4.0. The public code license does not change the data terms.

### AQAffinity — `SandboxAQ/AQAffinity` (HF)
- **Method and output:** Public replication of the **Boltz-2 affinity head**, built on an **OpenFold3-format** structural input → affinity. It is not structure-free.
- **Code and weights:** **Apache-2.0.** Weight access requires approval.
- **Release:** Released in 2026; no formal preprint is cited.
- **Terms:** Code and weights are Apache-2.0. Evaluate the replication on a held-out domain.

### LamNet — `RenlingHu/LamNet`
- **Method and output:** **Alchemical-path-aware GNN** — encodes the λ-coupling path,
  predicts RBFE and ABFE, and optimizes λ schedules. The paper reports up to a
  1000-fold speedup over traditional AFEM on 463 ligands across 16 proteins.
- **Code license:** **MIT;** trained checkpoint in-repository.
- **Paper:** *National Science Review* 13(3), Feb 2026 (peer-reviewed).
- **Status:** The last recorded code update was 2025-07. The repository does not
  provide one packaged workflow for setup, simulation, analysis, and reporting.
- **Terms:** Source code and the bundled checkpoint are MIT.

## Choosing

| Need | Pick | Notes |
|---|---|---|
| **Affinity estimate, cheap and fast** | **[Boltz-2](docking-and-cofolding.md)** (ML) | Model estimate; code and weights MIT; validate against relevant measurements |
| **Rank a congeneric / assay series (FEP-alternative)** | **LigUnity** (Apache) | relative ranking + active learning; ~100× cheaper than Glide-SP |
| **Rigorous RBFE on a congeneric series** | **OpenFE** | MIT source code; inspect force-field and dependency terms |
| **ABFE (absolute), one ligand** | **BAT.py/BAT2** (OpenMM path) | MIT; most GPU-intensive |
| **Cheap endpoint ranking** | **gmx_MMPBSA** | GPL-3; CPU post-processing; lower accuracy than FEP |
| **Analyze FEP output (any engine)** | **alchemlyb** | BSD-3, no GPU |
| **Multi-engine workflow orchestration** | **BioSimSpace** | GPL-3 (copyleft) |

Use docking or ML affinity estimates to narrow a congeneric series. Then use
**OpenFE RBFE** to support rank ordering before synthesis. See the tool cards and
[licensing-and-data.md](licensing-and-data.md) for component terms.
