# Docking and Co-Folding

Docking and co-folding predict complex geometry. They help you assess a
ligand **pose**, not whether a compound binds at a measured affinity. The tools
fall into three families:

- **Classical or physics-based docking** searches poses in a defined protein
  pocket and scores them with an empirical or force-field function. Examples
  include AutoDock Vina, smina, gnina, QuickVina, Vina-GPU, AutoDock-GPU,
  RxDock, and DOCK6.
- **Learned docking** predicts the bound pose from a protein structure or
  pocket and a ligand. Examples include DiffDock-L, Uni-Mol Docking v2,
  EquiBind, and TankBind.
- **Co-folding** predicts the protein structure and ligand pose from sequence
  and ligand inputs. Examples include Boltz-1, Boltz-2, Chai-1, NeuralPLexer,
  Umol, and AlphaFold 3.

Classical and learned docking require a protein structure from the PDB or a
method in [protein-structure-prediction.md](protein-structure-prediction.md).
They also require a pocket, which you can define with a detector in
[structure-based-generation.md](structure-based-generation.md).

Most learned docking and co-folding tools return **structure plus confidence**.
A confidence value ranks predicted structures; it does not estimate binding
affinity. Boltz-2, TankBind, and FlowDock add affinity heads, but their values
remain model estimates. Classical docking scores are empirical scoring
functions, not free-energy calculations. Use [binding-affinity-and-fep.md](binding-affinity-and-fep.md)
for affinity workflows.

Check code, released weights, training data, and hosted-service terms
separately. gnina's pretrained CNN weights lack stated terms, NeuralPLexer
weights are CC BY-NC-SA 4.0, and AlphaFold 3 parameters are request-gated under
separate terms.

---

## Classical or Physics-Based Docking

These tools require a protein structure and a defined pocket. Most run on CPUs
and use Apache, MIT, BSD, or LGPL code. gnina's pretrained CNN weights are an
exception; check their separate terms.

### AutoDock Vina — `ccsb-scripps/AutoDock-Vina`
- **Method and output:** physics-based empirical scoring (Vina + optional AD4 force field); pose + estimated affinity (kcal/mol). The field's default engine.
- **Code:** **Apache-2.0.** No ML weights.
- **Paper:** Eberhardt et al. (Vina 1.2.0), *JCIM* 61:3891, 2021. DOI 10.1021/acs.jcim.1c00203 (orig. Trott & Olson 2010, DOI 10.1002/jcc.21334).
- **Installation and hardware:** `pip install vina` / conda / binaries. **CPU** (multithreaded). Active — v1.2.x (2025).
- **Terms:** Source code is Apache-2.0.

### AutoDock-GPU — `ccsb-scripps/AutoDock-GPU`
- **Method:** GPU (CUDA/OpenCL) reimplementation of **AutoDock4.2** (lattice-grid, AD4 force field) with gradient local search. Accelerates AD4, not the Vina scorer.
- **Code:** ⚠️ The distribution includes **GPL-2.0** code and a secondary LGPL file. OpenBabel components have separate terms; check the files included in the build you distribute.
- **Paper:** Santos-Martins et al., *JCTC* 17(2):1060, 2021. DOI 10.1021/acs.jctc.0c01006.
- **Installation and hardware:** compile (`make DEVICE=CUDA`); needs Meeko + AutoGrid. **GPU required.** Active — v1.6 (2024).
- **Terms:** Source code is GPL-2.0.

### smina — `mwojcikowski/smina` *(GitHub mirror; canonical home SourceForge)*
- **Method:** Vina fork for improved empirical scoring/minimization + user-defined scoring functions; OpenBabel I/O.
- **Code:** **Dual Apache-2.0 + GPL-2.0** (GPL via OpenBabel = effective distribution constraint).
- **Paper:** Koes et al., *JCIM* 53(8):1893, 2013. DOI 10.1021/ci300604z.
- **Installation and hardware:** `conda install -c conda-forge smina` / static binary. **CPU.** ⚠️ **Dormant** (mirror frozen ~2018) — gnina is the maintained successor.
- **Terms:** The distribution includes Apache-2.0 and GPL-2.0 components through OpenBabel.

