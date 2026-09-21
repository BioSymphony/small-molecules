# Contributing

Contributions must improve tool selection, license clarity, or examples that
use public or synthetic data.

Before opening a change:

- Read `AGENTS.md` and `PUBLIC_RELEASE.md`.
- Use only public or synthetic data in examples.
- Cite primary repositories, papers, model cards, and license files.
- Record the source and verification date for status or license changes.
- Check code, weights, data, and base-model terms separately.
- Exclude model weights, non-public data, uncurated generated media, and raw
  service logs.
- Keep root skill instructions and references synchronized with
  `skills/small-molecule-design-tools/`.

Before you open a pull request, run the public-release check:

```bash
make release-check
```

License notes in this repository support an initial review; they are not legal
advice. When you change a license or model-card claim, cite the primary source
and record the date you checked it.
