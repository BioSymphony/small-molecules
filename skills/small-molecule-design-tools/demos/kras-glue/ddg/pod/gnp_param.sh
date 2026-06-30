#!/bin/bash
# Parameterize GppNHp (GNP): crystal coords lack H, so protonate at pH 7.4 with
# OpenBabel (this also fixes the triphosphate net charge), then GAFF2 + AM1-BCC.
set -e
cd /workspace/run
MM="/workspace/bin/micromamba run -p /workspace/md"
Q=$($MM python -c "
from openbabel import pybel
m=next(pybel.readfile('pdb','/workspace/inputs/gnp.pdb'))
m.OBMol.AddHydrogens(False, True, 7.4)
m.write('mol2','gnp_h.mol2',overwrite=True)
print(int(round(m.charge)))
" 2>gnp_protonate.log)
echo "GNP net charge at pH 7.4: $Q"
if $MM antechamber -i gnp_h.mol2 -fi mol2 -o gnp.mol2 -fo mol2 -c bcc -nc "$Q" -at gaff2 -rn GNP -pf y -dr no >gnp_antechamber.log 2>&1; then
  echo GNP_ANTECHAMBER_OK
else
  echo GNP_FAIL
  tail -25 gnp_antechamber.log
  exit 1
fi
$MM parmchk2 -i gnp.mol2 -f mol2 -o gnp.frcmod -s gaff2 && echo GNP_PARMCHK_OK
ls -la gnp.mol2 gnp.frcmod
