# Structure-Based (Pocket-Conditioned) Generation & Pocket Detection

The bridge between *"generate a molecule"* and *"will it bind the pocket."* **Pocket-conditioned generators** sample ligands directly into a target's 3D binding site (apo or holo), conditioning on the pocket atoms/surface — de novo design *for a specific target*, rather than the target-agnostic generation in [molecular-generation.md](molecular-generation.md).

**The critical limitation — and why this file points back at the synthesizability layer:** almost none of these generators constrain outputs to **synthesizable** chemical space. They emit 3D atom clouds or graphs that are frequently strained, non-makeable, or only weakly drug-like. **So they feed a downstream synthesizable-space projection / retrosynthesis step** — generate into the pocket here, then make it real with **PrexSyn / SynFormer / ChemProjector** ([synthesizable-generation.md](synthesizable-generation.md)) or filter via **AiZynthFinder** ([retrosynthesis-planning.md](retrosynthesis-planning.md)). This is exactly the "make-any-generator-real" loop that ties the two layers together.

**The upstream input** — the pocket itself — comes from binding-site detection (fpocket, P2Rank, DoGSiteScorer), on a structure from [protein-structure-prediction.md](protein-structure-prediction.md) or the PDB.

**A second limitation — chemotype scope (out-of-distribution targets):** these generators are trained on **drug-like small molecules in single, well-defined pockets** (CrossDocked/PDBBind). They degrade badly outside that distribution — **macrocycles, natural-product scaffolds, and molecular glues / induced-proximity binders** (which sit on a *composite* surface spanning two proteins, not a pocket). For a case like the pan-RAS(ON) glue **daraxonrasib** (a sanglifehrin-derived macrocycle on the CypA·RAS interface), de novo pocket generation is the *wrong* tool — use **scaffold-constrained enumeration** (REINVENT 4 LibInvent/Mol2Mol, RDKit) around the known ligand instead. See the [KRAS(ON) glue worked example](worked-example-kras-glue.md).

