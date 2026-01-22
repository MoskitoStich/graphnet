#!/bin/bash

# 1. Alte Pfade löschen
unset PYTHONPATH
unset PATH

# 2. IceCube Basis laden
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/setup.sh`

# 3. Deine Umgebung DAVOR schalten (Damit er dein PyTorch nimmt, nicht das alte)
# ACHTUNG: Pfad muss genau stimmen!
VENV_SITE="/data/user/efischer/graphnet/graphnet_venv/lib/python3.11/site-packages"
export PYTHONPATH=$VENV_SITE:$PYTHONPATH

# Venv aktivieren
source /data/user/efischer/graphnet/graphnet_venv/bin/activate

# 4. Info ausgeben
echo "Starte mit PYTHONPATH: $PYTHONPATH"

# 5. Den Befehl IN DER ICETRAY-UMGEBUNG ausführen
exec /cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/RHEL_7_x86_64/metaprojects/icetray/v1.9.2/env-shell.sh python "$@"