#!/bin/bash

# 1. delete old env vars to avoid conflicts
unset PYTHONPATH
unset PATH

# 2. load IceCube env
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/setup.sh`

# 3. using new pytorch version from venv
VENV_SITE="/data/user/efischer/graphnet/graphnet_venv/lib/python3.11/site-packages"
export PYTHONPATH=$VENV_SITE:$PYTHONPATH

# activate Venv 
source /data/user/efischer/graphnet/graphnet_venv/bin/activate

# 4. info output
echo "Starte mit PYTHONPATH: $PYTHONPATH"

# 5. execute the python script with the IceCube env
exec /cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/RHEL_7_x86_64/metaprojects/icetray/v1.9.2/env-shell.sh python "$@"