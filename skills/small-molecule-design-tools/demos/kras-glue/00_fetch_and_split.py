#!/usr/bin/env python3
"""
Stage 0a -- fetch + split (CPU only; deps: gemmi, rdkit, stdlib).

Pulls each target's mmCIF from RCSB, separates protein receptor from ligand(s),
and extracts the crystallographic primary ligand as the RMSD *reference pose*
(bonds assigned from the CCD template SMILES so a 58-atom macrocycle survives
intact). No docking/GPU deps -- this runs on a laptop and on a CUDA machine identically,
so we verify the riskiest prep step for free before renting a GPU.

Targets:
  9BG6  daraxonrasib (CCD A1AHB) . KRAS G12V . CypA . GppNHp (GNP) . Mg   [glue ternary]
  7RPZ  MRTX1133 . KRAS G12D . GDP                                        [positive control]

Per target -> prep/<PDBID>/:
  <id>.cif            cached download
  receptor_apo.pdb    protein chains only
  receptor_holo.pdb   protein chains + retained cofactors (nucleotide, Mg)
  ligand_ref.sdf      primary ligand, CRYSTAL coords, CCD bond orders  <- RMSD reference
  ligand.smiles       isomeric SMILES of the primary ligand (co-fold input)
  components.json      full inventory: chains+seqs, ligands, cofactors, metals, SMILES
"""
import json, os, sys, urllib.request
from rdkit import Chem
from rdkit.Chem import AllChem
import gemmi

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "prep")

TARGETS = {
    "9BG6": {"role": "glue ternary (daraxonrasib . KRAS G12V . CypA)"},
    "7RPZ": {"role": "positive control (MRTX1133 . KRAS G12D)"},
}
# residues never treated as the "primary" ligand of interest
NUCLEOTIDES = {"GNP", "GDP", "GTP", "GSP", "ANP", "ADP", "ATP", "GCP", "GNH"}
BUFFERS = {"EDO", "GOL", "PEG", "SO4", "PO4", "ACT", "DMS", "FMT", "CL", "NA", "K", "BR", "IOD"}


