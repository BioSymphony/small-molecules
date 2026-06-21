#!/usr/bin/env python3
"""
Stage 3 (stretch) -- Boltz-2 on the ternary: structure + a PREDICTED AFFINITY.

Boltz-2's unique add over Chai-1 here is the affinity head:
  affinity_pred_value        ~ log10(IC50 in uM)   (lower = tighter)
  affinity_probability_binary ~ P(ligand is a binder)

*** HONEST CAVEAT ***  The affinity head is trained on standard single-protein /
single-pocket binding. daraxonrasib is a cooperative GLUE (its "affinity" only
exists in the CypA+RAS ternary). So the number Boltz emits is OFF-LABEL here --
report it as a curiosity, NOT a validated metric. The structural prediction is
the meaningful part; affinity is "what does the tool say when pushed off-distribution."

Unlike Chai-1, Boltz-2 needs an MSA -> uses --use_msa_server (network required).

Deps (isolated venv): boltz, rdkit, gemmi, numpy.  Run after 00_fetch_and_split.py.
"""
import json, os, subprocess, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
PREP = os.path.join(HERE, "prep", "9BG6")
OUT = os.path.join(HERE, "cofold_boltz"); os.makedirs(OUT, exist_ok=True)
KRAS_CHAIN, CYPA_CHAIN = "A", "C"


def write_yaml(path):
    with open(os.path.join(PREP, "components.json")) as f:
        inv = json.load(f)
    seqs = {p["chain"]: p["seq"] for p in inv["proteins"]}
    sm = inv["smiles"]
    y = []
    y.append("version: 1")
    y.append("sequences:")
    y.append("  - protein:")
    y.append("      id: A")
    y.append(f"      sequence: {seqs[KRAS_CHAIN]}")
    y.append("  - protein:")
    y.append("      id: B")
    y.append(f"      sequence: {seqs[CYPA_CHAIN]}")
    y.append("  - ligand:")
    y.append("      id: C")
    y.append(f"      smiles: '{sm['A1AHB']['smiles']}'")
    y.append("  - ligand:")
    y.append("      id: D")
    y.append(f"      smiles: '{sm['GNP']['smiles']}'")
    y.append("  - ligand:")
    y.append("      id: E")
    y.append("      smiles: '[Mg+2]'")
    y.append("properties:")
    y.append("  - affinity:")
    y.append("      binder: C")          # daraxonrasib is the designated binder (off-label on a glue)
    with open(path, "w") as f:
        f.write("\n".join(y) + "\n")
    print(f"  wrote {path} (KRAS+CypA+A1AHB+GppNHp+Mg; affinity binder=C=daraxonrasib)")
    return path


def run_boltz(yaml_path):
    cmd = ["boltz", "predict", yaml_path, "--use_msa_server", "--out_dir", OUT]
    print("  $ " + " ".join(cmd))
    return subprocess.run(cmd).returncode


def report_affinity():
    js = glob.glob(os.path.join(OUT, "**", "affinity*.json"), recursive=True)
    if not js:
        print("  (no affinity json found; inspect", OUT, ")"); return
    with open(js[0]) as f:
        a = json.load(f)
    print("\n  --- Boltz-2 affinity (OFF-LABEL on a glue; curiosity only) ---")
    print(json.dumps(a, indent=2))
    v = a.get("affinity_pred_value")
    if v is not None:
        print(f"  affinity_pred_value ~ log10(IC50 uM) = {v}  => IC50 ~ {10**float(v):.3g} uM (interpret with caution)")


def main():
    y = write_yaml(os.path.join(OUT, "ternary.yaml"))
    if "--score-only" not in sys.argv:
        rc = run_boltz(y)
        if rc != 0:
            print(f"!! boltz failed rc={rc}"); sys.exit(rc)
    report_affinity()
    print("\nStructure RMSD vs 9BG6: score the Boltz .cif the same way as Chai")
    print("(superpose on CypA Calpha; see 02_cofold_chai.py score()).")


if __name__ == "__main__":
    main()
