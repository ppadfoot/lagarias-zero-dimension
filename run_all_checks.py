#!/usr/bin/env python3
from pathlib import Path
import sys,subprocess,json,hashlib
if sys.version_info<(3,10) or not __debug__:raise SystemExit('Requires Python>=3.10 with assertions enabled.')
root=Path(__file__).resolve().parent
out=root/'verification';out.mkdir(exist_ok=True)
results=[]
programs=['run_checks.py', 'code/root_exact_linear_checks.py', 'code/check_real_transfer.py', 'code/check_affine_carries.py', 'code/check_metric_digital_rigidity.py', 'code/check_positive_density.py']
for rel in programs:
 p=root/rel
 args=[sys.executable,str(p)]
 if 'metric_digital' in rel:args+=['--proof',str(root/'paper/metric_digital_rigidity.tex'),'--output',str(out/'metric_digital_rigidity_checks.json')]
 if 'positive_density' in rel:args+=['--proof',str(root/'paper/positive_density_section.tex'),'--output',str(out/'positive_density_checks.json')]
 r=subprocess.run(args,cwd=root,capture_output=True,text=True)
 (out/(rel.replace('/','_')+'.log')).write_text(r.stdout+r.stderr)
 results.append({'program':rel,'returncode':r.returncode,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 print(('PASS' if r.returncode==0 else 'FAIL'),rel,flush=True)
 if r.returncode:break
ok=len(results)==len(programs) and all(x['returncode']==0 for x in results)
(out/'combined_summary.json').write_text(json.dumps({'status':'PASS' if ok else 'FAIL','scope':'Finite checks, not formal proof certification','results':results},indent=2)+'\n')
raise SystemExit(0 if ok else 1)