def fetch(url, dest=None, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": "kras-demo-prep"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    if dest:
        with open(dest, "wb") as f:
            f.write(data)
    return data if binary else data.decode("utf-8", "replace")


def ccd_smiles(code):
    """Best isomeric SMILES for a CCD code from the RCSB chem-comp API."""
    try:
        j = json.loads(fetch(f"https://data.rcsb.org/rest/v1/core/chemcomp/{code}"))
    except Exception as e:
        return None, f"fetch failed: {e}"
    descs = j.get("pdbx_chem_comp_descriptor", []) or []
    # prefer OpenEye canonical *isomeric* SMILES, then any SMILES_CANONICAL, then any SMILES
    def pick(pred):
        for d in descs:
            if pred(d):
                return d.get("descriptor")
        return None
    s = (pick(lambda d: d.get("type") == "SMILES_CANONICAL" and d.get("program") == "OpenEye OEToolkits")
         or pick(lambda d: d.get("type") == "SMILES_CANONICAL")
         or pick(lambda d: d.get("type") == "SMILES"))
    name = (j.get("chem_comp", {}) or {}).get("name")
    return s, name


def residue_pdb_block(residue):
    """Minimal PDB string for one residue (for RDKit proximity bonding)."""
    out = gemmi.Structure()
    m = gemmi.Model("1")
    ch = gemmi.Chain("L")
    ch.add_residue(residue)
    m.add_chain(ch)
    out.add_model(m)
    out.setup_entities()
    return out.make_pdb_string()


def extract_reference(residue, template_smiles):
    """Crystal coords + CCD bond orders -> RDKit mol. Returns (mol, note)."""
    block = residue_pdb_block(residue)
    raw = Chem.MolFromPDBBlock(block, proximityBonding=True, removeHs=False, sanitize=False)
    if raw is None:
        return None, "RDKit could not read ligand PDB block"
    if not template_smiles:
        return raw, "no template SMILES -> bonds are proximity-perceived (UNRELIABLE for macrocycle)"
    templ = Chem.MolFromSmiles(template_smiles)
    if templ is None:
        return raw, "template SMILES unparseable -> proximity bonds only"
    try:
        fixed = AllChem.AssignBondOrdersFromTemplate(templ, raw)
        return fixed, "bonds assigned from CCD template (OK)"
    except Exception as e:
        return raw, f"template match FAILED ({e}) -> proximity bonds only"


def process(pdbid, meta):
    d = os.path.join(OUT, pdbid)
    os.makedirs(d, exist_ok=True)
    cif = os.path.join(d, f"{pdbid}.cif")
    if not os.path.exists(cif):
        fetch(f"https://files.rcsb.org/download/{pdbid}.cif", dest=cif, binary=True)

    st = gemmi.read_structure(cif)
    st.setup_entities()
    st.remove_alternative_conformations()
    model = st[0]

    proteins, ligands, metals, cofactors = [], [], [], []
    lig_residues = {}  # name -> gemmi residue (first instance)

    for chain in model:
        poly = chain.get_polymer()
        if len(poly) > 0:
            seq = gemmi.one_letter_code(poly.extract_sequence())
            proteins.append({"chain": chain.name, "length": len(poly), "seq": seq})
        for res in chain.get_ligands():
            natoms = len(res)
            entry = {"code": res.name, "chain": chain.name, "atoms": natoms}
            if natoms == 1 and res[0].element.is_metal:
                metals.append(entry)
            elif res.name in NUCLEOTIDES:
                cofactors.append(entry)
                lig_residues.setdefault(res.name, res)
            elif res.name in BUFFERS:
                pass  # ignore crystallization junk
            else:
                ligands.append(entry)
                lig_residues.setdefault(res.name, res)

    # primary ligand = most atoms among non-nucleotide, non-buffer, non-metal ligands
    primary = max(ligands, key=lambda x: x["atoms"]) if ligands else None

    # SMILES for every interesting component (primary + cofactors)
    smiles_map = {}
    for code in {c["code"] for c in ligands + cofactors}:
        s, nm = ccd_smiles(code)
        smiles_map[code] = {"smiles": s, "name": nm}

    # ---- write receptor (apo = protein only; holo = protein + nucleotide + Mg) ----
    apo = st.clone()
    apo.remove_ligands_and_waters()
    with open(os.path.join(d, "receptor_apo.pdb"), "w") as f:
        f.write(apo.make_pdb_string())

    holo = st.clone()
    holo.remove_waters()
    primary_code = primary["code"] if primary else None
    # drop crystallization junk and the primary ligand from holo
    for m in holo:
        for chain in m:
            for i in reversed(range(len(chain))):
                res = chain[i]
                if res.name in BUFFERS or res.name == primary_code:
                    del chain[i]
    with open(os.path.join(d, "receptor_holo.pdb"), "w") as f:
        f.write(holo.make_pdb_string())

    # ---- reference ligand pose ----
    ref_note = "no primary ligand found"
    heavy = None
    if primary:
        res = lig_residues[primary["code"]]
        templ_smiles = (smiles_map.get(primary["code"], {}) or {}).get("smiles")
        mol, ref_note = extract_reference(res, templ_smiles)
        if mol is not None:
            heavy = sum(1 for a in mol.GetAtoms() if a.GetSymbol() != "H")
            w = Chem.SDWriter(os.path.join(d, "ligand_ref.sdf"))
            mol.SetProp("_Name", f"{pdbid}_{primary['code']}")
            w.write(mol); w.close()
            if templ_smiles:
                with open(os.path.join(d, "ligand.smiles"), "w") as f:
                    f.write(f"{templ_smiles}\t{pdbid}_{primary['code']}\n")

    inventory = {
        "pdbid": pdbid, "role": meta["role"],
        "proteins": proteins, "primary_ligand": primary,
        "ligands": ligands, "cofactors": cofactors, "metals": metals,
        "smiles": smiles_map,
        "reference_pose": {"note": ref_note, "heavy_atoms": heavy},
    }
    with open(os.path.join(d, "components.json"), "w") as f:
        json.dump(inventory, f, indent=2)
    return inventory


def main():
    os.makedirs(OUT, exist_ok=True)
    for pdbid, meta in TARGETS.items():
        print(f"\n{'='*70}\n{pdbid} -- {meta['role']}\n{'='*70}")
        inv = process(pdbid, meta)
        for p in inv["proteins"]:
            tag = ("KRAS?" if "GKVKD" in p["seq"] or "YDPTIEDSY" in p["seq"]
                   else "CypA?" if "GFHRIIPGF" in p["seq"] or p["length"] < 200 and "VNPTVFFD" in p["seq"]
                   else "")
            print(f"  protein chain {p['chain']:2s}  len {p['length']:4d}  {tag}")
        pl = inv["primary_ligand"]
        print(f"  PRIMARY LIGAND : {pl['code'] if pl else None}  "
              f"atoms={pl['atoms'] if pl else '-'}  "
              f"ref_pose_heavy={inv['reference_pose']['heavy_atoms']}")
        print(f"  ref-pose status: {inv['reference_pose']['note']}")
        print(f"  cofactors      : {[c['code'] for c in inv['cofactors']]}")
        print(f"  metals         : {[m['code'] for m in inv['metals']]}")
        for code, v in inv["smiles"].items():
            s = v["smiles"]
            print(f"  SMILES[{code}]  : {(s[:60]+'...') if s and len(s)>60 else s}")
    print(f"\nWrote prep/ under {OUT}")


if __name__ == "__main__":
    main()
