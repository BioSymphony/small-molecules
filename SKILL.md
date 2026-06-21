---
name: small-molecule-design-tools
description: >-
  Agent skill for choosing open small-molecule design tools and keeping tool,
  model, data, and license constraints visible during long-horizon agent work.
  Use when an agent needs to generate makeable molecules, project a molecule
  into synthesizable space, design analogs, plan or check synthesis routes,
  score synthesizability, predict protein structures, dock ligands, co-fold
  protein-ligand complexes, estimate binding affinity with ML or free-energy
  methods, build QSAR or ADMET screens, check selectivity and off-target risk,
  generate molecules into a binding pocket, or compare code, weights, data, and
  base-model terms for tools such as PrexSyn, SynFormer, ReaSyn, SynCoGen,
  SynTwins, SynLlama, SyntheMol, APEX, GenMol, AiZynthFinder, ASKCOS,
  Syntheseus, SynPlanner, ReactionT5v2, RXNGraphormer, RetroDFM-R, DeepRetro,
  Synthelite, RDChiral, rxnutils, SynTemp, RetroScore, ChemDFM-R, Boltz-1,
  Boltz-2, Chai-1, DiffDock, Uni-Mol, AlphaFold, ColabFold, ESMFold, OpenFold,
  RoseTTAFold, AutoDock Vina, gnina, RxDock, OpenFE, OpenMM, Chemprop,
  DeepChem, Therapeutics Data Commons, ADMET-AI, ESP-Sim, the ChEMBL multitask
  model, REINVENT, DiffSBDD, Pocket2Mol, fpocket, P2Rank, AgentD, and CLADD.
---

# Small-Molecule Design Tools

This is an agent skill for routing small-molecule design tasks to suitable open
tools. It is meant to improve agent performance on complex workflows where the
agent must choose methods, load focused references, and keep licensing or data
constraints in view while it works.

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
  multi-step route planners such as AiZynthFinder, ASKCOS, Syntheseus, and
  SynPlanner.
- [references/singlestep-retrosynthesis.md](references/singlestep-retrosynthesis.md):
  one-step precursor prediction with ReactionT5v2, RXNGraphormer, GDiffRetro,
  RetroDiT, ConRetroBert, TempRe, and related models.
- [references/agentic-retrosynthesis.md](references/agentic-retrosynthesis.md):
  LLM and agent-assisted synthesis planners.
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
  ADMET, hERG, BBB, CYP, and deployable local predictors.
- [references/target-and-selectivity-prediction.md](references/target-and-selectivity-prediction.md):
  off-target, selectivity, shape, and pharmacophore tools.
- [references/structure-based-generation.md](references/structure-based-generation.md):
  pocket-conditioned generation and pocket detection.

Cross-cutting:

- [references/agentic-drug-design.md](references/agentic-drug-design.md):
  agent frameworks that orchestrate generation, scoring, ADMET, and affinity
  tools.
- [references/chemical-language-models.md](references/chemical-language-models.md):
  chemistry language models and multimodal chemistry models.
- [references/licensing-and-data.md](references/licensing-and-data.md):
  license layers, Enamine terms, PDB/PDBBind notes, ChEMBL/TDC data terms, and
  commercial-use checklist.
- [references/worked-example-kras-glue.md](references/worked-example-kras-glue.md):
  public worked example on daraxonrasib, KRAS, and CypA using PDB 9BG6.
- [references/watchlist.md](references/watchlist.md):
  promising tools with missing code, missing weights, missing license clarity, or
  immature releases.

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
| Check whether a tool is usable in commercial work | `licensing-and-data.md`, then the tool card |

## First Picks

Use these as starting points, then read the relevant reference file for details:

| Need | First pick |
|---|---|
| Synthesizable-space projection | PrexSyn |
| Training-free analog generation | SynTwins, with license review before reuse |
| 3D molecule and route co-generation | SynCoGen |
| Make-on-demand design over Enamine-style libraries | SyntheMol or APEX, depending on license needs |
| General de novo molecule generation | GenMol, with SmiSelf for validity repair |
| Multi-step route planning | AiZynthFinder first, ASKCOS when broader planning and conditions are needed |
| One-step retrosynthesis | ReactionT5v2 |
| LLM-assisted route planning | DeepRetro or Synthelite, followed by round-trip checks |
| Reaction templates and data cleanup | RDChiral or rdchiral_plus with rxnutils |
| Commercially clean ML affinity starting point | Boltz-2 |
| Protein-ligand co-folding | Boltz-1, Chai-1, or Umol after checking current weight terms |
| Learned docking into a known pocket | DiffDock-L or Uni-Mol Docking v2 |
| Classical CPU docking | AutoDock Vina |
| Physics-based relative free energy | OpenFE |
| QSAR from ChEMBL-style data | Chemprop or DeepChem |
| Local ADMET triage | ADMET-AI |
| Broad off-target scan | ChEMBL multitask model plus ESP-Sim where shape overlap matters |
| Pocket-conditioned generation | REINVENT 4, DiffSBDD, PILOT, Pocket2Mol, or TargetDiff, followed by makeability checks |

## Operating Notes

- Read source licenses directly. README badges and paper text can disagree with
  the repository license, model-card license, or dataset terms.
- Check code, weights, data, and base-model terms separately. LLM fine-tunes add
  the original model terms to the project terms.
- Treat docking and co-folding confidence scores as pose-confidence signals.
  Binding-affinity estimates require an affinity model or a free-energy method.
- For molecular glues, degraders, covalent binders, and macrocycles, choose tools
  that match the mechanism. A single-pocket docking workflow is often the wrong
  starting point for those systems.
- When an experimental ternary structure exists, consider perturbation and
  scoring on that scaffold before asking a co-folding model to rediscover it.
- Pair pocket-conditioned generators with a makeability step. Most structure-
  based generators do not guarantee a synthesis route.
- Re-check live upstream repositories for recent tools, especially pre-1.0
  models and 2026 additions.

## Pipeline Pattern

A full agent loop usually crosses both layers:

1. Get or predict the receptor structure.
2. Generate, dock, co-fold, or score candidate molecules for the target.
3. Filter for affinity, QSAR, ADMET, and selectivity.
4. Project survivors into synthesizable space.
5. Plan or validate routes.
6. Re-check licenses and data terms before claiming deployability.

Load the detailed reference file for install commands, model weights, benchmark
context, GPU needs, and current caveats.
