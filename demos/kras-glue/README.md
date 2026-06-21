# KRAS Glue Demo

This compact demo shows how the skill routes a small-molecule binding task when the target is a molecular glue rather than a standard single-pocket ligand.

The public structure is [PDB 9BG6](https://www.rcsb.org/structure/9BG6): daraxonrasib bound with KRAS G12V, CypA, GppNHp, and Mg. The positive-control pocket example uses PDB 7RPZ.

The demo is intentionally small. It keeps scripts and result summaries in the repo, while generated docking outputs, co-folding outputs, and large media builds stay out.

## What It Tests

| Test | Tool | Question |
|---|---|---|
| MRTX1133 into the KRAS G12D pocket | smina | Does the docking stack recover a known pocket pose? |
| daraxonrasib into CypA alone | smina | Does docking recover the presenter-side pocket? |
| daraxonrasib into KRAS alone | smina | Does docking find a KRAS-only site? |
| daraxonrasib with CypA and KRAS | Chai-1 | Does co-folding recover the ternary geometry from sequence and SMILES? |
| KRAS perturbations on the crystal ternary | soft interface score and MM-GBSA | Does scoring on the experimental scaffold separate tolerated mutations from a disruptor? |

The lesson for agents is concrete: choose the method by the physical problem. A standard pocket workflow fits the 7RPZ control. The daraxonrasib system needs the ternary structure and follow-up scoring on that scaffold.

## Run Order

Optional local dependencies:

```bash
python -m pip install -r ../../requirements-demo.txt
```

CPU prep and docking:

```bash
python 00_fetch_and_split.py
python 01_dock.py
```

GPU co-folding:

```bash
python 02_cofold_chai.py
python 03_cofold_boltz.py
```

Local perturbation scoring after Chai output exists:

```bash
python 04_perturb_score.py
python perturb/make_funnel_svg.py
```

MM-GBSA mutation scan on a prepared Amber/OpenMM runtime:

```bash
bash ddg/pod/run_ddg.sh
python ddg/pod/make_ddg_svg.py
```

`run.sh` executes the local CPU stages and skips perturbation scoring until a Chai prediction is present.

## Public Result Snapshot

Results from the public-data run on 2026-06-13:

| Test | Result |
|---|---|
| MRTX1133 into KRAS pocket | -14.2 kcal/mol, 0.39 A RMSD, 100% native contacts |
| daraxonrasib into CypA | -10.3 kcal/mol, 0.23 A RMSD, 100% native contacts |
| daraxonrasib into KRAS | -6.5 kcal/mol, 13.5 A RMSD, 18% native contacts |
| Chai-1 ternary | CypA C-alpha 0.34 A, KRAS C-alpha 23.3 A, ligand 4.1 A, ipTM 0.63 |
| perturbation funnel | crystal pose at -25.4 kcal/mol with 225 native contacts |
| MM-GBSA mutation scan | G12D, G12C, G12, and Q61H within +/-2 kcal/mol; M67R at +4.3 kcal/mol |

The numbers are a method-routing example, not a drug-development result. Use the worked example in [`../../references/worked-example-kras-glue.md`](../../references/worked-example-kras-glue.md) for the reasoning path across the skill.
