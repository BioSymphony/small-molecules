#!/usr/bin/env python3
"""
Stage 1 -- docking gradient (CPU, smina). The empirical core of the demo.

Three docks that trace the *binary-docking boundary* the worked example claims:

  POS   6IC (MRTX1133)  -> KRAS G12D pocket      (7RPZ, chain A + GDP/Mg)
        expect: clean cognate redock, low RMSD, native contacts recovered.
        => "the docking stack works when the ligand is drug-like and the pocket is real."

  CYPA  A1AHB (daraxonrasib) -> CypA pocket alone (9BG6, CypA chain auto-picked)
        expect: cyclophilin-anchoring portion buried (CypA contacts recovered),
        RAS-facing arm unconstrained -> whole-ligand RMSD inflated.
        => "docking captures the POCKET half of a glue, not the interface half."

  KRAS  A1AHB (daraxonrasib) -> KRAS surface     (9BG6, KRAS chain auto-picked + GNP/Mg)
        expect: no canonical pocket -> weak score, contacts NOT recovered.
        => "binary docking can't model the RAS side of a glue at all."

Ligand is fed to smina as SDF (rigid macrocycle ring): classic smina/Vina cannot read
Meeko's broken-macrocycle pdbqt (CG/G pseudo-atoms), so this is a cognate "re-place the
crystal conformer" test, not full ring sampling -- stated honestly in the README.

Metrics per pose: smina affinity (kcal/mol); symmetric pose-RMSD vs crystal with NO
re-superposition (spyrmsd, graph-matched -> order-independent); native receptor-contact
recovery (receptor residues the crystal ligand touches that the docked pose reproduces).

Deps (env): smina on PATH; python with rdkit, gemmi, spyrmsd, numpy. Run after 00_*.
"""
import json, os, subprocess, sys
import numpy as np
import gemmi
from rdkit import Chem
from rdkit.Chem import AllChem

HERE = os.path.dirname(os.path.abspath(__file__))
PREP = os.path.join(HERE, "prep")
OUT = os.path.join(HERE, "dock"); os.makedirs(OUT, exist_ok=True)

# candidate receptor chains; the one the reference ligand actually contacts is auto-picked
CONFIGS = [
    {"label": "POS_MRTX1133_into_KRAS", "pdbid": "7RPZ", "candidates": ["A"], "lig": "6IC",
     "note": "positive control: drug-like inhibitor, real switch-II pocket"},
    {"label": "CYPA_daraxonrasib",      "pdbid": "9BG6", "candidates": ["C", "D"], "lig": "A1AHB",
     "note": "glue, pocket half: dock macrocycle into CypA alone"},
    {"label": "KRAS_daraxonrasib",      "pdbid": "9BG6", "candidates": ["A", "B"], "lig": "A1AHB",
     "note": "glue, interface half: dock macrocycle into KRAS alone (no pocket)"},
]
SMINA = os.environ.get("SMINA_BIN", "smina")
SMINA_EXHAUST = int(os.environ.get("SMINA_EXHAUST", "8"))
SMINA_MODES = 9


def build_receptor(pdbid, keep_chains, strip_lig, out_pdb):
    """Receptor = chosen chains, waters + the redocked ligand removed, cofactors/metals kept."""
    st = gemmi.read_structure(os.path.join(PREP, pdbid, f"{pdbid}.cif"))
    st.setup_entities(); st.remove_waters(); st.remove_alternative_conformations()
    keep = set(keep_chains)
    model = st[0]
    for chain in list(model):
        if chain.name not in keep:
            model.remove_chain(chain.name); continue
        drop = [i for i, r in enumerate(chain) if r.name == strip_lig]
        for i in reversed(drop):
            del chain[i]
    st.setup_entities()
    with open(out_pdb, "w") as f:
        f.write(st.make_pdb_string())
    return out_pdb


def receptor_atoms(pdb):
    st = gemmi.read_structure(pdb)
    coords, reskeys = [], []
    for chain in st[0]:
        for res in chain:
            for atom in res:
                if atom.element == gemmi.Element("H"):
                    continue
                coords.append([atom.pos.x, atom.pos.y, atom.pos.z])
                reskeys.append(f"{chain.name}/{res.name}{res.seqid.num}")
    return np.array(coords), np.array(reskeys)


