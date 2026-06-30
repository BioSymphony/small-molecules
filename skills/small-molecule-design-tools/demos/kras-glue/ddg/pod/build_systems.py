#!/usr/bin/env python3
"""Build per-system KRAS+Mg PDBs for the ddG scan (runs on the pod, stdlib only).

WT = crystal KRAS-G12V. Mutants are made by keeping backbone (+CB) of the target
residue and renaming it; tleap rebuilds the new side chain. Mg2+ is appended so it
stays on the KRAS (ligand) side. CypA + drug + GNP are added later in tleap.
"""
import os
IN = "/workspace/inputs"
OUT = "/workspace/run"

# system -> (resseq, new_resname) or None for WT (crystal G12V)
SYSTEMS = {
    "wt":   None,
    "g12d": (12, "ASP"),   # pan-RAS: should be tolerated (small ddG)
    "g12c": (12, "CYS"),   # pan-RAS: should be tolerated
    "g12g": (12, "GLY"),   # true wild-type glycine: tolerated
    "q61h": (61, "HIE"),   # oncogenic, RAS(ON): tolerated
    "m67r": (67, "ARG"),   # disruptor control: hydrophobic switch-II contact -> charged; expect destabilizing
}
BB = {"N", "CA", "C", "O", "CB"}

def read_atoms(path):
    out = []
    for ln in open(path):
        if ln.startswith(("ATOM", "HETATM")):
            out.append(ln.rstrip("\n"))
    return out

def resseq(ln):  return int(ln[22:26])
def aname(ln):   return ln[12:16].strip()
def set_resname(ln, rn): return ln[:17] + f"{rn:>3}" + ln[20:]

kras = read_atoms(os.path.join(IN, "kras.pdb"))
mg   = read_atoms(os.path.join(IN, "mg.pdb"))

for sys, mut in SYSTEMS.items():
    lines = []
    for ln in kras:
        if mut and resseq(ln) == mut[0]:
            keep = BB - ({"CB"} if mut[1] == "GLY" else set())
            if aname(ln) not in keep:
                continue
            ln = set_resname(ln, mut[1])
        lines.append(ln)
    # append Mg2+ (single ion); ensure it reads as its own residue
    body = "\n".join(lines) + "\nTER\n" + "\n".join(mg) + "\nTER\nEND\n"
    p = os.path.join(OUT, f"{sys}_krasmg.pdb")
    open(p, "w").write(body)
    n = len([l for l in lines])
    print(f"{sys:5s} mut={mut}  KRAS atoms={n}  -> {p}")
print("done")