**Two license traps verified by reading the raw files (not GitHub's auto-detector):** **TargetDiff** and **PocketFlow** ship valid **MIT** licenses in *misspelled* filenames (`LICIENCE`; `Liscense` on the `master` branch), so GitHub reports "no license" — but the text is genuine MIT (keep a copy as evidence). Conversely **DecompDiff = CC-BY-NC (non-commercial)** and **Lingo3DMol = GPL-3.0 (copyleft)**. Read each license line. Verified **2026-06-13**.

---

## Pocket-conditioned generators

### Pocket2Mol — `pengxingang/Pocket2Mol`
- **Method:** **Autoregressive** (E(3)-equivariant; sequential atom/bond sampling in the pocket).
- **License:** ✅ **MIT** (clean). Weights on Google Drive.
- **Paper:** *Pocket2Mol*, **ICML 2022**, arXiv:2205.07249.
- **GPU/Status:** GPU (CUDA 11.3); dormant (2023) but a standard baseline.
- **Commercial:** ✅ MIT. **Synth-constrained: ❌** — no SA/retro filter; project downstream.

### TargetDiff — `guanjq/targetdiff`
- **Method:** **Diffusion** (SE(3)-equivariant, non-autoregressive); also outputs a binding-affinity *ranking*.
- **License:** ✅ **MIT** — ⚠️ trap: file misspelled `LICIENCE`, so GitHub shows "no license"; the text is genuine MIT (© 2023 Jiaqi Guan). Weights on Google Drive.
- **Paper:** *3D Equivariant Diffusion for Target-Aware Molecule Generation and Affinity Prediction*, **ICLR 2023**, arXiv:2303.03543.
- **GPU/Status:** GPU (CUDA 11.6); dormant (2023); standard SBDD benchmark.
- **Commercial:** ✅ MIT (keep a copy of the misspelled file). **Synth-constrained: ❌.**

### DiffSBDD — `arneschneuing/DiffSBDD`
- **Method:** **Diffusion** (E(3)-equivariant EGNN); de novo + inpainting/scaffold tasks.
- **License:** ✅ **MIT** (clean). 8 checkpoints on Zenodo (record 8183747).
- **Paper:** *Structure-based drug design with equivariant diffusion models*, **Nature Computational Science** 2024. DOI 10.1038/s43588-024-00737-x.
- **GPU/Status:** GPU; **actively maintained** (2025) — the most current diffusion SBDD repo.
- **Commercial:** ✅ MIT. **Synth-constrained: ❌** at generation (ships an optional `optimize.py` with an **SA objective** for post-hoc steering, but base sampling isn't makeability-aware).

### DecompDiff — `bytedance/DecompDiff`
- **Method:** **Diffusion** with **decomposed priors** (arms/scaffold via reference ligand or subpockets) + optional bond diffusion.
- **License:** ❌ **CC-BY-NC 4.0** — a content/**non-commercial** license, not an OSS license (GitHub reports NOASSERTION). Weights inherit the NC restriction. **Archived (read-only) Dec 2025.**
- **Paper:** *DecompDiff*, **ICML 2023**, arXiv:2403.07902.
- **Commercial:** ❌ **No — CC-BY-NC forbids commercial use.** The hardest "no" here. **Synth-constrained: ❌.**

### ResGen — `HaotianZhangAI4Science/ResGen`
- **Method:** **Autoregressive** parallel multi-scale (global pocket + local atomic context).
- **License:** ✅ **MIT.** Weights on Google Drive; data on Zenodo (DOI 10.5281/zenodo.7759114).
- **Paper:** *ResGen*, **Nature Machine Intelligence** 2023. DOI 10.1038/s42256-023-00712-7.
- **GPU/Status:** GPU (CUDA 11.3); mostly dormant (2024).
- **Commercial:** ✅ MIT. **Synth-constrained: ❌.**

### Lingo3DMol — `stonewiseAIDrugDesign/Lingo3DMol`
- **Method:** **Language model + 3D coords** (fragment-based SMILES with local/global geometry). StoneWise AI.
- **License:** ⚠️ **GPL-3.0 (strong copyleft).** Checkpoints on AWS S3.
- **Paper:** *Generation of 3D molecules in pockets via a language model*, **Nature Machine Intelligence** 2023. DOI 10.1038/s42256-023-00775-6.
- **GPU/Status:** GPU **≥5 GB VRAM** (lighter than diffusion); dormant (2023).
- **Commercial:** ⚠️ **GPL-3.0** — internal use fine; **distributing a product that incorporates it forces GPL-3 release.** Incompatible with closed-source distribution. **Synth-constrained: ❌** (authors report decent SA, but no hard filter).

### PocketFlow — `Saoge123/PocketFlow`
- **Method:** **Autoregressive flow** with explicit chemical-knowledge priors (valence rules → claims 100% chemical validity). Wet-lab validated (HAT1, YTHDC1).
- **License:** ✅ **MIT** — ⚠️ trap: file misspelled `Liscense` on the **`master`** branch, so GitHub shows "no license"; text is genuine MIT (© 2021). Checkpoint committed in-repo.
- **Paper:** *PocketFlow*, **Nature Machine Intelligence** 2024. DOI 10.1038/s42256-024-00808-8.
- **GPU/Status:** GPU (CPU fallback); lightly maintained (2025).
- **Commercial:** ✅ MIT (keep a copy of the misspelled file). **Synth-constrained: ⚠️→❌** — enforces chemical **validity**, not synthetic **accessibility**. Valid ≠ makeable — still project downstream.

### REINVENT 4 — `MolecularAI/REINVENT4` *(major maintained framework)*
- **Method:** Production molecular-design framework — de novo, scaffold hopping, R-group, **linker design (LinkInvent)**, library/R-group **(LibInvent)**, Mol2Mol — via **RL** over a multi-component scoring function. AstraZeneca.
- **Pocket-conditioning:** REINVENT is **ligand/SMILES-based, not natively 3D-pocket-conditioned**; it becomes pocket-aware by plugging **docking scores** (e.g. AutoDock Vina via DockStream — see [docking-and-cofolding.md](docking-and-cofolding.md)) into the RL **reward**. Pocket awareness is via the reward, not the generator.
- **License:** ✅ **Apache-2.0** (the most permissive + safest here; patent grant). Priors ship with the framework.
- **Paper:** *Reinvent 4: Modern AI-driven generative molecule design*, **J. Cheminform.** 2024. DOI 10.1186/s13321-024-00812-5.
- **GPU/Status:** GPU helps; CPU OK for RL scoring. **Actively maintained** — v4.x (2025). The most production-ready tool in this file.
- **Commercial:** ✅ Apache-2.0. **Synth-constrained: ⚠️ configurable** — *not* by default, but you can add **SA-score, reaction-filter, or AiZynthFinder retrosynthesis** scoring components to the reward (a clean way to bake the synthesizability layer directly into generation). Still commonly paired with a dedicated projection step.

### Apo2Mol — `AIDD-LiLab/Apo2Mol` *(2026, new)*
- **Method:** **Diffusion** (full-atom) — de novo design from **apo (unbound) pockets**, jointly generating ligand **and** holo-like pocket conformation (models pocket flexibility).
- **License:** ✅ **MIT** (verify the HF dataset license separately before training).
- **Paper:** *Apo2Mol*, **AAAI 2026**, arXiv:2511.14559.
- **GPU/Status:** GPU (full-atom diffusion is heavy); **new/immature** (2026) — confirm checkpoint availability.
- **Commercial:** ✅ MIT. **Synth-constrained: ❌.**

### PILOT / e3moldiffusion — `pfizer-opensource/e3moldiffusion` *(2025)*
- **Method:** **Diffusion** (E(3)-equivariant) — pocket-conditioned de novo with **multi-objective guidance via importance sampling** (steer toward docking score / SA at sampling time). Pfizer open-source.
- **License:** ✅ **Apache-2.0** (code; the *journal article* is CC-BY-NC, but the code repo governs the software). Best-licensed 3D pocket diffusion model here.
- **Paper:** *PILOT*, **Chemical Science (RSC)** 2024. DOI 10.1039/D4SC03523B (arXiv:2405.14925).
- **GPU/Status:** GPU (heavy); reasonably maintained (2025).
- **Commercial:** ✅ Apache-2.0. **Synth-constrained: ⚠️** — guidance can steer toward SA/QED but doesn't hard-constrain to makeable space; project downstream.

---

## Binding-site / pocket detection (the upstream input)

### fpocket — `Discngine/fpocket`
- **Method:** Geometry-based pocket detection + druggability scoring (**Voronoi / alpha-spheres**; no ML). Bundles `mdpocket` (trajectories), `dpocket`, `tpocket`.
- **License:** ✅ **MIT.** **CPU only**, very fast.
- **Paper:** Le Guilloux et al., *BMC Bioinformatics* 2009. DOI 10.1186/1471-2105-10-168.
- **Status:** Active — v4.2.3 (2026).
- **Commercial:** ✅ MIT.

### P2Rank — `rdk/p2rank`
- **Method:** **Machine-learning** ligand-binding-site prediction (random-forest over surface points → ranked pockets); no external feature deps. (`prankweb` is the web frontend.)
- **License:** ✅ **MIT.** **CPU only**, multi-threaded; needs **Java 17+**.
- **Paper:** Krivák & Hoksza, *J. Cheminform.* 2018. DOI 10.1186/s13321-018-0285-8.
- **Status:** Active — v2.5.1 (2025).
- **Commercial:** ✅ MIT.

### DoGSiteScorer — **WEB-ONLY** (ProteinsPlus, `proteins.plus`)
- **Method:** **Difference-of-Gaussians** grid pocket detection + descriptor-based druggability. ZBH, Univ. Hamburg.
- **License:** ❌ **No open source — proprietary web service, free for *academic* use only** (REST API via ProteinsPlus).
- **Paper:** Volkamer et al., *Bioinformatics* 28(15):2074, 2012. DOI 10.1093/bioinformatics/bts310.
- **Commercial:** ❌/⚠️ Academic-only; not embeddable. Commercial users contact ZBH.

---

## New 2026 — multi-task generators & the synthesis-aware exception

### PocketXMol — `pengxingang/PocketXMol` ⭐ *(2026 flagship, multi-task)*
- **Method:** Single atom-level generative **foundation** model doing pocket-conditioned 3D SBDD **plus** fragment linking/growing, PROTAC design, small-molecule + peptide docking, and conformer generation — no task-specific fine-tuning. Beat 55 baselines on 11/13 benchmarks; wet-lab validated (caspase-9, PD-L1). One model stands in for several single-purpose tools above.
- **License:** **MIT** code + **CC-BY-4.0** weights (Zenodo 17801271) — both permissive.
- **Paper:** *Cell*, Feb 2026. (Repo created 2024, but weights Dec 2025 + the Cell paper + active 2026 dev make it a 2026-era release.)
- **Commercial:** ✅ MIT + CC-BY-4.0. **Synth-constrained: ❌** — project downstream like the others.

### OMTRA — `gnina/OMTRA` *(2026, multi-task flow-matching)*
- **Method:** Multi-modal flow matching (gnina / Koes lab) — pocket-conditioned de novo + docking + conformer generation; conditions on pocket + pharmacophores; trained on a new ~500M-conformer dataset.
- **License:** **Apache-2.0** (code + trained models + dataset).
- **Paper:** arXiv:2512.05080 (Dec 2025).
- **Status:** Very active (pushed Jun 2026). **Commercial:** ✅ Apache — a maintained competitor to TargetDiff/Pocket2Mol. **Synth-constrained: ❌.**

### Saturn — `schwallergroup/saturn` *(2026, sample-efficient RL — a REINVENT alternative)*
- **Method:** Schwaller-group RL generative framework built for **sample efficiency** (far fewer oracle/docking calls than REINVENT) with a 2025 extension giving **steerable synthesizability control** (specify allowed/forbidden reactions; >90% exact-match to specified routes).
- **License:** ⚠️ **Apache-2.0 — LICENSE-detector false negative** (GitHub shows "NOASSERTION"; the file *is* Apache-2.0 — keep a copy as evidence).
- **Paper:** synthesizability-control arXiv:2505.08774 (2025-05); core Saturn 2024.
- **Status:** Extremely active (pushed Jun 2026, ~86★). **Commercial:** ✅ Apache. **Synth-constrained: ⚠️ configurable** (synthesizability control is a built-in feature — closer to synthesis-aware than REINVENT's default).

### Synthesis-*aware* pocket generators — the exception to "outputs aren't makeable"
Most pocket generators (above) need a downstream projector. These instead generate **synthesizable-by-construction** molecules (over reaction templates + building blocks) while still conditioning on the pocket — directly closing the loop this file keeps pointing at:
- **RxnFlow — `SeonghwanSeo/RxnFlow`** — synthesis-oriented **GFlowNet** over reaction templates + building blocks; SOTA pocket-conditional CrossDocked with **34.8% synthesizable by construction**. **MIT**; ICLR 2025, maintained to Apr 2026. ✅ MIT. **Synth-constrained: ✅** (rare here).
- **CGFlow / 3DSynthFlow — `tsa87/cgflow`** — compositional flows jointly designing the **synthesis pathway + 3D pose** (pocket-conditional *and* synthesizable; ~62% AiZynthFinder success, 15/15 LIT-PCBA). **MIT**; ICML 2025 (confirm 2026 maintenance). ✅ MIT. **Synth-constrained: ✅.**
- **ShEPhERD — `coleygroup/shepherd`** — equivariant diffusion generating 3D molecules conditioned jointly on **shape + electrostatics + pharmacophores** (bioisostere / scaffold-hop). **MIT** (weights on HF; weights license not separately stated). ICLR 2025 oral; very active (2026). The generative complement to the shape/pharmacophore *overlay* tools in [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md). **Synth-constrained: ❌.**

## Choosing

| Need | Pick | License |
|---|---|---|
| Best-licensed 3D pocket generator (commercial) | **PILOT / e3moldiffusion** (Apache), **OMTRA** (Apache), or **DiffSBDD** (MIT) | ✅ |
| Multi-task one-model (SBDD + fragment/linker/PROTAC/docking) | **PocketXMol** | ✅ MIT + CC-BY-4.0 |
| Synthesizable-*by-construction* pocket generation | **RxnFlow**, CGFlow | ✅ MIT |
| Production framework, configurable + synth-aware reward | **REINVENT 4** (+ AiZynthFinder) or **Saturn** | ✅ Apache |
| Validity-guaranteed pocket generation | **PocketFlow** | ✅ MIT (misspelled file) |
| Pocket flexibility / apo pockets | **Apo2Mol** | ✅ MIT (new) |
| Pocket detection (commercial) | **fpocket** / **P2Rank** | ✅ MIT |
| ❌ Avoid for commercial | **DecompDiff** (CC-BY-NC), **Lingo3DMol** (GPL-3) | ❌ / ⚠️ |

**The loop that matters:** *most* pocket-conditioned generators here are ❌ or ⚠️ on synthesizability — so the canonical pipeline is **detect pocket** (fpocket/P2Rank) → **generate into it** (PILOT/DiffSBDD/OMTRA/PocketXMol) → **project to makeable space + get a route** (PrexSyn/SynFormer + AiZynthFinder, [synthesizable-generation.md](synthesizable-generation.md)) → **score binding** ([docking-and-cofolding.md](docking-and-cofolding.md): pose via DiffDock-L/Boltz-1/SigmaDock; affinity via Boltz-2). **The exceptions that skip the projection step:** **RxnFlow** and **CGFlow** generate *synthesizable-by-construction* (over reaction templates + building blocks), and **REINVENT 4 / Saturn** can fold the synthesizability check *into* the reward — the cleanest way to bake the make-it layer into target-based generation. **Don't be fooled** by TargetDiff/PocketFlow showing "no license" on GitHub — both are genuinely MIT. See [licensing-and-data.md](licensing-and-data.md).
