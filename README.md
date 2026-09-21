![BioSymphony Small Molecules banner](assets/readme-banner.png)

# BioSymphony Small Molecules

BioSymphony Small Molecules is a skill that helps AI coding agents choose tools
for molecular generation, synthesis planning, docking, binding-affinity
estimation, and property prediction. Its reference guides compare methods,
describe setup requirements, and track code, model, and data licenses.

The repository supplies skill instructions, tool references, and a worked
example using a public KRAS structure. Install the selected tools and obtain
their model weights separately.

## Use the Skill

Clone the repository into a directory of your choice:

```bash
git clone https://github.com/BioSymphony/small-molecules.git
cd small-molecules
```

Ask your agent to read [SKILL.md](SKILL.md), describe your task, and include the
available inputs and compute resources. The skill directs the agent to the
relevant reference before it recommends tools or writes code.

For example:

> Read SKILL.md and recommend a CPU workflow to plan a synthesis route for a
> target SMILES. Specify the model, starting-material stock, and route checks.

> Read SKILL.md and compare tools for growing a fragment in a protein pocket
> while preserving selected atom coordinates. Explain the required inputs,
> checkpoint licenses, and pose-validation steps.

### Claude Code Installation

From the cloned repository directory, register the packaged skill in
[Claude Code's personal skills directory](https://code.claude.com/docs/en/skills):

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/small-molecule-design-tools" ~/.claude/skills/small-molecule-design-tools
```

Keep the clone in that location so the link remains valid. If a skill with that
name is already installed, check its location before replacing it.

Invoke it with `/small-molecule-design-tools` followed by your task.
Other agents can read `SKILL.md` and its linked Markdown references directly.

## Find a Reference

| Task | Reference |
|---|---|
| Compare tools across categories | [Tool matrix](references/tool-matrix.md) |
| Generate molecules with proposed synthesis routes or design analogs | [Synthesizable generation](references/synthesizable-generation.md) |
| Plan a route to a target molecule and check its starting materials | [Retrosynthesis planning](references/retrosynthesis-planning.md) |
| Dock ligands, predict complexes, and validate poses | [Docking and co-folding](references/docking-and-cofolding.md) |
| Estimate affinity or compare binding free energies | [Binding affinity and free energy](references/binding-affinity-and-fep.md) |
| Predict molecular properties or activity | [QSAR](references/property-and-qsar-prediction.md) and [ADMET](references/admet-prediction.md) |
| Compare related compounds and predict off-target activity | [Target and selectivity prediction](references/target-and-selectivity-prediction.md) |
| Generate molecules in a binding pocket | [Structure-based generation](references/structure-based-generation.md) |
| Use LDDM for docking, fragment editing, or generation | [LDDM](references/lddm.md) |
| Check code, weights, data, and base-model terms | [Licensing and data](references/licensing-and-data.md) |
| Explore a worked example using a public KRAS structure | [KRAS molecular-glue example](references/worked-example-kras-glue.md) |

The tool matrix contains 156 indexed rows across 18 categories. Grouped entries
and cross-references count as one row each. [SKILL.md](SKILL.md) maps additional
tasks, including reaction prediction, protein preparation, and chemistry
language models.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for source requirements and checks.

## License

The repository content uses the MIT License. Each upstream project sets its own
terms. The reference cards track source code, model weights, data, and base
models separately because one project can apply different terms to each layer.
