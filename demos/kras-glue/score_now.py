#!/usr/bin/env python3
"""Robust standalone scorer for the Chai-1 ternary prediction vs crystal 9BG6.

Protein metrics (CypA superposition + KRAS-Calpha RMSD) are computed directly and
never hang. Ligand RMSD (spyrmsd, symmetric on a 58-atom macrocycle) runs under a
60s SIGALRM so a combinatorial graph-iso can't stall the run. Handles 9BG6's two
ternary assemblies by trying both crystal CypA chains and keeping the best match.
"""
import os, json, glob, signal
import numpy as np
import gemmi
from rdkit import Chem

HERE = os.path.dirname(os.path.abspath(__file__))
PRED = os.path.join(HERE, "cofold_chai", "pred")
CRYST = os.path.join(HERE, "prep", "9BG6", "9BG6.cif")
LIG, KMIN = "A1AHB", 166


def ca_coords(p):
    st = gemmi.read_structure(p); st.setup_entities(); out = {}
    for ch in st[0]:
        for res in ch:
            t = gemmi.find_tabulated_residue(res.name)
            if not (t and t.is_amino_acid()):
                continue
            a = res.find_atom("CA", "*")
            if a is not None:
                out.setdefault(ch.name, []).append((res.seqid.num, [a.pos.x, a.pos.y, a.pos.z]))
    return {c: sorted(v) for c, v in out.items()}


def kab(P, Q):
    Pc, Qc = P.mean(0), Q.mean(0)
    H = (P - Pc).T @ (Q - Qc); U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1, 1, d]) @ U.T
    return lambda X: (X - Pc) @ R.T + Qc


def xyz(rl, n): return np.array([p[1] for p in rl[:n]])


def ligmols(p, only=None, largest=False):
    st = gemmi.read_structure(p); st.setup_entities(); st.remove_waters(); rs = []
    for ch in st[0]:
        for r in ch.get_ligands():
            if only and r.name != only:
                continue
            rs.append(r)
    if largest and rs:
        rs = [max(rs, key=lambda r: len(r))]
    ms = []
    for r in rs:
        o = gemmi.Structure(); m = gemmi.Model("1"); c = gemmi.Chain("L")
        c.add_residue(r); m.add_chain(c); o.add_model(m); o.setup_entities()
        mol = Chem.MolFromPDBBlock(o.make_pdb_string(), proximityBonding=True, removeHs=True, sanitize=False)
        if mol and mol.GetNumAtoms() > 3:
            ms.append(mol)
    return ms


class TO(Exception): pass


def main():
    cifs = sorted(glob.glob(os.path.join(PRED, "pred.model_idx_*.cif")))
    cifs.extend(sorted(glob.glob(os.path.join(HERE, "cofold_chai", "pred.model_idx_*.cif"))))
    if not cifs:
        raise SystemExit("no Chai prediction found under cofold_chai/")
    cif = cifs[0]
    pca, cca = ca_coords(cif), ca_coords(CRYST)
    pk = {c: v for c, v in pca.items() if len(v) >= KMIN}
    pcy = {c: v for c, v in pca.items() if len(v) < KMIN}
    ck = {c: v for c, v in cca.items() if len(v) >= KMIN}
    ccy = {c: v for c, v in cca.items() if len(v) < KMIN}
    res = {"pred_chains": {c: len(v) for c, v in pca.items()}, "model": os.path.basename(cif)}
    if not pcy or not ccy:
        res["error"] = "no CypA chain identified"; print(json.dumps(res, indent=2)); return
    pcyc, pkc = max(pcy.values(), key=len), max(pk.values(), key=len)

    best, bestT = None, None
    for cc, cv in ccy.items():
        n = min(len(pcyc), len(cv)); T = kab(xyz(pcyc, n), xyz(cv, n))
        cyr = float(np.sqrt(((T(xyz(pcyc, n)) - xyz(cv, n)) ** 2).sum(1).mean()))
        kr = min(float(np.sqrt(((T(xyz(pkc, min(len(pkc), len(kv)))) - xyz(kv, min(len(pkc), len(kv)))) ** 2).sum(1).mean()))
                 for kv in ck.values())
        cand = {"matched_cypa_chain": cc, "cypa_ca_rmsd": round(cyr, 2), "kras_ca_rmsd": round(kr, 2)}
        if best is None or kr < best["kras_ca_rmsd"]:
            best, bestT = cand, T

    lig = None
    try:
        signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TO())); signal.alarm(60)
        from spyrmsd import rmsd as sr
        from spyrmsd.molecule import Molecule
        pm, cm = ligmols(cif, largest=True), ligmols(CRYST, only=LIG)
        vals = []
        for cl in cm:
            a = Molecule.from_rdkit(cl); a.strip()
            b = Molecule.from_rdkit(pm[0]); b.strip()
            bx = bestT(np.asarray(b.coordinates, float))
            vals.append(float(sr.symmrmsd(np.asarray(a.coordinates, float), bx,
                                          a.atomicnums, b.atomicnums, a.adjacency_matrix, b.adjacency_matrix)))
        signal.alarm(0)
        lig = round(min(vals), 2) if vals else None
    except TO:
        lig = "timeout>60s"
    except Exception as e:
        lig = f"err:{type(e).__name__}"
    best["ligand_rmsd"] = lig
    res.update(best)
    try:
        score_files = sorted(glob.glob(os.path.join(PRED, "scores.model_idx_*.npz")))
        score_files.extend(sorted(glob.glob(os.path.join(HERE, "cofold_chai", "scores.model_idx_*.npz"))))
        if not score_files:
            raise FileNotFoundError("no Chai scores.model_idx_*.npz found")
        z = np.load(score_files[0])
        res["chai"] = {k: round(float(np.array(z[k]).mean()), 3) for k in z.files if np.array(z[k]).size <= 6}
    except Exception as e:
        res["chai_err"] = str(e)
    print(json.dumps(res, indent=2))
    with open(os.path.join(HERE, "cofold_chai", "score.json"), "w") as f:
        json.dump(res, f, indent=2)


if __name__ == "__main__":
    main()
