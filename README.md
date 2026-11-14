![BioSymphony Small Molecules banner](assets/readme-banner-v2.png)

# BioSymphony Small Molecules

Give your AI agent a guide to choosing and running small-molecule design tools.
Start with a protein structure, a compound library, or a target SMILES. The
guides help your agent choose tools, set them up, and pass outputs between
them. The upstream packages and services perform the calculations.

## Start with your agent

Point your agent at [SKILL.md](SKILL.md) or fill in the brackets in this prompt.

```text
Read https://github.com/BioSymphony/small-molecules/blob/main/SKILL.md

[Plan or run] a workflow for [task] using [inputs] on [available compute].
For each step, explain the tool choice and give the command or API, version,
setup, input and output files, and result checks. Show how outputs feed the
next tool, including format conversions. Check terms for code, weights, data,
and base models. For a run, return the results and report any failed steps.
```

### Example tasks

- **Screen a compound library.** “I have a CSV of compound IDs and SMILES.
  Run ADMET-AI on CPU. Return endpoint predictions by compound ID and flag
  molecules the model could not score.”
- **Design candidates and plan routes.** “I have a receptor PDB, a reference
  ligand, and one GPU. Plan a DiffSBDD generation run, pose checks, and
  ADMET screening. Keep candidate IDs when converting SDF records to SMILES.
  Use PrexSyn to propose alternatives with synthesis pathways. Re-score any
  changed molecules and plan routes for the shortlisted compounds.”
- **Plan a route for a known compound.** “I have a target SMILES and a
  building-block stock. Run AiZynthFinder on CPU, then pass its route JSON and
  the stock to RENKIN. Report which routes reach the selected stock and which
  checks lack the data needed to run.”

## Tools your agent can use

### Structure and generation