### gnina — `gnina/gnina` (code) + `gnina/models` (weights) ⚠️
- **Method:** Vina/smina fork that **rescores poses with an ensemble of CNNs**; v1.3 adds covalent docking + PyTorch.
- **Code:** **Dual Apache-2.0 + GPL-2.0** (GPL via OpenBabel; effective = GPL-2.0).
- **Weights:** The pretrained CNN weights in `gnina/models` do not state a license. They have CrossDocked2020/PDBbind provenance; the code license does not cover the weights.
- **Paper:** McNutt et al. (GNINA 1.3), *J. Cheminform.* 17:28, 2025. DOI 10.1186/s13321-025-00973-x.
- **Installation and hardware:** prebuilt binary (weights baked in) / source / Docker. **GPU strongly recommended** (CUDA). Active — v1.3.x (2025).
- **Terms:** Code includes GPL-2.0 components. The default CNN weights do not state terms, and the cited training-data provenance has separate terms.

### QuickVina 2 / QuickVina-W — `QVina/qvina`
- **Method:** speed-optimized Vina forks; QuickVina-W is tuned for whole-surface docking. Empirical Vina scoring.
- **Code:** **Apache-2.0.**
- **Paper:** Alhossary et al., *Bioinformatics* 31(13):2214, 2015. DOI 10.1093/bioinformatics/btv082 (QVina-W: Hassan et al., *Sci. Rep.* 7:15451, 2017).
- **Installation and hardware:** source/binaries. **CPU.** Dormant but stable (2023).
- **Terms:** Source code is Apache-2.0.

### Vina-GPU 2.1 — `DeltaGroupNJUPT/Vina-GPU-2.1`
- **Method:** OpenCL GPU acceleration of Vina + derivatives (bundles AutoDock-Vina-GPU, QuickVina2-GPU, QuickVina-W-GPU 2.1).
- **Code:** **Apache-2.0.**
- **Paper:** Tang et al., *IEEE/ACM TCBB* 2024. DOI 10.1109/TCBB.2024.3467127.
- **Installation and hardware:** source + OpenCL SDK + boost. **GPU required** (OpenCL; best on NVIDIA). Stable (2024).
- **Terms:** Source code is Apache-2.0.

### RxDock — GitLab `rxdock/rxdock` *(maintained fork of rDock)*
- **Method:** fast docking to **proteins *and* nucleic acids** (notably RNA); empirical scoring + GA sampling, HTVS-oriented. Original rDock died ~2014.
- **Code:** **LGPL-3.0** (weak copyleft).
- **Paper:** (rDock) Ruiz-Carmona et al., *PLoS Comput. Biol.* 10(4):e1003571, 2014. DOI 10.1371/journal.pcbi.1003571.
- **Installation and hardware:** `conda install -c bioconda rxdock`. **CPU.** ⚠️ Semi-dormant (v0.1.0, best-effort).
- **Terms:** Source code is LGPL-3.0.

### DOCK6 — `docking-org/dock6` and the UCSF Portal ⚠️
- **Method:** classic anchor-and-grow flexible docking + GB/SA scoring (UCSF). Physics-based.
- **Code:** The `docking-org/dock6` GitHub repository is **BSD-3-Clause**. Material distributed through the UCSF web portal has a separate academic-only EULA.
- **Paper:** Allen et al., *JCC* 36(15):1132, 2015. DOI 10.1002/jcc.23905.
- **Installation and hardware:** clone + build, or UCSF portal. **CPU** (MPI). Active (DOCK 6.12/6.13, 2026).
- **Terms:** GitHub source is BSD-3-Clause; UCSF portal material is governed by its separate EULA.

