# Binding Affinity & Free-Energy Calculation

This is the rigorous end of *"will it bind, and how tightly?"* **Physics-based free-energy methods** (alchemical FEP/TI, and the cheaper endpoint MM-PBSA/GBSA) compute binding affinity from molecular dynamics. On a congeneric series, alchemical **relative binding free energy (RBFE)** routinely reaches ~1 kcal/mol error — but each transformation costs hours-to-days of GPU MD and demands real expertise (force field, sampling, atom mapping).

**Where this sits vs. ML affinity:** ML/docking scorers (next paragraph) are orders of magnitude cheaper and scan millions of compounds, but are interpolative and unreliable out-of-distribution. The standard pattern is **ML/docking to triage → FEP to rank-order a short list** before synthesis.

**The ML-affinity options live in other files** — most importantly **[Boltz-2](docking-and-cofolding.md)** (the first open model approaching FEP accuracy, ~1000× faster; MIT code+weights), plus pose-rescoring functions **gnina** (CNN) and **RTMScore** in [docking-and-cofolding.md](docking-and-cofolding.md), and trainable QSAR affinity models in [property-and-qsar-prediction.md](property-and-qsar-prediction.md). This file is the **physics** layer.

> **Commercial landscape (proprietary, not open — reference points only):** Schrödinger **FEP+** (industry-standard RBFE/ABFE, OPLS), Cresset **Flare** (FEP + SBDD GUI), **Amber** TI/MMPBSA (academic-licensed, not OSI-open), **OpenEye/Cadence**. The open stack below is what competes with these. Licenses verified **2026-06-13**.

---

## OpenFE (Open Free Energy) — `OpenFreeEnergy/openfe` ⭐
- **What/method:** The flagship open **FEP+ alternative**. Production RBFE via an **OpenMM** hybrid-topology protocol (built on the Perses implementation), plus solvation/ABFE protocols. Default force fields OpenFF Sage 2.x (ligand) + ff14SB (protein); atom mapping via Kartograf/LOMAP.
- **Code license:** **MIT** (© 2022 OpenFreeEnergy).
- **Data/weights:** n/a (physics). Force fields ship under permissive licenses.
- **Citation:** Zenodo DOI 10.5281/zenodo.17258732 (versioned); methods cite Perses + Kartograf (*JCTC* 2024, 10.1021/acs.jctc.3c01206).
- **Install / GPU:** `mamba env create -f environment.yml` + `pip install --no-deps .` (conda/Docker/single-file installer). **GPU strongly recommended** (OpenMM CUDA/OpenCL); campaigns are GPU-heavy.
- **Status:** Very active — v1.11.1 (May 2026), funded consortium.
- **Commercial:** ✅ **MIT, unrestricted.** Caveat: compute- and expertise-heavy, not turnkey. **The default open RBFE pick.**

