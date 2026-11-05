#!/usr/bin/env python3
"""Run the finite reproducibility suite; this is not a formal proof checker."""
from pathlib import Path
import hashlib,json,subprocess,sys,time
if sys.version_info<(3,10):raise SystemExit('Python 3.10 or newer is required.')
if not __debug__:raise SystemExit('Assertions must be enabled; do not use python -O.')
root=Path(__file__).resolve().parent
out=root/'verification';logs=out/'logs';logs.mkdir(parents=True,exist_ok=True)
programs=['check_arithmetic.py','check_local_identities.py','check_entropy_transfer.py',
          'upstream_container_engine.py','check_nonlocal_replay.py','check_nonvacuous_budget.py']
results=[]
for name in programs:
 path=root/'code'/name
 args=[sys.executable,str(path)]
 if name=='check_local_identities.py':args+=['--output',str(root/'code'/'local_identities_results.json')]
 t=time.monotonic()
 with (logs/(name+'.log')).open('w') as log:
  p=subprocess.run(args,cwd=root,stdout=log,stderr=subprocess.STDOUT)
 record={'program':name,'status':'PASS' if p.returncode==0 else 'FAIL','returncode':p.returncode,
         'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'elapsed_seconds':round(time.monotonic()-t,3)}
 results.append(record);print(record['status'],name,flush=True)
 if p.returncode:break
result={'status':'PASS' if len(results)==len(programs) and all(x['returncode']==0 for x in results) else 'FAIL',
        'python':sys.version,'scope':'Finite identities, algorithm invariants, replay and entropy diagnostics. Not formal verification of the infinite theorem.',
        'programs':results}
(out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
if result['status']!='PASS':raise SystemExit(1)
print('All finite checks passed. This does not replace the mathematical proof.')
