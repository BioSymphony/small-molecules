# Agentic and LLM-Orchestrated Drug Design

These 2025–2026 LLM and multi-agent systems combine generation, docking,
affinity, ADMET, and retrosynthesis tools in semi-autonomous hit-to-lead
workflows. **Agentic retrosynthesis** covers route planning; see
[agentic-retrosynthesis.md](agentic-retrosynthesis.md).

Before you select a framework:

- **External model backend:** Many systems require an external or locally hosted language model. Review its data-handling and usage terms before submitting structures.
- **Research maturity:** Several repositories are reference implementations rather than long-lived dependencies. Verify maintenance, tests, and the licenses of every integrated tool.
- **Scientific validation:** Treat generated plans and candidate rankings as hypotheses that require independent chemical and experimental validation.

---

## AgentD — `hoon-ock/AgentD`
- **Method and output:** Single-orchestrator LLM agent (CMU, Barati Farimani lab) that links REINVENT and Mol2Mol for generation, Deep-PK for ADMET, BAPULM and **Boltz-2** for affinity/structure, UniProt/ChEMBL retrieval, RDKit, and FAISS-based retrieval through LangChain.
- **Code license:** **MIT.** The agent requires an external language-model backend.
- **Paper:** *LLM Agent for Modular Task Execution in Drug Discovery*, arXiv:2507.02925 (v1 Jun 2025 → v3 Dec 2025).
- **Status:** Public repository active as of February 2026.
- **Terms:** AgentD source code is MIT. The language-model backend and integrated tools have separate terms; Deep-PK is a hosted service (see [admet-prediction.md](admet-prediction.md)).

## CLADD — `Genentech/CLADD`
- **Method and output:** Training-free **RAG-enhanced multi-agent** system for molecular QA / DD reasoning — Planning + Knowledge-Graph + Molecule-Understanding agents retrieving from biomedical KGs (PrimeKG/PubChem). Industrial provenance (Genentech). QA/reasoning-oriented, *not* a generative design-make loop.
- **Code license:** **Apache-2.0** (read the file; © 2025 Genentech — GitHub shows "NOASSERTION" only due to a copyright preamble). Model-agnostic LLM backend.
- **Paper:** arXiv:2502.17506, **AAAI 2026**.
- **Status:** The repository received commits in November 2025.
- **Terms:** Source code is Apache-2.0. The selected language-model backend and knowledge-graph resources have separate terms.

## delta — `deltawave-tech/delta` *(reference architecture)*
- **Method and output:** Six-agent molecular-optimization system with a principal-researcher orchestrator, database, molecular-generation, medicinal-chemistry, ranking, and scientific-critique roles. It integrates UniProt, PDB, ChEMBL, AutoDock Vina, RDKit, and PLIP, and demonstrates an AKT1 case.
- **Code license:** **MIT.** The system requires an external language-model backend.
- **Paper:** arXiv:2508.03444 (Aug 2025).
- **Status:** Public repository last updated August 2025.
- **Terms:** Source code is MIT. The external language-model backend and integrated tools have separate terms.

## DrugPilot — `wzn99/DrugPilot`
- **Method and output:** ReActAgent / LlamaIndex framework with a multi-modal "parameter memory pool" for DD task automation.
- **Code license:** **MIT.** It requires an external language-model backend. Public repository last updated January 2026.
- **Terms:** Source code is MIT; the backend and any connected tools have separate terms.

---

## Watchlist (paper-only or no usable license)

- **Mozi** (arXiv:2603.03655, March 2026) — multi-agent workflow over Vina, AF3, DiffSBDD, ADMET-AI, REINVENT4, and **LigUnity**. The project page and `OpenMol/DD100` benchmark are public; no model code is published.
- **ToolMol** (arXiv:2605.12784) — tool-using agent; no public code is published.
- **OrchestRA** (arXiv:2512.21623), **FROGENT** (arXiv:2508.10760), **PharmAgents** (arXiv:2503.22164) — agentic-DD papers, no public code.
- **LIDDiA** (`ninglab/LIDDiA`, EMNLP 2025) and **Prompt-to-Pill** (`ChatMED/Prompt-to-Pill`, 2026) — code is public, but neither repository states a license.

> **Not small-molecule-specific:** **Robin** (`Future-House/robin`, Apache-2.0) is a general AI-scientist and repurposing agent, not a de novo small-molecule-design repository.

## Where this fits

These repositories form an **orchestration layer** over the generators ([synthesizable-generation.md](synthesizable-generation.md), [structure-based-generation.md](structure-based-generation.md)), docking and affinity tools ([docking-and-cofolding.md](docking-and-cofolding.md), [binding-affinity-and-fep.md](binding-affinity-and-fep.md)), ADMET tools ([admet-prediction.md](admet-prediction.md)), and retrosynthesis tools ([retrosynthesis-planning.md](retrosynthesis-planning.md)). Any resulting chemistry still requires independent validation, including synthesis assessment (see [synthesizability-scoring.md](synthesizability-scoring.md)).
