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

## Evidence Boundary

The preprint reports retrospective docking and generation benchmarks plus
prospective experiments across several targets. The public repository provides
inference scripts, two checkpoints, a KRAS example, structural filtering, and a
small reaction-space example. It does not provide the complete training
harness, all benchmark runners, the paper's target-specific ranking systems,
the Enamine REAL assets, or the complete candidate-selection process.

The prospective results therefore support the complete computational and
experimental campaigns more strongly than they support the released checkpoint
in isolation. Treat generated molecules, poses, and reaction traces as
hypotheses requiring independent validation.

## Independent Public-Structure Checks

The following checks used publicly deposited structures and the non-commercial
paper checkpoint. They describe that checkpoint only; they do not validate the
MIT checkpoint.

- On the bundled KRAS example from [PDB 8AZR](https://www.rcsb.org/structure/8AZR),
  9 of 10 redocking samples were within 2 angstrom of the deposited pose; the
  best was 0.362 angstrom. This structure can overlap the training corpus, so it
  is a pose-recovery check rather than a generalization test.
- Across five approved-drug complexes, imatinib/ABL1 (1IEP),
  methotrexate/DHFR (1U72), sotorasib/KRAS G12C (6OIM), darunavir/HIV-1
  protease (4LL3), and venetoclax/BCL-2 (6O0K), the best of 10 samples was below
  2 angstrom for four targets. All five ligands have older PDB records and can
  overlap PDB-derived training data.
- A temporally filtered panel used ligand components first deposited in the PDB
  on or after 2026-06-15. Among 29 scored targets, 21 had a best-of-five pose
  below 2 angstrom, with a median best-of-five RMSD of 1.18 angstrom. The
  checkpoint's training cutoff is not disclosed, so this panel must not be
  described as a confirmed holdout.
- Fixed fragment coordinates remained unchanged during tested fragment-growing
  runs. This supports scaffold-constrained use when the starting geometry is
  trusted.
- A docked sotorasib pose reached 0.832 angstrom RMSD while inverting its
  stereocentre. Coordinate RMSD alone did not detect the chemical error.
- Deliberately mismatched ligand-pocket pairs produced buried, clash-free poses
  with uncertainty values similar to cognate pairs. LDDM does not determine
  whether the supplied ligand belongs to the supplied target.

Report the checkpoint, source revision, random seeds, sample count, and whether
a value is top-1, median, or best-of-N. Compare every docked pose with all
relevant deposited ligand copies, because symmetric sites and alternate poses
can make a correct placement appear wrong.

## Implementation Notes

At the reviewed commit, the repository had three commits, no tagged release,
no continuous-integration configuration, and no automated test suite. The
locked environment targets Python 3.11, PyTorch 2.6 with CUDA 12.4, and a
CUDA-specific `torch-scatter` wheel.

Basic sampling was also exercised on CPU after changing one direct
`torch_scatter` import to use the repository's fallback module. That is a local
compatibility change, not the upstream installation path. The fallback remains
incomplete for aggregation paths that call `scatter_min`, `scatter_max`, or
`scatter_softmax`. Programmable generation also requires external GNINA and
Reduce binaries, while the supplied synthesis-space workflow is large enough
to make GPU execution the practical route.

The model loader uses `torch.load(..., weights_only=False)`, and the
synthesis-space workflow loads Python pickle files. These formats can execute
code during loading. Accept only fixed, trusted, checksum-verified checkpoints
and chemical-space assets. Do not expose checkpoint, pickle, executable, or
configuration paths as unrestricted user input.

## Validation Requirements

For every LDDM workflow:

1. Prepare and inspect the receptor, ligand, pocket, protonation, cofactors, and
   alternate deposited ligand copies.
2. Validate sanitization, valence, bond order, stereochemistry, geometry,
   clashes, and fixed-atom preservation.
3. Treat uncertainty as a ranking feature within the tested setup, not as
   affinity or target compatibility.
4. Re-score promising candidates with an independent structural or affinity
   method appropriate to the target.
5. Validate reaction traces with forward prediction, stock checks, route
   planning, and chemistry review.
6. Record the complete license stack and exact checkpoint identity.

## Selection Summary

Choose LDDM for an experimental workbench spanning pocket generation, docking,
fragment editing, and reaction-space proposals. Prefer established single-task
tools when one operation is sufficient or when release maturity is important.
Keep the paper checkpoint within uses permitted by its non-commercial terms,
and evaluate the MIT checkpoint separately before relying on it.
