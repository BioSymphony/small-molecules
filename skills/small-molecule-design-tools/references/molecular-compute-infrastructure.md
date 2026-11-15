# Molecular Compute Infrastructure

Use these libraries to prepare and compare molecular representations. They
provide conformers, fingerprints, descriptors, or graph features for downstream
models. Neither library is a learned affinity or ADMET predictor.

Sources and compatibility tables reviewed **2026-11-15**.

## nvMolKit — GPU Molecular Operations

[nvMolKit](https://github.com/NVIDIA-BioNeMo/nvMolKit) accelerates molecular
operations on NVIDIA GPUs. The [API documentation](https://nvidia-bionemo.github.io/nvMolKit/)
covers Morgan fingerprints, Tanimoto similarity, conformer embedding, MMFF
optimization, and clustering. RDKit molecules supply chemistry and atom
identity; GPU tensors carry results for downstream work. Synchronize GPU work
when timing operations or transferring results to the CPU.

Version 0.7.0 supports RDKit 2025.09.6 and 2026.03.1–2026.03.6 through conda.
Its standard PyPI wheel selects RDKit 2026.03.6; additional wheels target
specific RDKit versions. The C++ dependency makes the build variant important.
Use the [installation guide](https://github.com/NVIDIA-BioNeMo/nvMolKit#installation-guide)
for the exact package/RDKit pairing.

Conda installs use `nvmolkit`; ensure a GPU-enabled PyTorch and driver-compatible
CUDA runtime. The published pip wheels use CUDA 12 runtime packages; install a
compatible CUDA 12 PyTorch wheel first. A successful package installation alone
does not establish CUDA availability.

Source is [Apache-2.0](https://github.com/NVIDIA-BioNeMo/nvMolKit/blob/main/LICENSE/License.txt),
with [third-party notices](https://github.com/NVIDIA-BioNeMo/nvMolKit/blob/main/LICENSE/third-party.txt).
No trained checkpoint is required. Compare a small batch with RDKit under
matching fingerprint, hydrogen, stereochemistry, and conformer settings before
replacing an existing preprocessing step.

## cuik-molmaker — CPU Molecular Featurization

[cuik-molmaker](https://github.com/NVIDIA-BioNeMo/cuik-molmaker) uses C++ and
RDKit to convert SMILES into atom features, bond features, graph edges, and
molecular descriptors. It returns NumPy arrays for model input and runs on
CPUs. Chemprop and KERMT expose integrations.

The [compatibility table](https://github.com/NVIDIA-BioNeMo/cuik-molmaker/blob/main/docs/COMPATIBILITY.md)
distinguishes three package channels:

| Channel | Package | Version Meaning |
|---|---|---|
| conda-forge | `cuik_molmaker` | Library semantic version, such as 0.3.1 |
| PyPI | `cuik-molmaker-pin` | Exact RDKit version, such as 2026.9.2 |
| NVIDIA PyPI | `cuik_molmaker` | Library version in an RDKit-specific index |

Use `conda install -c conda-forge cuik_molmaker` or choose a compatible pinned
wheel. A PyPI date-version is not the library's semantic release number.
Match Python, operating system, architecture, and RDKit build to the table.

Source is [Apache-2.0](https://github.com/NVIDIA-BioNeMo/cuik-molmaker/blob/main/LICENSE/License.txt);
RDKit and other dependencies retain their terms. No learned weights are bundled.
Preserve feature order, descriptor normalization, explicit-hydrogen handling,
duplicate-edge settings, and self-loops when feeding an existing checkpoint.
Changing those options changes the model input even if the molecule is identical.

## Choosing

| Need | Library | Main Compatibility Check |
|---|---|---|
| GPU fingerprints, similarity, conformers, or MMFF | nvMolKit | RDKit build, CUDA runtime, PyTorch backend, and GPU driver |
| CPU graph and descriptor batches | cuik-molmaker | RDKit ABI and the trained model's feature schema |
| Energy and force models or MD | [Molecular potentials and simulation](molecular-potentials-and-simulation.md) | Potential, checkpoint, system composition, and units |
