import json,sys
from .core import simulate
s=json.load(open(sys.argv[1])); print(json.dumps(simulate(s['jobs'],s.get('workers',2),s.get('starvation',10)),indent=2))
