# Docking & Co-Folding

The **target-based / "will-it-bind?"** layer — the companion to the synthesizability ("can-I-make-it?") tools. These predict how a small molecule sits in a protein (a **pose**) and, for a few, how tightly it binds (an **affinity**). Three families, cheapest/most-mature first:

- **Classical / physics-based docking** — given a protein **structure** + pocket, search poses and score them with an empirical/force-field function. Mature, fast, mostly CPU, **licensing mostly simple** (Apache/MIT/BSD/LGPL). AutoDock Vina, smina, gnina (CNN-rescored), QuickVina, Vina-GPU, AutoDock-GPU, RxDock, DOCK6 (+ Meeko for prep, RTMScore for ML rescoring).
- **Deep-learning docking** — given a protein (structure or pocket) + ligand, predict the bound **pose** with a learned model. DiffDock(-L), Uni-Mol Docking v2, EquiBind, TankBind.
- **Co-folding** — given a protein **sequence** + ligand (no experimental structure needed), jointly fold the protein *and* place the ligand. AlphaFold3-class models: Boltz-1/-2, Chai-1, NeuralPLexer, Umol, AF3 itself.

(You need a protein structure first — from the PDB or [protein-structure-prediction.md](protein-structure-prediction.md) — and a pocket, from the detectors in [structure-based-generation.md](structure-based-generation.md).)

**The distinction that matters for screening (deep-learning / co-folding models):** most of these output **STRUCTURE ONLY** — a pose plus a *confidence* score (pLDDT/pTM/ipTM, or a pose-ranking confidence). **A confidence score is NOT a binding affinity.** Only **Boltz-2** (numerical affinity, FEP-approaching) and **TankBind** (an affinity-ranking head) predict binding strength. AlphaFold3 gives confidence/ranking metrics but **no** affinity number. (Classical docking returns an empirical *score* — a rough binding-energy estimate, better than a confidence but well short of FEP: see [binding-affinity-and-fep.md](binding-affinity-and-fep.md).)

