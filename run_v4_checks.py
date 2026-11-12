#!/usr/bin/env python3
"""Run v4 finite checks. These supplement, not replace, the proofs."""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys

if sys.version_info < (3, 10) or not __debug__:
    raise SystemExit('Requires Python >=3.10 with assertions enabled.')
try:
    import numpy
except ImportError:
    raise SystemExit('Install the verification dependency: python -m pip install -r requirements-checks.txt')

root = Path(__file__).resolve().parent
out = root / 'verification' / 'v4'
out.mkdir(parents=True, exist_ok=True)
results = []
for name in ['generalized', 'capacity', 'coding', 'generic', 'circle']:
    path = root / 'code' / 'v4' / name / 'check.py'
    run = subprocess.run([sys.executable, str(path)], cwd=root,
                         capture_output=True, text=True)
    log = (run.stdout + run.stderr).replace(str(root) + '/', '')
    (out / (name + '.log')).write_text(log)
    reports = []
    for report in sorted(path.parent.glob('*.json')):
        data = json.loads(report.read_text())
        target = out / (name + '_' + report.name)
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        reports.append(str(target.relative_to(root)))
    results.append({'program': str(path.relative_to(root)),
                    'returncode': run.returncode,
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'reports': reports})
    print(('PASS' if run.returncode == 0 else 'FAIL'), name, flush=True)
    if run.returncode:
        break
ok = len(results) == 5 and all(row['returncode'] == 0 for row in results)
(out / 'summary.json').write_text(json.dumps({
    'status': 'PASS' if ok else 'FAIL',
    'scope': 'Finite exact identities and finite combinatorial audits; not formal verification of dimension theorems.',
    'python': platform.python_version(), 'numpy': numpy.__version__,
    'results': results,
}, indent=2) + '\n')
raise SystemExit(0 if ok else 1)
