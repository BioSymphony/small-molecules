# November 2026 Tool Updates

Use these additions to choose a tool for a specific input and scientific
question. The category guides record the source, available artifacts, setup,
and terms. Verification dates are November 15, 2026; several additions are
older releases that expand the toolkit's coverage.

## Find a Tool for Your Question

| Question | Tools and Guide | Input and Result |
|---|---|---|
| Can I predict CYP inhibition with a released endpoint model? | [OpenADMET](admet-prediction.md) | SMILES → four CYP inhibition pIC50 predictions; KERMT is a separate backbone for supervised adaptation |
| What precursors could make this product? | [DianShi Direct](singlestep-retrosynthesis.md) | Product SMILES → ranked precursor sets from the released 4B model |
| What products can these building blocks form? | [SmartReact](forward-and-reaction-modeling.md) | Reactants and a reaction rule → enumerated products |
| Can I upgrade a reaction-constrained generator? | [RxnFlow 2.1.1](synthesizable-generation.md) | A trained policy and matched reaction environment → candidates and reaction paths; older checkpoints require retraining |
| Which molecules have useful optical properties? | [Multi-Fluor and TADF-PL](property-and-qsar-prediction.md) | Molecular inputs → model-specific optical endpoints; Multi-Fluor also requires solvent SMILES |
| Which structures explain an MS/MS or NMR measurement? | [MS-GPT, UltraNMR, PRISM, and NMRTrans](analytical-chemistry-models.md) | Required spectra, formula, and task assets → candidate structures or spectrum predictions |
| What metabolite could a biosynthetic cluster encode? | [DeepSeMS](multimodal-chemical-models.md) | Annotated cluster and Pfam features → ranked metabolite SMILES and ensemble consensus |
| Which microbial transport systems could associate with a molecule? | [ChemProFlow](property-and-qsar-prediction.md) | SMILES → transport-candidate labels, TCDB classes, and organism associations |
| Can I sample alternative protein–ligand conformations? | [OriDynamics and BioEmu-2](molecular-potentials-and-simulation.md) | Supported complex inputs and auxiliary assets → all-atom ensembles; temporal interpretation depends on the model |
| What are this geometry's energy and atomic forces? | [HyFF and AIMNet2](molecular-potentials-and-simulation.md) | Elements, coordinates, charge, and spin as required → energy and forces |
| How can I prepare an absolute binding free-energy calculation? | [BFEE3](binding-affinity-and-fep.md) | Prepared molecular system → simulation inputs and postprocessing through the selected geometric or alchemical route |
| How can I prepare molecular features in batches? | [cuik-molmaker and nvMolKit](molecular-compute-infrastructure.md) | SMILES or RDKit molecules → features, similarities, or conformers through CPU/GPU-specific interfaces |
| Does an encoder or generator improve the result I need? | [Evaluation methods](model-evaluation-and-benchmarks.md) | Matched baselines, chemical splits, and task metrics → a comparison for the intended decision |

## Release Changes That Affect Setup

- **RxnFlow 2.1.1:** the November 11 graph-feature change makes earlier
  checkpoints incompatible. Train a matching model before upgrading a workflow.
- **DianShi:** the released Direct model performs single-step prediction
  without retrieval. The multistep system uses a separate 397B planner and
  additional search assets.
- **MS-GPT:** the October release switches to official MIST encoders and fixes
  attention masking. Match the encoder, adapter, decoder, and reported results.
- **NMRTrans:** the updated branch changes masks, vocabulary, data, and splits.
  Load each checkpoint with its matching branch and configuration.
- **ChemCensor 1.4.0:** source is available under independent-benchmark-only
  terms. Those terms exclude workflow ranking, filtering, rewards, and training.
- **BFEE3:** its Lucid double-decoupling method uses the abbreviation LDDM.
  The [LDDM molecular generator](lddm.md) is a separate project.

## Run a First Functional Check

Start with a complete upstream example and the selected model's native
configuration. Keep its ensemble and sampling settings. Reduce the number of
input examples when preparing a small functional check.

The [evaluation guide](model-evaluation-and-benchmarks.md#first-functional-checks)
lists output checks for endpoint models, encoders, optical predictors, spectrum
decoders, molecular potentials, docking, and reactions. Use the full benchmark
protocol when comparing with published results.
