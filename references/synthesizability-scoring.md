# Synthesizability Scoring

Synthesizability scoring helps rank generated molecules by makeability.
Heuristic synthetic-accessibility scores are inexpensive but do not model a
route. The route-aware methods in this reference run or approximate retrosynthesis.
They require more compute and provide evidence tied to a proposed route.

## RetroScore — *route-aware accessibility score (MIT code)*

> Synthetic-accessibility scoring guided by **multistep** retrosynthesis. Couples a semi-template single-step model (Graph2Edits) with the Retro* search algorithm and adds a **graph-edit-distance** term so scores reward atom economy alongside route reliability/length.

- **Repository:** https://github.com/Snowgao320/RetroScore (created in October 2025).
- **License:** ⚠️ **split** — **code MIT**, while the **paper text is CC BY-NC-ND 4.0**. The repository and linked artifacts do not state an explicit license for the model weights or data (two checkpoints ship in `experiments/`; more weights are linked from Dropbox).
- **Paper:** *RetroScore: graph edit distance-guided retrosynthesis for accessibility scoring with route metrics*, J. Cheminform. 2025 (DOI 10.1186/s13321-025-01138-6).
- **Install and run:** `conda create -n RetroScore python=3.11`; `torch==2.6.0` (CUDA 11.8 wheel); `pip install -r requirements.txt`. A packaged API exists: `pip install retroscore` (author endorses it, but PyPI metadata is sparse).
- **Inputs and outputs:** molecule SMILES → accessibility score (route-derived) + route metrics (length, confidence, GED). Reported 97.37% planning success; beat 6/7 SA metrics on a generation task.
- **Dependencies and hardware:** PyTorch 2.6, RDKit, Graph2Edits, Retro*. GPU recommended for neural multistep search.
- **Maintenance:** The repository has four commits and no GitHub releases.
- **Use it when:** you want a route-aware SA score that accounts for atom economy when ranking or filtering generator output. Keep the code, weights, data, and paper terms separate.

## Round-trip score / round-trip accuracy — *a method, not a package*

> A low-cost synthesizability check. Pass the proposed precursors from a
> retrosynthetic disconnection to a forward reaction model. Then test whether
> the model recovers the original target. Round-trip accuracy is the fraction
> of one-step suggestions that recover the target. It measures precursor
> feasibility without ground-truth labels.

- **Origin:** Schwaller et al. — workshop version *Evaluation Metrics for Single-Step Retrosynthetic Models* (NeurIPS ML4PS 2019); full method in *Predicting retrosynthetic pathways using a combined linguistic model and hyper-graph exploration strategy*, Chem. Sci. 2020, 11, 3316 (DOI 10.1039/C9SC05704H), using the Molecular Transformer as the forward model.
- **Implementation:** No single repository defines this pattern. Pair each retrosynthetic suggestion with a forward model, such as **ReactionT5v2-forward**, **RXNGraphormer**, Molecular Transformer, or rxn4chemistry. Compare the predicted product with the target using canonical SMILES. ASKCOS-style workflows commonly use this check.
- **Use it when:** you need a low-cost first pass for routes from any planner. It is especially useful for LLM-assisted planners because they can propose invalid reactions.

## RetroTrim — *hallucination-filtering ensemble* ⚠️ preprint only

> The paper describes an ensemble of reaction scorers and database lookups for
> filtering proposed reactions. It reports results from the Standard Industries
> Retrosynthesis Challenge and higher route quality on hard drug-like targets.

- **Repository:** No public code-availability statement or GitHub link is listed in the paper; no installation package is described.
- **Paper:** *Trustworthy Retrosynthesis: Eliminating Hallucinations with a Diverse Ensemble of Reaction Scorers*, arXiv:2510.10645 (v3 2025-12). Preprint.
- **Use it when:** you are comparing ensemble-based route-validation methods. No public code is listed; approximate the method with a round-trip score plus multiple single-step scorers.

## shallow-tree — *depth-limited AiZynthFinder screen (2026)* ⚠️ GPL-3.0

> Depth-restricted DFS over AiZynthFinder with branch caching (~2–3× speedup)
> for screening large batches of generator output. It is intended as a
> pre-search route screen before RetroScore or full AiZynthFinder search.

- **Repository:** `Arhs99/shallow-tree` — **GPL-3.0**. Tied to a ChemRxiv "joint synthesis planning via common intermediates" (2026).
- **Maintenance:** The last recorded repository push was in June 2026.
- **Use it when:** you need depth-limited route triage over many candidates. The GPL-3.0 code license and AiZynthFinder dependency are separate from route data and model terms.

## Scope caveat — macrocycles & natural-product scaffolds

Every scorer and planner described in this reference was trained on
USPTO-style drug-like reaction corpora. Macrocyclizations, complex polycyclic
natural products, and stereochemically dense structures fall outside that
distribution and can receive over-pessimistic or meaningless scores.
Daraxonrasib is a sanglifehrin-derived macrocycle, so a chemist must review its
route-aware score. Treat a low score for a macrocyclic or natural-product
scaffold as an out-of-scope result rather than proof that the molecule cannot be
made. See the [KRAS(ON) glue worked example](worked-example-kras-glue.md).

## Choosing

| Need | Start with | Limit |
|---|---|---|
| Planner-independent check without labels | **Round-trip score** with ReactionT5v2-forward or RXNGraphormer | Tests whether a forward model recovers the target |
| Route-aware screen over many candidates | **shallow-tree** | GPL-3.0; depth-limited AiZynthFinder search |
| Route-aware score for generator output | **RetroScore** | Check the separate weight and data terms |
| Ensemble filtering by hallucination class | **RetroTrim method** | No public code; reproduce the pattern with round-trip checks and multiple scorers |

For a synthesis-aware workflow, generate candidates, score their routes, and
keep routes that pass round-trip and route checks. See
[synthesizable-generation.md](synthesizable-generation.md) and
[molecular-generation.md](molecular-generation.md).
