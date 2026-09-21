---
name: small-molecule-design-tools
description: Use when choosing or applying open or publicly documented small-molecule design, synthesis-planning, docking, binding-affinity, QSAR, ADMET, pocket-finding, or ligand-generation tools for work with public or synthetic data.
---

# Small-Molecule Design Tools

Use this skill to choose small-molecule design tools, compare their required
inputs and setup, and check their code, model, and data licenses.

Use the skill in two passes:

1. Identify the physical or chemical task.
2. Open the matching reference file before recommending tools or writing code.

For commercial or product-facing work, also open
[references/licensing-and-data.md](references/licensing-and-data.md). Code,
weights, data, and base-model terms often differ for the same upstream project.

## Reference Map

Start with [references/tool-matrix.md](references/tool-matrix.md) when the user
wants a broad comparison across categories.

Makeability and synthesis:

- [references/synthesizable-generation.md](references/synthesizable-generation.md):
  makeable molecule generation, analogs, make-on-demand libraries, and route
  co-generation.
- [references/molecular-generation.md](references/molecular-generation.md):
  general molecule generators where validity matters more than synthesis route
  guarantees.
- [references/retrosynthesis-planning.md](references/retrosynthesis-planning.md):
  multi-step route planners and validators such as AiZynthFinder, RENKIN,
  ASKCOS, Syntheseus, and SynPlanner.
- [references/singlestep-retrosynthesis.md](references/singlestep-retrosynthesis.md):
  one-step precursor prediction with ReactionT5v2, RXNGraphormer, GDiffRetro,
  RetroDiT, ConRetroBert, TempRe, and related models.
- [references/agentic-retrosynthesis.md](references/agentic-retrosynthesis.md):
  LLM and agent-assisted synthesis planners, including RetroAgent.
- [references/forward-and-reaction-modeling.md](references/forward-and-reaction-modeling.md):
  forward reaction and mechanism prediction.
- [references/template-and-rule-infrastructure.md](references/template-and-rule-infrastructure.md):
  reaction templates, SMARTS rules, RDChiral, rxnutils, and SynTemp.
- [references/synthesizability-scoring.md](references/synthesizability-scoring.md):
  makeability scoring and route consistency checks.

Target-based design:

- [references/protein-structure-prediction.md](references/protein-structure-prediction.md):
  receptor structure prediction and preparation.
- [references/docking-and-cofolding.md](references/docking-and-cofolding.md):
  classical docking, learned docking, protein-ligand co-folding, and pose
  scoring.
- [references/binding-affinity-and-fep.md](references/binding-affinity-and-fep.md):
  ML affinity, OpenFE, OpenMM, endpoint methods, and free-energy workflows.
- [references/property-and-qsar-prediction.md](references/property-and-qsar-prediction.md):
  QSAR, activity, property, and active-learning screens.
- [references/admet-prediction.md](references/admet-prediction.md):
  ADMET, hERG, BBB, CYP, and locally runnable predictors.
- [references/target-and-selectivity-prediction.md](references/target-and-selectivity-prediction.md):
  off-target, selectivity, shape, and pharmacophore tools.
- [references/structure-based-generation.md](references/structure-based-generation.md):
  pocket-conditioned generation and pocket detection.
- [references/lddm.md](references/lddm.md):
  focused review of LDDM capabilities, checkpoint terms, implementation limits,
  and validation procedures.

Cross-cutting:

- [references/agentic-drug-design.md](references/agentic-drug-design.md):
  agent frameworks that orchestrate generation, scoring, ADMET, and affinity
  tools.
- [references/chemical-language-models.md](references/chemical-language-models.md):
  chemistry language models and multimodal chemistry models.
- [references/licensing-and-data.md](references/licensing-and-data.md):
  license layers, Enamine terms, PDB/PDBBind notes, ChEMBL/TDC data terms, and
  terms-review checklist.
- [references/worked-example-kras-glue.md](references/worked-example-kras-glue.md):
  public worked example on daraxonrasib, KRAS, and CypA using PDB 9BG6.
- [references/watchlist.md](references/watchlist.md):
  tools with missing code, missing weights, unclear license terms, or early-stage
  releases.

## Routing Rules

Use the user's actual task to choose the first reference:

