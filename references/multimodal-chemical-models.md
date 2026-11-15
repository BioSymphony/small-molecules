# Multimodal Chemical Models

These models translate molecular, structural, biological, and text
representations. Select the task-specific tokenizer and decoding contract.
A generated property answer requires endpoint-specific validation; a generated
structure requires chemical and experimental review.

For fixed endpoint predictors, see [ADMET](admet-prediction.md) and
[property prediction](property-and-qsar-prediction.md). For spectral inputs,
see [analytical chemistry models](analytical-chemistry-models.md).

## DeepSeMS — Biosynthetic Clusters to Metabolite Candidates

- **Task and output:** Annotated antiSMASH GenBank or DeepBGC FASTA → Pfam domain sequence → ranked secondary-metabolite SMILES and ten-model consensus. Raw genome FASTA requires BGC annotation first. [Source](https://github.com/lab-of-biochemai/DeepSeMS), [paper](https://doi.org/10.1038/s43588-026-00983-1).
- **Artifacts and setup:** Obtain all ten `checkpoint0.ckpt`–`checkpoint9.ckpt` models, the Pfam database/index, and matching vocabularies. The [model deposit](https://zenodo.org/records/18692427) lists ten roughly 189 MB checkpoints and a Pfam archive. Source instructions provide Docker and conda installation, HMMER setup, and public GenBank/FASTA examples. Use the deposited checkpoints rather than the small repository placeholder.
- **Terms:** Apache-2.0 source; CC BY 4.0 deposit. Pfam and upstream training sources retain separate terms.
- **Use limits:** Ensemble scores rank candidate structures; they do not measure metabolite identity, novelty, or activity.
- **Reviewed:** 2026-11-15 (UTC).

## BioMatrix — Molecular Sequence, Structure, and Text Tokens

- **Task and output:** Wrapped SMILES/SELFIES, 3D structure tokens, protein tokens, and text → task-specific molecular or text output. Molecular examples include captioning, name conversion, editing, and structure generation. [Source](https://github.com/QizhiPei/BioMatrix), [paper](https://arxiv.org/abs/2606.22138).
- **Artifacts and setup:** The [BioMatrix-1.7B-SFT card](https://huggingface.co/QizhiPei/BioMatrix-1.7B-SFT) documents Transformers loading and exact modality wrappers. Preserve the model/tokenizer revision and task prompt. Molecular 3D output requires MolStructTok decoding; protein structure tokens require the separate GCP-VQVAE assets and setup.
- **Terms:** Apache-2.0 source and released model declaration. Base models, structure codecs, and aggregated training datasets require separate review.
- **Use limits:** Appendix 9.1 distinguishes the public merged all-task SFT checkpoint from the task-group models used in the main benchmark tables. Attribute scores to the evaluated checkpoint and task configuration.
- **Reviewed:** 2026-11-15 (UTC).

## LOGOS — Scientific-Grammar Generation

- **Task and output:** Serialized scientific grammar → reactants, protein pocket tokens, pocket-conditioned ligand tokens, or material tokens through four separate inference scripts. [Source](https://github.com/LOGOS-Hub/LOGOS), [paper](https://arxiv.org/abs/2606.16905).
- **Artifacts and setup:** Use the real [LOGOS-8B model](https://huggingface.co/LOGOS-Hub/LOGOS-8B), matching tokenizer, and task script. The source documents a CUDA-enabled PyTorch container. Its generic quick start retains a placeholder model ID; task scripts define the usable input/output contracts. Pocket-conditioned ligand generation consumes serialized interaction grammar, requiring conversion before an arbitrary PDB can serve as input.
- **Terms:** Apache-2.0 source; CC BY 4.0 model card. Base-model and data terms remain separate.
- **Use limits:** Retrosynthesis output requires route and stock checks; pocket-conditioned ligand tokens require decoding and independent binding evaluation.
- **Reviewed:** 2026-11-15 (UTC).
