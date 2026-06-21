# Agentic / LLM Retrosynthesis Planners

Planners that put a **large language model in the loop** — for strategy, constraint handling, route mutation, or natural-language explanation — usually wrapping a classical retro engine (AiZynthFinder, Syntheseus, MEEA*) for the actual chemistry. They are best treated as **chemist-in-the-loop aids**: every LLM-proposed disconnection needs feasibility checking, and most depend on a **paid commercial LLM API**.

> Two recurring caveats for everything here: (1) **hallucinated reactions** — LLMs propose chemically invalid steps, so validity/feasibility guarding is mandatory; (2) **API dependence** — the strongest configs call Anthropic/OpenAI/Gemini, which has cost and data-egress implications.

## Working code

## DeepRetro — *most production-ready; peer-reviewed, GUI*

> Hybrid retrosynthesis: template/MCTS engines + iterative LLM reasoning in a feedback loop, with validity/stability/hallucination checks, recursive route refinement, and a human-in-the-loop viewer.

- **Repo:** https://github.com/deepforestsci/DeepRetro (Deep Forest Sciences). MIT.
- **License:** **MIT** code. USPTO models auto-download (free); **Pistachio models are license-restricted** (commercial permission needed).
- **Paper:** **peer-reviewed** — *DeepRetro discovers retrosynthetic pathways through iterative large language model reasoning*, Scientific Reports 2026, 16:8448 (DOI 10.1038/s41598-026-38821-z); preprint arXiv:2507.07060.
- **LLM backend:** Claude 3 Opus / 3.7 Sonnet / 4 Sonnet (Anthropic) + DeepSeek-R1 (Fireworks). Needs `ANTHROPIC_API_KEY`, `FIREWORKS_API_KEY`.
- **Engine:** AiZynthFinder underneath; RDKit; Python 3.9.
- **Install / run:** Docker (`docker-compose up -d`) or conda (`environment.yml`, `download_public_data`, `python src/api.py`, serve `viewer/` GUI). Self-hostable; no public SaaS.
- **I/O:** target SMILES → reaction-pathway trees + interactive visualization; LLM proposes steps, loop adds validity/stability/hallucination checks; chemist edits in the GUI.
- **Use it when:** you want the most complete, citable, deployable LLM-assisted planner with explicit hallucination control. Best default in this category.

## Synthelite — *chemist-aligned, constraint-steerable*

> Decouples LLM strategic planning (Phase 1) from MCTS execution to keep LLM cost bounded; accepts natural-language synthesis constraints per target.

- **Repo:** https://github.com/schwallergroup/synthelite (Schwaller group, EPFL). Ignore the `cprabhukumar99-rgb/Synthelite` fork.
- **License:** **MIT** code. It is a **heavily-modified fork of AiZynthFinder**, so AiZynthFinder's terms also apply; precomputed routes on HF `SchwallerGroup/synthelite`. Uses an eMolecules stock.
- **Paper:** *Synthelite: Chemist-aligned and feasibility-aware synthesis planning with LLMs*, arXiv:2512.16424 (Dec 2025). Preprint.
- **LLM backend:** config presets for Claude-4.5-Sonnet and Gemini-2.5 (GPT-5 in results), via **OpenRouter**. Needs `OPENROUTER_API_KEY` + `OPENAI_API_KEY` (embeddings). Reported ~74% solve rate.
- **Install / run:** `conda env create -f env-dev.yml`; `poetry install --all-extras`; `synthelite_llm_cli --smiles targets.csv --config …claude4_5.yml`.
- **I/O:** CSV `(idx, smiles, steer_query)` where `steer_query` is a NL constraint → JSON route tree + LLM strategy text.
- **Use it when:** you want natural-language steering of routes and a feasibility-aware planner; young (early-stage) but actively pushed.

## LLM-Syn-Planner — *evolutionary LLM route search*

> LLMs generate full candidate routes (retrieval-augmented) and **iteratively mutate/select** them against a reward — an evolutionary search over routes.

- **Repo:** https://github.com/zoom-wang112358/LLM-Syn-Planner. MIT. (Not Samsung's `SAITPublic/llm_synth_planner`, which is unrelated.)
- **Paper:** *LLM-Augmented Chemical Synthesis and Design Decision Programs*, ICML 2025 (arXiv:2505.07027).
- **LLM backend:** GPT-4o + DeepSeek-V3 (both API keys required). No own weights.
- **Install / run:** conda py3.9 + PyTorch + `pip install PyTDC syntheseus[all] selfies rdchiral`; `python main.py --method planning --dataset_name USPTO-easy …`. Uses **Syntheseus** + rdchiral.
- **Maintenance:** lightly maintained (last push 2025-08; ~5 stars). Pistachio-derived benchmark data is restricted.
- **Use it when:** you want an evolutionary, route-level LLM planner and already use Syntheseus.

## Watchlist (no usable/licensed code yet)

These are promising but **not runnable / not safely reusable** today — fuller notes in [watchlist.md](watchlist.md).

- **LARC** (`ninglab/LARC`) — constrained agentic retro with an "Agent-as-a-Judge" injecting tool-grounded constraint feedback (avoid carcinogens/pyrophorics/etc.). Real code, but ⚠️ **no LICENSE file (all rights reserved)**; Claude-3.5-Sonnet / Mistral-Nemo backends; MEEA* engine. arXiv:2508.11860 (2025), under review.
- **Retro-Expert** — LLM (Qwen2.5-7B + RL) collaborating with specialist models (T5Chem, GraphRetro) for **interpretable** single-step retro with NL explanations. ⚠️ **No public repo** — preprint arXiv:2508.10967 (2025).
- **ReTriP** — end-to-end CoT retrosynthetic planning, RL with verifiable rewards, on a BioMedGPT-Mol (Qwen3-8B) base. ⚠️ **No code** — preprint arXiv:2603.29723 (2026).

## Choosing

- **Deployable, supported, hallucination-guarded:** **DeepRetro**.
- **Constraint/strategy steering in natural language:** **Synthelite** (or LARC once licensed).
- **Route-level evolutionary search:** **LLM-Syn-Planner**.
- **Self-hosted open-weight backbone (no commercial API):** the *designs* of Retro-Expert/ReTriP target this, but neither has released code — so in practice every usable tool here needs a paid LLM API.

Universal rule: validate LLM-proposed routes with a single-step model + forward round-trip check (see [synthesizability-scoring.md](synthesizability-scoring.md)) before trusting them.
