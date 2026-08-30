# Agentic and LLM-Assisted Retrosynthesis Planners

These planners use a large language model for strategy, constraint handling,
route revision, or natural-language explanation. Most use a conventional
retrosynthesis engine, such as AiZynthFinder, Syntheseus, or MEEA*, for reaction
prediction and search. Review every proposed disconnection and test it with a
forward-feasibility check.

For each system, review the terms for the planner, model weights, reaction
corpora, stock set, and external model services.

## Working code

## DeepRetro — *peer-reviewed GUI with iterative route refinement*

> Hybrid retrosynthesis: template/MCTS engines + iterative LLM reasoning in a feedback loop, with validity/stability/hallucination checks, recursive route refinement, and a human-in-the-loop viewer.

- **Repository:** https://github.com/deepforestsci/DeepRetro (Deep Forest Sciences). MIT.
- **License:** **MIT** code. Public USPTO models are available from the project; Pistachio-derived models have separate access and usage terms.
- **Paper:** **peer-reviewed** — *DeepRetro discovers retrosynthetic pathways through iterative large language model reasoning*, Scientific Reports 2026, 16:8448 (DOI 10.1038/s41598-026-38821-z); preprint arXiv:2507.07060.
- **LLM backend:** the repository supports externally hosted LLM backends; the service and model terms are separate from the MIT code license.
- **Engine:** AiZynthFinder underneath; RDKit; Python 3.9.
- **Install and run:** Docker (`docker-compose up -d`) or conda (`environment.yml`, `download_public_data`, `python src/api.py`, serve `viewer/` GUI).
- **Inputs and outputs:** Target SMILES → reaction-pathway trees and an interactive visualization. The LLM proposes steps; validity, stability, and hallucination checks evaluate each step; a chemist can edit the tree in the GUI.
- **Use it when:** you need a citable LLM-assisted planner with a GUI and explicit validity checks around AiZynthFinder.

## Synthelite — *chemist-aligned, constraint-steerable*

> Separates strategic LLM planning from MCTS execution and accepts
> natural-language synthesis constraints for each target.

- **Repository:** https://github.com/schwallergroup/synthelite (Schwaller group, EPFL). The `cprabhukumar99-rgb/Synthelite` repository is a fork.
- **License:** **MIT** code. The project is a heavily modified AiZynthFinder fork; review the AiZynthFinder repository license and the HF route and data records separately.
- **Paper:** *Synthelite: Chemist-aligned and feasibility-aware synthesis planning with LLMs*, arXiv:2512.16424 (Dec 2025). Preprint.
- **LLM backend:** configurable external LLM service; the repository does not publish its own model weights. The paper reports a ~74% solve rate.
- **Install and run:** `conda env create -f env-dev.yml`; `poetry install --all-extras`; `synthelite_llm_cli` accepts a target CSV and a configuration file.
- **Inputs and outputs:** CSV `(idx, smiles, steer_query)` where `steer_query` is a NL constraint → JSON route tree + LLM strategy text.
- **Use it when:** you want natural-language route steering and a feasibility-aware planner.

## LLM-Syn-Planner — *evolutionary LLM route search*

> LLMs generate candidate routes, then mutate and select them with a reward function.

- **Repository:** https://github.com/zoom-wang112358/LLM-Syn-Planner. MIT.
- **Paper:** *LLM-Augmented Chemical Synthesis and Design Decision Programs*, ICML 2025 (arXiv:2505.07027).
- **LLM backend:** external LLM service; no project weights are released.
- **Install and run:** conda py3.9 + PyTorch + `pip install PyTDC syntheseus[all] selfies rdchiral`; `python main.py --method planning --dataset_name USPTO-easy …`. Uses **Syntheseus** + rdchiral.
- **Maintenance:** The last recorded repository push was in August 2025. Pistachio-derived benchmark data is restricted.
- **Use it when:** you want an evolutionary, route-level LLM planner built around Syntheseus.

## RetroAgent — *structured-memory multi-step planner (MIT code; Apache-2.0-tagged weights)*

> LLM agent that searches an AND-OR graph of molecules and reactions through
> tool calls. The released policy is trained on a Qwen3-4B-Instruct-2507 base
> model and uses the search state at each step, not only one candidate route.

- **Repository:** https://github.com/SXKDZ/RetroAgent · **Paper:** [RetroAgent: Harnessing LLMs to Search Over Structured Memory for Agentic Retrosynthesis Planning](https://arxiv.org/abs/2607.14512) (COLM 2026).
- **License:** **MIT** repository code. The [Hugging Face model card](https://huggingface.co/SXKDZ/RetroAgent) labels the released checkpoint **Apache-2.0** and identifies `Qwen/Qwen3-4B-Instruct-2507` as its base model. Base-model and data terms remain separate.
- **Weights:** Hugging Face `SXKDZ/RetroAgent`; the model card identifies it as a 4B-parameter policy.
- **Inputs and outputs:** target molecule plus a tool harness containing single-step template prediction, building-block lookup, and molecular scoring → an AND-OR route search and completed-route result.
- **Data and dependencies:** the README identifies eMolecules building blocks and DESP/Retro* single-step assets, plus SCScore. These assets have terms separate from the repository code and checkpoint.
- **Use it when:** you want structured-memory search with a released policy and can provide the accompanying chemistry tools and data.

## Watchlist (code or artifact status incomplete)

These methods have incomplete public code, weights, or license information. The watchlist records their public code, weight, and license status.

- **LARC** (`ninglab/LARC`) — constrained agentic retrosynthesis with an "Agent-as-a-Judge" that adds tool-grounded constraints, such as avoiding carcinogens and pyrophoric compounds. The public repository has no `LICENSE` file; it uses the MEEA* engine. arXiv:2508.11860 (2025), under review.
- **Retro-Expert** — LLM (Qwen2.5-7B + RL) collaborating with specialist models (T5Chem, GraphRetro) for **interpretable** single-step retro with natural-language explanations. ⚠️ **No public repository** — preprint arXiv:2508.10967 (2025).
- **ReTriP** — CoT-based retrosynthetic planning with RL and verifiable rewards, on a BioMedGPT-Mol (Qwen3-8B) base. ⚠️ **No code** — preprint arXiv:2603.29723 (2026).
- **SynthEx** — strategy-first planning for complex natural products using editable reaction-graph actions. The [repository](https://github.com/schwallergroup/synthex) says code is not yet published and displays an Apache-2.0 release as planned; routes are browsable at [SynthAtlas](https://synthatlas.epfl.ch). Preprint [arXiv:2608.07454](https://arxiv.org/abs/2608.07454) (2026).

## Choosing

| Need | Start with | Limit |
|---|---|---|
| GUI and route-validity checks | **DeepRetro** | Requires an external model backend |
| Natural-language constraints and strategy | **Synthelite** | Requires an external model backend |
| Route-level evolutionary search | **LLM-Syn-Planner** | Requires an external model backend |
| Structured-memory search with released weights | **RetroAgent** | Requires its chemistry tools and data |
| Natural-product strategy planning | **SynthEx** | Code release is pending |

Validate every LLM-proposed route with a one-step model and a forward round-trip
check. See [synthesizability-scoring.md](synthesizability-scoring.md).
