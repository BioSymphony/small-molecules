# Analytical Chemistry Models

These tools use spectra to propose molecular structures, predict spectra from
structures, or estimate correction factors for analytical measurements. Select
the required modality, formula information, preprocessing, and decoder before
choosing a checkpoint. Candidate structures require comparison with independent
analytical evidence.

For structure-to-property prediction, see
[property and QSAR prediction](property-and-qsar-prediction.md). For molecular
and text generation, see [multimodal chemical models](multimodal-chemical-models.md).

## MS-GPT — Known-Formula MS/MS Structure Candidates

- **Task and output:** MS/MS spectrum plus known molecular formula → ranked candidate structures. A MIST spectrum encoder supplies fingerprint posteriors to a conditional molecule-language decoder. [Source](https://github.com/VIKI623/MS-GPT), [paper](https://arxiv.org/abs/2607.23607).
- **Corrected release:** The [corrected release](https://github.com/VIKI623/MS-GPT/blob/ec032f87dcaa54c6380176c2f959e11335440ae5/README.md) replaces legacy FRIGID-released encoders with official MIST checkpoints and corrects attention masking. Reported Top-1/Top-10 connectivity recovery is 17.09/27.59% on NPLIB1 and 10.22/13.21% on MassSpecGym, using 100 decoder samples per spectrum and InChIKey-14 matching. Earlier higher figures are superseded. Preserve the native sampling and ranking policy when comparing the release.
- **Artifacts and setup:** The linked asset bundle contains the decoder, dataset-specific official MIST encoder, matching posterior-aligned adapter, SAFE assets, and benchmark data. Build posterior caches and density calibration with the supplied scripts. Setup uses PyTorch 2.6/CUDA 12.4; an RTX 6000 Ada is the author's reproduction recommendation.
- **Terms:** Apache-2.0 source. Inspect separate encoder, decoder/base-model, adapter, and dataset terms before reuse.
- **Reviewed:** 2026-11-15 (UTC).

## UltraNMR — NMR Embeddings and Task Heads

- **Task and output:** Paired proton/carbon shift lists → spectral embeddings for search. Separate heads produce formula-conditioned SMILES, functional-group labels, or natural-product superclass labels. [Source](https://github.com/wuycM/UltraNMR), [paper](https://arxiv.org/abs/2606.20756).
- **Artifacts and setup:** Python 3.11 and editable installation are documented. Download the appropriate [checkpoint directory](https://huggingface.co/milesyc/ultranmr): the contrastive encoder, formula decoder, functional-group head, and classifier are distinct artifacts. Match the source JSONL schema, task configuration, and classifier mapping. The README supplies embedding and per-task inference commands, including optional beam search.
- **Terms:** MIT code; Apache-2.0 model repository. [NMRGym data](https://huggingface.co/datasets/meaw0415/NMRGym) has separate terms.
- **Use limits:** A downloadable encoder does not supply a searchable molecular reference index. Formula-conditioned candidates and optional stereochemical scoring require the corresponding evidence and evaluation protocol.
- **Reviewed:** 2026-11-15 (UTC).

## PRISM — Bidirectional NMR Translation

- **Task and output:** SMILES → detailed proton/carbon peak lists through `mol2spec`; peak lists with optional formula/solvent conditioning → SMILES through `spect2mol`. Proton records include splitting, coupling, integration, and shift ranges. This is the [Hoque/Glorius NMR project](https://github.com/alhqlearn/PRISM), [paper](https://doi.org/10.1002/anie.7185622).
- **Artifacts and setup:** Use the [October 2026 deposit](https://zenodo.org/records/23600371), which lists proton, carbon, and inverse checkpoints plus data splits. Match the source vocabulary and fitted normalization. Python 3.10+/PyTorch 2.1+ are documented; the README supports CPU inference.
- **Input gap:** The [inverse inference script](https://github.com/alhqlearn/PRISM/blob/8a00fa9c747d3827d7c78dfc20e9883f4207766c/spect2mol/inference.py) declares `--input_csv` but reads configured `tensors/test.pt`; the argument does not load a new CSV. Prepare matching tensors before inverse inference. Top-K weight averaging additionally requires the matching checkpoints and manifest. The forward list/CSV script accepts new SMILES directly.
- **Terms:** MIT source; CC BY 4.0 deposit. Source literature terms remain separate.
- **Use limits:** Forward/inverse agreement is model consistency, rather than independent structure confirmation.
- **Reviewed:** 2026-11-15 (UTC).

## NMRTrans — Experimental NMR Peak Sets to SMILES

- **Task and output:** Unordered proton/carbon peak sets, optionally with molecular formula → SMILES candidates. Choose a released checkpoint for the available modalities. [Source](https://github.com/little1d/NMRTrans), [paper](https://arxiv.org/abs/2602.10158).
- **Version pairing:** The [C-H-Formula card](https://huggingface.co/little1d/C-H-Formula) pairs `nmrtrans-c-h-nmr-formula.ckpt` with `main`. Its NMRexp-merged checkpoint requires `bugfix`, the corrected peak mask, and expanded 223-token vocabulary. Corpus and test split also change, so the two published result rows do not isolate the mask correction.
- **Artifacts and setup:** Use the matching YAML, modality flags, T5 assets, checkpoint, vocabulary, and [data cache](https://huggingface.co/datasets/little1d/NMRTrans-Data). The original cache does not establish access to the updated merged test split. Follow the source installation and `src/test.py` interface; training hardware examples do not establish minimum inference requirements.
- **Terms:** MIT source and listed model/data cards. T5 and literature-derived data provenance require separate review.
- **Reviewed:** 2026-11-15 (UTC).

## LCMS2Yield — UV Correction Factors

- **Task and output:** Product SMILES → full-spectrum UV correction factor. Combine the factor with measured LC-UV peak data and a known internal standard to estimate concentration or reaction yield. The model does not estimate yield from reaction conditions alone. [Source](https://github.com/xtalpi-inc/lcms2yield), [paper](https://doi.org/10.1021/jacsau.6c00812).
- **Artifacts and setup:** The source provides `predict_by_smiles_list`, a bundled checkpoint, and training/benchmark CSVs. It documents Python 3.11, PyTorch 2.3, and PyG 2.5.3 on CPU, with optional CUDA. Supply explicit checkpoint paths or follow the source's working-directory convention.
- **Terms:** The README declares Apache-2.0. Confirm the exact code, checkpoint, and dataset grant before redistribution; the declaration does not replace missing artifact-specific terms.
- **Use limits:** Check the internal-standard and wavelength-integration definitions before quantifying a sample. A predicted correction factor is distinct from a measured isolated yield.
- **Reviewed:** 2026-11-15 (UTC).

## NMRexp — Literature-Extracted NMR Data

- **Task and output:** The [v2 deposit](https://zenodo.org/records/17296666) supplies 3.37 million experimental NMR records extracted from published supporting information for six nuclei, with a parser and manually checked subsets. These are structured literature records rather than raw instrument acquisitions.
- **Artifacts and setup:** CSV and Parquet variants include a reduced-stereocenter subset. Match source DOI, molecular identity, nucleus, solvent, and peak conventions before training. Split by molecule and inspect duplicate literature records before evaluation.
- **Terms:** CC BY 4.0 deposit. Source publications and the [dataset paper](https://doi.org/10.1038/s41597-025-06245-5) retain separate terms.
- **Reviewed:** 2026-11-15 (UTC).

## Choosing

| Input and Task | Starting Point | Required Companion Assets |
|---|---|---|
| MS/MS with known formula → candidates | MS-GPT | Official MIST encoder, matching adapter/decoder, calibration |
| NMR shift lists → embeddings or task labels | UltraNMR | Task head; a reference index for library search |
| SMILES → detailed proton/carbon peaks | PRISM forward model | Channel checkpoint and matching vocabulary |
| NMR peaks → SMILES | NMRTrans or PRISM inverse model | Correct branch/cache or correctly preprocessed tensors |
| Measured LC-UV yield quantification | LCMS2Yield | Internal standard and measured peak integrations |
| NMR dataset construction/evaluation | NMRexp | Identity checks, source provenance, molecule-disjoint split |
