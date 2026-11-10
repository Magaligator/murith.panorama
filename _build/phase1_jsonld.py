# Phase 1-D : JSON-LD (dates réelles des articles, headline = H1, FuneralHome hasMap, un seul FAQPage par question)
import re, json, os, html, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
DATES = {'blog/deces-proche-suisse-10-etapes': ('2026-05-21T17:25:44+00:00', '2026-08-11T12:20:16+00:00'),
         'blog/prevoyance-funeraire-geneve': ('2026-05-23T08:10:39+00:00', '2026-06-24T16:30:18+00:00'),
         'blog/cout-rapatriement-corps': ('2026-05-23T09:00:41+00:00', '2026-06-10T16:41:47+00:00')}
MAP = 'https://www.google.ch/maps/place/Bd+de+la+Cluse+89,+1205+Gen%C3%A8ve/@46.1942832,6.1451822,17z'
n = 0
def dump(o): return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(',', ':')) + '</script>'
for lg in ['', 'en/', 'de/', 'es/', 'pt/']:
    for name, (pub, mod) in DATES.items():
        p = f'{lg}{name}.html'; s = open(p, encoding='utf-8').read()
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S); h1 = html.unescape(re.sub(r'<[^>]+>', '', h1.group(1))).strip()
        def fix(m):
            o = json.loads(m.group(1))
            if o.get('@type') == 'Article':
                o['headline'] = h1; o['datePublished'] = pub; o['dateModified'] = mod
            return dump(o)
        s2 = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)
        if s2 != s: open(p, 'w', encoding='utf-8').write(s2); n += 1
    p = f'{lg}index.html'; s = open(p, encoding='utf-8').read()
    def fix(m):
        o = json.loads(m.group(1)); t = o.get('@type')
        if t == 'FAQPage': return ''            # Phase 3 : nouvelle FAQ d'accueil ; le FAQPage reste sur /obseques
        if isinstance(t, list) and 'FuneralHome' in t:
            o['hasMap'] = MAP
            o['sameAs'] = [x for x in o.get('sameAs', []) if 'facebook.com' not in x]
        return dump(o)
    s2 = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)
    if s2 != s: open(p, 'w', encoding='utf-8').write(s2); n += 1
print('fichiers JSON-LD mis à jour :', n)
