#!/usr/bin/env bash
# Reproduce the daraxonrasib (RMC-6236) binding-tool demo end-to-end.
#
# Deps (CPU stages 0,1,4):  gemmi numpy scipy rdkit spyrmsd  (pip)  +  smina (conda-forge, on PATH for stage 1)
# GPU stages (2,3) run on a CUDA machine; see setup_pod.sh. They are not launched here.
#
# Override the interpreter if your env isn't the default python3:
#   PYTHON=/path/to/venv/bin/python ./run.sh
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"

echo "== Stage 0: prep: fetch + split 9BG6 / 7RPZ, extract macrocycle (CPU, local) =="
"$PY" 00_fetch_and_split.py

echo "== Stage 1: docking gradient: POS / CypA / KRAS (CPU; needs smina on PATH) =="
"$PY" 01_dock.py

echo "== Stage 2-3: co-fold the ternary (GPU) =="
echo "   (CUDA)  python 02_cofold_chai.py     # -> cofold_chai/score.json   (Chai-1, MSA-free)"
echo "   (CUDA)  python 03_cofold_boltz.py    # -> cofold_boltz/            (Boltz-2 affinity, off-label)"

if [ -f cofold_chai/pred.model_idx_0.cif ] || [ -d cofold_chai/pred ]; then
  echo "== Stage 4: perturb-and-score: rigid-body KRAS sweep -> soft-vdW energy funnel (CPU, local) =="
  "$PY" 04_perturb_score.py
  "$PY" perturb/make_funnel_svg.py
else
  echo "== Stage 4 skipped: run Stage 2 first so cofold_chai/ contains a Chai prediction =="
fi

echo
echo "Done."
echo "Results: dock/results.json; cofold_chai/score.json after Stage 2; perturb/funnel.json after Stage 4"