def ligand_ref(ref_sdf):
    m = Chem.SDMolSupplier(ref_sdf, sanitize=True, removeHs=True)[0]
    conf = m.GetConformer()
    xyz = np.array([[conf.GetAtomPosition(i).x, conf.GetAtomPosition(i).y,
                     conf.GetAtomPosition(i).z] for i in range(m.GetNumAtoms())])
    return xyz, m


def prep_ligand_sdf(ref_sdf, out_sdf):
    """Add Hs onto the crystal heavy atoms (smina docks the SDF directly; rigid ring)."""
    m = Chem.SDMolSupplier(ref_sdf, sanitize=True, removeHs=True)[0]
    mh = Chem.AddHs(m, addCoords=True)
    w = Chem.SDWriter(out_sdf); w.write(mh); w.close()
    return out_sdf


def contacts(lig_xyz, rec_xyz, rec_keys, cutoff=4.0):
    if len(rec_xyz) == 0 or len(lig_xyz) == 0:
        return set()
    d = np.sqrt(((lig_xyz[:, None, :] - rec_xyz[None, :, :]) ** 2).sum(-1))
    return set(np.unique(rec_keys[(d < cutoff).any(0)]).tolist())


def box(lig_xyz, rec_xyz, pad=7.0):
    d = np.sqrt(((lig_xyz[:, None, :] - rec_xyz[None, :, :]) ** 2).sum(-1))
    contact_atoms = lig_xyz[(d < 4.5).any(1)]
    center = contact_atoms.mean(0) if len(contact_atoms) else lig_xyz.mean(0)
    size = np.clip((lig_xyz.max(0) - lig_xyz.min(0)) + 2 * pad, 18.0, 30.0)
    return center, size


def pick_chain(pdbid, candidates, lig_xyz, strip_lig, workdir):
    """Pick the candidate chain the reference ligand actually contacts most."""
    best, best_n, best_rec = candidates[0], -1, None
    for ch in candidates:
        rec = build_receptor(pdbid, [ch], strip_lig, os.path.join(workdir, f"_recep_{ch}.pdb"))
        rx, rk = receptor_atoms(rec)
        n = len(contacts(lig_xyz, rx, rk))
        if n > best_n:
            best, best_n, best_rec = ch, n, rec
    return best, best_n, best_rec


def run_smina(rec_pdb, lig_sdf, center, size, out_sdf, logf):
    cmd = [SMINA, "-r", rec_pdb, "-l", lig_sdf,
           "--center_x", f"{center[0]:.2f}", "--center_y", f"{center[1]:.2f}",
           "--center_z", f"{center[2]:.2f}",
           "--size_x", f"{size[0]:.1f}", "--size_y", f"{size[1]:.1f}", "--size_z", f"{size[2]:.1f}",
           "--exhaustiveness", str(SMINA_EXHAUST), "--num_modes", str(SMINA_MODES),
           "--seed", "42", "-o", out_sdf]
    with open(logf, "w") as lf:
        return subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT).returncode


def read_poses(out_sdf):
    """Robust read of smina output (don't trust obabel valences)."""
    supp = Chem.SDMolSupplier(out_sdf, sanitize=False, removeHs=False)
    poses = []
    for m in supp:
        if m is None:
            continue
        try:
            m.UpdatePropertyCache(strict=False); Chem.FastFindRings(m)
        except Exception:
            pass
        poses.append(m)
    return poses


def heavy_xyz(mol):
    conf = mol.GetConformer()
    idx = [a.GetIdx() for a in mol.GetAtoms() if a.GetAtomicNum() > 1]
    return np.array([[conf.GetAtomPosition(i).x, conf.GetAtomPosition(i).y,
                      conf.GetAtomPosition(i).z] for i in idx])


def sym_rmsd(ref_mol, pose_mol):
    from spyrmsd import rmsd as sr
    from spyrmsd.molecule import Molecule
    a = Molecule.from_rdkit(ref_mol); a.strip()
    b = Molecule.from_rdkit(pose_mol); b.strip()
    return float(sr.symmrmsd(a.coordinates, b.coordinates, a.atomicnums, b.atomicnums,
                             a.adjacency_matrix, b.adjacency_matrix))


