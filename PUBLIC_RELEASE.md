# Public Release Checklist

Use this checklist before you publish or update the public repository.

## Scope

- Keep `SKILL.md`, `README.md`, and `references/` as the primary public files.
- Keep demos compact and public-data-only.
- Leave non-release artifacts, raw cloud outputs, large media builds, and
  ignored generated directories out of the public repository.

## Repository Metadata

Repository name:

```text
small-molecules
```

GitHub About text:

```text
Agent skill for routing small-molecule design tasks to open and publicly documented tools, focused references, and license-aware implementation paths.
```

Suggested topics:

```text
ai-agents, agentic-ai, agent-skills, small-molecules, cheminformatics, drug-discovery, medicinal-chemistry, molecular-modeling, molecular-docking, molecular-generation, retrosynthesis, admet, qsar, protein-ligand, computational-biology, bioinformatics, biological-research, research-software, open-science, workflow-automation
```

## Checks

- [ ] No copied `.git` history from another repository.
- [ ] No `.env`, credentials, tokens, signed URLs, local workstation paths, or
      raw service logs.
- [ ] No unpublished biological data, non-public structures, non-public molecules,
      non-public assays, raw reads, model weights, or restricted datasets.
- [ ] No large generated media unless it is reviewed for public release.
- [ ] `make release-check` passes.
- [ ] Each changed license or status claim cites a primary source and records
      its verification date.
- [ ] Demo claims are labeled as public-data demos and not drug-discovery output.

## Standalone Skill

The tool-selection skill must remain useful without the KRAS demo. The demo
illustrates the documented workflow with public inputs.
