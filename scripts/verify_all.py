#!/usr/bin/env python3
"""Run every chapter's numerical checks; fail if any script fails."""
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
results = {}
for script in sorted((root / 'scripts').glob('verify_*.py')):
    if script.name == Path(__file__).name:
        continue
    run = subprocess.run([sys.executable, str(script)], cwd=root, capture_output=True, text=True)
    if run.returncode:
        sys.stderr.write(run.stderr + run.stdout)
        raise SystemExit(f'{script.name} failed with exit code {run.returncode}')
    results[script.name] = json.loads(run.stdout)
print(json.dumps({'status': 'PASS', 'checks': len(results), 'results': results}, ensure_ascii=False, indent=2))
