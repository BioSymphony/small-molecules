# Protein Structure Prediction (Receptor Prep)

Before you can dock a ligand or co-fold a complex, you need the **target's 3D structure**. If an experimental structure (X-ray/cryo-EM, e.g. a 5-HT receptor in the PDB) exists, use it. When it doesn't — a novel target, a specific mutant, an alternative conformation — these tools predict it from sequence. This is the *upstream* of the [docking & co-folding](docking-and-cofolding.md) layer.

**License nuance is the whole story in this section.** Code and weights diverge constantly here, and the divergence is where commercial pipelines get blocked:

- **AlphaFold3 weights** are the hardest block — request-gated, non-commercial, no redistribution.
- **ESM3 / ESM-C** changed terms recently (see card) — historically non-commercial, reportedly relicensed in 2026; re-verify.
- **RoseTTAFold (original) weights** are non-commercial; **RoseTTAFold All-Atom** appears to have relaxed.

All licenses below were read from the live LICENSE / terms files; facts verified **2026-06-13**. Where a term changed very recently, it's flagged to re-confirm.

> If you only need a *complex* structure with a ligand already placed, jump to [docking-and-cofolding.md](docking-and-cofolding.md) (Boltz/Chai/AF3/RFAA co-fold protein **and** ligand). This file is about folding the **receptor** itself.

---

## AlphaFold2 — `google-deepmind/alphafold`
- **What/method:** MSA + template deep-learning structure predictor; monomer + complexes (via AlphaFold-Multimer). The field's baseline. Slow (needs MSA generation over ~2.5 TB of databases). Does **not** place small-molecule ligands.
- **Code license:** **Apache-2.0** (LICENSE file).
- **Weights:** **CC BY 4.0** — verified separately (README); auto-downloaded params (`alphafold_params_2022-12-06`). **Commercial use OK with attribution.**
- **Paper:** Jumper et al., *Nature* 2021. DOI 10.1038/s41586-021-03819-2.
- **Install / GPU:** Docker; Linux; modern NVIDIA GPU (A100-tested) + large genetic DBs.
- **Status:** Stable, low activity. Last release v2.3.2 (2023).
- **Commercial:** ✅ **Clean** — Apache code + CC BY 4.0 weights.

## AlphaFold3 — `google-deepmind/alphafold3`
- **What/method:** Diffusion-based complex predictor — proteins, nucleic acids, ions, **and ligands/small molecules** (CCD codes or SMILES). The strongest *open-code* ligand-bound complex predictor. (Also listed in [docking-and-cofolding.md](docking-and-cofolding.md) for its co-folding role — gives confidence/ranking, **no affinity number**.)
- **Code license:** **Apache-2.0** (the non-commercial restriction is on the *weights*, not the code).
- **Weights:** ❌ **Request-gated + strictly non-commercial + no-redistribution.** Not in the repo; obtained via a Google form at Google's discretion, under the *AlphaFold 3 Model Parameters Terms of Use*. Operative bars: *"only available for non-commercial use by, or on behalf of, non-commercial organizations"*; *"must not publish or share"* the parameters (except internally); outputs *"must not be used to train"* competing structure predictors. Clinical/diagnostic reliance prohibited.
- **Paper:** Abramson et al., *Nature* 2024. DOI 10.1038/s41586-024-07487-w.
- **Install / GPU:** Docker; large-VRAM NVIDIA GPU (A100/H100 80 GB for big complexes); CPU for the data pipeline. Active (v3.0.x, 2026).
- **Commercial:** ❌ **The biggest landmine in this section.** Code is Apache-2.0 but weights are non-commercial *and* commercial entities cannot even obtain them. → For shippable co-folding use **Boltz-1/-2, Chai-1, Protenix, HelixFold3** (see [docking-and-cofolding.md](docking-and-cofolding.md)).

