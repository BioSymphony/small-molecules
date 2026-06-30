#!/bin/bash
# Drug A1AHB: Gasteiger charges + GAFF2. AM1-BCC stalls on the 116-atom macrocycle's
# default geometry optimization; Gasteiger is robust, and since the drug is identical
# across all six systems its charges cancel in the *relative* ddG.
set -e
cd /workspace/run
MM="/workspace/bin/micromamba run -p /workspace/md"
$MM antechamber -i /workspace/inputs/drug.sdf -fi sdf -o drug.mol2 -fo mol2 \
   -c gas -nc 0 -at gaff2 -rn DRG -pf y -dr no
$MM parmchk2 -i drug.mol2 -f mol2 -o drug.frcmod -s gaff2
echo "DRUG_OK"; ls -la drug.mol2 drug.frcmod
