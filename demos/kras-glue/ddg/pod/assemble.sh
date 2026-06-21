#!/bin/bash
# Assemble each system in tleap and split into complex/receptor/ligand prmtops.
# Combine order {krasmg GNP cypa DRG} makes the ligand side (KRAS+Mg+GNP) the first
# contiguous residue block (:1-170), receptor (CypA+drug) the rest (:171-335).
set -e
cd /workspace/run
MM="/workspace/bin/micromamba run -p /workspace/md"
if [ "$#" -gt 0 ]; then
  SYS=("$@")
else
  SYS=(wt g12d g12c g12g q61h m67r)
fi
for sys in "${SYS[@]}"; do
  cat > "leap_${sys}.in" <<EOF
source leaprc.protein.ff14SB
source leaprc.gaff2
source leaprc.water.tip3p
loadamberparams frcmod.ions234lm_126_tip3p
DRG = loadmol2 drug.mol2
loadamberparams drug.frcmod
GNP = loadmol2 gnp.mol2
loadamberparams gnp.frcmod
krasmg = loadpdb ${sys}_krasmg.pdb
cypa = loadpdb /workspace/inputs/cypa.pdb
comp = combine {krasmg GNP cypa DRG}
set default PBRadii mbondi3
saveamberparm comp ${sys}.prmtop ${sys}.inpcrd
quit
EOF
  $MM tleap -f "leap_${sys}.in" > "leap_${sys}.log" 2>&1 || { echo "$sys TLEAP FAIL"; tail -20 "leap_${sys}.log"; continue; }
  if [ ! -f "${sys}.prmtop" ]; then echo "$sys NO PRMTOP"; tail -25 "leap_${sys}.log"; continue; fi
  rm -f "${sys}_com.prmtop" "${sys}_rec.prmtop" "${sys}_lig.prmtop"   # ante-MMPBSA won't overwrite
  $MM ante-MMPBSA.py -p "${sys}.prmtop" -r "${sys}_rec.prmtop" -l "${sys}_lig.prmtop" -m ":1-170" --radii=mbondi3 > "ante_${sys}.log" 2>&1 || { echo "$sys ANTE FAIL"; tail -15 "ante_${sys}.log"; continue; }
  echo "$sys OK  ($(grep -c '^ATOM\|^HETATM' "${sys}_krasmg.pdb" 2>/dev/null) krasmg atoms)"
done
