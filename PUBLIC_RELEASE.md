# Public Release Checklist

Use this checklist before publishing or refreshing the public repository.

## Scope

- Keep `SKILL.md`, `README.md`, and `references/` as the primary public surface.
- Keep demos compact and public-data-only.
- Leave non-release artifacts, raw cloud outputs, large media builds, and
  ignored generated directories out of the public repo.

## Repository Metadata

Repository name:

```text
biosymphony-small-molecules
```

GitHub About text:

```text
Agent skill for routing small-molecule design tasks to open tools, focused references, and license-aware implementation paths.
```

Suggested topics:

```text
ai-agents, agentic-ai, agent-skills, small-molecules, cheminformatics, drug-discovery, medicinal-chemistry, molecular-modeling, molecular-docking, molecular-generation, retrosynthesis, admet, qsar, protein-ligand, computational-biology, bioinformatics, biological-research, research-software, open-science, workflow-automation
```

## Checks

- [ ] No copied `.git` history from another repository.
- [ ] No `.env`, credentials, tokens, signed URLs, local workstation paths, provider IDs,
      raw logs, or cost ledgers.
- [ ] No unpublished biological data, non-public structures, non-public molecules,
      non-public assays, raw reads, model weights, or restricted datasets.
- [ ] No large generated media unless it is intentionally curated for public
      release.
- [ ] `make release-check` passes.
- [ ] Live license-sensitive claims have either been re-verified or still carry
      their existing verification date.
- [ ] Demo claims are labeled as public-data demos and not drug-discovery output.

## Public Cut

The public repo should read as a useful tool-selection skill even if the KRAS
demo is ignored. The demo supports the method boundary; it is not the product.