### Meeko — `forlilab/Meeko`
- **Method:** ligand/receptor **prep** (SMILES/SDF → PDBQT, macrocycle/flex-residue handling, RDKit interop) for the AutoDock family. Companion, not a docking engine.
- **Code:** **LGPL-2.1.**
- **Paper:** Forli Lab, *ChemRxiv* 2025. DOI 10.26434/chemrxiv-2025-6b37n.
- **Installation and hardware:** `pip install meeko` or use conda. **CPU.** Maintained.
- **Terms:** Source code is LGPL-2.1.

### RTMScore — `sc8668/RTMScore`
- **Method:** ML **rescoring** (graph-transformer + mixture-density net → residue–atom distance-likelihood potential) to rerank Vina/gnina poses + boost VS enrichment.
- **Code and weights:** **MIT.** Weights are bundled in the repository under the same license.
- **Paper:** Shen et al., *J. Med. Chem.* 65(15):10691, 2022. DOI 10.1021/acs.jmedchem.2c00991.
- **Installation and hardware:** git (PyTorch + DGL + RDKit). GPU recommended. Dormant (2023) but stable.
- **Terms:** Source code and bundled weights are MIT. PDBbind provenance has separate data terms.

> **PLANTS** (ant-colony docking) is distributed as an academic binary; no public source repository is listed. See [watchlist.md](watchlist.md).

---

**Deep-learning docking and co-folding** predict poses or full complex
structures. Check released model artifacts separately from the code.

## Boltz-2 — *co-folding with an ML affinity estimate*

> Boltz-2 jointly predicts complex structure, a binder probability, and an
> affinity estimate. `affinity_pred_value` reports log10(IC50), with IC50 in
> µM. Use it to prioritize candidates, then confirm important decisions with
> an appropriate free-energy calculation or experiment.

