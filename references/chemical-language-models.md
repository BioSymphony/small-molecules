# Chemical Language Models

These general and specialized language models support chemistry reasoning,
molecular understanding, image-based chemistry, and synthesizable generation.
For task-specific retrosynthesis models, see
[singlestep-retrosynthesis.md](singlestep-retrosynthesis.md) and
[agentic-retrosynthesis.md](agentic-retrosynthesis.md).

Each model has a distinct combination of source-code, weight, data, and
base-model terms. Some combinations include non-commercial source terms,
AGPL-3.0 weights, or no stated code license. Review each layer separately. See
[licensing-and-data.md](licensing-and-data.md) for a consolidated view.

## SynLlama — *synthesizable analog generation* — UC non-commercial terms

> Fine-tuned Llama-3 that generates **synthesizable molecules and analogs** by emitting full synthetic pathways (building blocks + reaction templates) — effectively a constrained retrosynthesis module mapping a target into synthesizable space. Teresa Head-Gordon's lab, UC Berkeley.

- **Repository:** https://github.com/THGLab/SynLlama.
- **Terms:** The repository `LICENSE` is the UC Berkeley Regents Non-Commercial license, while the paper describes MIT terms. GitHub classifies the repository as `NOASSERTION`. The base models carry **Llama 3.1 / 3.2 Community Licenses**; Figshare weights do not state a separate license.
- **Paper:** *SynLlama: Generating Synthesizable Molecules and Their Analogs with Large Language Models*, ACS Central Science 2025, 11:2108 (DOI 10.1021/acscentsci.5c01285); preprint arXiv:2503.12602.
- **Weights:** Figshare (not HF) — `SynLlama-8B-500k`, `SynLlama-1B-500k`, `SynLlama-1B-2M`; authors recommend **SynLlama-1B-2M**. Bases: Llama-3.1-8B, Llama-3.2-1B.
- **Install and run:** `conda env create -f environment.yml`; `pip install -e .`; download Figshare weights; follow the inference guide.
- **Inputs and outputs:** target SMILES → JSON synthetic route (SMARTS steps, building-block SMILES, intermediates). Baselines: SynNet, ChemProjector, SynFormer. ~230K Enamine building blocks (train).
- **Maintenance:** The repository received commits in 2026.
- **Use it for:** Synthesizable analog generation in settings consistent with the repository, weight, and base-model terms. For alternatives, see [synthesizable-generation.md](synthesizable-generation.md).

## ChemDFM-R — *chemistry reasoning LLM* ⚠️ AGPL-3.0 weights

> Chemistry-specialized **reasoning** LLM (released as ChemDFM-R-14B) enhanced with functional-group-level "atomized" knowledge; emits explicit `<think>…</think><answer>…</answer>` chains. SJTU X-LANCE / OpenDFM (sibling of RetroDFM-R).

- **Repository:** no dedicated GitHub repository (the HF model card is primary). The adjacent
  functional-group toolkit `OpenDFM/ChemFG-Tool` uses Apache-2.0. The older
  `OpenDFM/ChemDFM` is a separate project.
- **Terms (three layers):** ChemFG-Tool source code is Apache-2.0; the weights are tagged AGPL-3.0; Qwen2.5-14B is Apache-2.0.
- **Paper:** *ChemDFM-R: A Chemical Reasoning LLM Enhanced with Atomized Chemical Knowledge*, arXiv:2507.21990 (2025–26). Preprint; abstract notes performance competitive with o4-mini.
- **Weights:** HF `OpenDFM/ChemDFM-R-14B` (~15B, BF16). Base Qwen2.5-14B. Load via plain `transformers` (gen params on the card: top_k 20, top_p 0.9, temp 0.9).
- **Dependencies and hardware:** transformers, torch, RDKit. ~28–30 GB VRAM fp16 (A100-40GB class); less when quantized (card gives no VRAM/quant builds — estimates).
- **Terms:** The released weights are AGPL-3.0. The permissive code and base-model licenses do not change those weight terms. Consult the AGPL-3.0 text and any model-card updates for a proposed deployment.
- **Use it for:** Chemistry-reasoning research with the terms documented above.

## Mol-LLaMA — *molecular understanding assistant* ⚠️ no code license + Llama base

