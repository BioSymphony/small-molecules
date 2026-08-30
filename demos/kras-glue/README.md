# KRAS Glue Demo

This compact demo shows how the skill routes a small-molecule binding task for
a molecular glue rather than a standard single-pocket ligand.

The public structure is [PDB 9BG6](https://www.rcsb.org/structure/9BG6):
daraxonrasib bound with KRAS G12V, CypA, GppNHp, and Mg. The positive-control
pocket example uses PDB 7RPZ.

The repository includes the scripts and result summaries. It excludes generated
docking output, co-folding output, and large media builds.

## What It Tests

| Test | Tool | Check |
|---|---|---|
| MRTX1133 into the KRAS G12D pocket | smina | Recovery of a known pocket pose |
| daraxonrasib into CypA alone | smina | Recovery of the presenter-side pocket |
| daraxonrasib into KRAS alone | smina | Presence of a KRAS-only site |
| daraxonrasib with CypA and KRAS | Chai-1 | Recovery of ternary geometry from sequence and SMILES |
| KRAS perturbations on the crystal ternary | soft interface score and MM-GBSA | Separation of tolerated mutations from a disruptor |

Choose the method by the physical problem. A standard pocket workflow fits the
7RPZ control. The daraxonrasib system requires the ternary structure and
follow-up scoring on that scaffold.

## Decision Rules

- Use the 7RPZ redock as the standard-pocket control before reading the glue
  cases.
- For molecular glues, split the presenter side from the target side. Docking
  can test a presenter pocket, but the target interface might exist only in the
  ternary assembly.
- When a public ternary structure exists, perturb and score that structure.
  Estimate mutation effects, rank analogs, use MM-GBSA for triage, and use RBFE
  or FEP when the setup supports it.
- When no ternary structure exists, calibrate co-folding on a related public
  glue structure. Align on the presenter protein and measure target-chain and
  ligand displacement in that frame.
- Use perturbation and MM-GBSA output for triage. Evaluate separation between
  tolerated variants and disruptors rather than small differences within a
  tolerated set.

## Run the Demo

Optional: install local dependencies.

```bash
python -m pip install -r ../../requirements-demo.txt
```

Prepare inputs and run CPU docking.

```bash
python 00_fetch_and_split.py
python 01_dock.py
```

Run GPU co-folding.

```bash
python 02_cofold_chai.py
python 03_cofold_boltz.py
```

After Chai output exists, run local perturbation scoring.

```bash
python 04_perturb_score.py
python perturb/make_funnel_svg.py
```

In a prepared Amber and OpenMM environment, run the MM-GBSA mutation scan.

```bash
bash ddg/pod/run_ddg.sh
python ddg/pod/make_ddg_svg.py
```

The `run.sh` script runs the local CPU stages and skips perturbation scoring
until a Chai prediction is present.

## Public Result Snapshot

Results from the public-data run on 2026-06-13:

| Test | Result |
|---|---|
| MRTX1133 into KRAS pocket | -14.2 kcal/mol, 0.39 Å RMSD, 100% native contacts |
| daraxonrasib into CypA | -10.3 kcal/mol, 0.23 Å RMSD, 100% native contacts |
| daraxonrasib into KRAS | -6.5 kcal/mol, 13.5 Å RMSD, 18% native contacts |
| Chai-1 ternary | CypA C-alpha 0.34 Å, KRAS C-alpha 23.3 Å, ligand 4.1 Å, ipTM 0.63 |
| perturbation funnel | crystal pose at -25.4 kcal/mol with 225 native contacts |
| MM-GBSA mutation scan | G12D, G12C, G12 (wild type at residue 12), and Q61H within ±2 kcal/mol; M67R at +4.3 kcal/mol |

These results demonstrate method routing; they are not drug-development
results. See
[`../../references/worked-example-kras-glue.md`](../../references/worked-example-kras-glue.md)
for the complete reasoning path.
