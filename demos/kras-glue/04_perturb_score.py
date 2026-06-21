#!/usr/bin/env python3
"""
04_perturb_score.py  —  the constructive half of the KRAS-glue demo.

The negative result (01_dock, 02_cofold) showed that neither binary docking nor
MSA-free co-folding can *find* the KRAS engagement of the daraxonrasib glue: the
KRAS surface only becomes a binding site once the drug*CypA composite is formed,
so there is no pocket for a search to fall into.

This stage asks the complementary question: if you stop trying to *predict* the
assembly and instead *score perturbations on the experimental scaffold*, is the
energy landscape actually correct?  We hold the CypA*drug composite fixed (the
"presenter + glue" — the real binder, per the mechanism), rigid-body displace
KRAS away from its crystal pose across a 0->~28 A Ca-RMSD spread, and score the
KRAS <-> (CypA*drug) interface at every decoy with a transparent soft van der
Waals / clash energy.  If the crystal pose sits at the funnel minimum, then the
scoring landscape is right and only the *search* fails for glues  ->  the
productive workflow is perturb-and-score on a crystal scaffold, not de-novo
prediction.

We also drop the actual Chai-1 prediction onto the same funnel (by superposing
predicted CypA onto crystal CypA) so you can see exactly where it landed.

Light by design: numpy + scipy.cKDTree on a ~5k-atom complex.  No GPU, no MM
force field, peak RAM a few hundred MB.  Reuses the /tmp/kras-demo-venv interp.
"""
import os, glob, json, numpy as np
import gemmi
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
CRYS = os.path.join(HERE, "prep", "9BG6", "9BG6.cif")
PRED_CANDIDATES = [
    os.path.join(HERE, "cofold_chai", "pred.model_idx_0.cif"),
    *glob.glob(os.path.join(HERE, "cofold_chai", "pred", "**", "pred.model_idx_*.cif"), recursive=True),
]
OUT  = os.path.join(HERE, "perturb")
DEC  = os.path.join(OUT, "decoys")
os.makedirs(DEC, exist_ok=True)

# --- native ternary assembly (confirmed by 9BG6 chain/ligand geometry) ---
# KRAS = chain A ; CypA = chain D ; drug A1AHB 201 sits in D and bridges to A.
KRAS_CH, CYPA_CH, DRUG = "A", "D", ("A1AHB", 201)

# Bondi van der Waals radii (heavy atoms only); generic fallback 1.70.
VDW = {"C":1.70,"N":1.55,"O":1.52,"S":1.80,"P":1.80,"F":1.47,
       "CL":1.75,"BR":1.85,"I":1.98,"MG":1.73,"NA":2.27,"ZN":1.39}
EPS  = 0.10          # kcal/mol well depth (uniform, transparent)
CUT  = 8.0           # A, interface energy cutoff
CCUT = 4.5           # A, native-contact definition
CLAMP= 0.75          # repulsion clamp at r = CLAMP * r0 (bounds clash spikes)

def vdw(el): return VDW.get(el.upper(), 1.70)

def heavy_atoms(model, chain, hetres=None, polymer_only=True):
    """Return (coords Nx3, elements list, meta list, ca_index list).
    If hetres=(resname,seqid) given, take only that residue; else the polymer."""
    xyz, els, meta, ca = [], [], [], []
    for ch in model:
        if ch.name != chain: continue
        for res in ch:
            if hetres is not None:
                if not (res.name == hetres[0] and res.seqid.num == hetres[1]):
                    continue
            else:
                if polymer_only and res.het_flag == "H":
                    continue
            seen = set()                                  # dedupe alt-conf atoms
            for a in res:
                if a.is_hydrogen() or a.element.name in ("H", ""): continue
                nm = a.name.strip()
                if nm == "" or nm in seen: continue       # keep first conformer
                seen.add(nm)
                xyz.append(a.pos.tolist()); els.append(a.element.name)
                meta.append((ch.name, res.name, res.seqid.num, nm))
                if nm == "CA" and a.element.name == "C" and hetres is None:
                    ca.append(len(xyz)-1)
    return np.array(xyz, float), els, meta, np.array(ca, int)

def rotmat(axis, ang):
    axis = axis/ (np.linalg.norm(axis)+1e-12)
    x,y,z = axis; c=np.cos(ang); s=np.sin(ang); C=1-c
    return np.array([[c+x*x*C, x*y*C-z*s, x*z*C+y*s],
                     [y*x*C+z*s, c+y*y*C, y*z*C-x*s],
                     [z*x*C-y*s, z*y*C+x*s, c+z*z*C]])

def kabsch(P, Q):
    """Rigid R,t mapping P onto Q (least squares)."""
    Pc, Qc = P.mean(0), Q.mean(0)
    H = (P-Pc).T @ (Q-Qc)
    U,S,Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1,1,d]) @ U.T
    return R, Qc - R@Pc