## Perses — `choderalab/perses`
- **What/method:** Alchemical free energy via expanded-ensemble / nonequilibrium switching — **RBFE, ABFE, and protein point-mutation** free energies. **OpenMM**-based (the research engine OpenFE's RBFE protocol derives from).
- **Code license:** **MIT.**
- **Citation:** Zenodo DOI 10.5281/zenodo.8350218.
- **Install / GPU:** `conda install -c conda-forge perses`. GPU (CUDA) for production.
- **Status:** Active but explicitly **pre-alpha** ("API can change at any time"); last tag v0.10.3 (2023).
- **Commercial:** ✅ MIT. ⚠️ Watch the optional **OpenEye** dependency (separate commercial license) for some setup paths — the OpenFF path avoids it; and the pre-alpha API.

## Alchemlyb — `alchemistry/alchemlyb`
- **What/method:** **FEP *analysis*, not simulation.** Parsers for GROMACS/AMBER/NAMD dHdl output + best-practice estimators (**MBAR, BAR, TI**) + an automated ABFE analysis workflow. Engine-agnostic post-processing.
- **Code license:** **BSD-3-Clause.**
- **Citation:** Wu et al., *JOSS* 9(101):6934, 2024. DOI 10.21105/joss.06934.
- **Install / GPU:** `pip install alchemlyb` / conda. **No GPU** (pandas/numpy/pymbar).
- **Status:** Active — v2.5.0 (2025).
- **Commercial:** ✅ BSD-3, lightweight, no compute burden. Use it to analyze whatever engine you run.

## OpenMM — `openmm/openmm`
- **What/method:** The high-performance, GPU-accelerated **MD engine** underneath most of this stack (custom forces/integrators → the alchemical machinery Perses/OpenFE build on). Not an FEP tool itself.
- **Code license:** **Dual MIT / LGPL** — API + Reference + CPU platforms are **MIT**; **CUDA and OpenCL platforms are LGPL**. (So it's *not* a clean "MIT" label.)
- **Citation:** Eastman et al., *PLoS Comput. Biol.* 13(7):e1005659, 2017. DOI 10.1371/journal.pcbi.1005659.
- **Install / GPU:** `conda install -c conda-forge openmm`. **GPU** (CUDA primary; OpenCL).
- **Status:** Very active — v8.x (2026).
- **Commercial:** ✅ Permissive overall. ⚠️ GPU platforms are LGPL — fine for normal (dynamic) use; static-linking/modifying those sources triggers LGPL obligations.

## BioSimSpace — `OpenBioSim/BioSimSpace`
- **What/method:** Interoperable Python **FEP workflow layer** — write a perturbation pipeline once, run it across **GROMACS, AMBER, SOMD, OpenMM** back-ends (RBFE + solvation FE). Built on Sire.
- **Code license:** ⚠️ **GPL-3.0 (copyleft)** — note the contrast with the MIT/BSD tools.
- **Citation:** Hedges et al., *JOSS* 4(43):1831, 2019. DOI 10.21105/joss.01831.
- **Install / GPU:** `conda create -n openbiosim -c conda-forge -c openbiosim biosimspace`. GPU via the chosen back-end.
- **Status:** Active — 2025.x.
- **Commercial:** ✅ allowed, but **GPL-3.0 copyleft**: distributing a derived product forces GPL-3 release. Fine internally; ⚠️ for embedding in proprietary distributed software. Inherits each back-end's force-field/engine licensing (e.g. AMBER `pmemd`).

## gmx_MMPBSA — `Valdes-Tresanco-MS/gmx_MMPBSA`
- **What/method:** **Endpoint** binding free energy from **GROMACS** trajectories — **MM-PBSA / MM-GBSA** (a GROMACS-native re-implementation of AMBER's `MMPBSA.py`; needs AmberTools ≥20). Lower accuracy than alchemical FEP, but far cheaper — good for **ranking/triage**.
- **Code license:** **GPL-3.0.**
- **Citation:** Valdés-Tresanco et al., *JCTC* 17(10):6281, 2021. DOI 10.1021/acs.jctc.1c00645.
- **Install / GPU:** `pip install gmx_MMPBSA` (+ AmberTools + GROMACS). **CPU-bound** post-processing (only the upstream MD needs GPU).
- **Status:** Active — v1.6.x (2026).
- **Commercial:** ✅ allowed under GPL-3; ⚠️ copyleft on redistribution.

## BAT.py / BAT2 — `GHeinzelmann/BAT.py`
- **What/method:** Fully automated **absolute binding free energy (ABFE)** workflow (also RBFE). Double-decoupling / SDR for ABFE; common-core or SepTop for RBFE. **AMBER (`pmemd.cuda`) + OpenMM** engines.
- **Code license:** **MIT.**
- **Citation:** Heinzelmann, Huggins, Gilson, *JCTC* 20:6518, 2024.
- **Install / GPU:** Anaconda; dependency-heavy (VMD, OpenBabel, USalign, AmberTools20+). **GPU-intensive** (ABFE = many λ windows × decoupling legs).
- **Status:** Active — v2.4 (2026).
- **Commercial:** ✅ MIT on BAT itself. ⚠️ The AMBER (`pmemd`) back-end is separately licensed; the **OpenMM path stays fully open.**

## GROMACS *(engine note)* — GitLab `gromacs/gromacs`
- Mainstream high-performance **MD engine** with built-in alchemical FEP (soft-core λ, TI, `gmx bar`; dH/dλ consumable by alchemlyb). Back-end for BioSimSpace, gmx_MMPBSA, and many ABFE workflows. **LGPL-2.1**, strong CUDA/HIP/SYCL GPU acceleration. **Commercial:** ✅ weak copyleft, unproblematic as an engine.

## Yank *(legacy)* — `choderalab/yank`
- Early open ABFE framework (Hamiltonian replica exchange on OpenMM). **MIT**, but **effectively unmaintained** (last real release 2019; superseded by openmmtools + Perses + OpenFE). ✅ MIT but ❌ **not recommended for new work** — use OpenFE/Perses.

> **Other open ABFE workflows worth knowing:** **BindFlow** (MM(PB/GB)SA *or* FEP-level ABFE, GROMACS; bioRxiv 2025, 10.1101/2025.09.25.678545) and **FEP-SPell-ABFE** (*JCIM* 2024, 10.1021/acs.jcim.4c01986) — both newer, automated, open-source.

---

## New 2026 — ML affinity & ML-accelerated FEP

### LigUnity — `IDEA-XL/LigUnity` ⭐
- **What/method:** Foundation model over a shared pocket-ligand space doing joint **virtual screening + hit-to-lead ranking**, explicitly benchmarked as a cheap **FEP+ alternative** with a built-in **active-learning** loop. Beats 24 methods by >50% on DUD-E/DEKOIS; on Merck/JACS FEP sets, few-shot fine-tuning approaches FEP+ at ~100× lower cost than Glide-SP. Relative *ranking* per-assay — distinct from Boltz-2's absolute co-folded affinity.
- **Code license:** **Apache-2.0** (data CC-BY-NC-4.0; weights HF `fengb/LigUnity_VS`).
- **Paper:** bioRxiv 2025.02 → peer-reviewed in **Patterns** (Cell Press), Oct 2025.
- **Status:** Very active (pushed Mar 2026, ~58★).
- **Commercial:** ✅ Apache code; ⚠️ training data is CC-BY-NC (affects retraining/redistribution, not inference). The on-point FEP-alternative + active-learning pick.

### AQAffinity — `SandboxAQ/AQAffinity` (HF)
- **What/method:** Open replication of the **Boltz-2 affinity head**, built on an **OpenFold3-format** structural input → affinity. First independent open replica of the Boltz-2 affinity module, under a cleaner license, from a credible team (SandboxAQ + OpenFold Consortium). Not structure-free.
- **Code + weights:** **Apache-2.0** (HF; weights behind a trivial auto-approve form).
- **Released:** ~Jan–Feb 2026; ⚠️ no formal preprint yet.
- **Commercial:** ✅ Apache. Caveat: a *replication*, not a new algorithm; like Boltz-2 it degrades out-of-distribution (see the reliability-eval note in [docking-and-cofolding.md](docking-and-cofolding.md)).

### LamNet — `RenlingHu/LamNet`
- **What/method:** **Alchemical-path-aware GNN** — bakes the λ-coupling path into a physics-informed representation, predicts RBFE + ABFE, and **optimizes λ-schedules to speed conventional FEP convergence** (claims up to 1000× vs traditional AFEM; 463 ligands / 16 proteins). A genuinely novel *ML-accelerated free-energy* method (Hou lab), not just an ML regressor.
- **Code license:** **MIT;** trained checkpoint in-repo.
- **Paper:** *National Science Review* 13(3), Feb 2026 (peer-reviewed).
- **Status:** ⚠️ Code lightly maintained (last push 2025-07) — promising but not yet turnkey.
- **Commercial:** ✅ MIT.

## Choosing

| Need | Pick | Notes |
|---|---|---|
| **Affinity number, cheap & fast, commercial** | **[Boltz-2](docking-and-cofolding.md)** (ML) | FEP-approaching, ~1000× faster, MIT/MIT — start here for screening |
| **Rank a congeneric / assay series (FEP-alternative)** | **LigUnity** (Apache) | relative ranking + active learning; ~100× cheaper than Glide-SP |
| **Rigorous RBFE on a congeneric series** | **OpenFE** | MIT, production-grade, the open FEP+ analog |
| **ABFE (absolute), one ligand** | **BAT.py/BAT2** (OpenMM path) | MIT; most GPU-intensive |
| **Cheap endpoint ranking** | **gmx_MMPBSA** | GPL-3; CPU post-processing; lower accuracy than FEP |
| **Analyze FEP output (any engine)** | **alchemlyb** | BSD-3, no GPU |
| **Multi-engine workflow orchestration** | **BioSimSpace** | GPL-3 (copyleft) |

**Practical loop:** triage millions with docking/ML affinity ([Boltz-2](docking-and-cofolding.md)) → narrow to a congeneric short list → **OpenFE RBFE** to rank-order before synthesis. **Commercial-clean physics stack:** OpenFE + OpenMM + alchemlyb + BAT (all MIT/BSD); the GPL tools (BioSimSpace, gmx_MMPBSA, GROMACS-LGPL) are usable but copyleft on redistribution — see [licensing-and-data.md](licensing-and-data.md).
