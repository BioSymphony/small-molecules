# Molecular Potentials And Simulation

Choose a potential for energies and atomic forces, an MD engine for integrating
motion, or a generative model for structural ensembles. These outputs answer
different questions. A single-point energy or sampled ensemble does not supply
a binding free energy without a defined thermodynamic calculation.

Sources and artifact terms reviewed **2026-11-15**.

## Choosing

| Task | Starting Point | Inputs And Outputs |
|---|---|---|
| Organic-molecule energy and forces | AIMNet2 | Elements, coordinates, charge → energy and forces |
| Broad-element molecular potential | HyFF | Elements, coordinates, charge, spin → energy and forces |
| Biomolecular potential with released configuration | UBio-MolFM V1.5 | Matching checkpoint/configuration and geometry → energy and forces |
| Bonded mechanics with a learned correction | ResFF | Molecular graph and geometry → combined potential |
| ML or mixed ML/MM simulation | OpenMM-ML | Topology, selected potential, optional MM system → OpenMM System |
| Batched optimization, dynamics, or distillation | ALCHEMI Toolkit | User-selected models and atomic data → optimized structures, trajectories, or trained models |
| Partner-conditioned conformational ensemble | OriDynamics | Molecular composition and MSAs → unordered all-atom conformations |
| Ensemble sampling or learned lagged endpoints | BioEmu-2 | Molecular system, optional starting frames → sampled structures |

## Energies And Forces

### AIMNet2 — Charge-Aware Molecular Potentials