def score_poses(out_sdf, ref_mol, ref_xyz, rec_xyz, rec_keys, crystal_contacts):
    rows = []
    for i, pose in enumerate(read_poses(out_sdf)):
        aff = float(pose.GetProp("minimizedAffinity")) if pose.HasProp("minimizedAffinity") else None
        pxyz = heavy_xyz(pose)
        # RMSD: symmetric graph-matched if possible, else indexed (atom order preserved from our SDF)
        rmsd = None
        try:
            rmsd = sym_rmsd(ref_mol, pose)
        except Exception:
            if pxyz.shape == ref_xyz.shape:
                rmsd = float(np.sqrt(((pxyz - ref_xyz) ** 2).sum(1).mean()))
        pc = contacts(pxyz, rec_xyz, rec_keys)
        recov = (len(pc & crystal_contacts) / len(crystal_contacts)) if crystal_contacts else None
        rows.append({"pose": i + 1, "affinity": aff, "rmsd": rmsd, "contact_recovery": recov})
    return rows


def main():
    results = {}
    for cfg in CONFIGS:
        lab = cfg["label"]
        print(f"\n{'='*72}\n{lab}\n  {cfg['note']}\n{'='*72}")
        d = os.path.join(OUT, lab); os.makedirs(d, exist_ok=True)
        ref_sdf = os.path.join(PREP, cfg["pdbid"], "ligand_ref.sdf")
        ref_xyz, ref_mol = ligand_ref(ref_sdf)

        chain, ncontact, rec_pdb = pick_chain(cfg["pdbid"], cfg["candidates"], ref_xyz, cfg["lig"], d)
        # rewrite the winning receptor to the canonical name
        rec_pdb = build_receptor(cfg["pdbid"], [chain], cfg["lig"], os.path.join(d, "receptor.pdb"))
        rec_xyz, rec_keys = receptor_atoms(rec_pdb)
        crystal_contacts = contacts(ref_xyz, rec_xyz, rec_keys)
        center, size = box(ref_xyz, rec_xyz)
        print(f"  receptor chain {chain} (auto)  atoms={len(rec_xyz)}  crystal contacts={len(crystal_contacts)} residues")
        print(f"  box center=({center[0]:.1f},{center[1]:.1f},{center[2]:.1f}) size=({size[0]:.0f},{size[1]:.0f},{size[2]:.0f})")

        lig_sdf = prep_ligand_sdf(ref_sdf, os.path.join(d, "ligand.sdf"))
        out_sdf = os.path.join(d, "docked.sdf")
        rc = run_smina(rec_pdb, lig_sdf, center, size, out_sdf, os.path.join(d, "smina.log"))
        if rc != 0 or not os.path.exists(out_sdf) or os.path.getsize(out_sdf) == 0:
            print(f"  !! smina failed (rc={rc}); see smina.log")
            results[lab] = {"error": f"smina rc={rc}"}; continue

        rows = score_poses(out_sdf, ref_mol, ref_xyz, rec_xyz, rec_keys, crystal_contacts)
        rows = [r for r in rows if r["rmsd"] is not None]
        if not rows:
            print("  !! no scorable poses"); results[lab] = {"error": "no poses"}; continue
        top = rows[0]
        best = min(rows, key=lambda r: r["rmsd"])
        print(f"  TOP pose : aff={top['affinity']:.2f} kcal/mol  RMSD={top['rmsd']:.2f} A  "
              f"contacts={top['contact_recovery']*100:.0f}%")
        print(f"  BEST RMSD: pose#{best['pose']}  RMSD={best['rmsd']:.2f} A  "
              f"contacts={best['contact_recovery']*100:.0f}%")
        results[lab] = {"note": cfg["note"], "receptor_chain": chain,
                        "crystal_contact_residues": len(crystal_contacts),
                        "top": top, "best_rmsd": best, "all_poses": rows}

    with open(os.path.join(OUT, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {os.path.join(OUT, 'results.json')}")
    print(f"\n{'test':28s} {'aff':>7s} {'RMSD_top':>9s} {'RMSD_best':>10s} {'contacts':>9s}")
    for lab, r in results.items():
        if "top" in r:
            print(f"{lab:28s} {r['top']['affinity']:7.2f} {r['top']['rmsd']:9.2f} "
                  f"{r['best_rmsd']['rmsd']:10.2f} {r['top']['contact_recovery']*100:8.0f}%")
        else:
            print(f"{lab:28s} {r.get('error','?'):>7s}")


if __name__ == "__main__":
    main()
