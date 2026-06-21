#!/usr/bin/env bash
# Pod bootstrap for the GPU co-folding step (Stage 2/3).
# Target: a CUDA GPU pod, >=24 GB VRAM (L40S 48GB or A100 80GB recommended),
# on a runpod/pytorch:* image (CUDA torch preinstalled).
#
# Chai-1 runs MSA-FREE by default -> no external MSA server needed (de-risked).
# Boltz-2 (stretch, adds an affinity number) DOES need --use_msa_server.
set -euo pipefail

echo "=== GPU ==="
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader || echo "no nvidia-smi"

echo "=== Chai-1 into system python (reuses preinstalled CUDA torch) ==="
pip install --upgrade pip >/dev/null
pip install chai_lab rdkit gemmi spyrmsd numpy scipy
python - <<'PY'
import torch, chai_lab
print("chai_lab OK | torch", torch.__version__, "| cuda", torch.cuda.is_available(),
      "|", (torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"))
PY

echo
echo "Chai-1 ready. First fold downloads weights (~few GB) to ~/.chai once."
echo "Run:  python 02_cofold_chai.py        # assembles ternary.fasta, folds, scores vs 9BG6"
echo
cat <<'NOTE'
--- Boltz-2 (optional / stretch: adds a predicted affinity) -------------------
Isolated venv to avoid dep clashes with chai_lab:
  pip install uv
  uv venv /opt/boltz --python 3.11
  uv pip install --python /opt/boltz/bin/python boltz rdkit gemmi spyrmsd numpy
  /opt/boltz/bin/python 03_cofold_boltz.py     # needs network for --use_msa_server

--- Docking on the pod (only if NOT run locally) ------------------------------
  apt-get update && apt-get install -y openbabel
  pip install meeko
  # smina static linux binary:
  curl -L -o /usr/local/bin/smina \
    https://sourceforge.net/projects/smina/files/smina.static/download
  chmod +x /usr/local/bin/smina
  python 01_dock.py
NOTE