[AIMNet2](https://github.com/isayevlab/aimnetcentral) accepts atomic numbers,
coordinates in Å, and charge. Its calculator returns energies in eV and forces
in eV/Å, with additional charge, stress, and Hessian interfaces. Install `aimnet`;
use the `ase` extra for an ASE calculator.

The general `aimnet2` family covers H, B, C, N, O, F, Si, P, S, Cl, As, Se, Br,
and I. Other families have different element coverage and reference methods.
The short alias selects **member 0** of a four-member family; it does not
average the ensemble. Record the resolved model name and member.

Source is [MIT](https://github.com/isayevlab/aimnetcentral/blob/main/LICENSE).
The [ωB97M-D3 checkpoint card](https://huggingface.co/isayevlab/aimnet2-wb97m-d3)
also declares MIT. Check each alternative checkpoint and training dataset
separately. Gas-phase calculations omit solvent contributions; choose a
reference method and environment that match the task.

### HyFF — Broad-Element Energy And Force Models

[HyFF](https://github.com/Tencent-Hunyuan/Hyra-results/tree/main/AI4Science/hyff)
provides five OMol25-trained potentials, ranging from 2.31 million to 1.20
billion parameters. The interface takes elements, coordinates, total charge,
and spin multiplicity, with an optional periodic cell. It returns energy in eV
and forces in eV/Å. The release describes coverage of 83 elements, H through Bi.

Install the `AI4Science/hyff` subpackage using its README. `hyff models` lists
available variants; the package downloads the selected weights on demand.
Use the single-structure interface for initial checks, then its engine or ASE
interface for repeated evaluations. Match the CPU or CUDA installation to the
selected operation.

The README states Apache-2.0 and links the repository license; weights are
published in the [HyFF release](https://github.com/Tencent-Hunyuan/Hyra-results/releases/tag/hyff-v0.2.0).
OMol25 data and dependencies retain separate terms. Published speed and error
figures apply to the authors' systems and reference calculations.

### UBio-MolFM V1.5 — Biomolecular Potential

[UBio-MolFM](https://github.com/IQuestLab/UBio-MolFM) provides energy, force,
relaxation, and dynamics interfaces for molecular systems. The
[V1.5 release](https://huggingface.co/IQuestLab/IQuest-UBio-MolFM-V1.5) supplies
`molfm-v1p5-stage-3.pt` and a matching flattened `config.yaml`. Download both.

Use the supplied Python 3.12 environment; the README specifies PyTorch 2.8.0
and CUDA 12.8 with matching PyG and FAISS builds. Its ASE interface returns
energies and forces; GPU-native dynamics can write HDF5 trajectories.
The README warns that `strict=False` checkpoint loading can silently retain
randomly initialized parameters when architecture and configuration differ.
Verify the configuration and loaded parameter keys before evaluating a system.

The source is MIT, and the model card states MIT for the model, companion data,
and associated code. Upstream training datasets retain their own terms.
Check supported elements, charge/spin treatment, and periodic settings for the
selected configuration before extending the model to new chemistry.

### ResFF — Bonded Mechanics With A Neural Residual

[ResFF](https://github.com/Ameki0/ResFF) combines learned bonded force-field
terms with a neural residual. Molecular connectivity and atom ordering are
part of its input contract. The repository includes pretrained weights,
optimization examples, and an OpenMM protein–ligand example. Use its pinned
environment: the published recipe includes Python 3.9-era PyTorch/DGL builds
and OpenMM 7.7.

In the [protein–ligand example](https://github.com/Ameki0/ResFF/blob/main/scripts/openmm-interface/run_simulation.py),
the learned component applies to the ligand;
conventional terms handle the surrounding system. Check the actual force
assignment before interpreting a result as learned intermolecular energetics.
The example also requires a modified Espaloma template generator.
Match each checkpoint with its model configuration and graph construction.

The [repository license](https://github.com/Ameki0/ResFF/blob/main/LICENSE)
and [v1.0.0 archive](https://zenodo.org/records/20484065) state MIT. The
[paper](https://www.nature.com/articles/s41467-026-74983-0) describes the
method and evaluation; dataset and dependency terms remain separate.

## Simulation Interfaces

### OpenMM-ML — ML And Hybrid ML/MM Systems

[OpenMM-ML](https://github.com/openmm/openmm-ml) builds OpenMM systems using
learned potentials. `createSystem()` uses the selected potential for the
system; `createMixedSystem()` selects an ML region inside a conventional
force-field system. The documented ligand example replaces ligand internal
energy and retains MM interactions with the receptor and solvent.

Install `openmmml` with pip, then install the selected model package separately.
The reviewed README lists AIMNet2, MACE, TorchMD-Net/AceFF, FeNNol/FeNNix-Bio1,
Orb, NequIP/Allegro, ANI, DeePMD, and a general ASE-calculator interface.
[Version 1.8](https://github.com/openmm/openmm-ml/releases/tag/1.8), released
September 16, 2026, adds link atoms across ML/MM boundaries and additional
AIMNet and MACE models. Mechanical embedding is the available embedding in
that release. Consult the [model-specific documentation](https://openmm.github.io/openmm-ml/)
for supported options and hardware.

[OpenMM-ML source](https://github.com/openmm/openmm-ml/blob/main/LICENSE)
is MIT. Model packages, checkpoints, OpenMM components, and training data have
separate terms. Confirm the ML region, exclusions, charge handling, and units
before using a mixed system for free-energy work.

### ALCHEMI Toolkit 0.3 — Batched Simulation And Distillation

[NVIDIA ALCHEMI Toolkit](https://github.com/NVIDIA/nvalchemi-toolkit) combines
atomic data, potential wrappers, optimization, and dynamics. The
[v0.3.0 release](https://github.com/NVIDIA/nvalchemi-toolkit/releases/tag/v0.3.0)
adds teacher–student distillation, enhanced sampling, replica exchange, and
batched nudged elastic band calculations. Distillation accepts teacher labels
or labels structures generated by the student's own dynamics.

Version 0.3 specifies Python 3.11–3.14, PyTorch ≥2.8,
`nvalchemi-toolkit-ops` ≥0.5.0, and NumPy ≥2,<3. Select the CUDA and model
extras using the release's installation guide. Source is
[Apache-2.0](https://github.com/NVIDIA/nvalchemi-toolkit/blob/main/LICENSE).
Supply separately licensed model checkpoints and datasets. Evaluate the
student's held-out accuracy and trajectory stability before substituting it
for the teacher.

## Generative Ensembles

### OriDynamics — Unordered Partner-Conditioned Samples

[OriDynamics](https://github.com/LG-FrontierAI/oridynamics) generates all-atom
conformations for proteins and complexes with protein or small-molecule
partners. Inputs contain molecular definitions and matching protein MSAs;
an initial structure is optional. Output `ensemble.cif` contains sampled
conformations without physical time ordering. Use those conformations for
structural hypotheses, not estimates of transition rates.

The [installation guide](https://github.com/LG-FrontierAI/oridynamics/blob/main/INSTALL.md)
requires `ae.ckpt`, `oridynamics.ckpt`, the Protenix
`protenix_base_default_v1.0.0.pt` backbone, and **both** `components.cif` and
`components.cif.rdkit_mol.pkl`. The shipped examples include MSAs; custom
proteins need matching alignments. Follow the GPU environment and resource
path configuration before sampling.

Code and the [two OriDynamics checkpoints](https://huggingface.co/LG-FrontierAI/oridynamics)
declare Apache-2.0. Protenix, chemical-component resources, and MSA services
retain their own terms. The [November 9, 2026 preprint](https://arxiv.org/abs/2611.11958)
describes ensemble evaluation.

### BioEmu-2 — Ensembles And Learned Lagged Propagation

[BioEmu-2](https://github.com/microsoft/bioemu2) accepts molecular-system YAML
or structure-derived systems, including bound ligands. Equilibrium sampling
returns conformations. A separate propagation mode takes starting frames and
a lag in nanoseconds and predicts endpoints using a learned transfer model.
Those endpoints are model predictions; intervening motion is not resolved.

The [preview checkpoint card](https://huggingface.co/microsoft/bioemu2)
states MIT, matching the source license. It warns that sample frequencies are
**uncalibrated** and must not be converted into Boltzmann probabilities or
quantitative free energies. Reference data and upstream components have
separate notices.

Use Linux, a supported NVIDIA GPU, and the repository's Python/CUDA recipe.
The README lists tested devices smaller than the model card's stated smallest
tested 80 GB A100, so these sources do not establish a single minimum-memory
requirement. Size the system using the current installation guidance.

The [sampling guide](https://github.com/microsoft/bioemu2/blob/main/docs/sampling.md)
explains that `samples.xtc` retains rejected frames; `physicality.json` records
per-frame status. Filter explicitly and report counts. Its physicality checks
cover protein atoms; assess ligand identity, geometry, and clashes separately.

## Validation Before Simulation

Check finite energies and forces on a supported small system, then compare a
rigidly transformed copy. Declare energy/force units, charge, spin, cell,
checkpoint, and reference method. For dynamics, inspect energy conservation
under appropriate integration conditions and count failed or rejected frames.
For binding free energies, continue with
[binding-affinity-and-fep.md](binding-affinity-and-fep.md).
