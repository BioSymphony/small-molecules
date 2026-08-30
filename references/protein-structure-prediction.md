# Protein Structure Prediction and Receptor Preparation

Use an experimental receptor structure when it matches the construct and
conformational state you need. Use a predicted structure when public structural
data do not cover the sequence, mutation, or state. For a protein-ligand
complex, use [docking-and-cofolding.md](docking-and-cofolding.md); this page
covers receptor prediction.

Check source code, released parameters, reference data, and base-model terms
separately. On **2026-08-30**, AlphaFold 3 parameters were request-gated and
non-commercial. The `Biohub/esm` repository listed MIT terms for its code and
models. Original RoseTTAFold weights were non-commercial.

---

## AlphaFold2 — `google-deepmind/alphafold`
- **Method and output:** MSA + template deep-learning structure predictor; monomer + complexes (via AlphaFold-Multimer). The field's baseline. Slow (needs MSA generation over ~2.5 TB of databases). Does **not** place small-molecule ligands.
- **Code license:** **Apache-2.0** (LICENSE file).
- **Weights:** **CC BY 4.0** (README); auto-downloaded parameters are named `alphafold_params_2022-12-06`.
- **Paper:** Jumper et al., *Nature* 2021. DOI 10.1038/s41586-021-03819-2.
- **Installation and hardware:** Docker; Linux; modern NVIDIA GPU (A100-tested) + large genetic DBs.
- **Status:** Stable, low activity. Last release v2.3.2 (2023).
- **Terms:** Source code is Apache-2.0; weights are CC BY 4.0.