# ---------- load native scaffold ----------
st = gemmi.read_structure(CRYS); st.setup_entities(); m = st[0]
kP,  kEl,  kMeta,  kCA  = heavy_atoms(m, KRAS_CH)                 # KRAS (mobile)
cP,  cEl,  cMeta,  _    = heavy_atoms(m, CYPA_CH)                 # CypA
dP,  dEl,  dMeta,  _    = heavy_atoms(m, CYPA_CH, hetres=DRUG)    # drug
qP   = np.vstack([cP, dP])                                       # composite (fixed)
qR   = np.array([vdw(e) for e in cEl+dEl])
kR   = np.array([vdw(e) for e in kEl])
print(f"KRAS heavy {len(kP)} (CA {len(kCA)}) | CypA {len(cP)} | drug {len(dP)} | composite {len(qP)}")

treeQ = cKDTree(qP)

def interface_energy(P):
    """Soft-LJ inter-partner energy between mobile P (KRAS) and fixed composite."""
    nb = treeQ.query_ball_point(P, CUT)
    e = 0.0
    for i, js in enumerate(nb):
        if not js: continue
        js = np.array(js)
        r  = np.linalg.norm(qP[js] - P[i], axis=1)
        r0 = qR[js] + kR[i]
        r  = np.maximum(r, CLAMP*r0)
        sg = r0 / 2**(1/6)
        ratio = sg / r
        e += np.sum(4*EPS*(ratio**12 - ratio**6))
    return float(e)

def native_contact_set(P):
    nb = treeQ.query_ball_point(P, CCUT)
    s = set()
    for i, js in enumerate(nb):
        for j in js: s.add((i, j))
    return s

NATIVE_CONTACTS = native_contact_set(kP)
def frac_contacts(P):
    nb = treeQ.query_ball_point(P, CCUT)
    cur = set()
    for i, js in enumerate(nb):
        for j in js: cur.add((i, j))
    if not NATIVE_CONTACTS: return 0.0
    return len(cur & NATIVE_CONTACTS) / len(NATIVE_CONTACTS)

native_ca = kP[kCA]
c0 = native_ca.mean(0)
e_native = interface_energy(kP)
print(f"native interface soft-LJ energy = {e_native:.1f} kcal/mol  ({len(NATIVE_CONTACTS)} contacts)")

def caRMSD(P): return float(np.sqrt(((P[kCA]-native_ca)**2).sum(1).mean()))

def chai_iptm():
    score_path = os.path.join(HERE, "cofold_chai", "score.json")
    try:
        data = json.load(open(score_path))
        return data.get("chai", {}).get("iptm")
    except Exception:
        return None

# ---------- generate decoys (rigid-body KRAS moves) ----------
rng = np.random.default_rng(0)
rows = [{"rmsd":0.0, "e":e_native, "frac":1.0, "tag":"native"}]
reps = {0.0:(kP.copy(),"native")}   # representative structures to dump
N_FAR, N_NEAR = 520, 120
def make(P, ang, tmag):
    axis = rng.normal(size=3); tdir = rng.normal(size=3); tdir/= (np.linalg.norm(tdir)+1e-12)
    R = rotmat(axis, np.deg2rad(ang))
    return (P - c0) @ R.T + c0 + tdir*tmag
for _ in range(N_FAR):
    P = make(kP, rng.uniform(0,150), rng.uniform(0,22))
    rows.append({"rmsd":caRMSD(P), "e":interface_energy(P), "frac":frac_contacts(P), "tag":"decoy", "_P":P})
for _ in range(N_NEAR):                              # densify the funnel bottom
    P = make(kP, rng.uniform(0,25), rng.uniform(0,5))
    rows.append({"rmsd":caRMSD(P), "e":interface_energy(P), "frac":frac_contacts(P), "tag":"decoy", "_P":P})

# pick representatives nearest target RMSDs for an optional 3D ladder
for target in (5.0, 10.0, 15.0, 23.0):
    best = min((r for r in rows if r["tag"]=="decoy"), key=lambda r: abs(r["rmsd"]-target))
    reps[target] = (best["_P"], f"d{int(target):02d}")

