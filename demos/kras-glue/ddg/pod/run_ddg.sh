#!/bin/bash
# End-to-end driver (run on the pod after MD stack installed + inputs uploaded to
# /workspace/inputs): parameterize ligands -> build mutants -> tleap assemble+split
# -> MM-GBSA per system -> collect ddG.
set -e
cd /workspace/run
MM="/workspace/bin/micromamba run -p /workspace/md"
SYS=(wt g12d g12c g12g q61h m67r)

echo "### parameterize drug (Gasteiger) + GppNHp (AM1-BCC)"
[ -f drug.frcmod ] || bash drug_param.sh
[ -f gnp.frcmod ]  || bash gnp_param.sh

echo "### build mutant KRAS+Mg PDBs"
$MM python build_systems.py

echo "### assemble + split prmtops"
bash assemble.sh "${SYS[@]}"

echo "### MM-GBSA per system"
for s in "${SYS[@]}"; do
  { [ -f "${s}.prmtop" ] && [ -f "${s}_rec.prmtop" ] && [ -f "${s}_lig.prmtop" ]; } || { echo "$s: no prmtop, skipping"; continue; }
  $MM python mmgbsa.py "$s" 2>"${s}_mmgbsa.err" | grep RESULT || { echo "$s MMGBSA FAIL"; tail -8 "${s}_mmgbsa.err"; }
done

echo "### collect ddG"
$MM python -c "
import json, glob
d={}
for f in glob.glob('*_dG.json'):
    j=json.load(open(f)); d[j['system']]=j
if 'wt' not in d:
    print('NO WT RESULT'); raise SystemExit
wt=d['wt']['dG_bind']
order=['wt','g12d','g12c','g12g','q61h','m67r']
labels={'wt':'G12V (crystal)','g12d':'G12D','g12c':'G12C','g12g':'G12 (true WT)','q61h':'Q61H','m67r':'M67R (disruptor ctrl)'}
rows=[]
print(f\"{'system':22s} {'dG_bind':>9s} {'ddG_vs_G12V':>12s}\")
for s in order:
    if s in d:
        ddg=d[s]['dG_bind']-wt
        rows.append({'system':s,'label':labels[s],'dG_bind':d[s]['dG_bind'],'ddG':round(ddg,2)})
        print(f\"{labels[s]:22s} {d[s]['dG_bind']:9.2f} {ddg:12.2f}\")
json.dump({'reference':'wt (G12V crystal)','rows':rows,'method':'single-trajectory MM-GBSA (GBn2/igb8), ff14SB+GAFF2, AM1-BCC ligands, single minimized snapshot','raw':d}, open('ddg_results.json','w'), indent=1)
print('wrote ddg_results.json')
"
