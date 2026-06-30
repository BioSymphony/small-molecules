#!/usr/bin/env python3
"""
Stage 2 -- co-fold the daraxonrasib . CypA . KRAS ternary with Chai-1 (GPU).

This is the FRONTIER test: can a SOTA co-folding model reproduce a 2026 molecular
glue *from sequence + SMILES alone*? Chai-1 runs MSA-FREE by default (ESM embeddings),
which removes the external MSA-server dependency -- the biggest schedule risk.

Input assembled from 00_fetch_and_split.py output (prep/9BG6/components.json):
  protein  KRAS  (chain A seq)
  protein  CypA  (chain C seq)
  ligand   daraxonrasib  (A1AHB SMILES)
  ligand   GppNHp        (GNP SMILES)   <- locks the ON state the glue requires
  ligand   Mg            [Mg+2]

Scoring vs crystal 9BG6 (the answer key). 9BG6 has TWO ternary assemblies, so we
brute-force the pairing: superpose predicted CypA onto each crystal CypA chain and
keep the assembly that best matches, reporting:
  - CypA-Calpha RMSD (the superposition quality)
  - KRAS-Calpha RMSD in that frame   <- did it get the ternary ARRANGEMENT (headline)
  - ligand heavy-atom RMSD in that frame (spyrmsd, symmetric) <- did the drug land right

Honest expectation: glues are hard. Chai may fold each chain well yet misplace the
relative arrangement and/or the ligand. EITHER result is the deliverable.

Deps: chai_lab (pip), torch+CUDA, rdkit, gemmi, numpy, spyrmsd.
"""
import json, os, subprocess, sys, glob, shutil
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PREP = os.path.join(HERE, "prep", "9BG6")
OUT = os.path.join(HERE, "cofold_chai"); os.makedirs(OUT, exist_ok=True)
KRAS_CHAIN, CYPA_CHAIN = "A", "C"   # which crystal chains to pull SEQUENCES from for the fasta
LIG_CODE = "A1AHB"
KRAS_MIN_LEN = 166                  # KRAS ~168/169, CypA ~164 -> clean split


def load_inventory():
    with open(os.path.join(PREP, "components.json")) as f:
        return json.load(f)


def write_fasta(inv, path):
    seqs = {p["chain"]: p["seq"] for p in inv["proteins"]}
    sm = inv["smiles"]
    recs = [
        ("protein|name=KRAS", seqs[KRAS_CHAIN]),
        ("protein|name=CypA", seqs[CYPA_CHAIN]),
        ("ligand|name=daraxonrasib", sm["A1AHB"]["smiles"]),
        ("ligand|name=GppNHp", sm["GNP"]["smiles"]),
        ("ligand|name=Mg", "[Mg+2]"),
    ]
    with open(path, "w") as f:
        for h, s in recs:
            f.write(f">{h}\n{s}\n")
    print(f"  wrote {path}: KRAS({len(seqs[KRAS_CHAIN])}) + CypA({len(seqs[CYPA_CHAIN])}) + A1AHB + GppNHp + Mg")
    return path


def run_chai(fasta, outdir):
    cmd = ["chai-lab", "fold", fasta, outdir]   # MSA-free is the default
    print("  $ " + " ".join(cmd))
    return subprocess.run(cmd).returncode


# ---------- scoring ----------
def kabsch(P, Q):
    Pc, Qc = P.mean(0), Q.mean(0)
    H = (P - Pc).T @ (Q - Qc)
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    return lambda X: (X - Pc) @ R.T + Qc


def ca_coords(struct_path):
    import gemmi
    st = gemmi.read_structure(struct_path); st.setup_entities()
    out = {}
    for chain in st[0]:
        for res in chain:
            tab = gemmi.find_tabulated_residue(res.name)
            if not (tab and tab.is_amino_acid()):
                continue
            ca = res.find_atom("CA", "*")
            if ca is not None:
                out.setdefault(chain.name, []).append((res.seqid.num, [ca.pos.x, ca.pos.y, ca.pos.z]))
    return {c: sorted(v) for c, v in out.items()}


def split_chains(ca):
    kras = {c: v for c, v in ca.items() if len(v) >= KRAS_MIN_LEN}
    cypa = {c: v for c, v in ca.items() if len(v) < KRAS_MIN_LEN}
    return kras, cypa


def ordered_xyz(reslist, n):
    return np.array([p[1] for p in reslist[:n]])


def ca_rmsd(T, P_res, Q_res):
    n = min(len(P_res), len(Q_res))
    return float(np.sqrt(((T(ordered_xyz(P_res, n)) - ordered_xyz(Q_res, n)) ** 2).sum(1).mean()))