| Task | Tool and starting input | Output |
| --- | --- | --- |
| Predict a receptor structure | [ColabFold](references/protein-structure-prediction.md) with a protein sequence | Structure models and confidence scores |
| Find a binding pocket | [P2Rank](references/structure-based-generation.md#p2rank--rdkp2rank) with a receptor structure | Ranked pocket predictions |
| Design candidates in a pocket | [DiffSBDD](references/structure-based-generation.md#diffsbdd--arneschneuingdiffsbdd) with a receptor PDB and pocket residues or a reference ligand | Candidate structures in 3D |
| Grow, decorate, or link molecular fragments | [GenMol](references/molecular-generation.md) with a fragment or scaffold | Candidate molecules |
| Find candidates similar to a query molecule | [PrexSyn](references/synthesizable-generation.md) with a query SMILES or a supported fingerprint | Candidate molecules with proposed synthesis pathways |

### Docking and binding

| Task | Tool and starting input | Output |
| --- | --- | --- |
| Prepare files for docking | [Meeko](references/docking-and-cofolding.md) with a receptor PDB and a 3D ligand SDF with explicit hydrogens | Receptor and ligand PDBQT files |
| Dock a ligand into a known pocket | [AutoDock Vina](references/docking-and-cofolding.md) with prepared receptor and ligand files and a search box | Ranked poses and empirical docking scores |
| Predict poses with learned docking | [DiffDock-L](references/docking-and-cofolding.md) with a receptor structure and ligand | Ranked poses and pose-confidence scores |
| Check docked poses | [PoseBusters](references/docking-and-cofolding.md#validate-poses) with docked poses in SDF and a receptor PDB | Per-pose geometry and clash checks |
| Predict a protein–ligand complex | [Boltz-2](references/docking-and-cofolding.md) with a protein sequence and ligand SMILES or CCD code, typically with a multiple sequence alignment | Predicted complex structure and an optional affinity estimate |
| Compare binding across related ligands | [OpenFE](references/binding-affinity-and-fep.md) with a prepared receptor PDB and ligand poses in SDF, in the same coordinate frame | Relative binding free-energy estimates |

### Properties, selectivity, and synthesis

| Task | Tool and starting input | Output |
| --- | --- | --- |
| Predict an assay endpoint | [Chemprop](references/property-and-qsar-prediction.md) with labeled molecules to train on and new molecules to score | Endpoint predictions for new molecules |
| Screen ADMET endpoints | [ADMET-AI](references/admet-prediction.md) with ligand SMILES | Predicted absorption, distribution, metabolism, excretion, and toxicity endpoints |
| Compare a candidate with a known off-target ligand | [ESP-Sim](references/target-and-selectivity-prediction.md) with 3D ligand conformers | Shape and electrostatic similarity scores |
| Propose precursors for one reaction | [ReactionT5v2](references/singlestep-retrosynthesis.md) with a product SMILES and the retrosynthesis checkpoint | Ranked precursor sets |
| Search for multi-step synthesis routes | [AiZynthFinder](references/retrosynthesis-planning.md) with a target SMILES and a configured model and stock | Ranked routes as route-tree JSON |
| Check proposed synthesis routes | [RENKIN](references/retrosynthesis-planning.md) with route JSON and a starting-material stock | Route structure, stock coverage, and reaction replay checks |

Use the [tool matrix](references/tool-matrix.md) to compare alternatives. The
reference guides link to upstream documentation and describe setup, hardware,
and method limits. For artifact terms, see the
[licensing and data guide](references/licensing-and-data.md).

## How tools connect

The public 1IEP example asks whether CPU docking can recover imatinib’s
experimental pose. Meeko stores the ligand’s SMILES and atom mapping in the
PDBQT file. Keep those records through the Vina run so Meeko can reconstruct
the ligand’s bond orders when exporting the poses to SDF.
[AutoDock Vina tutorial and input files](https://autodock-vina.readthedocs.io/en/latest/docking_basic.html) ·
[Meeko export](https://meeko.readthedocs.io/en/develop/export_usage.html) ·
[PoseBusters CLI](https://posebusters.readthedocs.io/en/latest/cli.html)

![CPU redocking workflow. Meeko writes receptor and ligand PDBQT files and a Vina search box config. AutoDock Vina returns docked poses in PDBQT and empirical docking scores. Meeko exports the poses to SDF. PoseBusters takes the pose SDF and reference files and writes a per-pose CSV report.](assets/skill-map.svg)

[Open the full-size diagram](assets/skill-map.svg)

Use the docking scores to rank poses and PoseBusters to check geometry,
clashes, and recovery of the crystal pose. Binding affinity requires a
separate method. [Affinity and free-energy guide](references/binding-affinity-and-fep.md)

For synthesis planning, pass AiZynthFinder's route-tree JSON and a declared
building-block stock to RENKIN. RENKIN checks route structure and stock
membership. Where reaction data permits, it also checks whether each declared
reaction regenerates the expected product.
[RENKIN walkthrough with a public route export](https://kent-tokyo.github.io/renkin/guides/aizynthfinder-audit-demo/)

## More references

- [Forward reaction modeling](references/forward-and-reaction-modeling.md)
  covers product prediction and checks for proposed retrosynthetic steps.
- [Agentic drug design](references/agentic-drug-design.md) compares frameworks
  that orchestrate multiple tools.
- [LDDM](references/lddm.md) covers docking, fragment editing, and generation
  with a single model family.
- [KRAS molecular-glue example](references/worked-example-kras-glue.md) shows how
  a public ternary structure changes the choice of modeling method.

<details>
<summary>Use the packaged skill in Claude Code</summary>

Clone the repository and register the skill in your
[Claude Code skills directory](https://code.claude.com/docs/en/skills).

```sh
git clone https://github.com/BioSymphony/small-molecules.git
cd small-molecules
mkdir -p ~/.claude/skills
ln -s "$PWD/skills/small-molecule-design-tools" ~/.claude/skills/small-molecule-design-tools
```

Invoke `/small-molecule-design-tools` with your task. Codex can use the
[packaged skill](skills/small-molecule-design-tools/SKILL.md) from the checkout.

</details>

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for source requirements and checks.

## License

The repository uses the [MIT License](LICENSE). Upstream tools and artifacts
have their own terms.
