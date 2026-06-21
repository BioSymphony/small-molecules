# Synthesizability Scoring

How to answer "**is this generated molecule actually makeable?**" — the scoring layer that sits between a generator and a chemist. Heuristic SAscore is fast but route-blind; the tools here are **route-aware** (they run or approximate retrosynthesis) and so correlate better with real synthesizability, at higher compute cost.

## RetroScore — *route-aware accessibility score (MIT code)*

> Synthetic-accessibility scoring guided by **multistep** retrosynthesis. Couples a semi-template single-step model (Graph2Edits) with the Retro* search algorithm and adds a **graph-edit-distance** term so scores reward atom economy alongside route reliability/length.

- **Repo:** https://github.com/Snowgao320/RetroScore (new, created 2025-10; ~1 star).
- **License:** ⚠️ **split** — **code MIT**, but the **paper text is CC BY-NC-ND 4.0** (non-commercial; governs the article, not the code), and the **model weights/data have no explicit license** (two checkpoints ship in `experiments/`; more weights via Dropbox). Treat the weights as unspecified — verify before commercial use.
- **Paper:** *RetroScore: graph edit distance-guided retrosynthesis for accessibility scoring with route metrics*, J. Cheminform. 2025 (DOI 10.1186/s13321-025-01138-6).
- **Install / run:** `conda create -n RetroScore python=3.11`; `torch==2.6.0` (CUDA 11.8 wheel); `pip install -r requirements.txt`. A packaged API exists: `pip install retroscore` (author endorses it, but PyPI metadata is sparse).
- **I/O:** molecule SMILES → accessibility score (route-derived) + route metrics (length, confidence, GED). Reported 97.37% planning success; beat 6/7 SA metrics on a generation task.
- **Deps / hardware:** PyTorch 2.6, RDKit, Graph2Edits, Retro*. **GPU recommended** (it runs a neural multistep search) — the most compute-heavy scorer here.
- **Maintenance:** brand-new, minimal history (4 commits, no releases on GitHub). Longevity unproven.
- **Use it when:** you want a route-aware SA score that accounts for atom economy, for ranking/filtering generator output. Confirm the weights license before any commercial deployment.

## Round-trip score / round-trip accuracy — *a method, not a package*

> **The cheapest credible synthesizability sanity check.** Take a predicted retrosynthetic disconnection (the proposed precursors), run them through a **forward** reaction-prediction model, and check whether the original target is recovered. The fraction of single-step suggestions that round-trip = round-trip accuracy. It measures precursor validity/feasibility **without ground-truth labels**.

- **Origin:** Schwaller et al. — workshop version *Evaluation Metrics for Single-Step Retrosynthetic Models* (NeurIPS ML4PS 2019); full method in *Predicting retrosynthetic pathways using a combined linguistic model and hyper-graph exploration strategy*, Chem. Sci. 2020, 11, 3316 (DOI 10.1039/C9SC05704H), using the Molecular Transformer as the forward model.
- **Implementation:** no single repo — it's a pattern. Pair any retro suggestion with a forward model (e.g., **ReactionT5v2-forward**, **RXNGraphormer**, Molecular Transformer / rxn4chemistry) and compare the predicted product to the target (canonical-SMILES match). Commonly used in ASKCOS-style validation.
- **Use it when:** validating routes from any planner — especially **LLM/agentic** planners ([agentic-retrosynthesis.md](agentic-retrosynthesis.md)), where hallucinated steps are the main risk. It's the practical first filter before deeper scoring.

## RetroTrim — *hallucination-filtering ensemble* ⚠️ preprint only

> A "trustworthy retrosynthesis" system that filters **hallucinated** reactions using a **diverse ensemble of reaction scorers** (ML models + database lookups), each catching a different hallucination class. Won the Standard Industries Retrosynthesis Challenge; reported as the only method that removes hallucinated reactions while keeping the most high-quality routes on hard drug-like targets.

- **Repo:** ⚠️ **None found** — no code-availability statement or GitHub link in the paper. **Not installable.** See [watchlist.md](watchlist.md).
- **Paper:** *Trustworthy Retrosynthesis: Eliminating Hallucinations with a Diverse Ensemble of Reaction Scorers*, arXiv:2510.10645 (v3 2025-12). Preprint.
- **Use it when:** conceptually the right direction for route validation/scoring; watch for a code release. Until then, approximate its idea with a **round-trip score + multiple single-step scorers** (a poor-man's diverse ensemble).

## shallow-tree — *fast synthesizability screen via depth-limited AiZynthFinder (2026)* ⚠️ GPL-3.0

> Depth-restricted DFS over **AiZynthFinder** with branch caching (~2–3× speedup) for screening large batches of generator output — a fast route-aware filter to run *before* the heavier RetroScore / full search.

- **Repo:** `Arhs99/shallow-tree` — ⚠️ **GPL-3.0** (copyleft — matters if you embed/ship). Tied to a ChemRxiv "joint synthesis planning via common intermediates" (2026).
- **Maintenance:** pushed Jun 2026 (solo-dev, early-stage).
- **Commercial:** ⚠️ GPL-3.0; fine for research/internal screening. Use it when you need a fast route-aware triage over many candidates and GPL is acceptable; otherwise approximate with depth-capped AiZynthFinder directly.

## Scope caveat — macrocycles & natural-product scaffolds

Every scorer here (and the planners they wrap) is trained on **USPTO-style drug-like reaction corpora**. They are unreliable outside that distribution: **macrocyclizations, complex polycyclic/stereochemically dense natural products, and NP-derived drugs** get over-pessimistic or simply meaningless scores. Concrete case: **daraxonrasib** (the pan-RAS(ON) glue) is a **sanglifehrin-derived macrocycle** — a route-aware score from these tools is low-confidence and must be cross-checked by a chemist, not trusted as a filter. Treat a bad synthesizability score on a macrocyclic/NP scaffold as "out of model scope," not "unmakeable." See the [KRAS(ON) glue worked example](worked-example-kras-glue.md).

## Choosing

- **Cheap, label-free, works with any planner:** **round-trip score** (pair a retro suggestion with ReactionT5v2-forward / RXNGraphormer). Start here.
- **Fast route-aware screen over many candidates (GPL-3.0):** **shallow-tree** (depth-limited AiZynthFinder).
- **Route-aware SA score for ranking generator output:** **RetroScore** (mind the weights license).
- **Hallucination-class ensemble filtering:** **RetroTrim** in spirit — no code yet; emulate with round-trip + several scorers.

These pair naturally with the generators ([synthesizable-generation.md](synthesizable-generation.md), [molecular-generation.md](molecular-generation.md)): generate → score synthesizability → keep only routes that round-trip.