def ligand_mols(path, only_name=None, largest=False):
    import gemmi
    from rdkit import Chem
    st = gemmi.read_structure(path); st.setup_entities(); st.remove_waters()
    residues = []
    for chain in st[0]:
        for res in chain.get_ligands():
            if only_name and res.name != only_name:
                continue
            residues.append(res)
    if largest and residues:
        residues = [max(residues, key=lambda r: len(r))]
    mols = []
    for res in residues:
        out = gemmi.Structure(); m = gemmi.Model("1"); ch = gemmi.Chain("L")
        ch.add_residue(res); m.add_chain(ch); out.add_model(m); out.setup_entities()
        mol = Chem.MolFromPDBBlock(out.make_pdb_string(), proximityBonding=True, removeHs=True, sanitize=False)
        if mol is not None and mol.GetNumAtoms() > 3:
            mols.append(mol)
    return mols


def sym_lig_rmsd(cryst_mol, pred_mol, T):
    from spyrmsd import rmsd as sr
    from spyrmsd.molecule import Molecule
    a = Molecule.from_rdkit(cryst_mol); a.strip()
    b = Molecule.from_rdkit(pred_mol); b.strip()
    bxyz = T(np.asarray(b.coordinates, float))
    return float(sr.symmrmsd(np.asarray(a.coordinates, float), bxyz,
                             a.atomicnums, b.atomicnums, a.adjacency_matrix, b.adjacency_matrix))


def score(pred_cif, outdir):
    cryst = os.path.join(PREP, "9BG6.cif")
    pred_ca, cryst_ca = ca_coords(pred_cif), ca_coords(cryst)
    p_kras, p_cypa = split_chains(pred_ca)
    c_kras, c_cypa = split_chains(cryst_ca)
    res = {"pred_chains": {c: len(v) for c, v in pred_ca.items()}}
    if not p_cypa or not c_cypa:
        res["error"] = "could not identify CypA chain"; return res
    pcypa = max(p_cypa.values(), key=len)
    pkras = max(p_kras.values(), key=len) if p_kras else None
    pred_lig = ligand_mols(pred_cif, largest=True)
    cryst_lig = ligand_mols(cryst, only_name=LIG_CODE)

    best = None
    for cc, ccoords in c_cypa.items():
        n = min(len(pcypa), len(ccoords))
        T = kabsch(ordered_xyz(pcypa, n), ordered_xyz(ccoords, n))
        cypa_rmsd = float(np.sqrt(((T(ordered_xyz(pcypa, n)) - ordered_xyz(ccoords, n)) ** 2).sum(1).mean()))
        kras_rmsd = min((ca_rmsd(T, pkras, kk) for kk in c_kras.values()), default=None) if pkras else None
        lig_rmsd = None
        if pred_lig and cryst_lig:
            vals = []
            for cl in cryst_lig:
                try:
                    vals.append(sym_lig_rmsd(cl, pred_lig[0], T))
                except Exception as e:
                    res.setdefault("lig_errors", []).append(str(e))
            lig_rmsd = min(vals) if vals else None
        cand = {"matched_cypa_chain": cc, "cypa_ca_rmsd": round(cypa_rmsd, 2),
                "kras_ca_rmsd": round(kras_rmsd, 2) if kras_rmsd is not None else None,
                "ligand_rmsd": round(lig_rmsd, 2) if lig_rmsd is not None else None}
        if best is None or (kras_rmsd is not None and kras_rmsd < (best["kras_ca_rmsd"] or 1e9)):
            best = cand
    res.update(best or {})
    with open(os.path.join(outdir, "score.json"), "w") as f:
        json.dump(res, f, indent=2)
    return res


def main():
    inv = load_inventory()
    PRED = os.path.join(OUT, "pred")
    fasta = write_fasta(inv, os.path.join(OUT, "ternary.fasta"))
    if "--score-only" not in sys.argv:
        if os.path.exists(PRED):
            shutil.rmtree(PRED)
        rc = run_chai(fasta, PRED)
        if rc != 0:
            print(f"!! chai-lab failed rc={rc}"); sys.exit(rc)
    cifs = sorted(glob.glob(os.path.join(PRED, "**", "*.cif"), recursive=True))
    cifs.extend(sorted(glob.glob(os.path.join(OUT, "pred.model_idx_*.cif"))))
    cifs = [c for c in cifs if "9BG6" not in os.path.basename(c)]
    if not cifs:
        print("!! no predicted cif found; inspect", OUT); sys.exit(1)
    pred = cifs[0]
    print(f"  scoring predicted model: {pred}  ({len(cifs)} models)")
    res = score(pred, OUT)
    print(json.dumps(res, indent=2))
    print("\nReads as:")
    print("  ligand_rmsd + kras_ca_rmsd both small -> co-folding RECOVERED the glue ternary")
    print("  proteins fold but kras_ca_rmsd large   -> right chains, WRONG arrangement (typical glue failure)")


if __name__ == "__main__":
    main()