# ---------- place the actual Chai-1 prediction on the funnel ----------
chai = None
try:
    pred_path = next((p for p in PRED_CANDIDATES if os.path.exists(p)), None)
    if pred_path is None:
        raise FileNotFoundError("no Chai prediction found under cofold_chai/")
    ps = gemmi.read_structure(pred_path); ps.setup_entities(); pm = ps[0]
    # pred chains: A=KRAS(168), B=CypA(164) per score.json
    pk, pkEl, pkMeta, pkCA = heavy_atoms(pm, "A")
    pc, pcEl, pcMeta, pcCA = heavy_atoms(pm, "B")
    # CA lists ordered by residue number, paired by position (mirrors score_now.py:
    # pred/crystal have offset numbering but identical residue order, so position-
    # pairing is correct and equal-seqid pairing is not)
    def ca_sorted(P, meta, ca_idx):
        return np.array([c for _,c in sorted(((meta[i][2], P[i]) for i in ca_idx),
                                             key=lambda z: z[0])])
    cryst_cypa = ca_sorted(cP, cMeta, [i for i,mt in enumerate(cMeta) if mt[3]=="CA"])
    pred_cypa  = ca_sorted(pc, pcMeta, list(pcCA))
    cryst_kras = ca_sorted(kP, kMeta, list(kCA))
    pred_kras  = ca_sorted(pk, pkMeta, list(pkCA))
    nC = min(len(pred_cypa), len(cryst_cypa))
    R,t = kabsch(pred_cypa[:nC], cryst_cypa[:nC])
    pk_moved = (pk @ R.T) + t
    cypa_fit = float(np.sqrt((((pred_cypa[:nC]@R.T)+t - cryst_cypa[:nC])**2).sum(1).mean()))
    nK = min(len(pred_kras), len(cryst_kras))
    Pk = (pred_kras[:nK] @ R.T) + t
    chai_rmsd = float(np.sqrt(((Pk - cryst_kras[:nK])**2).sum(1).mean()))
    chai_e = interface_energy(pk_moved)
    chai = {"rmsd":chai_rmsd, "e":chai_e, "cypa_fit":cypa_fit, "iptm":chai_iptm(),
            "n_cypa":nC, "n_kras":nK}
    reps[round(chai_rmsd,1)] = (pk_moved, "chai")
    print(f"Chai-1 placed: CypA fit {cypa_fit:.2f} A | KRAS Ca-RMSD {chai_rmsd:.1f} A | interface E {chai_e:.1f}")
except Exception as ex:
    print("Chai placement skipped:", ex)

# ---------- summary stats ----------
dec = [r for r in rows if r["tag"]=="decoy"]
emin = min(rows, key=lambda r: r["e"])
near = [r for r in rows if r["rmsd"]<=12]
from numpy import corrcoef
sp = float(corrcoef([r["rmsd"] for r in near],[r["e"] for r in near])[0,1])
# funnel envelope: min energy per 1.5 A bin
bins = {}
for r in rows:
    b = round(r["rmsd"]/1.5)*1.5
    bins[b] = min(bins.get(b, 1e9), r["e"])
env = sorted(bins.items())
print(f"global-min decoy energy {emin['e']:.1f} at RMSD {emin['rmsd']:.2f} A "
      f"(native={e_native:.1f}; native is global min: {e_native<=emin['e']+1e-6 or emin['rmsd']<1.0})")
print(f"energy-vs-RMSD corr (<=12 A) = {sp:+.2f}  (positive = funnel)")

# ---------- write outputs ----------
def write_pdb(path, P, El, Meta, extraP=None, extraEl=None, extraMeta=None, extra_chain="Z"):
    lines=[]; sn=0
    def emit(xyz, els, meta, chov=None):
        nonlocal sn
        for (x,y,z),el,mt in zip(xyz, els, meta):
            sn+=1; ch = chov or mt[0]
            lines.append(f"ATOM  {sn:5d} {mt[3]:<4.4s}{mt[1]:>3.3s} {ch}{mt[2]%10000:4d}    "
                         f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00          {el:>2.2s}")
    emit(P, El, Meta)
    if extraP is not None: emit(extraP, extraEl, extraMeta)
    lines.append("END")
    open(path,"w").write("\n".join(lines)+"\n")

# representative decoy PDBs (KRAS pose + fixed composite) for the 3D ladder
comb_extraP = np.vstack([cP, dP]); comb_extraEl = cEl+dEl; comb_extraMeta = cMeta+dMeta
for rmsd_key,(P,name) in reps.items():
    write_pdb(os.path.join(DEC, f"{name}.pdb"), P, kEl, kMeta,
              extraP=comb_extraP, extraEl=comb_extraEl, extraMeta=comb_extraMeta)

funnel = {
    "scorer": {"type":"soft-LJ (12-6) inter-partner interface energy",
               "eps_kcal":EPS, "vdw":"Bondi heavy-atom", "cutoff_A":CUT,
               "contact_cutoff_A":CCUT, "repulsion_clamp":CLAMP,
               "note":"composite (CypA chain D + drug A1AHB) held fixed; KRAS chain A rigid-body displaced"},
    "native": {"e":e_native, "contacts":len(NATIVE_CONTACTS)},
    "chai": chai,
    "stats": {"n_decoys":len(dec), "min_decoy_e":emin["e"], "min_decoy_rmsd":emin["rmsd"],
              "native_is_global_min": bool(e_native <= emin["e"]+1e-6 or emin["rmsd"]<1.0),
              "corr_e_rmsd_le12": sp},
    "envelope": [{"rmsd":b,"e":e} for b,e in env],
    "decoys": [{"rmsd":round(r["rmsd"],2),"e":round(r["e"],2),"frac":round(r["frac"],3)} for r in rows],
}
json.dump(funnel, open(os.path.join(OUT,"funnel.json"),"w"), indent=1)
print("wrote", os.path.join(OUT,"funnel.json"), "and", len(reps), "representative decoy PDBs")
