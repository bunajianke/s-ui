#!/usr/bin/env python3
"""Restore an install-ui.py snapshot. Does not touch S-UI or its database."""
import json
import os
from pathlib import Path
import subprocess
import sys

if os.geteuid() != 0 or len(sys.argv) != 2:
    sys.exit('Usage (root): rollback-ui.py /opt/magicnet-sui/ui/backups/SNAPSHOT')
snapshot = Path(sys.argv[1])
state = json.loads((snapshot / 'state.json').read_text())
Path(state['site']).write_bytes((snapshot / 'nginx-site').read_bytes())
include = Path(state['include'])
if (snapshot / 'nginx-include').exists():
    include.write_bytes((snapshot / 'nginx-include').read_bytes())
else:
    include.unlink(missing_ok=True)
current = Path(state['current'])
current.unlink(missing_ok=True)
if state['previous_link']:
    current.symlink_to(state['previous_link'])
subprocess.run(['nginx', '-t'], check=True)
subprocess.run(['systemctl', 'reload', 'nginx'], check=True)
print('Restored UI snapshot. S-UI and all accounts were left running.')