**The license trap here is the mirror image of the synthesizability space.** There it was Enamine data; here it is **weights diverging from code on co-folding models.** Several flagship models ship permissive code (MIT/Apache) but lock the **weights** behind a non-commercial clause — and at least one (Chai-1) *relaxed* its weights license over time, so stale blog posts are wrong. Always read the weights terms separately. (The classical-docking family is mostly permissive — its one weights trap is **gnina's** unlicensed CNN weights.) All facts below verified against live repos, LICENSE files, HF/Zenodo cards, and papers on **2026-06-13**.

---

## Classical / physics-based docking

Mature, fast, mostly CPU, and **licensing is mostly simple** (Apache/MIT/BSD/LGPL) — the weights-vs-code trap further down is a DL/co-folding problem, not a Vina-family one (the one exception: **gnina's CNN weights**). The workhorse default when you already have a protein **structure + pocket**.

### AutoDock Vina — `ccsb-scripps/AutoDock-Vina`
- **Method/output:** physics-based empirical scoring (Vina + optional AD4 force field); pose + estimated affinity (kcal/mol). The field's default engine.
- **Code:** **Apache-2.0.** No ML weights.
- **Paper:** Eberhardt et al. (Vina 1.2.0), *JCIM* 61:3891, 2021. DOI 10.1021/acs.jcim.1c00203 (orig. Trott & Olson 2010, DOI 10.1002/jcc.21334).
- **Install/GPU:** `pip install vina` / conda / binaries. **CPU** (multithreaded). Active — v1.2.x (2025).
- **Commercial:** ✅ **Clean** — Apache-2.0.

### AutoDock-GPU — `ccsb-scripps/AutoDock-GPU`
- **Method:** GPU (CUDA/OpenCL) reimplementation of **AutoDock4.2** (lattice-grid, AD4 force field) with gradient local search. Accelerates AD4, not the Vina scorer.
- **Code:** ⚠️ **GPL-2.0** (a secondary LGPL file exists, but treat the whole as copyleft GPL-2.0).
- **Paper:** Santos-Martins et al., *JCTC* 17(2):1060, 2021. DOI 10.1021/acs.jctc.0c01006.
- **Install/GPU:** compile (`make DEVICE=CUDA`); needs Meeko + AutoGrid. **GPU required.** Active — v1.6 (2024).
- **Commercial:** ⚠️ GPL-2.0 copyleft — internal use fine; redistributing derivatives triggers source disclosure.

### smina — `mwojcikowski/smina` *(GitHub mirror; canonical home SourceForge)*
- **Method:** Vina fork for improved empirical scoring/minimization + user-defined scoring functions; OpenBabel I/O.
- **Code:** **Dual Apache-2.0 + GPL-2.0** (GPL via OpenBabel = effective distribution constraint).
- **Paper:** Koes et al., *JCIM* 53(8):1893, 2013. DOI 10.1021/ci300604z.
- **Install/GPU:** `conda install -c conda-forge smina` / static binary. **CPU.** ⚠️ **Dormant** (mirror frozen ~2018) — gnina is the maintained successor.
- **Commercial:** ⚠️ GPL-2.0 effective; internal use clean, redistribution copyleft.

### gnina — `gnina/gnina` (code) + `gnina/models` (weights) ⚠️
- **Method:** Vina/smina fork that **rescores poses with an ensemble of CNNs**; v1.3 adds covalent docking + PyTorch.
- **Code:** **Dual Apache-2.0 + GPL-2.0** (GPL via OpenBabel; effective = GPL-2.0).
- **Weights:** 🔴 **Major trap — the pretrained CNN weights live in `gnina/models`, which has NO LICENSE file = all rights reserved**, and carry CrossDocked2020/PDBbind provenance. The code license does **not** cover them.
- **Paper:** McNutt et al. (GNINA 1.3), *J. Cheminform.* 17:28, 2025. DOI 10.1186/s13321-025-00973-x.
- **Install/GPU:** prebuilt binary (weights baked in) / source / Docker. **GPU strongly recommended** (CUDA). Active — v1.3.x (2025).
- **Commercial:** ⚠️→❌ **Code GPL-2.0 (manageable), but the default CNN weights are unlicensed (all rights reserved) + NC-flavored data provenance** — commercial use of the CNN scoring is legally unclear. Safe path: empirical (Vina) scoring only, or retrain on clean data.

### QuickVina 2 / QuickVina-W — `QVina/qvina`
- **Method:** speed-optimized Vina forks; QuickVina-W tuned for blind/whole-surface docking. Empirical (Vina) scoring.
- **Code:** **Apache-2.0.**
- **Paper:** Alhossary et al., *Bioinformatics* 31(13):2214, 2015. DOI 10.1093/bioinformatics/btv082 (QVina-W: Hassan et al., *Sci. Rep.* 7:15451, 2017).
- **Install/GPU:** source/binaries. **CPU.** Dormant but stable (2023).
- **Commercial:** ✅ Apache-2.0.

### Vina-GPU 2.1 — `DeltaGroupNJUPT/Vina-GPU-2.1`
- **Method:** OpenCL GPU acceleration of Vina + derivatives (bundles AutoDock-Vina-GPU, QuickVina2-GPU, QuickVina-W-GPU 2.1).
- **Code:** **Apache-2.0.**
- **Paper:** Tang et al., *IEEE/ACM TCBB* 2024. DOI 10.1109/TCBB.2024.3467127.
- **Install/GPU:** source + OpenCL SDK + boost. **GPU required** (OpenCL; best on NVIDIA). Stable (2024).
- **Commercial:** ✅ Apache-2.0.

### RxDock — GitLab `rxdock/rxdock` *(maintained fork of rDock)*
- **Method:** fast docking to **proteins *and* nucleic acids** (notably RNA); empirical scoring + GA sampling, HTVS-oriented. Original rDock died ~2014.
- **Code:** **LGPL-3.0** (weak copyleft).
- **Paper:** (rDock) Ruiz-Carmona et al., *PLoS Comput. Biol.* 10(4):e1003571, 2014. DOI 10.1371/journal.pcbi.1003571.
- **Install/GPU:** `conda install -c bioconda rxdock`. **CPU.** ⚠️ Semi-dormant (v0.1.0, best-effort).
- **Commercial:** ✅ LGPL-3.0 — commercial use + linking OK; modifications to RxDock shared under LGPL.

### DOCK6 — `docking-org/dock6` (GitHub) vs UCSF portal ⚠️
- **Method:** classic anchor-and-grow flexible docking + GB/SA scoring (UCSF). Physics-based.
- **Code:** ⚠️ **Dual-track:** the **GitHub repo is BSD-3-Clause** (clean, 2026), but material from the **UCSF web portal** is governed by a **proprietary academic-only EULA** (no redistribution; commercial license required). **Provenance determines your rights.**
- **Paper:** Allen et al., *JCC* 36(15):1132, 2015. DOI 10.1002/jcc.23905.
- **Install/GPU:** clone + build, or UCSF portal. **CPU** (MPI). Active (DOCK 6.12/6.13, 2026).
- **Commercial:** ⚠️ ✅ if obtained from `docking-org/dock6` (BSD-3) / ❌ if from the UCSF portal (academic EULA). **Confirm where you got it.**

### Meeko — `forlilab/Meeko`
- **Method:** ligand/receptor **prep** (SMILES/SDF → PDBQT, macrocycle/flex-residue handling, RDKit interop) for the AutoDock family. Companion, not a docking engine.
- **Code:** **LGPL-2.1.**
- **Paper:** Forli Lab, *ChemRxiv* 2025. DOI 10.26434/chemrxiv-2025-6b37n.
- **Install/GPU:** `pip install meeko` / conda. **CPU.** Very active.
- **Commercial:** ✅ LGPL-2.1 — usable as a library; modifications shared under LGPL.

### RTMScore — `sc8668/RTMScore`
- **Method:** ML **rescoring** (graph-transformer + mixture-density net → residue–atom distance-likelihood potential) to rerank Vina/gnina poses + boost VS enrichment.
- **Code + weights:** ✅ **MIT** — weights bundled in-repo under the same MIT (notably cleaner than gnina's weights).
- **Paper:** Shen et al., *J. Med. Chem.* 65(15):10691, 2022. DOI 10.1021/acs.jmedchem.2c00991.
- **Install/GPU:** git (PyTorch + DGL + RDKit). GPU recommended. Dormant (2023) but stable.
- **Commercial:** ✅ MIT code + MIT weights (verify PDBbind provenance if redistributing the trained model).

> **PLANTS** (ant-colony docking) — closed-source, academic-binary-only, site stale; **no public source.** ❌ not usable for open/commercial pipelines. See [watchlist.md](watchlist.md).

---

**Deep-learning docking & co-folding** — learned pose/structure prediction; this is where the **weights-vs-code license trap** bites (read the weights terms separately). The flagship is **Boltz-2** — the only fully-open model that also predicts a binding *affinity*.

## Boltz-2 — *first open model approaching FEP-level binding-affinity accuracy (structure + AFFINITY)* ⭐

> Boltz-2 is an open biomolecular foundation model that goes beyond AlphaFold3/Boltz-1 by **jointly predicting complex 3D structure AND binding affinity** in a single model. It is the flagship here: output is **STRUCTURE + AFFINITY** — it emits a numerical affinity (`affinity_pred_value`, reported as log10(IC50) with IC50 in µM) plus a binary binder probability, *and* the full complex structure. Reported as the first deep-learning model to approach physics-based **FEP** accuracy on binding affinity while running ~1000× faster — a genuine virtual-screening / lead-optimization tool, not just a structure predictor. **Both code and weights are MIT** (verified) — a rare fully-open flagship.

- **Repo:** `jwohlwend/boltz` — https://github.com/jwohlwend/boltz (~4k stars; shared mono-repo for Boltz-1 **and** Boltz-2). ⚠️ **Collision/entity note:** distinct from **Boltz PBC / "Boltz Lab"**, the commercial spinout (boltz.bio; Corso CEO, Wohlwend, Passaro) — same team, different thing from this MIT repo. A community fork adds Tenstorrent support.
- **What it does / method:** Co-folding model in the AlphaFold3 family with an added affinity head; trained with Recursion's data/compute. Benchmarked against FEP+ and OpenFE. Requires an MSA (ColabFold/MMseqs2).
- **Output:** **STRUCTURE + AFFINITY.** Numerical binding affinity (`affinity_pred_value` = log10(IC50), µM) + `affinity_probability_binary` (0–1), in addition to the 3D complex. This is the distinguishing capability of the whole file.
- **Code license:** **MIT** — `raw.githubusercontent.com/jwohlwend/boltz/main/LICENSE` (© 2024 Jeremy Wohlwend, Gabriele Corso, Saro Passaro). README: *"Our model and code are released under MIT License, and can be freely used for both academic and commercial purposes."*
- **Weights/model license + location:** **MIT** (verified SEPARATELY). Hosted at https://huggingface.co/boltz-community/boltz-2 — HF card `license: mit`, **no** non-commercial rider despite Recursion's involvement. Also mirrored as an **NVIDIA NIM**. Auto-downloaded by the CLI.
- **Paper:** *Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction*, Passaro, Corso, Wohlwend et al. (MIT + Recursion). bioRxiv 2025-06-18. DOI 10.1101/2025.06.14.659707 (PMC12262699).
- **Install:** `pip install boltz[cuda] -U` (same package as Boltz-1; the CLI selects Boltz-2 weights).
- **GPU needs:** ~**24–48 GB VRAM** datacenter GPU (A100/H100/L40S). On an L40S (48 GB): ~11 GB structure + ~7–8 GB affinity. NVIDIA NIM packaging recommends ≥48 GB.
- **Maintenance:** Actively maintained; latest release v2.2.1 (2025-09-08), ~437 commits. MIT CSAIL/Jameel Clinic team; sustained commercial involvement (Recursion, NVIDIA) and the Boltz PBC spinout (shipped BoltzGen Nov 2025, Boltz Lab Jan 2026).
- **Commercial-use read:** ✅ **Clearly OK — the rare fully-open flagship.** 4-layer: **code = MIT** / **weights = MIT** (HF verified, no NC clause) / **data = MIT-released per repo** (Recursion contributed data; no NC rider found) / **base = none restrictive** (trained from scratch). The flagged tension resolves cleanly: code MIT **and** weights MIT with no hidden non-commercial clause. Only soft caveat is governance drift (the team's newer *hosted* products are commercial), but that does not retroactively change the MIT terms on the released Boltz-1/-2 artifacts.

## Boltz-1 — *first fully open model to approach AlphaFold3 accuracy (structure only)*

> Boltz-1 is the open AlphaFold3-class co-folding model that predicts 3D structures of biomolecular complexes (proteins, RNA, DNA, small molecules) at AF3-level accuracy, plus a "Boltz-steering" inference-time technique to fix hallucinated/non-physical predictions. Output is **STRUCTURE-ONLY** — 3D coordinates, no affinity head. Use Boltz-2 if you need binding strength; Boltz-1 if you only need the complex structure.

- **Repo:** `jwohlwend/boltz` — https://github.com/jwohlwend/boltz (same mono-repo as Boltz-2; ~4k stars). Collision note: see Boltz-2 (Boltz PBC spinout ≠ this repo).
- **What it does / method:** Co-folding model in the AF3 family; architecture/speed innovations + inference-time steering. Requires an MSA (ColabFold/MMseqs2).
- **Output:** **STRUCTURE-ONLY.** No affinity head.
- **Code license:** **MIT** (same LICENSE file as Boltz-2).
- **Weights/model license + location:** **MIT.** https://huggingface.co/boltz-community/boltz-1 — HF card `license: mit`. The bioRxiv abstract explicitly states weights/datasets/benchmarks are released "under the MIT open license." (The bioRxiv *PDF* metadata is tagged CC-BY — that governs the document, not the model/code.)
- **Paper:** *Boltz-1: Democratizing Biomolecular Interaction Modeling*, Wohlwend, Corso, Passaro et al. bioRxiv 2024-11-20. DOI 10.1101/2024.11.19.624167. (Not yet journal-published.)
- **Install:** `pip install boltz[cuda] -U` (drop `[cuda]` for CPU).
- **GPU needs:** Not separately stated; GPU-memory-bound for large complexes (community LMI4Boltz project exists to cut VRAM and roughly double the token-size limit on consumer hardware).
- **Maintenance:** Active in the shared repo; release v2.2.1 (2025-09-08). MIT team (Wohlwend/Corso/Passaro; Barzilay group).
- **Commercial-use read:** ✅ **Clearly OK.** 4-layer: code MIT / weights MIT / data MIT-released / no restrictive base. Fully open with no catch — but structure only, no affinity.

## Chai-1 — *AF3-class open foundation model; code + weights RELAXED to Apache 2.0 (structure only)* ⚠️→✅

> Chai-1 (Chai Discovery) is a multimodal foundation model for **biomolecular structure prediction** — proteins, small-molecule ligands, DNA, RNA, glycosylations, covalent modifications — benchmarked roughly AlphaFold3-class. It can optionally be prompted with experimental restraints (wet-lab contacts) for a double-digit-% boost, and runs in single-sequence (no-MSA) mode with most accuracy preserved. Output is **STRUCTURE-ONLY** — 3D coordinates + confidence (pTM/ipTM/PAE); it does **NOT** predict binding affinity.

- **Repo:** `chaidiscovery/chai-lab` — https://github.com/chaidiscovery/chai-lab (~1.95k stars, Chai Discovery, Inc.). Name collisions are unrelated: `chaijs/chai` (JS assertion lib), Chai Builder/Studio, chaipredict.com — none are this tool.
- **What it does / method:** AF3-class diffusion all-atom structure predictor across proteins + ligands + nucleic acids + modifications; optional restraint conditioning; optional MSA-free mode. MSAs via MMseqs2/ColabFold server when used.
- **Output:** **STRUCTURE-ONLY.** Atomic coordinates (CIF/PDB) + confidence (pTM, ipTM, PAE-style). No ΔG/Kd/affinity head. (Affinity-style scoring is a *later, separate* Chai capability — not part of Chai-1.)
- **Code license:** **Apache 2.0.** Single `LICENSE` at repo root; GitHub `spdx_id: Apache-2.0`. No non-commercial clause.
- **Weights/model license + location:** ✅ **Weights are ALSO Apache 2.0 (current state) — NOT a separate restricted license.** README verbatim: *"Chai-1 is released under an Apache 2.0 License (both code and model weights)… can be used for both academic and commercial purposes, including for drug discovery."* No `LICENSE-MODEL`/`MODEL_LICENSE`/community-license file exists (only one `LICENSE`). Weights auto-download via the `chai_lab` package (Chai-hosted). ⚠️ **CRITICAL history — the divergence the prompt flagged:** the *original* Oct 2024 release locked the **weights** under a **non-commercial "Chai Discovery Community License Agreement"** (no commercial use; no using outputs to train models >10k params or any structure/drug/enzyme-design tech). Chai Discovery **relaxed this to Apache 2.0 for code + weights on ~2024-11-21** (official announcement + GitHub issue #192). **Any web result quoting a non-commercial "Community License" is quoting the SUPERSEDED terms** — verify you're on the current release. (The bioRxiv *paper* PDF carries a CC BY-NC license — that's the document, not the software.)
- **Paper:** *Chai-1: Decoding the molecular interactions of life*, Chai Discovery team (corresp. Joshua Meier). bioRxiv 2024-10-11. DOI 10.1101/2024.10.10.615955. (Tech report; not peer-reviewed.)
- **Install:** `pip install chai_lab==0.6.1` (or `pip install git+https://github.com/chaidiscovery/chai-lab.git`). CLI: `chai fold`.
- **GPU needs:** Linux, Python ≥3.10, CUDA GPU with bf16. Recommended A100/H100 80GB or **L40S 48GB**; A10/A30 and RTX 4090 work for smaller complexes. VRAM scales with complex size (AF3-class profile).
- **Maintenance:** Active. Last commit 2026-04-11; latest tagged release v0.6.1 (2025-03-18) — commits continue past the last formal release. ~1.95k stars.
- **Commercial-use read:** ✅ **YES — commercial drug-discovery use permitted, no carve-outs (current Apache-2.0 state).** 4-layer: **code = Apache 2.0** / **weights = Apache 2.0** (relaxed Nov 2024 from a prior NC Community License; *no* "no-competing-models" restriction remains — but confirm you pulled the current release) / **data/MSA = ⚠️** default MSA hits the public ColabFold/MMseqs2 server, so self-host MSAs for closed pipelines / **base = N/A** (trained from scratch). The whole point of this card: the weights *used to* diverge non-commercially and no longer do.
  - **↳ Chai-2 / Chai-3 note — NOT open:** Chai-2 is Chai Discovery's **proprietary** zero-shot antibody/protein *de novo design* platform (different task), bioRxiv 2025 (DOI 10.1101/2025.07.05.663018), commercialized via partnerships (Pfizer, Lilly) — **no code/weights in `chai-lab`** (the repo only cites it). A proprietary Chai-3 has also been referenced. **Chai-1 is the only open release** in this family.

## DiffDock & DiffDock-L — *diffusion generative blind docking (poses + confidence, NOT affinity)*

> DiffDock treats molecular docking as a generative problem: a **diffusion model over the ligand's degrees of freedom** (translation, rotation, torsion) using SE(3)-equivariant networks, sampling multiple candidate poses, then ranking them with a separate confidence model. **DiffDock-L** (Feb 2024) is the larger/improved successor in the *same repo* and is now the default — trained with "Confidence Bootstrapping" + the DockGen benchmark for better generalization to unseen pockets, plus a later memory-reduction update. Output is **STRUCTURE-ONLY**: 3D poses + a per-pose **confidence score**. The confidence score ranks pose quality/likelihood and is explicitly **NOT a binding affinity** — the repo FAQ says so verbatim.

- **Repo:** `gcorso/DiffDock` — https://github.com/gcorso/DiffDock (~1.5k stars; Gabriele Corso, MIT). DiffDock-L lives in this same repo (no separate repo). Forks/derivatives (not collisions): `labdao/diffdock`, the distinct `plainerman/DiffDock-Pocket` (sidechain-flexible), HF Spaces `reginabarzilaygroup/DiffDock-Web` and `simonduerr/diffdock`.
- **What it does / method:** Blind docking via diffusion over the ligand pose manifold; SE(3)-equivariant score model generates poses, separate confidence model ranks them.
- **Output:** **STRUCTURE-ONLY** (ranked 3D poses) + confidence score. **Confidence ≠ affinity** (explicitly disclaimed in the README FAQ).
- **Code license:** **MIT.** `raw.githubusercontent.com/gcorso/DiffDock/main/LICENSE` (© 2022 Gabriele Corso, Hannes Stärk, Bowen Jing).
- **Weights/model license + location:** **MIT** (verified separately). README: *"The code and model weights are released under MIT license."* Weights ship with / are handled by the repo (first run caches lookup tables); hosted demo on HF Spaces and NVIDIA BioNeMo (`build.nvidia.com/mit/diffdock`). (An old direct weights URL 404'd, issue #293 — current path is bundled/Spaces.)
- **Paper(s):** DiffDock — *DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking*, Corso, Stärk, Jing, Barzilay, Jaakkola, **ICLR 2023**, arXiv:2210.01776. DiffDock-L — *Deep Confident Steps to New Pockets: Strategies for Docking Generalization*, Corso, Deng, Polizzi, Barzilay, Jaakkola, **ICLR 2024**, arXiv:2402.18396.
- **Install:** `git clone … && conda env create --file environment.yml && conda activate diffdock`. Docker image `rbgcsail/diffdock`. Needs ESM2 embeddings (`esm2_t33_650M_UR50D`) for protein sequence input.
- **GPU needs:** GPU recommended, **runs on CPU** too (slower). No official VRAM minimum; practically a single consumer GPU (≈8–16 GB; ESM2-650M is the main memory driver).
- **Maintenance:** Latest release v1.1.3 (2024-09-04); last code push 2025-05-02; active, not archived. Corso (MIT) + Jacob Silterra (engineering).
- **Commercial-use read:** ✅ 4-layer: **code MIT** / **weights MIT** (explicitly) / **data** PDBBind-derived (PDB is public-domain; PDBBind *redistribution* terms can carry academic caveats if you redistribute the dataset itself) / **base** ESM2 (MIT, Meta). Permissive across the board; the only soft spot is PDBBind dataset terms if you redistribute training data.

## Uni-Mol Docking v2 — *deep-learning binding-pose prediction, strong on PoseBusters (poses, NOT affinity)*

> Uni-Mol Docking v2 (DP Technology) predicts a ligand's 3D **binding pose** in a protein pocket, built on the Uni-Mol SE(3) 3D representation. It emphasizes physically realistic outputs (no chirality inversions / steric clashes) and reports strong PoseBusters results (77.6% of ligands < 2.0 Å RMSD on the N=428 set; 95.29% on Astex N=85). Output is **STRUCTURE-ONLY** — the binding pose; it does **NOT** output binding affinity.

- **Repo:** `deepmodeling/Uni-Mol` — https://github.com/deepmodeling/Uni-Mol (~1.1k stars; DP Technology / Bohrium). Uni-Mol Docking v2 lives in the **`unimol_docking_v2/`** subfolder of this monorepo (which also hosts original Uni-Mol, Uni-Mol+, Uni-Mol Tools). No notable name collisions.
- **What it does / method:** Deep-learning protein-ligand docking on the Uni-Mol 3D representation; predicts ligand pose given a pocket, engineered to reduce chirality/clash errors.
- **Output:** **STRUCTURE-ONLY** (binding pose). No affinity.
- **Code license:** **MIT.** `raw.githubusercontent.com/deepmodeling/Uni-Mol/main/LICENSE` (© 2022 DP Technology).
- **Weights/model license + location:** **MIT** (project-wide; no separate restrictive model license found). Checkpoint is a **direct Dropbox download** — `unimol_docking_v2_240517.pt` (~464 MB, 2024-05-17), linked from `unimol_docking_v2/README.md`. Hosted no-install service as a **Bohrium app** (bohrium.dp.tech). Weights are on Dropbox/Bohrium, not HuggingFace.
- **Paper:** *Uni-Mol Docking V2: Towards Realistic and Accurate Binding Pose Prediction*, Alcaide et al., arXiv:2405.11769 (2024-05-20; preprint). (Predecessor: *Uni-Mol*, ICLR 2023 — distinct framework.)
- **Install:** No one-liner. From `unimol_docking_v2/`: install **Uni-Core** (DP's training lib), then `pip install rdkit-pypi==2022.9.3 biopandas==0.4.1 tqdm scikit-learn` + PyTorch; download the `.pt` checkpoint.
- **GPU needs:** Not officially specified; a CUDA GPU is expected (Uni-Core is CUDA-oriented). The 464 MB model is modest — single common GPU.
- **Maintenance:** Docking v2 released 2024-05-20; last code push 2025-05-29; active monorepo, not archived. DP Technology / DeepModeling.
- **Commercial-use read:** ✅ 4-layer: **code MIT** / **weights MIT** (no carve-out found) / **data** PoseBusters/PDBBind-style (PDB public-domain; PDBBind redistribution caveats if redistributing the set) / **base** Uni-Core + RDKit (MIT/BSD). ⚠️ Minor: confirm the **Bohrium hosted-service ToS** separately if you use DP's hosted API rather than self-hosting the MIT weights.

## NeuralPLexer — *generative diffusion co-folding; code permissive but WEIGHTS non-commercial* ⚠️

> NeuralPLexer predicts 3D protein-ligand complex structures directly from a protein **sequence** + ligand **graph (SMILES)** using a multiscale **generative diffusion** model that iteratively samples residue contact maps and all heavy-atom coordinates, capturing binding-site conformational change. Output is **STRUCTURE-ONLY** — complex structure + confidence (pLDDT/pTM-style); no affinity. The license catch: **BSD-3-Clear code, but the released weights are CC BY-NC-SA (non-commercial)** — verify before any commercial use.

- **Repo:** `zrqiao/NeuralPLexer` — https://github.com/zrqiao/NeuralPLexer (~330 stars; Zhuoran Qiao, Caltech lineage). Last push 2025-10-06, not archived. Fork (not canonical): `GsGithub17/Co-folding-NeuralPLexer`.
- **What it does / method:** Sequence + ligand graph → multiscale geometric DL + diffusion → atomistic complex; benchmarked on blind docking and flexible binding-site recovery; reported to beat AF2 on global accuracy under large conformational change.
- **Output:** **STRUCTURE-ONLY** (complex structure + confidence). No affinity.
- **Code license:** **BSD 3-Clause *Clear* License** (SPDX `BSD-3-Clause-Clear`, © 2023 California Institute of Technology; verified via GitHub `/license` API + LICENSE file). Permissive, commercial use allowed, **but the Clear variant explicitly withholds patent rights**: *"NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED."*
- **Weights/model license + location:** ⚠️ **DIFFERENT from code — NON-COMMERCIAL.** Pretrained checkpoints on Zenodo (DOI 10.5281/zenodo.10373581) under **CC BY-NC-SA 4.0** (README: *"available… for non-commercial usage under the CC BY-NC-SA 4.0 license"*). This is the binding constraint.
- **Paper:** Qiao, Nie, Vahdat, Miller, Anandkumar, *State-specific protein-ligand complex structure prediction with a multiscale deep generative model*, **Nature Machine Intelligence** 6, 195–208 (2024). DOI 10.1038/s42256-024-00792-z. Preprint arXiv:2209.15171.
- **Install:** `make environment` then `make install` (conda-based).
- **GPU needs:** README requires CUDA ≥10.2; VRAM not pinned — a mid-range NVIDIA GPU suffices for inference.
- **Maintenance:** Active-ish (last commit 2025-10-06), but core development has effectively migrated to the **closed NeuralPLexer3** (below).
- **Commercial-use read:** ⚠️ **Code ✅ permissive (BSD-3-Clear, no patent grant) / weights ❌ CC BY-NC-SA non-commercial / data PDB-derived / base standalone.** You may use the *code* commercially but the *released weights are non-commercial* — for commercial use you would retrain. The patent-rights carve-out adds risk.
  - **↳ NeuralPLexer3 — PROPRIETARY, NOT open:** *NeuralPLexer3: Accurate Biomolecular Complex Structure Prediction with Flow Models*, Qiao et al. (**Iambic Therapeutics**), arXiv:2412.10743 (Dec 2024; NeurIPS 2025 poster). A physics-inspired **flow-matching** model, AF3-class accuracy. **No model code or weights released** — Iambic's GitHub org has only `np-bench` (a *benchmark*, BSD-3-Clause); no `neuralplexer3` model repo exists. **Commercial-use read: ❌ not available** (no public artifact). See [watchlist.md](watchlist.md).

## Umol — *AF2-style co-folding from sequence; the most commercially usable co-folder here* ✅

> Umol predicts the 3D structure of a protein-ligand complex from a protein **sequence** (via MSA, no experimental structure needed) + ligand **SMILES**, using an **AlphaFold2-style** network adapted to jointly fold the protein and place the ligand. Output is **STRUCTURE-ONLY** — complex structure + plDDT-style confidence; no affinity. Notable because **both layers are commercially permissive** (Apache-2.0 code + CC BY 4.0 weights).

- **Repo:** `patrickbryant1/Umol` — https://github.com/patrickbryant1/Umol (~240 stars; Patrick Bryant). Default branch `master`; last push 2025-07-31, not archived.
- **What it does / method:** Protein MSA + ligand SMILES → AF2-style Evoformer/structure module → complex coordinates + confidence. Colab notebook available.
- **Output:** **STRUCTURE-ONLY** (complex structure + plDDT/confidence). No affinity.
- **Code license:** **Apache 2.0** — **README-stated only.** ⚠️ Verification flag: there is **NO standalone LICENSE file** (LICENSE/.md/.txt all 404; GitHub `/license` API 404, so GitHub does not auto-detect it). The Apache-2.0 grant exists only as README prose — a clear stated grant but weaker provenance than a committed file.
- **Weights/model license + location:** ✅ **CC BY 4.0 — commercially permissive (attribution only)**, verified SEPARATELY (README: *"The Umol parameters are made available under the terms of the CC BY 4.0 license"*). Checkpoints/data on Zenodo (record 10809161); weights are pulled by the install/data scripts.
- **Paper:** Bryant, Kelkar, Guljas, Clementi, Noé, *Structure prediction of protein-ligand complexes from sequence information with Umol*, **Nature Communications** 15, 4536 (2024). DOI 10.1038/s41467-024-48837-6. Preprint bioRxiv 2023.11.03.565471.
- **Install:** `bash install_dependencies.sh` (miniconda required).
- **GPU needs:** README assumes **CUDA 12** (CUDA 11 needs edits); runtime "a few minutes" on an **NVIDIA A100**. Feasible on a single modern GPU.
- **Maintenance:** Moderately maintained; last commit 2025-07-31, not archived.
- **Commercial-use read:** ✅ (with a documentation caveat). 4-layer: **code Apache-2.0** (README-stated; missing-LICENSE-file is a formality gap) / **weights CC BY 4.0** (commercial OK, attribution required) / **data PDB-derived** / **base** AF2-*style* architecture, independently trained — **no AF2-weights dependency**. The most commercially usable co-folder in this file; just provide attribution and note the missing LICENSE-file formality.

## EquiBind — *one-shot SE(3)-equivariant blind docking; fast, pose-only, legacy* (superseded by DiffDock)

> EquiBind performs **direct-shot blind docking**: in a single forward pass an SE(3)-equivariant GNN predicts both the binding location and the ligand's bound pose — no search, sampling, or scoring loop, so it is extremely fast (sub-second). Output is **STRUCTURE-ONLY** (a pose); **no affinity, no docking score**. Largely **superseded by DiffDock** from the same MIT lab lineage (Stärk/Ganea) — the README itself points to DiffDock as the successor.

- **Repo:** `HannesStark/EquiBind` — https://github.com/HannesStark/EquiBind (~545 stars; Hannes Stärk).
- **What it does / method:** SE(3)-equivariant GNN regressing a single bound complex geometry directly (keypoint alignment, no candidate enumeration).
- **Output:** **STRUCTURE-ONLY** (predicted pose, .sdf). Explicitly no affinity/score.
- **Code license:** **MIT** (LICENSE file, © 2022 Hannes Stärk; SPDX `MIT`).
- **Weights/model license + location:** Pretrained weights **bundled in-repo** (the `runs/` directory; used by `inference.py`) — no separate external host or weights license, so they ship under the repo's **MIT**. (README gives no standalone download URL — weights travel with the clone.)
- **Paper:** *EquiBind: Geometric Deep Learning for Drug Binding Structure Prediction*, Stärk, Ganea et al., **ICML 2022**, arXiv:2202.05146.
- **Install:** `git clone … && conda env create -f environment.yml` (or `environment_cpuonly.yml`) `&& conda activate equibind && python inference.py --config=configs_clean/inference.yml`.
- **GPU needs:** Modest. PyTorch 1.10 / CUDA 10.2-era; runs on a small GPU or **CPU-only** (env provided). Very low VRAM (single forward pass).
- **Maintenance:** **Legacy / minimal.** Last push 2025-02-19 (housekeeping); substantive work ended ~2022; not archived. **Superseded by DiffDock.**
- **Commercial-use read:** ✅ 4-layer: code MIT / bundled weights MIT / no field-of-use restriction / no foreign base. Permissive but stale — for production blind docking use the lab's own DiffDock (also permissive).

## TankBind — *trigonometry-aware net predicting pose AND an affinity ranking (structure + AFFINITY); legacy*

> TankBind is a trigonometry-aware neural network that predicts the binding **pose AND a binding-affinity score** in one model — its distinguishing feature versus pure pose predictors (EquiBind, DiffDock). It segments the protein into functional blocks, predicts interaction via triangle-inequality-constrained distance maps, then selects the best block/pose plus an affinity. Output: **STRUCTURE + AFFINITY** (the affinity value is usable for **ranking compounds in virtual screening**). Legacy but notable as the one *docking* (non-co-folding) tool here with an affinity head.

- **Repo:** `luwei0917/TankBind` — https://github.com/luwei0917/TankBind (~183 stars; Wei Lu / Galixir Technologies / SJTU).
- **What it does / method:** Trigonometry-aware net; predicts inter-molecular distance maps under triangle constraints, scores protein functional blocks, jointly outputs a pose + a scalar affinity.
- **Output:** **STRUCTURE + AFFINITY** (the key differentiator vs EquiBind/DiffDock). Confirmed in README.
- **Code license:** **MIT** (LICENSE file, © 2022 Wei Lu, Galixir Technologies; SPDX `MIT`). Clean MIT — not absent, not restrictive.
- **Weights/model license + location:** Pretrained checkpoints **bundled in-repo** (`saved_models/`), shipping under the repo's **MIT** (no separate Zenodo/download URL). ⚠️ The README points to a **commercial Galixir platform** (m1.galixir.com) as the "latest version" — that hosted service is separate and **not** covered by the MIT repo.
- **Paper:** *TankBind: Trigonometry-Aware Neural Networks for Drug-Protein Binding Structure Prediction*, Lu et al., **NeurIPS 2022**. Preprint bioRxiv 2022.06.06.495043 (DOI 10.1101/2022.06.06.495043).
- **Install:** `conda create -n tankbind_py38 python=3.8 && conda activate tankbind_py38`; `conda install pytorch cudatoolkit=11.3 -c pytorch`; `conda install torchdrug=0.1.2 pyg=2.1.0 biopython nglview jupyterlab -c milagraph -c conda-forge -c pytorch -c pyg`; `pip install torchmetrics tqdm mlcrate pyarrow`. (P2Rank for pocket detection in screening.)
- **GPU needs:** GPU required (CUDA 11.3-era); modest single-GPU footprint; fast inference (its screening design goal).
- **Maintenance:** **Legacy / dormant.** Last push 2023-11-01; release v0.5.0 (Jun 2022); not archived but development moved to Galixir's commercial product.
- **Commercial-use read:** ✅ (for the open repo). 4-layer: code MIT / bundled weights MIT / no field-of-use restriction / no foreign base. ⚠️ Caveats: legacy/dormant; the **dependency stack** (torchdrug 0.1.2, pyg 2.1.0, CUDA 11.3) is dated and painful to install; and the maintained "latest version" is a **commercial Galixir service** with its own non-MIT terms — do not conflate the two.

## AlphaFold 3 — *co-folds protein-ligand complexes; confidence/ranking but NO affinity; weights gated non-commercial* ❌ (covered in depth elsewhere)

> AlphaFold 3 predicts structures of biomolecular complexes — including **protein-ligand co-folding** — from sequence/ligand inputs via end-to-end generative (diffusion) structure prediction. For docking purposes it produces a predicted complex **structure plus confidence/ranking metrics** (pLDDT, PAE, pTM, ipTM, composite `ranking_score`) but **NO explicit binding-affinity value** (no Kd/IC50/pKi/ΔG). So: **STRUCTURE + CONFIDENCE/RANKING**, not affinity. Listed briefly here for the docking-relevant flag; structure prediction is covered in depth by the protein-structure layer. The critical point: **code is open (Apache 2.0) but weights are gated and strictly non-commercial.**

- **Repo:** `google-deepmind/alphafold3` — https://github.com/google-deepmind/alphafold3 (~8.2k stars). Inference-pipeline implementation.
- **What it does / method:** End-to-end model (Pairformer + diffusion) for complexes of proteins, nucleic acids, ligands, ions, modified residues. Ligand co-folding places a small molecule into the folded pocket (implicit docking/co-folding).
- **Output:** **STRUCTURE + CONFIDENCE/RANKING** (pLDDT, PAE, pTM, ipTM, `ranking_score`, `chain_pair_iptm`, `has_clash`, `contact_probs`). **No binding-affinity output** — confidence metrics rank poses but are not an affinity prediction.
- **Code license:** **Apache 2.0** — verified from LICENSE file. (NOT CC BY-NC-SA — the non-commercial restriction lives in the **weights** terms, not the code.)
- **Weights/model license + location:** ❌ **Gated + non-commercial.** Parameters are **NOT freely distributed**; access is **request-only via a Google form** (~2–3 business days) under the separate **"AlphaFold 3 Model Parameters Terms of Use."** Verified clauses: parameters/output are *"only available for non-commercial use by, or on behalf of, non-commercial organizations"*; *"must not"* use in connection with *"any commercial activities, including research on behalf of commercial organizations"*; *"must not publish or share"* the parameters (except internally); outputs *must not* be used to train competing structure-prediction models. As of 2026-06: **still request-gated, still non-commercial.**
- **Paper:** Abramson et al., *Accurate structure prediction of biomolecular interactions with AlphaFold 3*, **Nature** 630(8016):493–500 (2024). DOI 10.1038/s41586-024-07487-w.
- **Install:** Docker-based; mount downloaded parameters + genetic databases (GPU container for inference; CPU for the MSA/template pipeline).
- **GPU needs:** NVIDIA GPU for inference; large-VRAM datacenter GPUs (A100/H100 class) for sizable complexes; CPU suffices for the data-search stage.
- **Maintenance:** Actively maintained; latest release v3.0.3 (2026-06-09), not archived.
- **Commercial-use read:** ❌ **Not commercially usable as-is.** 4-layer: **code Apache 2.0** (permissive *alone*) / **weights non-commercial + request-gated + no redistribution → gates the whole pipeline for commercial users** / **output restriction** (cannot train competing structure-prediction models on AF3 output) / base N/A. **For commercial-friendly co-folding use the open reimplementations — Boltz-1/-2, Chai-1, Protenix, HelixFold3** — which target AF3-level prediction under permissive licenses (and Boltz-2 adds an affinity head, which AF3 lacks).

---

## New / notable 2026 additions

### SigmaDock — `alvaroprat97/sigmadock` *(DL docking — the new pose-quality leader)*
- **What/output:** Fragment-based **SE(3) Riemannian diffusion** docking (Oxford/OPIG). Reportedly the **first DL docker to beat classical physics-based docking on the strict PoseBusters PB-split** — Top-1 (RMSD < 2 Å **and** PB-valid) > 79.9% vs 12.7–30.8% for prior DL. **STRUCTURE-ONLY** (pose), no affinity. A real step up over DiffDock-L on physically-valid pose quality.
- **Code + weights:** **BSD-3-Clause** (commercial OK); checkpoint via GitHub Releases (same BSD-3).
- **Paper:** arXiv:2511.04854 (v1 Nov 2025; v2 Mar 2026), ICLR 2026 submission.
- **Status:** ⚠️ **Young / beta** (~9 commits; README warns APIs may change).
- **Commercial:** ✅ BSD-3 — best new docking result under a permissive license; caveat it's early.

### FlowDock — `BioinfoMachineLearning/FlowDock` *(docking + affinity)*
- **What/output:** Geometric **flow-matching** joint docking **+ binding-affinity** from apo structures; MSA-free (~51% blind docking on PoseBusters). The affinity head differentiates it from pose-only DiffDock. ⚠️ Borderline recency (preprint Dec 2024; quiet since v0.0.3, Mar 2025).
- **Code + weights:** **MIT**; checkpoints on Zenodo (MIT).
- **Paper:** arXiv:2412.10966; published ISMB 2025 (*Bioinformatics*).
- **Commercial:** ✅ MIT — a permissive structure+affinity option, but lightly maintained.

> **Read before trusting ML affinity:** *On the Reliability of AI Methods in Drug Discovery: Evaluation of Boltz-2* (arXiv:2603.05532, Mar 2026) is a sober external assessment — ML affinity (Boltz-2, FlowDock, TankBind) degrades out-of-distribution. Use it to triage, confirm with FEP ([binding-affinity-and-fep.md](binding-affinity-and-fep.md)) on the short list.

## Choosing

- **Need a binding-affinity number (virtual screening / lead-opt), commercially clean?** → **Boltz-2** (MIT code **and** MIT weights; FEP-approaching affinity). The standout pick of this file.
- **AF3-class complex *structure*, commercially clean, from sequence?** → **Boltz-1** (MIT/MIT) or **Chai-1** (Apache/Apache — confirm you're on the post-Nov-2024 release). **Umol** (Apache code + CC BY 4.0 weights) is the cleanest pure co-folder license-wise.
- **Blind docking into a known structure/pocket?** → **DiffDock-L** (MIT, diffusion, generalizes to new pockets) or **Uni-Mol Docking v2** (MIT, PoseBusters-strong, realistic poses). Both give a pose + confidence, **not affinity**.
- **Fastest possible pose, low resources / CPU OK?** → **EquiBind** (MIT, one-shot) — but legacy; prefer DiffDock unless speed is critical.
- **Pose + affinity in one *docking* model (not co-folding)?** → **TankBind** (MIT, affinity head) — legacy, dated deps, but the only docking tool here with affinity.
- **State-specific complex with large conformational change?** → **NeuralPLexer** — ⚠️ **weights are non-commercial (CC BY-NC-SA)**; commercial use needs retraining. NeuralPLexer3 is proprietary (Iambic).
- **Best raw accuracy regardless of license / research only?** → **AlphaFold 3** — ❌ commercial use blocked (gated non-commercial weights); use a Boltz/Chai/Protenix reimplementation if you need to ship.

**Affinity vs structure, at a glance:** only **Boltz-2** (numerical, FEP-approaching) and **TankBind** (ranking-grade) predict **binding affinity**. Everything else is **structure + a confidence score** — and **confidence ≠ affinity**. Don't rank compounds by DiffDock confidence or AF3 ipTM as if it were ΔG.

**License pattern to remember (mirror of the Enamine trap in the synthesizability files):** on co-folding models, **read the weights license separately from the code.** Boltz-1/-2 = MIT/MIT (clean). Chai-1 = Apache/Apache *now* (was non-commercial weights until Nov 2024 — stale sources are wrong). Umol = Apache/CC BY 4.0 (clean). NeuralPLexer = permissive code but **CC BY-NC-SA weights** (the catch). AF3 = Apache code but **gated non-commercial weights** (the hard block). See [licensing-and-data.md](licensing-and-data.md) for the four-layer checklist.