## AlphaFold3 — `google-deepmind/alphafold3`
- **Method and output:** Diffusion-based complex predictor for proteins, nucleic acids, ions, and **ligands/small molecules** (CCD codes or SMILES). It is also listed in [docking-and-cofolding.md](docking-and-cofolding.md) for co-folding; it returns confidence/ranking, not an affinity value.
- **Code license:** **Apache-2.0.** The code is separate from the model-parameter terms.
- **Weights:** Request-gated under the separate [AlphaFold 3 Model Parameters Terms of Use](https://github.com/google-deepmind/alphafold3/blob/main/WEIGHTS_TERMS_OF_USE.md). Those terms restrict commercial use and redistribution of the released parameters and impose output-use restrictions.
- **Paper:** Abramson et al., *Nature* 2024. DOI 10.1038/s41586-024-07487-w.
- **Installation and hardware:** Docker; large-VRAM NVIDIA GPU for sizeable complexes; CPU for the data pipeline. **v3.0.2** was released on 2026-04-20.
- **Terms:** The released parameter terms restrict commercial use and redistribution; see the linked terms for the exact version you use.

## ColabFold — `sokrypton/ColabFold`
- **Method and output:** AF2 / AF2-Multimer implementation using **MMseqs2** for rapid MSAs instead of the full AF2 database stack. It wraps AF2 and does not place ligands.
- **Code license:** **MIT.**
- **Weights:** Uses **AF2 parameters (CC BY 4.0)**.
- **Paper:** Mirdita et al., *Nature Methods* 2022. DOI 10.1038/s41592-022-01488-1.
- **Installation and hardware:** Colab (free T4 works, ~2000-residue limit), local pip/conda, or Docker. NVIDIA GPU.
- **Status:** Actively maintained (v1.6.x).
- **Terms:** Source code is MIT and AF2 weights are CC BY 4.0. The public MMseqs2 MSA server is a separate hosted service with its own terms and data-handling considerations.

## ESMFold + ESM-2 — `facebookresearch/esm`
- **Method and output:** ESM-2 protein language model; ESMFold folds **single sequences (no MSA)** ~10–60× faster than AF2 for monomers, slightly lower accuracy. No ligand complexes.
- **Code license:** **MIT.**
- **Weights:** **MIT** (HF `facebook/esm2_*`, `facebook/esmfold_v1`; also via `fair-esm`). No non-commercial restriction.
- **Paper:** Lin et al., *Science* 2023. DOI 10.1126/science.ade2574.
- **Installation and hardware:** `pip install "fair-esm[esmfold]"` (historically pins Python ≤3.9). NVIDIA GPU; ESMFold ~16+ GB VRAM for long sequences.
- **Status:** ⚠️ **Archived / read-only since Aug 2024.** Development moved to EvolutionaryScale → CZ Biohub (see ESM3). Stable and widely used.
- **Terms:** Source code and weights are MIT.

## ESM3 / ESM-C — `Biohub/esm`
- **Method and output:** ESM3 = generative multimodal (sequence/structure/function) protein LM; ESM-C ("Cambrian") = ESM-2-successor embedding models (300M/600M/6B). Generation + representation, not a ligand-complex docker.
- **Code license:** On 2026-08-30, the `Biohub/esm` repository listed **MIT** terms.
- **Weights:** On 2026-08-30, the listed Biohub ESMC and ESM3 releases used **MIT** terms. Earlier EvolutionaryScale distributions used Cambrian licenses; check the model card for the exact checkpoint you download.
- **Paper:** Hayes et al., *Science* 2025 (ESM3). DOI 10.1126/science.ads0018.
- **Installation and hardware:** `pip install esm` / HF `transformers`; large variants need substantial VRAM.
- **Terms:** On 2026-08-30, the Biohub repository listed MIT terms for its code and models. Earlier EvolutionaryScale checkpoints can have different model-card terms.

## OpenFold — `aqlaboratory/openfold`
- **Method and output:** Faithful, **trainable** PyTorch reproduction of AF2 / AF2-Multimer; memory/GPU-optimized; can be **retrained / fine-tuned** (its differentiator). No ligand complexes.
- **Code license:** **Apache-2.0** (inherited from AF2).
- **Weights:** **CC BY 4.0** for both DeepMind's AF2 parameters and OpenFold's retrained weights.
- **Paper:** Ahdritz et al., *Nature Methods* 2024. DOI 10.1038/s41592-024-02272-z (bioRxiv 2022).
- **Installation and hardware:** Conda + Docker; NVIDIA GPU (CUDA 11/12); supports training.
- **Status:** Active (v2.x, PyTorch 2 / CUDA 12).
- **Terms:** Source code is Apache-2.0 and the listed weights are CC BY 4.0.

## RoseTTAFold — `RosettaCommons/RoseTTAFold`
- **Method and output:** Original three-track network for protein + protein-protein complex prediction. Predecessor to RFAA; doesn't handle arbitrary small molecules.
- **Code license:** **MIT.**
- **Weights:** ❌ **Non-commercial** — *"trained weights and data … for non-commercial use only under the … Rosetta-DL Software license."* Clear code/weights split.
- **Paper:** Baek et al., *Science* 2021. DOI 10.1126/science.abj8754.
- **Installation and hardware:** Conda + ~300+ GB DBs; NVIDIA GPU.
- **Status:** Superseded; the last release was v1.1.0 in 2021. Use RoseTTAFold2 or RFAA for later workflows.
- **Terms:** Source code is MIT; released weights and data are subject to the Rosetta-DL Software license's non-commercial terms.

## RoseTTAFold All-Atom — `baker-laboratory/RoseTTAFold-All-Atom`
- **Method and output:** All-atom predictor — proteins, nucleic acids, **small molecules/ligands**, covalent mods, metals. The Baker-lab open analog to AF3-style ligand-bound complex prediction. (Also relevant to [docking-and-cofolding.md](docking-and-cofolding.md).)
- **Code and weights license:** **BSD-3-Clause.** The live `LICENSE` states that it covers both source code and model weights.
- **Data caveat:** The bundled PDB template database, `pdb100_2021Mar03`, is **CC BY-NC-SA 4.0**. Optional SignalP6 has separate terms.
- **Paper:** Krishna et al., *Science* 2024. DOI 10.1126/science.adl2528.
- **Installation and hardware:** Conda/mamba; SE3Transformer build; ~399 GB DBs; NVIDIA GPU required.
- **Status:** Maintained (moderate activity).
- **Terms:** Code and listed weights are BSD-3-Clause. The bundled template database is CC BY-NC-SA 4.0, and SignalP6 has separate terms.

---

## Open protein-ligand co-folders

These tools predict a complex structure from protein and ligand inputs. Their
confidence values rank predicted structures; they do not establish binding
affinity.

### OpenFold3 Preview and OpenBind-0 — `aqlaboratory/openfold-3`
- **Method and output:** OpenFold3-preview predicts structures for proteins, nucleic acids, and small molecules. **OpenBind-0** is the default parameter set in OpenFold3 >=0.5.0 and focuses on protein-small-molecule co-folding.
- **Code, weights, and data:** The OpenBind-0 release states that its code, parameters, training data, and training recipes are **Apache-2.0**. The project also publishes the OpenFold3-preview training data.
- **Evidence:** The [OpenBind-0 release announcement](https://openbind.uk/news/blog-openbind-0-advancing-open-molecular-structure-prediction/) is dated 2026-08-21. Its public benchmark reports target-dependent pose performance and poor results on several flexible systems. It is a structure predictor, not an affinity model.
- **Status:** OpenFold3 remains a preview; the maintainers state that the final model is still in development. OpenFold3-preview2 parameters require an older compatible package release.
- **Terms:** The OpenBind-0 release states Apache-2.0 terms for its code, parameters, training data, and recipes. Other OpenFold3 parameter sets can have different terms.

### Protenix (v1 / v2) — `bytedance/Protenix`
- **Method and output:** ByteDance AF3-class co-folder for proteins, ligands, and other biomolecular complexes. `protenix-v2` has 464M parameters; its public release date is 2026-04-08.
- **Code and weights:** **Apache-2.0** — explicitly "both code and model parameters."
- **Data:** `protenix-v2` and the default v1.0.0 parameters use a 2021-09-30 training cutoff. The separately released `protenix_base_20250630_v1.0.0` uses a 2025-06-30 cutoff.
- **Status:** The public repository lists Protenix-v2 and the two v1.0.0 parameter sets.
- **Terms:** The repository states Apache-2.0 for code and model parameters.

## Choosing

| Need | Pick | Why |
|---|---|---|
| Standard monomer/complex | **ColabFold** (or AF2) | MIT/Apache code + CC BY 4.0 weights; MMseqs2 provides fast MSAs |
| Fast single-sequence prediction | **ESMFold** | MIT source and weights; no MSA; archived but stable |
| Retrain/fine-tune an AF2-class model | **OpenFold** | Apache-2.0 code + CC BY 4.0 weights; trainable |
| Receptor **+ ligand** complex with open artifacts | **OpenBind-0**, **Protenix**, or [Boltz/Chai](docking-and-cofolding.md) | Released terms differ by tool; check code, weights, and data |
| AlphaFold 3 parameters | **AlphaFold3** | Request-gated; released parameter terms restrict commercial use |

For receptor prediction, compare the construct, conformational state, input
requirements, and terms of ColabFold/AlphaFold2, ESMFold, OpenFold, and
RoseTTAFold All-Atom. For protein-ligand co-folding, OpenBind-0 and Protenix
state Apache-2.0 terms for their released artifacts; Boltz and Chai are
described in [docking-and-cofolding.md](docking-and-cofolding.md). AlphaFold 3
parameters and original RoseTTAFold weights have non-commercial terms. See
[licensing-and-data.md](licensing-and-data.md) for the four-layer checklist.
