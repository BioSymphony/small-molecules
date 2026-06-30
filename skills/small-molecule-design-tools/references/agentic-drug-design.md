# Agentic / LLM-Orchestrated Drug Design

A fast-emerging 2025–2026 category: **LLM / multi-agent systems that orchestrate the other tools in this compilation** — generation, docking, affinity, ADMET, retrosynthesis — into autonomous or semi-autonomous hit-to-lead loops. This is distinct from **agentic *retrosynthesis*** (route-planning only — see [agentic-retrosynthesis.md](agentic-retrosynthesis.md)); these aim at the *whole* design-make-test loop.

**Reality check before adopting any of these:**
- **API-dependent + chemist-in-the-loop.** Almost all drive a paid commercial LLM (GPT/Claude/Gemini) or a large open-weight model; they cost money per run and send your structures to that model. Treat outputs as drafts to verify.
- **Young.** Most are single-author academic code drops or reference architectures, not maintained dependencies. The value is often the *blueprint* (which tools to wire together, with a critic/verification loop) as much as the code.
- **Highly relevant to an orchestration platform** — these are essentially open prototypes of what a `biosymphony`-style system does (route a task across generation → dock → ADMET → retro). Mine them for architecture.

Verified **2026-06-13**. Licenses read from the actual LICENSE file / HF card; recency and code-availability flagged where uncertain.

---

## AgentD — `hoon-ock/AgentD` ⭐ *(the runnable one)*
- **What/method:** Single-orchestrator LLM agent (CMU, Barati Farimani lab) running a real small-molecule pipeline — REINVENT + Mol2Mol (generation), Deep-PK (ADMET, ~75 props), BAPULM + **Boltz-2** (affinity/structure), UniProt/ChEMBL retrieval, RDKit, FAISS-RAG — via LangChain. The best-maintained, genuinely-clonable, small-molecule-specific orchestration agent found.
- **Code license:** **MIT.** Backend API-dependent (GPT-4o primary; Claude-3.7 / DeepSeek optional).
- **Paper:** *LLM Agent for Modular Task Execution in Drug Discovery*, arXiv:2507.02925 (v1 Jun 2025 → v3 Dec 2025).
- **Status:** Pushed 2026-02; ~39★ (most active academic agentic-DD repo).
- **Commercial:** ✅ MIT code; ⚠️ you pay for the LLM API and the orchestrated tools carry their own licenses (it wires up Boltz-2, REINVENT, Deep-PK — note Deep-PK is a non-commercial web tool, see [admet-prediction.md](admet-prediction.md)).

## CLADD — `Genentech/CLADD`
- **What/method:** Training-free **RAG-enhanced multi-agent** system for molecular QA / DD reasoning — Planning + Knowledge-Graph + Molecule-Understanding agents retrieving from biomedical KGs (PrimeKG/PubChem). Industrial provenance (Genentech). QA/reasoning-oriented, *not* a generative design-make loop.
- **Code license:** **Apache-2.0** (read the file; © 2025 Genentech — GitHub shows "NOASSERTION" only due to a copyright preamble). Model-agnostic LLM backend.
- **Paper:** arXiv:2502.17506, **AAAI 2026**.
- **Status:** Pushed 2025-11; ~20★.
- **Commercial:** ✅ Apache-2.0 code; ⚠️ + LLM API. Best open *reasoning/QA* multi-agent blueprint here.

## delta — `deltawave-tech/delta` *(reference architecture)*
- **What/method:** Six-agent "auditable molecular optimisation" platform — Principal Researcher orchestrator + Database + AI-Expert (de novo via Prot2Mol) + Medicinal Chemist + Ranking + **Scientific Critic**; tools = UniProt/PDB/ChEMBL + **AutoDock Vina, RDKit, PLIP**. Demonstrated on AKT1. The clearest *critic-loop computational-medchem-campaign* blueprint.
- **Code license:** **MIT.** API-dependent (Claude-3.7/Sonnet-4, o3, Gemini-2.5-Pro, GPT-4.1 benchmarked).
- **Paper:** arXiv:2508.03444 (Aug 2025).
- **Status:** ⚠️ One-shot code drop (pushed 2025-08, ~7★) — a blueprint, not a living dependency.
- **Commercial:** ✅ MIT; ⚠️ + API. **Watchlist-grade** — adopt the architecture, not the package.

## DrugPilot — `wzn99/DrugPilot`
- **What/method:** ReActAgent / LlamaIndex framework with a multi-modal "parameter memory pool" for DD task automation.
- **Code license:** **MIT;** API-driven. Pushed 2026-01; ~21★. Notebook-grade.
- **Commercial:** ✅ MIT; ⚠️ evaluate code quality first. **Watchlist.**

---

## Watchlist (paper-only or no usable license)

- **Mozi** (arXiv:2603.03655, Mar 2026) — the strongest *architecture* seen: governed multi-agent over Vina / AF3 / DiffSBDD / ADMET-AI / REINVENT4 / **LigUnity**, runs on open-weight Qwen3/DeepSeek (no paid API). **Project page + `OpenMol/DD100` benchmark only — no code yet.** Watch for release.
- **ToolMol** (arXiv:2605.12784) — tool-using agent on open GPT-OSS-120B. No public code yet.
- **OrchestRA** (arXiv:2512.21623), **FROGENT** (arXiv:2508.10760), **PharmAgents** (arXiv:2503.22164) — agentic-DD papers, no public code.
- **LIDDiA** (`ninglab/LIDDiA`, EMNLP 2025) and **Prompt-to-Pill** (`ChatMED/Prompt-to-Pill`, 2026) — code exists but **no LICENSE file** (all rights reserved) → not safely reusable.

> **Not small-molecule-specific (so not added):** **Robin** (`Future-House/robin`, Apache-2.0) is an excellent general AI-scientist / repurposing agent, but not de-novo small-molecule design. Worth knowing as orchestration prior art.

## Where this fits

These are the **orchestration layer over the rest of the compilation** — they call the generators ([synthesizable-generation.md](synthesizable-generation.md), [structure-based-generation.md](structure-based-generation.md)), dockers/affinity ([docking-and-cofolding.md](docking-and-cofolding.md), [binding-affinity-and-fep.md](binding-affinity-and-fep.md)), ADMET ([admet-prediction.md](admet-prediction.md)), and retro ([retrosynthesis-planning.md](retrosynthesis-planning.md)) tools. If you're building a platform, treat AgentD / delta / Mozi as reference designs for *which tools to wire together and how to add a verification/critic loop* — and remember every one still needs round-trip validation of its chemistry (see [synthesizability-scoring.md](synthesizability-scoring.md)).
