# Worked Example: Route a KRAS(ON) Molecular-Glue Task

This example uses public structure 9BG6 to choose methods for daraxonrasib, a
KRAS(ON) tri-complex inhibitor. The experimental ternary structure supports
perturbation and scoring workflows that a binary docking model cannot represent.
Source status date: **2026-08-30**.

## Public Starting Point

- [Daraxonrasib (RMC-6236)](https://www.nejm.org/doi/full/10.1056/NEJMoa2505783)
  is an oral RAS(ON) multiselective inhibitor under clinical evaluation. The
  cited May 2026 article reports phase 1/2 results in previously treated
  RAS-mutated pancreatic cancer.
- Daraxonrasib forms a noncovalent complex with cyclophilin A (CypA) and active,
  GTP-bound RAS. The composite complex blocks RAS effector binding.
- [PDB 9BG6](https://www.rcsb.org/structure/9BG6) contains daraxonrasib, KRAS
  G12V, CypA, GppNHp, and magnesium at 1.66 Å resolution. RCSB PDB reports a
  deposit date of 2024-04-18 and a release date of 2025-03-19.

The method choice follows three properties of the system: the ligand binds a
ternary interface, the active-state nucleotide and magnesium are part of the
complex, and an experimental structure is available.

## Method Fit

| Task | Method | Fit |
|---|---|---|
| Predict the drug + CypA + RAS tri-complex | Boltz, Chai-1, or another AF3-class co-folding model | Limited. These models accept multiple chains and a ligand, but 9BG6 already provides the experimental geometry. |
| Dock daraxonrasib into KRAS alone | Vina, gnina, or smina | Poor. Daraxonrasib binds the composite CypA-RAS interface rather than a KRAS-only pocket. |
| Estimate mutation effects | OpenFE, Perses, or OpenMM on 9BG6 | Plausible with specialist setup. Protein-mutation free-energy calculations require careful parameterization and sampling. |
| Rank close analogs | RBFE plus scaffold-constrained enumeration | Good candidate workflow when each analog preserves the CypA-binding core and the RAS-facing contacts. |
| Generate unrelated glue chemotypes | Pocket2Mol, TargetDiff, or PocketXMol | Low confidence. Their training domains do not establish performance on macrocycles at two-protein interfaces. |
| Check analog makeability | Retrosynthesis plus synthesizability scoring | Useful as triage. USPTO-trained models can be unreliable for macrocyclic, natural-product-derived chemistry. |
| Screen ADMET and selectivity | ADMET and target-prediction tools | Relevant for prioritization, subject to each model's endpoint and training-data limits. |

## Why the Experimental Structure Matters

De novo ternary-complex prediction remains uncertain for molecular glues. PDB
9BG6 supplies the measured geometry, so the following workflow tests defined
mutations or close analogs on that structure. Each stage starts with 9BG6.

## Demo Runbook

The runbook covers two controlled changes: mutate KRAS or change daraxonrasib.

### Stage 0: Prepare the Structure

- Download `9BG6.cif` or `9BG6.pdb` from RCSB PDB.
- Extract KRAS chain A, CypA chain C, ligand `A1AHB`, `GNP`, and `MG`.
- Add missing atoms and hydrogens with PDBFixer or a preparation workflow that
  supports the selected force field. Keep GppNHp and Mg²⁺ because they define
  the active-state complex.
- Extract `A1AHB`, get its structure from the PDB Chemical Component
  Dictionary or PubChem, and parameterize it with OpenFF or GAFF.
- Review the GppNHp and macrocycle parameters before interpreting energies. A
  default protein force field might not provide them.

### Stage A: Estimate KRAS Mutation Effects

- Build the target variants on the KRAS chain in the complex. PDB 9BG6 already
  contains G12V; relevant comparisons can include wild type, G12D, and Q61H.
- Use gmx_MMPBSA for an initial endpoint estimate. See
  [binding-affinity-and-fep.md](binding-affinity-and-fep.md).
- Use Perses or OpenFE for protein-mutation free-energy calculations that compare
  bound and unbound states.
- Compare the computed mutation trend with published multiselective activity.
  Investigate parameterization and sampling when the calculation predicts large,
  unexplained effects for remote mutations.

### Stage B: Rank Close Analogs

- Keep the CypA-binding macrocycle core and vary RAS-facing substituents. Use
  RDKit reaction enumeration or REINVENT 4
  LibInvent/Mol2Mol with scaffold constraints. See
  [structure-based-generation.md](structure-based-generation.md).
- Align each analog to the fixed core, minimize the complex, and use MM-GBSA or
  gnina rescoring for an initial rank.
- Calculate relative binding free energies for a congeneric series with OpenFE
  or Perses in the ternary context.
- Check both interfaces. An analog that loses CypA binding no longer tests the
  intended ternary mechanism.

### Stage C: Apply Makeability, ADMET, and Selectivity Filters

- Use AiZynthFinder and RetroScore for makeability triage. Treat results for
  macrocyclic, natural-product-derived chemistry as low confidence, and ask a
  chemist to review the proposed routes. See
  [synthesizability-scoring.md](synthesizability-scoring.md).
- Use ADMET-AI only for endpoints represented by its documented models and
  training data.
- Treat CypA engagement as a required design dimension rather than a generic
  off-target score. See
  [target-and-selectivity-prediction.md](target-and-selectivity-prediction.md).

## Method Boundaries

- **Classical docking of daraxonrasib into KRAS** does not represent the ternary
  binding mechanism because daraxonrasib binds the composite CypA-RAS
  interface.
- Pocket2Mol, TargetDiff, DiffSBDD, and PocketXMol were trained on drug-like
  small molecules in single pockets. Their published evaluations do not
  establish performance for a macrocyclic glue at a two-protein interface.
- An FEP setup for GppNHp, Mg²⁺, a macrocycle, and a protein-protein interface
  requires specialist parameterization and convergence checks.
- Co-folding is unnecessary for this example because 9BG6 provides the
  experimental structure. Published evaluations do not establish glue
  prediction performance.

## Public Demo Results (2026-06-13)

The runnable scripts are in [`demos/kras-glue/`](../demos/kras-glue/). The demo
applies docking and co-folding to 9BG6 as method-routing checks. These outputs
do not validate a drug-discovery model or predict clinical activity.

| Tool | Test | Result | Verdict |
|---|---|---|---|
| smina (docking) | MRTX1133 in the KRAS pocket *(control)* | −14.2 kcal/mol, RMSD 0.39 Å | Recovered the reference pocket pose |
| smina | daraxonrasib with CypA alone | −10.3 kcal/mol, 100% native contacts | Recovered the CypA-side pose |
| smina | daraxonrasib with KRAS alone | −6.5 kcal/mol, 18% contacts, 13.5 Å displacement | Did not recover a KRAS-only pose |
| Chai-1 *(co-fold, MSA-free)* | daraxonrasib, CypA, and KRAS | CypA-Cα 0.34 Å, KRAS-Cα 23.3 Å, ligand 4.1 Å, ipTM 0.63 | Folded both proteins but did not recover their relative geometry |

The KRAS-only docking test and the Chai-1 co-folding test both miss the
RAS-engagement geometry. Docking finds no stable KRAS-only pose. Chai-1 places
KRAS 23.3 Å from the experimental frame and reports an ipTM of 0.63. Use 9BG6
for perturbation studies instead of treating either result as a recovered
ternary structure. The scripts and compact result files are in
[`demos/kras-glue/`](../demos/kras-glue/README.md).

## Related Public Ternary Structures

[PDB 9CTB](https://www.rcsb.org/structure/9CTB) provides a 1.29 Å structure of
zoldonrasib (RMC-9805), KRAS G12D, and CypA. RCSB PDB records a deposit date of
2024-07-24 and a release date of 2025-07-23. This measured ternary geometry
provides a separate starting point for zoldonrasib method-routing work.

When no relevant public structure exists, co-fold the protein chains and ligand,
then calibrate the same setup on a related complex with an experimental
structure. The Chai-1 calibration in this demo misplaced KRAS by 23.3 Å, so
that setup does not support an unmeasured glue geometry.

## Tool References

- [Docking and co-folding](docking-and-cofolding.md): Boltz, Chai-1, and gnina
- [Binding affinity and free energy](binding-affinity-and-fep.md): OpenFE,
  Perses, OpenMM, and gmx_MMPBSA
- [Structure-based generation](structure-based-generation.md): REINVENT 4 and RDKit
- [Retrosynthesis planning](retrosynthesis-planning.md) and
  [synthesizability scoring](synthesizability-scoring.md): AiZynthFinder and
  RetroScore
- [ADMET prediction](admet-prediction.md) and
  [target and selectivity prediction](target-and-selectivity-prediction.md)
- [Licensing and data terms](licensing-and-data.md)
