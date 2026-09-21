# LDDM

LDDM, the Large Drug Discovery Model, is a pocket-conditioned three-dimensional
generative model for docking, fragment editing, de novo design, and
reaction-space-constrained generation. This note was checked on 2026-09-21
against upstream commit
[`f254fb4`](https://github.com/LPDI-EPFL/lddm/tree/f254fb4f8525b3803e79eb95e9f1a163fe8b2459)
and the September 2026
[bioRxiv preprint](https://doi.org/10.64898/2026.09.15.751537). The paper is a
preprint, and the repository is an early research release.

## Task Fit

LDDM uses one fragment-masked model to generate atom types, bonds, and
coordinates while preserving selected input information. Its public interface
supports:

- de novo ligand generation in a prepared pocket
- fragment growing and fragment linking
- whole-molecule docking
- partial docking with selected coordinates held fixed
- programmable generation with structural filters
- generation over supplied building blocks and reaction templates

Use LDDM when one experimental workflow needs several of these operations or
when trusted ligand atoms must stay fixed during local redesign. Use a dedicated
docking tool for a simpler pose-only workflow and a dedicated retrosynthesis
planner when the target molecule is already fixed.

LDDM does not predict a calibrated binding affinity. Its uncertainty output is
a pose or generation signal, not a substitute for an affinity model, free-energy
calculation, selectivity assay, or experimental measurement.

## Released Artifacts and Terms

| Layer | Published terms | Selection consequence |
|---|---|---|
| Source code | [MIT](https://github.com/LPDI-EPFL/lddm/blob/f254fb4f8525b3803e79eb95e9f1a163fe8b2459/LICENSE.md) | Permissive source-code terms. |
| `lddm.ckpt`, named `CD+BB+BN` upstream | [CC BY-NC 4.0](https://github.com/LPDI-EPFL/lddm/blob/f254fb4f8525b3803e79eb95e9f1a163fe8b2459/README.md#checkpoint-geometry-reference) | Paper checkpoint; includes BindingNet training data and is labeled non-commercial. |
| `lddm_CDBB.ckpt`, named `CD+BB` upstream | MIT | Checkpoint trained without BindingNet. The paper does not establish that it reproduces the paper checkpoint's performance. |
| Public reaction-space example | 44,944 SynSpace-derived building blocks and three reactions | Compact workflow example; review the artifact and source-data terms before redistribution. |
| Enamine REAL workflow | Separately licensed reactions and building blocks | Upstream does not redistribute these assets. Obtain applicable permission separately. |
| GNINA-based filtering | Separate code, model, and data terms | Review the GNINA components selected by the programmable workflow. |

The upstream usage examples select `lddm.ckpt`, the non-commercial paper
checkpoint. A workflow that requires different terms must select the exact
checkpoint deliberately, record its checksum, and benchmark it independently.
A repository-level or artifact-record license label does not replace the
checkpoint-specific terms stated by the authors.

## Implementation Notes

At the reviewed commit, the repository had three commits, no tagged release,
no continuous-integration configuration, and no automated test suite. The
locked environment targets Python 3.11, PyTorch 2.6 with CUDA 12.4, and a
CUDA-specific `torch-scatter` wheel.

Follow the [upstream setup instructions](https://github.com/LPDI-EPFL/lddm/tree/f254fb4f8525b3803e79eb95e9f1a163fe8b2459#setup).
Programmable generation requires external GNINA and Reduce binaries, plus the
geometry-reference data linked upstream.

The model loader uses `torch.load(..., weights_only=False)`, and the
synthesis-space workflow loads Python pickle files. These formats can execute
code during loading. Accept only fixed, trusted, checksum-verified checkpoints
and chemical-space assets. Do not expose checkpoint, pickle, executable, or
configuration paths as unrestricted user input.

## Validate Outputs

Inspect the prepared receptor, ligand protonation, pocket, and required cofactors
before sampling.

Select checks for the operation you run:

- For docking, check molecular identity, stereochemistry, and geometry before
  measuring pose recovery. Use the
  [pose-validation procedure](docking-and-cofolding.md#validate-poses).
- For partial docking, derive atom selections from the exact input structure.
  The upstream `--atoms_to_dock` option lists movable atoms; all other atoms
  retain their input coordinates.
- For fragment editing, check both the preserved atoms and the generated
  region. Fixed-coordinate agreement measures constraint preservation.
- For covalent complexes, check the attachment atoms and bonded geometry using
  the [covalent-pose procedure](docking-and-cofolding.md#covalent-poses).
- For reaction-space generation, check reaction steps and terminal compounds
  using the [route-validation procedure](retrosynthesis-planning.md#validate-routes).

Before ranking candidates, test the selected scorer with a reference pose and
decoys prepared by the same procedure. Record which controls it ranks correctly.
If the scorer fails the intended comparison, revise the setup before using its
ranking to select candidates.

For reproducible comparisons, record the checkpoint checksum, source revision,
input structures, atom selections, seeds, sample count, and scoring settings.
Report top-ranked results separately from the best result among all samples.
