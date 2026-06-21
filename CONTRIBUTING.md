# Contributing

Contributions should improve tool selection, licensing clarity, or public-safe
examples.

Before opening a change:

- read `AGENTS.md` and `PUBLIC_RELEASE.md`
- keep examples public-data-only
- cite upstream repos, papers, model cards, and license files
- separate code, weights, data, and base-model terms
- avoid adding model weights, non-public datasets, generated media, or raw run logs

Run:

```bash
make release-check
```

License notes in this repo are diligence aids, not legal advice. If a license or
model-card claim has changed upstream, update the verification date and source
context in the relevant reference file.
