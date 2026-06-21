# Chemical Language Models / LLMs for Chemistry

General and specialized LLMs for chemistry — reasoning chat, molecular understanding, multimodal (image) chemistry, and LLM-based synthesizable generation. For task-specific retrosynthesis LLMs see [singlestep-retrosynthesis.md](singlestep-retrosynthesis.md) (RetroDFM-R) and [agentic-retrosynthesis.md](agentic-retrosynthesis.md).

> ⚠️ **Every model in this file has a license trap.** None is cleanly usable in a closed-source commercial product without legal review — each fails for a *different* reason (AGPL weights, no code license, noncommercial base model, university non-commercial license). The licensing detail is the whole point of these cards. See [licensing-and-data.md](licensing-and-data.md) for the consolidated view.

## SynLlama — *synthesizable analog generation* ⚠️ UC non-commercial (paper says MIT — it's wrong)

> Fine-tuned Llama-3 that generates **synthesizable molecules and analogs** by emitting full synthetic pathways (building blocks + reaction templates) — effectively a constrained retrosynthesis module mapping a target into synthesizable space. Teresa Head-Gordon's lab, UC Berkeley.

- **Repo:** https://github.com/THGLab/SynLlama.
- **License — read carefully:** the repo **LICENSE is the UC Berkeley Regents NON-COMMERCIAL license** ("educational, research, and not-for-profit purposes" only; commercial use needs a signed agreement via UC Berkeley OTL, otl@berkeley.edu). GitHub classifies it as **NOASSERTION**. ⚠️ **The paper claims "MIT" — that is inaccurate; the LICENSE file is binding.** Base models add **Llama 3.1 / 3.2 Community Licenses**; weights are on Figshare (untagged).
- **Paper:** *SynLlama: Generating Synthesizable Molecules and Their Analogs with Large Language Models*, ACS Central Science 2025, 11:2108 (DOI 10.1021/acscentsci.5c01285); preprint arXiv:2503.12602.
- **Weights:** Figshare (not HF) — `SynLlama-8B-500k`, `SynLlama-1B-500k`, `SynLlama-1B-2M`; authors recommend **SynLlama-1B-2M**. Bases: Llama-3.1-8B, Llama-3.2-1B.
- **Install / run:** `conda env create -f environment.yml`; `pip install -e .`; download Figshare weights; follow the inference guide.
- **I/O:** target SMILES → JSON synthetic route (SMARTS steps, building-block SMILES, intermediates). Baselines: SynNet, ChemProjector, SynFormer. ~230K Enamine building blocks (train).
- **Maintenance:** peer-reviewed, established lab; lightly/actively maintained (~49 stars; commits into 2026).
- **Use it when:** **research/non-commercial** synthesizable analog generation with an LLM. **Do not deploy commercially** without a UC OTL agreement + Llama compliance. For commercial synthesizable generation, prefer PrexSyn (MIT) — see [synthesizable-generation.md](synthesizable-generation.md).

## ChemDFM-R — *chemistry reasoning LLM* ⚠️ AGPL-3.0 weights

> Chemistry-specialized **reasoning** LLM (released as ChemDFM-R-14B) enhanced with functional-group-level "atomized" knowledge; emits explicit `<think>…</think><answer>…</answer>` chains. SJTU X-LANCE / OpenDFM (sibling of RetroDFM-R).

