# BioSymphony Small Molecules Agent Guide

Use this guide when you update the public skill repository.

## Mission

Maintain an agent-readable map of open small-molecule design tools: synthesis
planning, synthesizable generation, docking, co-folding, free energy, QSAR,
ADMET, selectivity, and structure-based generation.

The repository helps an agent choose a tool, review each license layer, and
distinguish model confidence from experimental evidence.

## Public Safety Rules

Do not add:

- API keys, provider credentials, signed URLs, SSH keys, or registry authentication
- local workstation paths or copied repository history
- pod IDs, network volume IDs, account IDs, raw provider logs, or cost ledgers
- non-public issue text, non-release planning notes, unpublished structures,
  non-public sequences, non-public assays, non-public datasets, raw reads,
  database mirrors, or model weights
- generated media or large demo artifacts unless they are reviewed for public
  release

Use only public structures, public tool metadata, synthetic examples, or compact
public demo artifacts. Cite the public repository, paper, model card, or license
file that supports each claim.

## Required Checks

Run before committing public-release changes:

```bash
make release-check
```

This command compiles the public Python scripts, scans for local paths and secret
patterns, and checks the Markdown links that can be checked locally.

## Skill Loop

Use `SKILL.md`:

1. Identify the task category.
2. Open the matching reference file.
3. Check the code, model weights, data, and base-model terms separately.
4. Recommend the smallest tool path that fits the request.

## Claim Boundaries

Treat this repository as tool-selection guidance, not legal advice, medical
advice, or validated drug-discovery output. Before product use, re-check the
upstream licenses and data terms.