- **Repository:** `jwohlwend/boltz` — https://github.com/jwohlwend/boltz. The repository contains Boltz-1 and Boltz-2.
- **Method and output:** AlphaFold3-family co-folding model with an affinity head. It requires an MSA.
- **Output:** **Structure and affinity.** It returns a complex, `affinity_pred_value`, and `affinity_probability_binary`.
- **Code license:** **MIT.** See the repository [license](https://github.com/jwohlwend/boltz/blob/main/LICENSE).
- **Weights and model license:** **MIT.** The [Boltz-2 model card](https://huggingface.co/boltz-community/boltz-2) states `license: mit`.
- **Paper:** *Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction*, Passaro, Corso, Wohlwend et al. (MIT + Recursion). bioRxiv 2025-06-18. DOI 10.1101/2025.06.14.659707 (PMC12262699).
- **Install:** `pip install boltz[cuda] -U` (same package as Boltz-1; the CLI selects Boltz-2 weights).
- **Hardware:** High-memory GPU recommended; requirements vary with complex size and whether the affinity module is enabled.
- **Maintenance:** v2.2.1 (verified 2026-08-30).
- **Terms:** Code and released weights are MIT. Evaluate affinity estimates on task-relevant held-out data.

## Boltz-1 — *structure-only co-folding*

> Boltz-1 predicts structures of complexes containing proteins, RNA, DNA, and
> small molecules. It returns coordinates but no affinity estimate.

- **Repository:** `jwohlwend/boltz` — https://github.com/jwohlwend/boltz (the same repository as Boltz-2).
- **Method and output:** AlphaFold3-family co-folding model that requires an MSA.
- **Output:** **STRUCTURE-ONLY.** No affinity head.
- **Code license:** **MIT** (same LICENSE file as Boltz-2).
- **Weights and model license:** **MIT.** The [Boltz-1 model card](https://huggingface.co/boltz-community/boltz-1) lists `license: mit`.
- **Paper:** *Boltz-1: Democratizing Biomolecular Interaction Modeling*, Wohlwend, Corso, Passaro et al. bioRxiv 2024-11-20. DOI 10.1101/2024.11.19.624167. (Not yet journal-published.)
- **Install:** `pip install boltz[cuda] -U` (drop `[cuda]` for CPU).
- **Hardware:** GPU memory requirements increase with complex size.
- **Maintenance:** v2.2.1 (verified 2026-08-30).
- **Terms:** Code and released weights are MIT. Boltz-1 produces structure, not an affinity estimate.

## Chai-1 — *AF3-class foundation model; Apache-2.0 code and weights (structure only)*

> Chai-1 predicts structures of proteins, ligands, nucleic acids,
> glycosylations, and covalent modifications. It returns coordinates and pTM,
> ipTM, and PAE-style confidence, not an affinity estimate.

- **Repository:** `chaidiscovery/chai-lab` — https://github.com/chaidiscovery/chai-lab.
- **Method and output:** AF3-class diffusion all-atom structure predictor across proteins + ligands + nucleic acids + modifications; optional restraint conditioning; optional MSA-free mode. MSAs via MMseqs2/ColabFold server when used.
- **Code license:** **Apache-2.0.** The repository has a single root `LICENSE` file.
- **Weights and model license:** The `chai-lab` repository states Apache-2.0 terms for code and model weights. Earlier releases used different parameter terms. The paper is CC BY-NC.
- **Paper:** *Chai-1: Decoding the molecular interactions of life*, Chai Discovery team (corresp. Joshua Meier). bioRxiv 2024-10-11. DOI 10.1101/2024.10.10.615955. (Tech report; not peer-reviewed.)
- **Install:** `pip install chai_lab==0.6.1` (or `pip install git+https://github.com/chaidiscovery/chai-lab.git`). CLI: `chai fold`.
- **Hardware:** Linux, Python ≥3.10, CUDA GPU with bf16. Recommended A100/H100 80GB or **L40S 48GB**; A10/A30 and RTX 4090 work for smaller complexes. VRAM scales with complex size (AF3-class profile).
- **Maintenance:** v0.6.1; public commits continued through April 2026.
- **Terms:** Current Chai-1 code and weights are Apache-2.0. MSA services and any reference data have separate terms.

## DiffDock and DiffDock-L — *diffusion docking with pose confidence*

> DiffDock uses an SE(3)-equivariant diffusion model to sample ligand
> translation, rotation, and torsion. DiffDock-L is the larger successor in the
> same repository. It returns ranked three-dimensional poses and confidence
> values, not affinity estimates.

- **Repository:** `gcorso/DiffDock` — https://github.com/gcorso/DiffDock. DiffDock-L is in the same repository.
- **Method and output:** The score model generates poses, and a separate confidence model ranks them.
- **Code license:** **MIT.** `raw.githubusercontent.com/gcorso/DiffDock/main/LICENSE` (© 2022 Gabriele Corso, Hannes Stärk, Bowen Jing).
- **Weights and model license:** **MIT.** The README states that code and model weights are MIT.
- **Papers:** DiffDock — *DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking*, Corso, Stärk, Jing, Barzilay, Jaakkola, **ICLR 2023**, arXiv:2210.01776. DiffDock-L — *Deep Confident Steps to New Pockets: Strategies for Docking Generalization*, Corso, Deng, Polizzi, Barzilay, Jaakkola, **ICLR 2024**, arXiv:2402.18396.
- **Install:** `git clone … && conda env create --file environment.yml && conda activate diffdock`. Docker image `rbgcsail/diffdock`. Needs ESM2 embeddings (`esm2_t33_650M_UR50D`) for protein sequence input.
- **Hardware:** GPU recommended, **runs on CPU** too (slower). No official VRAM minimum; practically a single consumer GPU (≈8–16 GB; ESM2-650M is the main memory driver).
- **Maintenance:** v1.1.3 was released on 2024-09-04; public code activity continued through May 2025.
- **Terms:** Code and weights are MIT. PDBbind-derived data and the ESM2 base model have separate terms.

## Uni-Mol Docking v2 — *deep-learning binding-pose prediction, strong on PoseBusters (poses, NOT affinity)*

> Uni-Mol Docking v2 (DP Technology) predicts a ligand's 3D **binding pose** in a protein pocket, built on the Uni-Mol SE(3) 3D representation. It emphasizes physically realistic outputs (no chirality inversions / steric clashes) and reports strong PoseBusters results (77.6% of ligands < 2.0 Å RMSD on the N=428 set; 95.29% on Astex N=85). Output is **STRUCTURE-ONLY** — the binding pose; it does **NOT** output binding affinity.

- **Repository:** `deepmodeling/Uni-Mol` — https://github.com/deepmodeling/Uni-Mol. Uni-Mol Docking v2 is in the `unimol_docking_v2/` subdirectory.
- **Method and output:** Deep-learning protein-ligand docking on the Uni-Mol 3D representation; predicts ligand pose given a pocket, engineered to reduce chirality/clash errors.
- **Output:** **STRUCTURE-ONLY** (binding pose). No affinity.
- **Code license:** **MIT.** `raw.githubusercontent.com/deepmodeling/Uni-Mol/main/LICENSE` (© 2022 DP Technology).
- **Weights and model license:** **MIT** at the project level; no separate model license is stated. The checkpoint is linked from `unimol_docking_v2/README.md`.
- **Paper:** *Uni-Mol Docking V2: Towards Realistic and Accurate Binding Pose Prediction*, Alcaide et al., arXiv:2405.11769 (2024-05-20; preprint). (Predecessor: *Uni-Mol*, ICLR 2023 — distinct framework.)
- **Install:** No one-liner. From `unimol_docking_v2/`: install **Uni-Core** (DP's training lib), then `pip install rdkit-pypi==2022.9.3 biopandas==0.4.1 tqdm scikit-learn` + PyTorch; download the `.pt` checkpoint.
- **Hardware:** Not officially specified; a CUDA GPU is expected (Uni-Core is CUDA-oriented). The 464 MB model is modest — single common GPU.
- **Maintenance:** Docking v2 was released 2024-05-20; public code activity continued through May 2025.
- **Terms:** Code and listed weights are MIT. PoseBusters/PDBbind-style data, Uni-Core, and RDKit have separate terms.

## NeuralPLexer — *generative diffusion co-folding; BSD-3-Clear code and CC BY-NC-SA weights*

> NeuralPLexer predicts 3D protein-ligand complex structures directly from a protein **sequence** and ligand **graph (SMILES)** using a multiscale generative-diffusion model. Output is **STRUCTURE-ONLY**: complex structure plus pLDDT/pTM-style confidence, not affinity. The source code is BSD-3-Clear; released weights are CC BY-NC-SA 4.0.

- **Repository:** `zrqiao/NeuralPLexer` — https://github.com/zrqiao/NeuralPLexer. Public code activity continued through October 2025.
- **Method and output:** Sequence + ligand graph → multiscale geometric DL + diffusion → atomistic complex; benchmarked on blind docking and flexible binding-site recovery; reported to beat AF2 on global accuracy under large conformational change.
- **Output:** **STRUCTURE-ONLY** (complex structure + confidence). No affinity.
- **Code license:** **BSD-3-Clause-Clear.** Its text includes no patent grant.
- **Weights and model license:** Released checkpoints on Zenodo (DOI 10.5281/zenodo.10373581) are **CC BY-NC-SA 4.0**.
- **Paper:** Qiao, Nie, Vahdat, Miller, Anandkumar, *State-specific protein-ligand complex structure prediction with a multiscale deep generative model*, **Nature Machine Intelligence** 6, 195–208 (2024). DOI 10.1038/s42256-024-00792-z. Preprint arXiv:2209.15171.
- **Install:** `make environment` then `make install` (conda-based).
- **Hardware:** README requires CUDA ≥10.2; VRAM not pinned — a mid-range NVIDIA GPU suffices for inference.
- **Maintenance:** Public code activity continued through October 2025.
- **Terms:** Source code is BSD-3-Clause-Clear; released weights are CC BY-NC-SA 4.0. PDB-derived data have separate terms.

## Umol — *AF2-style co-folding from sequence; Apache-2.0 code and CC BY 4.0 weights*

> Umol predicts a 3D protein-ligand complex from a protein **sequence** (via MSA) and ligand **SMILES** using an AlphaFold2-style network. Output is **STRUCTURE-ONLY**: complex structure plus plDDT-style confidence, not affinity. The README states Apache-2.0 code terms and CC BY 4.0 parameter terms.

- **Repository:** `patrickbryant1/Umol` — https://github.com/patrickbryant1/Umol. Public code activity continued through July 2025.
- **Method and output:** Protein MSA + ligand SMILES → AF2-style Evoformer/structure module → complex coordinates + confidence. Colab notebook available.
- **Output:** **STRUCTURE-ONLY** (complex structure + plDDT/confidence). No affinity.
- **Code license:** **Apache-2.0, README-stated.** The repository has no standalone `LICENSE` file.
- **Weights and model license:** **CC BY 4.0**, as stated in the README. Checkpoints and data are on Zenodo (record 10809161).
- **Paper:** Bryant, Kelkar, Guljas, Clementi, Noé, *Structure prediction of protein-ligand complexes from sequence information with Umol*, **Nature Communications** 15, 4536 (2024). DOI 10.1038/s41467-024-48837-6. Preprint bioRxiv 2023.11.03.565471.
- **Install:** `bash install_dependencies.sh` (miniconda required).
- **Hardware:** README assumes **CUDA 12** (CUDA 11 needs edits); runtime "a few minutes" on an **NVIDIA A100**. Feasible on a single modern GPU.
- **Maintenance:** Public code activity continued through July 2025.
- **Terms:** The README states Apache-2.0 code terms and CC BY 4.0 weight terms. The repository does not contain a standalone license file; PDB-derived data have separate terms.

## EquiBind — *one-shot SE(3)-equivariant blind docking; fast, pose-only, legacy* (superseded by DiffDock)

> EquiBind performs **direct-shot blind docking**: in a single forward pass an SE(3)-equivariant GNN predicts both the binding location and the ligand's bound pose — no search, sampling, or scoring loop, so it is extremely fast (sub-second). Output is **STRUCTURE-ONLY** (a pose); **no affinity, no docking score**. Largely **superseded by DiffDock** from the same MIT lab lineage (Stärk/Ganea) — the README itself points to DiffDock as the successor.

- **Repository:** `HannesStark/EquiBind` — https://github.com/HannesStark/EquiBind (Hannes Stärk).
- **Method and output:** SE(3)-equivariant GNN regressing a single bound complex geometry directly (keypoint alignment, no candidate enumeration).
- **Output:** **STRUCTURE-ONLY** (predicted pose, .sdf). Explicitly no affinity/score.
- **Code license:** **MIT** (LICENSE file, © 2022 Hannes Stärk; SPDX `MIT`).
- **Weights and model license:** Pretrained weights are bundled in the `runs/` directory. No separate weights license is stated; they are distributed with the MIT repository.
- **Paper:** *EquiBind: Geometric Deep Learning for Drug Binding Structure Prediction*, Stärk, Ganea et al., **ICML 2022**, arXiv:2202.05146.
- **Install:** `git clone … && conda env create -f environment.yml` (or `environment_cpuonly.yml`) `&& conda activate equibind && python inference.py --config=configs_clean/inference.yml`.
- **Hardware:** PyTorch 1.10 and CUDA 10.2; runs on a small GPU or with the provided **CPU-only** environment. Inference uses a single forward pass.
- **Maintenance:** **Legacy / minimal.** Last push 2025-02-19 (housekeeping); substantive work ended ~2022; not archived. **Superseded by DiffDock.**
- **Terms:** Source code and bundled weights are MIT. The repository is legacy; DiffDock is the documented successor.

## TankBind — *pose and affinity prediction; legacy*

> TankBind predicts a binding pose and an affinity score. It uses protein
> functional blocks and triangle-constrained distance maps. Its affinity score
> is a model estimate, not a measurement.

- **Repository:** `luwei0917/TankBind` — https://github.com/luwei0917/TankBind (Wei Lu, Galixir Technologies, and SJTU).
- **Method and output:** Trigonometry-aware net; predicts inter-molecular distance maps under triangle constraints, scores protein functional blocks, jointly outputs a pose + a scalar affinity.
- **Output:** **STRUCTURE + AFFINITY**; EquiBind and DiffDock return structure
  and confidence without an affinity output.
- **Code license:** **MIT.**
- **Weights and model license:** Pretrained checkpoints are bundled in `saved_models/` and have no separately stated license. A separate hosted service is not covered by the MIT repository terms.
- **Paper:** *TankBind: Trigonometry-Aware Neural Networks for Drug-Protein Binding Structure Prediction*, Lu et al., **NeurIPS 2022**. Preprint bioRxiv 2022.06.06.495043 (DOI 10.1101/2022.06.06.495043).
- **Install:** `conda create -n tankbind_py38 python=3.8 && conda activate tankbind_py38`; `conda install pytorch cudatoolkit=11.3 -c pytorch`; `conda install torchdrug=0.1.2 pyg=2.1.0 biopython nglview jupyterlab -c milagraph -c conda-forge -c pytorch -c pyg`; `pip install torchmetrics tqdm mlcrate pyarrow`. (P2Rank for pocket detection in screening.)
- **Hardware:** GPU required (CUDA 11.3-era); modest single-GPU footprint; fast inference (its screening design goal).
- **Maintenance:** Legacy and dormant. The last public push was 2023-11-01; v0.5.0 was released in June 2022.
- **Terms:** Source code and bundled weights are MIT. The dependency stack is dated, and the separate hosted service has its own terms.

## AlphaFold 3 — *co-folds protein-ligand complexes; confidence/ranking, not affinity*

> AlphaFold 3 predicts structures of biomolecular complexes, including **protein-ligand co-folding**, from sequence and ligand inputs. It produces **structure plus confidence/ranking metrics** (pLDDT, PAE, pTM, ipTM, and `ranking_score`), not Kd, IC50, pKi, or ΔG. Source code is Apache-2.0; released parameters are request-gated under separate non-commercial terms. See [protein-structure-prediction.md](protein-structure-prediction.md) for the full card.

- **Repository:** `google-deepmind/alphafold3` — https://github.com/google-deepmind/alphafold3.
- **Method and output:** Pairformer and diffusion model for complexes of proteins, nucleic acids, ligands, ions, and modified residues. Ligand co-folding places a small molecule into the folded pocket.
- **Output:** **STRUCTURE + CONFIDENCE/RANKING** (pLDDT, PAE, pTM, ipTM, `ranking_score`, `chain_pair_iptm`, `has_clash`, `contact_probs`). **No binding-affinity output** — confidence metrics rank poses but are not an affinity prediction.
- **Code license:** **Apache-2.0.** The parameter terms are separate from the code license.
- **Weights and model license:** Parameters are request-gated under the [AlphaFold 3 Model Parameters Terms of Use](https://github.com/google-deepmind/alphafold3/blob/main/WEIGHTS_TERMS_OF_USE.md). The terms restrict commercial use and redistribution of the released parameters, as well as specified uses of their outputs.
- **Paper:** Abramson et al., *Accurate structure prediction of biomolecular interactions with AlphaFold 3*, **Nature** 630(8016):493–500 (2024). DOI 10.1038/s41586-024-07487-w.
- **Install:** Docker-based; mount downloaded parameters + genetic databases (GPU container for inference; CPU for the MSA/template pipeline).
- **Hardware:** NVIDIA GPU for inference; large-VRAM datacenter GPUs (A100/H100 class) for sizable complexes; CPU suffices for the data-search stage.
- **Maintenance:** v3.0.2 was released on 2026-04-20.
- **Terms:** Source code is Apache-2.0; released parameters are governed by the separate linked terms.

---

## 2026 Additions

### OpenBind-0 — `aqlaboratory/openfold-3` *(protein-ligand co-folding)*
- **Method and output:** OpenBind-0 is a protein-small-molecule co-folding parameter set built on the forthcoming OpenFold3 architecture. It predicts complex structures and ranks them with structure-confidence metrics. The public release does not describe an affinity head.
- **Code, weights, and data:** **Apache-2.0.** The release states that it includes code, model parameters, training data, and training recipes under Apache-2.0.
- **Evidence:** Released on 2026-08-21, with a training cutoff of 2025-06-30. The public benchmark reports target-dependent performance and weak pose success on several flexible systems.
- **Status:** OpenBind-0 is the default parameter set for OpenFold3 >=0.5.0. OpenFold3-preview2 parameters require an older compatible package release.
- **Terms:** OpenBind-0 states Apache-2.0 terms for code, parameters, training data, and recipes. Other OpenFold3 parameter sets can have different terms.

### SigmaDock — `alvaroprat97/sigmadock` *(DL docking; pose quality)*
- **Method and output:** Fragment-based **SE(3) Riemannian diffusion** docking (Oxford/OPIG). The authors report 79.9% Top-1 success (RMSD <2 Å and PoseBusters-valid) on the PB-split. Output is **STRUCTURE-ONLY**: pose, not affinity.
- **Code and weights:** **BSD-3-Clause.** The checkpoint is published through GitHub Releases under the same terms.
- **Paper:** arXiv:2511.04854 (v1 Nov 2025; v2 Mar 2026), ICLR 2026 submission.
- **Status:** ⚠️ **Beta.** The README warns that APIs can change.
- **Terms:** Source code and the listed checkpoint are BSD-3-Clause; the API is still marked as subject to change.

### FlowDock — `BioinfoMachineLearning/FlowDock` *(docking + affinity)*
- **Method and output:** Geometric flow-matching model for joint docking and binding-affinity prediction from apo structures. It is MSA-free; the paper reports approximately 51% blind-docking success on PoseBusters.
- **Code and weights:** **MIT**; checkpoints on Zenodo (MIT).
- **Paper:** arXiv:2412.10966; published ISMB 2025 (*Bioinformatics*).
- **Terms:** Source code and the listed Zenodo checkpoints are MIT. The repository is lightly maintained.

> The 2026 evaluation of Boltz-2, *On the Reliability of AI Methods in Drug
> Discovery* (arXiv:2603.05532), reports reduced affinity performance outside
> its evaluated domain. Confirm important rankings with FEP or experiments.

## Choosing

| Need | Start with | Limits and terms |
|---|---|---|
| Binding-affinity estimate for screening or lead optimization | **Boltz-2** | MIT code and weights; model estimate that requires validation |
| Protein-ligand complex from sequence | **OpenBind-0**, **Boltz-1**, **Chai-1**, or **Protenix** | Check code, parameter, and data terms for the selected release |
| Docking into a known structure or pocket | **DiffDock-L** or **Uni-Mol Docking v2** | Returns pose and confidence, not affinity |
| Pose prediction with limited compute | **EquiBind** | MIT; legacy repository |
| Pose and affinity from one docking model | **TankBind** | MIT; legacy dependency stack |
| State-specific complex with a large conformational change | **NeuralPLexer** | Released weights use CC BY-NC-SA 4.0 |
| AlphaFold 3 complex prediction | **AlphaFold 3** | Released parameters are request-gated under non-commercial terms |

**Affinity compared with structure:** Boltz-2, TankBind, and FlowDock return affinity
predictions. DiffDock confidence, AlphaFold 3 ipTM, and OpenBind-0 structure
confidence rank structural hypotheses; they are not ΔG, Kd, IC50, or pKi.

For co-folding tools, read the weights license separately from the code.
Boltz-1/-2 use MIT terms, Chai-1 uses Apache-2.0, Umol uses Apache-2.0 code
and CC BY 4.0 weights, NeuralPLexer weights are CC BY-NC-SA, and AlphaFold 3
parameters are request-gated and non-commercial. See
[licensing-and-data.md](licensing-and-data.md) for the four-layer checklist.