- **Repo:** no dedicated GitHub repo (the HF model card is primary). Only adjacent code is the functional-group toolkit `OpenDFM/ChemFG-Tool` (Apache-2.0). Don't confuse with the older `OpenDFM/ChemDFM`.
- **License (three layers differ):** ChemFG-Tool **code Apache-2.0**; **weights tagged AGPL-3.0** (the binding constraint); base **Qwen2.5-14B is Apache-2.0**.
- **Paper:** *ChemDFM-R: A Chemical Reasoning LLM Enhanced with Atomized Chemical Knowledge*, arXiv:2507.21990 (2025–26). Preprint; abstract notes performance competitive with o4-mini.
- **Weights:** HF `OpenDFM/ChemDFM-R-14B` (~15B, BF16). Base Qwen2.5-14B. Load via plain `transformers` (gen params on the card: top_k 20, top_p 0.9, temp 0.9).
- **Deps / hardware:** transformers, torch, RDKit. ~28–30 GB VRAM fp16 (A100-40GB class); less when quantized (card gives no VRAM/quant builds — estimates).
- **Commercial caveat:** ⚠️ **AGPL-3.0 weights = strong network copyleft.** Serving over a network triggers an obligation to release your complete corresponding source under AGPL. The permissive code/base do **not** loosen this. Not usable in a closed-source/SaaS product without full AGPL compliance or a separate commercial license (none advertised).
- **Use it when:** research chemistry reasoning where AGPL is acceptable (or you'll open-source your stack).

## Mol-LLaMA — *molecular understanding assistant* ⚠️ no code license + Llama base

> Fine-tunes a **frozen Llama backbone** with 2D + 3D molecular encoders (fused via cross-attention) + a Q-Former, instruction-tuned to explain a molecule's structural/chemical/biological properties with reasoning. A molecular *assistant*, not a generative designer.

- **Repo:** https://github.com/DongkiKim95/Mol-LLaMA (default branch `master`).
- **License:** ⚠️ **code has NO license file (all rights reserved)**; weights are HF-tagged `apache-2.0` but that's **legally inconsistent** with the Llama base and most plausibly covers only the glue/LoRA code. Binding terms: **Llama 3.1 / Llama 2 Community Licenses** (commercial allowed *with* "Built with Llama" attribution, name-prefixing, and the >700M-MAU carve-out).
- **Paper:** *Mol-LLaMA: Towards General Understanding of Molecules in Large Molecular Language Model*, arXiv:2502.13449 (NeurIPS 2025 per metadata).
- **Weights:** HF `DongkiKim/Mol-Llama-3.1-8B-Instruct` and `DongkiKim/Mol-Llama-2-7b-chat`; dataset `DongkiKim/Mol-LLaMA-Instruct`. Also uses frozen MoleculeSTM (2D), Uni-Mol (3D), SciBERT Q-Former — each with its own upstream terms.
- **Install / run:** Python 3.10, PyTorch 2.4.1, flash-attn, PyG, OpenBabel; `python stage1.py`/`stage2.py`; inference `python playground.py`. vLLM/SGLang servers advertised.
- **I/O:** molecule (SMILES/IUPAC → 2D+3D) + NL query → NL explanation with reasoning. Benchmarks: PAMPA, BBBP, MoleculeQA.
- **Commercial caveat:** ⚠️ needs legal review — add a code license + reconcile Llama terms before any deployment.
- **Use it when:** research molecular Q&A / property explanation; not a route or molecule generator.

## ChemMLLM — *multimodal (molecule images) chemistry* ⚠️ no code license, no weights, noncommercial base

> Unified model that **understands and generates** across text, SMILES, and **molecule images** (its differentiator is molecule-image *generation*). Chameleon-7B backbone + a custom molecular image tokenizer (Mol-VQGAN). Five tasks incl. optical structure recognition and controllable image generation.

- **Repo:** https://github.com/bbsbz/ChemMLLM (distinct from ChemVLM / ChemDFM-X).
- **License:** ⚠️ **code has NO license (all rights reserved)**; **no weights released at all**; base **Chameleon-7B is under Meta's Chameleon Research License — noncommercial research only**, with mandatory attribution and a bar on users in Illinois/Texas. The Apache-2.0 Lumina-mGPT *framework* does not relicense Chameleon weights.
- **Paper:** *ChemMLLM: Chemical Multimodal Large Language Model*, arXiv:2505.16326; peer-reviewed in Cell Reports Physical Science 2026 (PII S2666-3864(26)00216-X).
- **Run:** **train-it-yourself only** — repo ships a data-generation script + Mol-VQGAN training guide, no checkpoints, no inference script. RDKit + Lumina-mGPT + Meta Chameleon VQ-VAE weights.
- **Commercial caveat:** ⚠️ **noncommercial research only** (no code license + Chameleon noncommercial base). Anything you train inherits the Chameleon restriction.
- **Use it when:** research into multimodal/molecule-image chemistry, and you can train it. Not deployable.

## Also LLM-based, documented elsewhere

- **RetroDFM-R** — 8B reasoning LLM for single-step retrosynthesis. Code Apache-2.0, **weights GPL-3.0** + Llama-3 base. See [singlestep-retrosynthesis.md](singlestep-retrosynthesis.md).
- **ChemDual** — dual-task retro+forward LLM (LLaMA-3.1-8B), Apache-2.0 code but **no weights released**. See [forward-and-reaction-modeling.md](forward-and-reaction-modeling.md).

## Choosing (and the license reality)

| Need | Model | The catch |
|---|---|---|
| Synthesizable analog generation (research) | SynLlama | UC **non-commercial** (paper's "MIT" is wrong) |
| Chemistry reasoning chat | ChemDFM-R | weights **AGPL-3.0** (network copyleft) |
| Molecular property Q&A / explanation | Mol-LLaMA | **no code license** + Llama terms |
| Multimodal / molecule images | ChemMLLM | **no license, no weights**, Chameleon noncommercial |

For anything **commercial**, none of these is a clean choice. If you need commercial synthesizable generation, use **PrexSyn** (MIT code+weights, Enamine data terms aside). If you need a general chemistry LLM commercially, you're likely better off with a permissively/commercially-licensed base model you control plus retrieval, rather than these fine-tunes.