> Fine-tunes a **frozen Llama backbone** with 2D + 3D molecular encoders (fused via cross-attention) + a Q-Former, instruction-tuned to explain a molecule's structural/chemical/biological properties with reasoning. A molecular *assistant*, not a generative designer.

- **Repository:** https://github.com/DongkiKim95/Mol-LLaMA (default branch `master`).
- **Terms:** The repository has no code license file. The HF weights card is tagged `apache-2.0`, while the model uses Llama 3.1 and Llama 2 bases with their own Community Licenses. Review the repository, model card, and base-model terms together.
- **Paper:** *Mol-LLaMA: Towards General Understanding of Molecules in Large Molecular Language Model*, arXiv:2502.13449 (NeurIPS 2025 per metadata).
- **Weights:** HF `DongkiKim/Mol-Llama-3.1-8B-Instruct` and `DongkiKim/Mol-Llama-2-7b-chat`; dataset `DongkiKim/Mol-LLaMA-Instruct`. Also uses frozen MoleculeSTM (2D), Uni-Mol (3D), SciBERT Q-Former — each with its own upstream terms.
- **Install and run:** Python 3.10, PyTorch 2.4.1, flash-attn, PyG, OpenBabel; `python stage1.py`/`stage2.py`; inference `python playground.py`. vLLM/SGLang servers advertised.
- **Inputs and outputs:** molecule (SMILES/IUPAC → 2D+3D) + NL query → NL explanation with reasoning. Benchmarks: PAMPA, BBBP, MoleculeQA.
- **Terms:** No code license is stated; the checkpoint and base-model terms are separate.
- **Use it for:** Molecular Q&A and property explanation, not route or molecule generation.

## ChemMLLM — *multimodal (molecule images) chemistry* ⚠️ no code license, no weights, noncommercial base

> Unified model that **understands and generates** across text, SMILES, and **molecule images** (its differentiator is molecule-image *generation*). Chameleon-7B backbone + a custom molecular image tokenizer (Mol-VQGAN). Five tasks incl. optical structure recognition and controllable image generation.

- **Repository:** https://github.com/bbsbz/ChemMLLM (distinct from ChemVLM / ChemDFM-X).
- **Terms:** The repository has no code license and releases no weights. The Chameleon-7B base model uses the Chameleon Research License. The Apache-2.0 Lumina-mGPT framework does not alter the Chameleon base-model terms.
- **Paper:** *ChemMLLM: Chemical Multimodal Large Language Model*, arXiv:2505.16326; peer-reviewed in Cell Reports Physical Science 2026 (PII S2666-3864(26)00216-X).
- **Run:** **train-it-yourself only** — repository ships a data-generation script + Mol-VQGAN training guide, no checkpoints, no inference script. RDKit + Lumina-mGPT + Meta Chameleon VQ-VAE weights.
- **Terms:** The project publishes no code or weight license, and the stated base-model terms are research-only.
- **Use it for:** Research into multimodal molecule-image chemistry when training is feasible.

## Also LLM-based, documented elsewhere

- **RetroDFM-R** — 8B reasoning LLM for single-step retrosynthesis. The
  repository code is MIT; the checkpoint is tagged Apache-2.0 and identifies
  Qwen3-8B as its base. See
  [singlestep-retrosynthesis.md](singlestep-retrosynthesis.md).
- **ChemDual** — dual-task retro+forward LLM (LLaMA-3.1-8B), Apache-2.0 code but **no weights released**. See [forward-and-reaction-modeling.md](forward-and-reaction-modeling.md).

## Choosing (and the license reality)

| Need | Model | Terms to check |
|---|---|---|
| Synthesizable analog generation | SynLlama | UC Non-Commercial repository terms; Llama base terms; untagged weights |
| Chemistry reasoning chat | ChemDFM-R | AGPL-3.0 weights; Apache-2.0 code and base |
| Molecular property Q&A / explanation | Mol-LLaMA | No stated code license; HF and Llama terms |
| Multimodal / molecule images | ChemMLLM | No stated code/weights terms; Chameleon Research License base |

For a particular use, verify the current source-code, checkpoint, base-model, and data terms with the rights holders. For synthesis-oriented alternatives, see [synthesizable-generation.md](synthesizable-generation.md).
