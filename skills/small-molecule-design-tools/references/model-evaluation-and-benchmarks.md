# Model Evaluation and Benchmarks

Choose an evaluation that matches the decision you need to make: predict an
assay endpoint, rank poses, or compare generated molecules. Use the same input
compounds, split, and selection budget when comparing methods.

Source and artifact notes were checked on **2026-11-15**. Published benchmark
results apply to the reported datasets, models, and protocols.

## Choose a Comparison

| Question | Starting comparison | Keep fixed |
|---|---|---|
| Does an encoder improve an assay model? | ECFP counts and a tree-based learner versus the selected encoder and prediction head | Molecular identities, labels, chemical split, and tuning budget |
| Does a method rank supplied poses correctly? | Pyrite with its temporal split and per-structure scoring | Pose pairs, allowed features, and aggregation rule |
| Does a pocket generator produce useful candidates? | MolGenBench with its target and generation protocol | Targets, requested samples, preprocessing, and metric versions |
| Does a model distinguish unfamiliar chemistry? | Scaffold or time split with train/test neighbor analysis | Identity rules, endpoint definition, and evaluation population |
| Does the installed tool run correctly? | One complete upstream fixture with native inference settings | Source, checkpoint, tokenizer/configuration, and expected output schema |

## FewShot4Chem

[FewShot4Chem](https://github.com/TheorChemGroup/FewShot4Chem/tree/bca3acf6eb9d8fa1b7a46fde381b25d7a61e1194)
compares molecular encoders, classical descriptors, fingerprints, and
table-prompted language models on small labeled datasets. The
[October 30 preprint](https://arxiv.org/abs/2610.41899) and released files include
fixed cohorts, splits, stored responses, per-repeat results, and reproduction
tables. The project is MIT with component notices; CLAMP has GPL-3.0 terms.

Use the fixed cohorts to compare methods under the same selection rules.
Recomputing scores from stored responses requires fewer resources than running
every encoder or making new language-model calls. Its public-task results do
not establish performance on a new assay. Retain shuffled-label controls and
check whether training or pretraining data overlap the evaluation compounds.

## Molecular Embedding Benchmark

The [November 3 revision](https://arxiv.org/html/2508.06199v5) of
*Benchmarking Pretrained Molecular Embedding Models* compares frozen molecular
embeddings with ECFP count fingerprints on 25 classification datasets. CheMeleon led the initial
comparison; scaffold-based external validation did not resolve an advantage
over ECFP. Compare both representations for a new QSAR task.

The [released source](https://github.com/MLCIL/benchmarking_molecular_models/tree/17d2aa12912f8f662494c92b893a9f864896162a)
was last committed in September 2025 at that revision. Its README grants
research use with citation and says individual model implementations retain
their own licenses. That snapshot alone does not reproduce every result added
to the November paper. The paper's refitted CLAMP weights are a separate
artifact from the original checkpoint.

## Representation Limits

Oxford's [November preprint](https://arxiv.org/abs/2611.08420) studies graph,
shape, and ADMET similarity. It reports fingerprint degeneracy in large
libraries and split leakage from clustering procedures, alongside limitations
of learned embeddings. These similarity tests answer different questions from
endpoint-specific fine-tuning.

The [analysis repository](https://github.com/oxpig/On-the-limitations-of-molecular-representations/tree/446564cff3d010c55aac02a397c874ec50187978)
contains notebooks and embedding environments; no source license was identified
in the inspected tree. Use graph identifiers for compound identity and
deduplication. Inspect train/test neighbors after splitting, and select a
similarity representation for the intended endpoint.

## Pyrite: Supplied-Pose Ranking

[Pyrite](https://github.com/genesistherapeutics/pyrite/tree/013d5655a8b19fde7184859f8ee047aad175420a)
asks which of two poses is closer to the crystal pose. Its
[November 10 paper](https://arxiv.org/abs/2611.14511) accompanies two 750-pair
sets with 113 columns. The dataset license is CC BY 4.0. The repository provides
data and a viewer; trained ranking-agent weights and implementation are
separate release requirements.

Use the declared temporal split and average accuracy within each structure
before averaging across structures. Exclude `correct`, `MM_correct`,
`metric_rmsd_*`, `pose_rmsds_*`, `metric_lddt_pli_*`,
`metric_gt_interaction_*`, `gt_frac`, `a_frac`, and `b_frac` from model inputs.
Pose-intrinsic checks such as `metric_pb_valid_A/B` remain usable features.
The supplied pairs include a good pose, and the pose generator is
proprietary. Report pair-ranking accuracy separately from end-to-end docking
success.

## MolGenBench: Pocket Generation and Lead Optimization

[MolGenBench](https://github.com/Intelligent-Drug-Discovery-Lab/MolGenBench/tree/126e73134959e817d18f432c01d9023e0774fb8a)
evaluates pocket-conditioned generation and hit-to-lead optimization. Its
[Nature Communications study](https://www.nature.com/articles/s41467-026-78105-8)
compares molecular recovery, structural properties, and docking-related
metrics. Source is MIT; the separate
[version 4 dataset](https://zenodo.org/records/20233505) declares CC BY 4.0.

The documented de novo protocol requests **1,000 samples per target** and
retains the model's outputs without additional filtering. The hit-to-lead
protocol requests **200 samples per chemical series**. Record attempted,
valid, and unique molecule counts. Pin the metric dependencies, including
PoseCheck commit `57a1938`, used for the published strain calculation.
Small fixture checks establish interface compatibility; comparisons with the
published benchmark require its full sampling and evaluation protocol.

## First Functional Checks

Use a complete upstream example before starting a benchmark:

1. Pin the source, environment, checkpoint, configuration, and auxiliary assets.
2. Run the example with the model's native inference and ensemble settings.
3. Save raw outputs with stable molecule or structure identifiers.
4. Check the output using an independent parser and task-specific criteria.
5. Record failures, elapsed time, observed memory use, and artifact hashes.

| Tool class | Useful result check |
|---|---|
| Endpoint predictor | Aligned rows, declared endpoint units, finite values, and explicit invalid-input handling |
| Molecular encoder | Correct dimensions, finite features, and stable row mapping |
| Optical predictor | Solute/solvent identity, the selected ensemble, and correct endpoint columns and units |
| Spectrum decoder | Required formula/modalities, parseable candidates, and formula or graph checks |
| Molecular potential | Supported elements/charge/spin, finite energy and forces, declared units, and rigid-transform consistency |
| Docking or co-folding | Complete structure output, preserved atom identity, pose checks, and confidence fields |
| Reaction predictor | Parseable ranked reactions, component identity, and the selected beam or sampling settings |

For task-specific interfaces, use [properties](property-and-qsar-prediction.md),
[analytical chemistry](analytical-chemistry-models.md),
[molecular simulation](molecular-potentials-and-simulation.md), and
[docking](docking-and-cofolding.md).
