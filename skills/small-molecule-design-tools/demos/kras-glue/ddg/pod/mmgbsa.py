#!/usr/bin/env python3
"""Single-trajectory MM-GBSA endpoint dG for one system (runs on the pod, OpenMM).

Minimize the complex in GBn2 implicit solvent, then evaluate complex / receptor /
ligand GB energies at that geometry:  dG_bind = E_complex - E_receptor - E_ligand.
Single-snapshot, no entropy -> a semi-quantitative ranking energy (the honest label).
The receptor/ligand split uses the contiguous block ordering from assemble.sh:
ligand (KRAS+Mg+GNP) = first n_lig atoms, receptor (CypA+drug) = the rest.
"""
import sys, json
from openmm import app, unit, LangevinIntegrator, Platform
import openmm as mm

def platform():
    # conda CUDA build mismatches the pod driver (PTX); try OpenCL on the GPU, else
    # CPU. A 1.6 nm cutoff keeps GBn2 ~O(N) so even CPU stays fast.
    for p in ("OpenCL", "CPU"):
        try:
            return Platform.getPlatformByName(p), ({"Threads": "8"} if p == "CPU" else {})
        except Exception:
            continue

PLAT, PROPS = platform()
print("platform:", PLAT.getName())

def sim_for(prmtop):
    prm = app.AmberPrmtopFile(prmtop)
    system = prm.createSystem(implicitSolvent=app.GBn2,
                              nonbondedMethod=app.CutoffNonPeriodic,
                              nonbondedCutoff=1.6*unit.nanometer,
                              constraints=None, removeCMMotion=False,
                              soluteDielectric=1.0, solventDielectric=78.5)
    integ = LangevinIntegrator(300*unit.kelvin, 1/unit.picosecond, 0.001*unit.picoseconds)
    return app.Simulation(prm.topology, system, integ, PLAT, PROPS), prm

def energy(prmtop, positions, minimize=False):
    s, prm = sim_for(prmtop)
    s.context.setPositions(positions)
    if minimize:
        s.minimizeEnergy(maxIterations=1200)
    st = s.context.getState(getEnergy=True, getPositions=True)
    E = st.getPotentialEnergy().value_in_unit(unit.kilocalorie_per_mole)
    pos = st.getPositions(asNumpy=True)
    return E, pos

name = sys.argv[1]
inp = app.AmberInpcrdFile(f"{name}.inpcrd")
# complex = the full (dry) system; ante-MMPBSA split it into two contiguous blocks:
#   *_rec.prmtop = residues :1-170  (KRAS + Mg + GNP)  -> first atom block
#   *_lig.prmtop = residues :171-335 (CypA + drug)     -> second atom block
# dG = E_complex - E_rec - E_lig is symmetric in the rec/lig labels.
E_com, pos = energy(f"{name}.prmtop", inp.positions, minimize=True)
n_first = app.AmberPrmtopFile(f"{name}_rec.prmtop").topology.getNumAtoms()
E_rec, _ = energy(f"{name}_rec.prmtop", pos[:n_first])
E_lig, _ = energy(f"{name}_lig.prmtop", pos[n_first:])
dG = E_com - E_rec - E_lig
out = {"system": name, "E_com": round(E_com,2), "E_rec": round(E_rec,2),
       "E_lig": round(E_lig,2), "dG_bind": round(dG,2), "n_first_block": n_first,
       "platform": PLAT.getName()}
print("RESULT " + json.dumps(out))
open(f"{name}_dG.json","w").write(json.dumps(out))