## ColabFold — `sokrypton/ColabFold`
- **What/method:** Fast, accessible AF2 / AF2-Multimer using **MMseqs2** for rapid MSAs instead of the giant AF2 databases. The practical way most people run AF2. (Wraps AF2; doesn't itself place ligands.)
- **Code license:** **MIT.**
- **Weights:** Uses **AF2 params (CC BY 4.0)**. Commercial OK with attribution.
- **Paper:** Mirdita et al., *Nature Methods* 2022. DOI 10.1038/s41592-022-01488-1.
- **Install / GPU:** Colab (free T4 works, ~2000-residue limit), local pip/conda, or Docker. NVIDIA GPU.
- **Status:** Actively maintained (v1.6.x).
- **Commercial:** ✅ Code MIT + AF2 weights CC BY 4.0. ⚠️ The public MMseqs2 MSA server is a shared free resource — **run your own MSA server for production/commercial throughput** (and to avoid sending sequences to a public host).

## ESMFold + ESM-2 — `facebookresearch/esm`
- **What/method:** ESM-2 protein language model; ESMFold folds **single sequences (no MSA)** ~10–60× faster than AF2 for monomers, slightly lower accuracy. No ligand complexes.
- **Code license:** **MIT.**
- **Weights:** **MIT** (HF `facebook/esm2_*`, `facebook/esmfold_v1`; also via `fair-esm`). No non-commercial restriction.
- **Paper:** Lin et al., *Science* 2023. DOI 10.1126/science.ade2574.
- **Install / GPU:** `pip install "fair-esm[esmfold]"` (historically pins Python ≤3.9). NVIDIA GPU; ESMFold ~16+ GB VRAM for long sequences.
- **Status:** ⚠️ **Archived / read-only since Aug 2024.** Development moved to EvolutionaryScale → CZ Biohub (see ESM3). Stable and widely used.
- **Commercial:** ✅ **Clean** — code and weights both MIT. The cleanest single-sequence option.

## ESM3 / ESM-C — `evolutionaryscale/esm` (→ reportedly `Biohub/esm`)
- **What/method:** ESM3 = generative multimodal (sequence/structure/function) protein LM; ESM-C ("Cambrian") = ESM-2-successor embedding models (300M/600M/6B). Generation + representation, not a ligand-complex docker.
- **Code license:** **MIT** (current repo).
- **Weights:** ⚠️ **Term change — re-verify before commercial use.** Agent research (2026-06-13) indicates CZ Biohub (which acquired EvolutionaryScale, Nov 2025) **relicensed the ESM family to MIT in June 2026**, with the repo moving under a Biohub org and the only behavioral limit being an Acceptable-Use Policy. **Historically (Dec 2024 release), `esm3-sm-open-v1` weights were under the Cambrian *Non-Commercial* License**, with larger ESM3 models commercial-/API-gated. Because the MIT relicense is very recent and post-dates this compiler's knowledge cutoff, **treat ESM3/ESM-C weights as "verify the live HF model card"**: if MIT, commercial use is fine; if you find the Cambrian NC license, it's research-only.
- **Paper:** Hayes et al., *Science* 2025 (ESM3). DOI 10.1126/science.ads0018.
- **Install / GPU:** `pip install esm` / HF `transformers`; large variants need substantial VRAM.
- **Commercial:** ⚠️ **Conditional — depends on which license is live.** ESM-2/ESMFold (above) are unambiguously MIT; for ESM3/ESM-C, read the current weights license. (This is exactly the kind of "license ≠ what an old blog says" trap this repo exists to catch — in *both* directions.)

## OpenFold — `aqlaboratory/openfold`
- **What/method:** Faithful, **trainable** PyTorch reproduction of AF2 / AF2-Multimer; memory/GPU-optimized; can be **retrained / fine-tuned** (its differentiator). No ligand complexes.
- **Code license:** **Apache-2.0** (inherited from AF2).
- **Weights:** **CC BY 4.0** — both DeepMind's AF2 params and OpenFold's own retrained weights. Commercial OK with attribution.
- **Paper:** Ahdritz et al., *Nature Methods* 2024. DOI 10.1038/s41592-024-02272-z (bioRxiv 2022).
- **Install / GPU:** Conda + Docker; NVIDIA GPU (CUDA 11/12); supports training.
- **Status:** Active (v2.x, PyTorch 2 / CUDA 12).
- **Commercial:** ✅ Apache code + CC BY 4.0 weights. The pick if you need to **retrain/fine-tune** an AF2-class model on your own data.

## RoseTTAFold — `RosettaCommons/RoseTTAFold`
- **What/method:** Original three-track network for protein + protein-protein complex prediction. Predecessor to RFAA; doesn't handle arbitrary small molecules.
- **Code license:** **MIT.**
- **Weights:** ❌ **Non-commercial** — *"trained weights and data … for non-commercial use only under the … Rosetta-DL Software license."* Clear code/weights split.
- **Paper:** Baek et al., *Science* 2021. DOI 10.1126/science.abj8754.
- **Install / GPU:** Conda + ~300+ GB DBs; NVIDIA GPU.
- **Status:** Superseded; last release v1.1.0 (2021). Use RoseTTAFold2 / RFAA for new work.
- **Commercial:** ⚠️→❌ Code MIT (reusable) but **weights non-commercial** → the model as-run isn't commercial without a UW license (contact UW CoMotion / IPD).

## RoseTTAFold All-Atom — `baker-laboratory/RoseTTAFold-All-Atom`
- **What/method:** All-atom predictor — proteins, nucleic acids, **small molecules/ligands**, covalent mods, metals. The Baker-lab open analog to AF3-style ligand-bound complex prediction. (Also relevant to [docking-and-cofolding.md](docking-and-cofolding.md).)
- **Code + weights license:** **BSD-3-Clause — and the live LICENSE states it covers *both* source code and model weights** (© 2024 University of Washington). ⚠️ This is a relaxation vs. the older RoseTTAFold non-commercial posture — verify on the live LICENSE, but as read it permits commercial use of code **and** weights.
- **Data caveat:** the bundled PDB template DB `pdb100_2021Mar03` is **CC BY-NC-SA 4.0 (non-commercial)** — commercial users must supply their own templates or run template-free. Optional SignalP6 dep is separately licensed.
- **Paper:** Krishna et al., *Science* 2024. DOI 10.1126/science.adl2528.
- **Install / GPU:** Conda/mamba; SE3Transformer build; ~399 GB DBs; NVIDIA GPU required.
- **Status:** Maintained (moderate activity).
- **Commercial:** ✅ for code + weights (BSD, per current LICENSE) / ⚠️ only the **pdb100 template DB is NC** — replace it (or go template-free) and check SignalP6 if used.

---

## New open AF3-class co-folders (2026) — the commercial-clean alternatives to AlphaFold3

AlphaFold3's weights are non-commercial; these 2026 reproductions close that gap with **Apache-2.0 code *and* weights**, and all co-fold protein-ligand complexes (cross-listed in [docking-and-cofolding.md](docking-and-cofolding.md) alongside Boltz/Chai). Verified 2026-06-13.

### OpenFold3 — `aqlaboratory/openfold-3` ⭐
- **What/method:** Fully-open AF3 reproduction — protein-ligand co-folding + nucleic acids; reported AF3-parity and beating Boltz-2 on protein-ligand. The flagship *truly-open* AF3.
- **Code + weights:** **Apache-2.0** (both); weights on HF `OpenFold/OpenFold3`; **training data also released** (AWS Open Data) — rare.
- **Paper:** "OpenFold3 Technical Report" (preview Oct 2025; major update + training-data release Mar 2026). ⚠️ Technical report, **not peer-reviewed**; some release-tag dates couldn't be pinned exactly.
- **Status:** Very active (commits Jun 2026).
- **Commercial:** ✅ Apache code + Apache weights + open data — the cleanest open AF3.

### Protenix (v1 / v2) — `bytedance/Protenix`
- **What/method:** ByteDance open AF3 reproduction; protein-ligand co-folding (+ a separate Protenix-Dock empirical docker). v1 reportedly beats AF3 under matched data/compute; v2 (368M) improves antibody-antigen + ligand plausibility.
- **Code + weights:** **Apache-2.0** — explicitly "both code and model parameters."
- **Paper:** v1 bioRxiv Feb 2026; v2 bioRxiv Apr 2026 (original reproduction Jan 2025). ⚠️ the `10.64898` bioRxiv DOI prefix is unusual but real.
- **Status:** Very active (v2.0.0, Apr 2026).
- **Commercial:** ✅ Apache code + weights.

### IntelliFold-2 (formerly IntFold) — `IntelliGen-AI/IntelliFold`
- **What/method:** Controllable AF3-class co-folder with **binding-affinity adapters**; reportedly beats AF3 on FoldBench, strongest in antibody-antigen + protein-ligand. (IntFold was renamed IntelliFold — same product.)
- **Code + weights:** **Apache-2.0** (both); HF `intelligenAI/intellifold` (the "Pro" tier is server-side only).
- **Paper:** IntelliFold-2 bioRxiv Feb 2026 (earlier IntFold arXiv 2507.02025, Jul 2025).
- **Status:** Active (v2.0.2, Mar 2026).
- **Commercial:** ✅ Apache. Antibody-antigen strength is the differentiator; the affinity adapters also make it relevant to [binding-affinity-and-fep.md](binding-affinity-and-fep.md).

## Choosing

| Need | Pick | Why |
|---|---|---|
| Standard monomer/complex, commercial | **ColabFold** (or AF2) | MIT/Apache code + CC BY 4.0 weights; MMseqs2 = fast MSAs |
| Fastest, single-sequence, commercial | **ESMFold** | MIT/MIT, no MSA; archived but stable |
| Retrain/fine-tune your own AF2-class model | **OpenFold** | Apache + CC BY 4.0, trainable |
| Receptor **+ ligand** complex in one shot | **RoseTTAFold All-Atom**, or co-fold via [Boltz/Chai](docking-and-cofolding.md) | all-atom incl. ligands |
| Best raw accuracy, research only | **AlphaFold3** | ❌ non-commercial gated weights — don't ship on it |

**Commercial-clean shortlist:** ColabFold/AF2, ESMFold, OpenFold (all CC BY 4.0 weights), RoseTTAFold All-Atom code+weights (mind the pdb100 template DB), and — for **ligand-bound complexes / AF3-class accuracy** — the new **OpenFold3 / Protenix / IntelliFold-2** (Apache code *and* weights). **Avoid for commercial:** AlphaFold3 weights (gated NC), RoseTTAFold-original weights (Rosetta-DL NC). **Re-verify:** ESM3/ESM-C (term changed recently). See [licensing-and-data.md](licensing-and-data.md) for the four-layer checklist.