| User task | Start with |
|---|---|
| Generate makeable analogs of a hit | `synthesizable-generation.md` |
| Project a molecule into synthesizable space | `synthesizable-generation.md` |
| Generate valid molecules for exploration | `molecular-generation.md` |
| Plan a route to a known target molecule | `retrosynthesis-planning.md` |
| Predict one reaction step | `singlestep-retrosynthesis.md` |
| Check whether a proposed reaction route is plausible | `forward-and-reaction-modeling.md`, then `synthesizability-scoring.md` |
| Prepare or predict a receptor structure | `protein-structure-prediction.md` |
| Dock a ligand into a known structure | `docking-and-cofolding.md` |
| Co-fold a protein-ligand complex from sequence and ligand | `docking-and-cofolding.md` |
| Estimate binding affinity | `binding-affinity-and-fep.md` |
| Build a QSAR or property model | `property-and-qsar-prediction.md` |
| Screen ADMET risk | `admet-prediction.md` |
| Screen off-target or selectivity risk | `target-and-selectivity-prediction.md` |
| Generate molecules into a pocket | `structure-based-generation.md` |
| Orchestrate a full agentic loop | `agentic-drug-design.md`, then the category references it calls |
| Check a tool's terms for product-facing work | `licensing-and-data.md`, then the tool card |

## First Picks

Use these as starting points, then read the relevant reference file for details:

| Need | First pick |
|---|---|
| Synthesizable-space projection | PrexSyn |
| Training-free analog generation | Review SynTwins after confirming its code terms; the repository has no `LICENSE` file |
| 3D molecule and route co-generation | Review SynCoGen; its weights and data are labeled MIT, but its code has no stated license |
| Make-on-demand design over Enamine-style libraries | SyntheMol; APEX has no stated repository or artifact license |
| General de novo molecule generation | GenMol after checking its separate model terms |
| Multi-step route planning | AiZynthFinder for a local baseline; RENKIN for route validation; ASKCOS when broader planning and conditions are needed |
| One-step retrosynthesis | ReactionT5v2 |
| LLM-assisted route planning | DeepRetro, RetroAgent, or Synthelite, followed by round-trip checks |
| Reaction templates and data cleanup | RDChiral or rdchiral_plus with rxnutils |
| ML affinity with MIT-licensed code and weights | Boltz-2 |
| Protein-ligand co-folding | OpenBind-0, Boltz-1, Chai-1, or Umol after checking the terms for the selected release |
| Learned docking into a known pocket | DiffDock-L or Uni-Mol Docking v2 |
| Classical CPU docking | AutoDock Vina |
| Physics-based relative free energy | OpenFE |
| QSAR from ChEMBL-style data | Chemprop or DeepChem |
| Local ADMET triage | ADMET-AI |
| Broad off-target scan | ChEMBL multitask model plus ESP-Sim where shape overlap matters |
| Pocket-conditioned generation | REINVENT 4, LDDM, DiffSBDD, PILOT, Pocket2Mol, or TargetDiff, followed by makeability checks |

## Operating Notes

- Read source licenses directly. README badges and paper text can disagree with
  the repository license, model-card license, or dataset terms.
- Check code, weights, data, and base-model terms separately. For an LLM
  fine-tune, record both the project terms and the original base-model terms.
- Treat docking and co-folding confidence scores as pose-confidence signals.
  Binding-affinity estimates require an affinity model or a free-energy method.
- For molecular glues, degraders, covalent binders, and macrocycles, choose tools
  that model the complete mechanism. A single-pocket docking workflow omits
  important components of these systems.
- When an experimental ternary structure exists, perturb and score that
  structure before asking a co-folding model to predict it again.
- Pair pocket-conditioned generators with a makeability step. Most structure-
  based generators do not guarantee a synthesis route.
- For LDDM, record the exact checkpoint. The paper checkpoint is labeled
  non-commercial; the MIT checkpoint requires separate performance validation.
- Re-check upstream repositories for pre-1.0 models and entries with recent
  verification dates.

## Pipeline Pattern

Connect candidate design with synthesis planning:

1. Get or predict the receptor structure.
2. Generate, dock, co-fold, or score candidate molecules for the target.
3. Filter for affinity, QSAR, ADMET, and selectivity.
4. Project survivors into synthesizable space.
5. Re-score any molecules changed by projection, including their poses and
   predicted properties.
6. Plan or validate routes and check terminal compounds against the selected
   stock using [retrosynthesis-planning.md](references/retrosynthesis-planning.md).
7. Re-check licenses and data terms before deployment.

Load the detailed reference file for install commands, model weights, benchmark
context, GPU needs, and documented caveats.
