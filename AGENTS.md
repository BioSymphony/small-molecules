# BioSymphony Small Molecules Agent Guide

Guide for agents and operators working in this public-safe skill repo.

## Mission

Maintain an agent-readable map of open small-molecule design tools: synthesis
planning, synthesizable generation, docking, co-folding, free energy, QSAR,
ADMET, selectivity, and structure-based generation.

The repo is a routing and diligence layer. It helps an agent choose a tool,
understand the license stack, and avoid treating confidence scores or README
badges as stronger support than they are.

## Public Safety Rules

Do not add:

- API keys, provider credentials, signed URLs, SSH keys, or registry auth
- local workstation paths or copied repository history
- pod IDs, network volume IDs, account IDs, raw provider logs, or cost ledgers
- non-public issue text, non-release planning notes, unpublished structures,
  non-public sequences, non-public assays, non-public datasets, raw reads, database mirrors, or
  model weights
- generated media or large demo artifacts unless they are explicitly curated for
  public release

Use only public structures, public tool metadata, synthetic examples, or compact
public demo artifacts. Keep claims tied to the support in the docs.

## Required Checks

Run before committing public-release changes:

```bash
make release-check
```

That gate compiles the public Python scripts, scans for local paths and secret
patterns, and checks the markdown links that can be checked locally.

## Skill Loop

Use `SKILL.md`. Summary: identify the task category, open the matching
reference file, check code/weights/data/base-model licenses separately, then
recommend the smallest tool path that fits the user request.

## Claim Boundaries

Treat this repo as tool-selection guidance, not legal advice, medical advice, or
validated drug-discovery output. Before commercial use, re-check live upstream
licenses and data terms.
