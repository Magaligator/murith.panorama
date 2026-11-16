import json, sys, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import *
units = {}   # chaîne FR -> catégorie
for rel in fr_pages():
    s = soup_of(ROOT / rel)
    for r in unit_roots(s):
        t, els = serialize(r)
        if t and LET.search(re.sub(r'\{/?x?\d+\}', '', t)): units.setdefault(t, 'u')
    for el, a, v in attr_items(s): units.setdefault(re.sub(r'\s+', ' ', v).strip(), 'a')
    for sc in s.find_all('script', type='application/ld+json'):
        try: j = json.loads(sc.string)
        except Exception: continue
        for v in json_strings(j): units.setdefault(v.strip(), 'j')
out = pathlib.Path(sys.argv[1]); out.write_text(json.dumps(units, ensure_ascii=False, indent=0), encoding='utf8')
print(len(units), sum(len(k) for k in units), {c: sum(1 for v in units.values() if v == c) for c in 'uaj'})
