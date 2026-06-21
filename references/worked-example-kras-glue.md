# Worked Example — KRAS(ON) Molecular Glues (daraxonrasib): which layers apply, which don't, and how to actually run it

A concrete stress-test of this toolkit against a **2026 frontier drug**. It shows where the target-based layer fits, where it breaks, and — the practical core — how an **experimental structure turns an intractable "predict a molecular glue" problem into a tractable "perturb and score" one.** Verified **2026-06-13**.

## The molecule

- **daraxonrasib (RMC-6236)** — Revolution Medicines; first-in-class oral **pan-RAS(ON)** inhibitor. Phase 1/2 in *NEJM* (May 2026); FDA Breakthrough Therapy + expanded-access for previously treated metastatic pancreatic cancer (PDAC). It hits the RAS mutants the G12C drugs miss (G12D/V/S, G13X, Q61X).
- **Mechanism — a noncovalent *molecular glue*, not a pocket binder.** It binds **cyclophilin A (CypA)** first; the drug·CypA composite then lies on the **flat switch-I/II face of *active, GTP-bound* RAS**, gluing CypA onto RAS and blocking RAF/MEK/ERK. It is a **macrocycle derived from the natural product sanglifehrin A**.
- **The structure exists — [PDB 9BG6](https://www.rcsb.org/structure/9BG6):** *"Tri-complex of Daraxonrasib (RMC-6236), KRAS G12V, and CypA."* X-ray **1.66 Å**; chains KRAS (A, B) + CypA/PPIA (C, D); ligands daraxonrasib (CCD **A1AHB**), **GNP** (GppNHp — the non-hydrolyzable GTP analog that locks the **ON** state) and **Mg²⁺**. Deposited 2024-04-18, released 2025-03-19.

Three facts decide everything downstream: it's a **glue** (no canonical KRAS pocket), it acts on the **ON (GTP) state** (so the nucleotide and Mg²⁺ are not optional), and the complex is a **ternary macrocyclic-NP assembly we already have at 1.66 Å**.

## Which layers apply — and which don't

| Task | Our layer | Fit |
|---|---|---|
| Predict the drug + CypA + RAS **tri-complex** | co-folding — **Boltz-2, Chai-1, AF3-class** (OpenFold3/Protenix) | ◐ Right *family* (multi-chain + ligand), but glue/induced-proximity accuracy is **unproven** — and **9BG6 makes prediction unnecessary** |
| **Dock** daraxonrasib into a KRAS pocket | classical docking — Vina/gnina/smina | ✗ **Wrong model.** It's a glue; no canonical RAS pocket. (You *can* dock the CypA half — a real cyclophilin pocket — but that misses the RAS-selectivity story) |
| Effect of **G12D/V/Q61X** on binding | FEP — **OpenFE/Perses/OpenMM** on 9BG6 | ◑ **Tractable** via protein-mutation RBFE; ternary setup is advanced but this is what FEP is *for* |
| **Rank analogs** of daraxonrasib | FEP RBFE + scaffold enumeration (REINVENT 4 / RDKit) | ✓ **Classic lead-opt** on a fixed ternary scaffold — strongest fit |
| **De novo** new glue chemotypes into the site | pocket-conditioned generators (Pocket2Mol/TargetDiff/PocketXMol) | ✗/◐ macrocycle + composite 2-protein surface is **out of training distribution** |
| **Can we make the analogs?** | Layer 1 — retro + synthesizability scoring | ✓ Valuable — but ⚠️ macrocyclic NP chemistry is itself out-of-distribution for USPTO-trained route models (see [synthesizability-scoring.md](synthesizability-scoring.md)) |
| ADMET / PK / transporters | ADMET layer | ✓ Relevant — daraxonrasib has documented transporter/PK liabilities |

## The pivot — why this is tractable

Predicting a molecular-glue ternary complex *de novo* is a frontier problem and unreliable. **But we don't have to:** 9BG6 is the experimental answer at 1.66 Å. That flips the question from *"predict the glue"* (hard, untrustworthy) to *"given the complex, perturb one thing and score the change"* — a standard, well-posed free-energy problem. **Everything below starts from 9BG6.** This is the difference between the toolkit being a poor fit and a good one.

## Demo runbook — perturb & score from 9BG6

Two perturbation axes from the same crystal: **mutate the protein** ("does this drug still bind the mutant?") and **modify the drug** ("can we make a better analog?").

### Stage 0 — Structure prep *(CPU, minutes)*
- Fetch: `wget https://files.rcsb.org/download/9BG6.cif` (or `.pdb`).
- Split components: KRAS chain (A), CypA chain (C), ligand `A1AHB`, `GNP`, `MG`.
- Protein prep: **PDBFixer** (OpenMM) — add hydrogens/caps, protonate at pH 7.4. **Keep GppNHp + Mg²⁺** — they define the ON state the glue requires.
- Ligand prep: extract `A1AHB`; pull its SMILES from the **CCD / PubChem** (do *not* hand-type a 50-atom macrocycle); parameterize with **OpenFF/GAFF**.
- ⚠️ First friction point: **GppNHp is a non-standard residue** and the **macrocycle** needs custom parameters — neither is in a default protein force field. Budget time here.

### Stage A — Mutant effect: does daraxonrasib survive KRAS G12D / Q61H? *(the "KRAS mutant" question)*
- Goal: ΔΔG of binding across variants. 9BG6 is already **G12V**; build WT, **G12D**, **Q61H**, etc. on the KRAS chain *in the complex* (PyMOL/ChimeraX mutagenesis, or FoldX/Rosetta).
- **Quick triage** *(hours, CPU/1 GPU)*: **gmx_MMPBSA** (MM-GBSA) endpoint ΔΔG per variant — cheap ranking. → [binding-affinity-and-fep.md](binding-affinity-and-fep.md)
- **Rigorous** *(days, GPU)*: **protein-mutation RBFE** with **Perses** (it supports amino-acid mutations) or **OpenFE** — alchemically mutate residue 12/61 in the bound vs. free states.
- **Built-in sanity check:** because the drug binds *away* from residues 12/61, ΔΔG should be **small** across G12X/Q61X — recapitulating the known pan-mutant profile. If your pipeline reproduces that, it's calibrated; if it predicts a large ΔΔG, suspect your params/sampling, not the biology.

### Stage B — Analog exploration: modify daraxonrasib and rank *(the "explore changes" question)*
- Goal: rank modifications of daraxonrasib by predicted affinity **in the ternary**.
- **Enumerate (scaffold-constrained, NOT de novo):** keep the CypA-binding macrocycle core fixed; vary the RAS-facing substituents. **RDKit** reaction enumeration or **REINVENT 4** LibInvent/Mol2Mol with the scaffold locked. → [structure-based-generation.md](structure-based-generation.md). *Do not* reach for pocket de-novo generators here (macrocycle = out of distribution; see Boundaries).
- **Cheap rank** *(per analog, minutes)*: core-align the analog into the fixed complex (constrained embed), minimize, then **MM-GBSA** (gmx_MMPBSA) or **gnina** CNN rescoring of the held complex. Triage hundreds.
- **Rigorous rank** *(GPU, ~hours each)*: **relative binding free energy (RBFE)** across the congeneric series with **OpenFE / Perses** in the ternary context — textbook lead-opt, here on a fixed CypA·RAS scaffold.
- ⚠️ Two-sided constraint: every analog must preserve **CypA binding *and* the RAS-facing surface**. Perturbations that break CypA engagement are physically meaningless — the scoring must hold the CypA contacts.

### Stage C — Reality filters *(makeability, ADMET, selectivity)*
- **Makeability:** **AiZynthFinder** / **RetroScore** ([synthesizability-scoring.md](synthesizability-scoring.md)). ⚠️ macrocyclic, NP-derived chemistry is **out of distribution** for USPTO-trained route models — treat scores as low-confidence and cross-check a chemist.
- **ADMET:** **ADMET-AI** (local). daraxonrasib has documented transporter/PK liabilities (AACR PK abstract) — the thing to optimize against.
- **Selectivity / anti-target:** CypA is a broadly expressed chaperone; off-target **CypA binding / immunosuppression** (the sanglifehrin/cyclosporin lineage) is a real anti-target axis — screen analogs for it. → [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md)

## What does NOT work here — honest boundaries

- **Classical docking of daraxonrasib into KRAS** — wrong model: no canonical RAS pocket; the drug doesn't bind RAS alone.
- **De novo pocket-conditioned generation** (Pocket2Mol/TargetDiff/DiffSBDD/PocketXMol) — trained on drug-like small molecules in single pockets; a macrocyclic glue spanning a two-protein composite surface is out of distribution. Use scaffold-constrained enumeration instead.
- **Naive FEP** — GppNHp + Mg²⁺ + macrocycle parameters + a protein–protein interface make this an **expert setup**, not push-button. Budget for parameterization and sampling convergence.
- **Co-folding to *obtain* the structure** — unnecessary here (9BG6 exists) and unproven on glues.

## Demo results — public-data run (2026-06-13)

A runnable version lives in [`demos/kras-glue/`](../demos/kras-glue/). Both binding-tool families were executed against 9BG6: docking on CPU and co-folding on GPU. The numbers confirm the boundary empirically:

| Tool | Test | Result | Verdict |
|---|---|---|---|
| smina (docking) | MRTX1133 → KRAS pocket *(control)* | −14.2 kcal/mol, RMSD 0.39 Å | stack works on a real pocket |
| smina | daraxonrasib → **CypA** alone | −10.3 kcal/mol, 100% native contacts | **presenter** half dockable |
| smina | daraxonrasib → **KRAS** alone | −6.5 kcal/mol, 18% contacts, pose flees 13.5 Å | **target** half undockable — no pocket |
| Chai-1 *(co-fold, MSA-free)* | predict the daraxonrasib·CypA·KRAS ternary | CypA-Cα 0.34 Å, **KRAS-Cα 23.3 Å**, ligand 4.1 Å, ipTM 0.63 | folds each protein, **misplaces KRAS 23 Å** — glue geometry not recovered |

Both tools fail at the same glue-specific step — the **RAS engagement**. Docking finds no RAS pocket (there isn't one); co-folding folds both chains superbly but can't place them in the right relative geometry, and its own **ipTM (0.63) honestly flags the doubt**. This is precisely why the experimental ternary is load-bearing: 9BG6 lets you *skip* the prediction both tools fail at and go straight to perturb-and-score. Full runbook + scripts: [`demos/kras-glue/README.md`](../demos/kras-glue/README.md).

## Transfer — when you DON'T have a structure

For **zoldonrasib (RMC-9805, KRAS G12D ON-glue)** or the **G12D degraders (e.g., setidegrasib)** where a public ternary may not exist, you're back to *predicting* the complex → **co-folding (Boltz-2 / Chai-1 / AF3-class)** with both protein chains + ligand is the only in-repo option, at the frontier. **Calibrate first:** predict the *daraxonrasib* complex and check RMSD against 9BG6 before trusting any predicted glue you can't crystallize. **We ran exactly this calibration (see measured results above): Chai-1 folded both chains but misplaced KRAS by 23 Å with ipTM 0.63 — it did *not* carry the glue.** That is the honest gate on whether co-folding can carry a glue program, and here it says "not yet."

## Tools used (all from this repo)

- Co-folding / docking → [docking-and-cofolding.md](docking-and-cofolding.md) (Boltz-2, Chai-1, gnina)
- Free energy (MM-GBSA + RBFE, protein-mutation & ligand) → [binding-affinity-and-fep.md](binding-affinity-and-fep.md) (OpenFE, Perses, OpenMM, gmx_MMPBSA)
- Scaffold-constrained analog enumeration → [structure-based-generation.md](structure-based-generation.md) (REINVENT 4) + RDKit
- Makeability → [retrosynthesis-planning.md](retrosynthesis-planning.md) (AiZynthFinder) + [synthesizability-scoring.md](synthesizability-scoring.md) (RetroScore)
- ADMET + selectivity → [admet-prediction.md](admet-prediction.md) (ADMET-AI) + [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md)
- Licensing before any commercial use → [licensing-and-data.md](licensing-and-data.md)

**The one-line lesson:** the newest KRAS drugs (tri-complex glues, degraders) defeat the *binary-docking* half of this toolkit, but an experimental ternary structure (9BG6) makes the *free-energy* half — mutation effect and analog ranking — genuinely usable. Know which problem you have before picking the tool.
