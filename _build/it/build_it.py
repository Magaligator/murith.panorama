"""Ajoute l'italien : (1) sélecteur FR EN DE IT ES PT + hreflang IT sur toutes les pages, (2) génère it/ depuis les pages FR.
Idempotent. Usage : venv/bin/python _build/it/build_it.py"""
import json, re, sys, copy, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import *
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
class KeepOrder(HTMLFormatter):
    def attributes(self, tag): return list(tag.attrs.items())
FMT = KeepOrder()

DICT = json.load(open(ROOT / '_build/it/it_dict.json', encoding='utf8'))
LANGS = ['fr', 'en', 'de', 'es', 'pt']
ASSET = re.compile(r'^/(img|fonts|docs|style\.css|app\.js|manifest\.webmanifest|robots\.txt|sitemap\.xml|favicon)')
missing = set()

def norm(s): return re.sub(r'\s+', ' ', s).strip()

def all_pages():
    out = []
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in ('_archive-wix', '_build', '_img-src', '_src', 'docs', '.git', 'node_modules'): continue
        out.append(rel)
    return out

def write(path, soup):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(soup.decode(formatter=FMT).replace('<!DOCTYPE html>\n\n', '<!DOCTYPE html>\n', 1), encoding='utf8')

# ---------- 1) sélecteur de langue + hreflang sur les pages existantes ----------
def augment(soup):
    ch = False
    lang = soup.find(class_='lang')
    if lang and not lang.find('a', attrs={'data-l': 'it'}):
        de = lang.find('a', attrs={'data-l': 'de'})
        a = soup.new_tag('a', attrs={'data-l': 'it', 'href': de['href'].replace('/de', '/it', 1) if de['href'].startswith('/de') else de['href'], 'hreflang': 'it'})
        a.string = 'IT'
        de.insert_after(a); ch = True
    de_link = soup.find('link', rel='alternate', hreflang='de')
    if de_link and not soup.find('link', rel='alternate', hreflang='it'):
        n = soup.new_tag('link', attrs={'rel': 'alternate', 'hreflang': 'it', 'href': de_link['href'].replace('murith.ch/de', 'murith.ch/it', 1)})
        de_link.insert_after(n); ch = True
    return ch

n_aug = 0
for rel in all_pages():
    if rel.parts[0] == 'it': continue
    s = soup_of(ROOT / rel)
    if augment(s): write(ROOT / rel, s); n_aug += 1
print('pages augmentées :', n_aug)

# ---------- 2) génération de it/ ----------
def tr_unit(key):
    t = DICT.get(key)
    if t is None: missing.add(key)
    return t

def prefix_href(h):
    if not h.startswith('/') or h.startswith('//') or ASSET.match(h): return h
    if h == '/': return '/it'
    if h.startswith('/#') or h.startswith('/?'): return '/it' + h
    return '/it' + h

def to_it_url(u):
    if not u.startswith('https://www.murith.ch'): return u
    if re.search(r'#(entreprise|site)$', u) or '/img/' in u or '/docs/' in u: return u
    path = u[len('https://www.murith.ch'):]
    if path.startswith('/it'): return u
    if path in ('', '/'): return 'https://www.murith.ch/it'
    if path.startswith('/#'): return 'https://www.murith.ch/it' + path[1:]
    return 'https://www.murith.ch/it' + path

def jwalk(o, key=None):
    if isinstance(o, dict):
        if o.get('@type') == 'VideoObject': return {k: (v if k == 'inLanguage' else jwalk(v, k)) for k, v in o.items()}
        return {k: jwalk(v, k) for k, v in o.items()}
    if isinstance(o, list): return [jwalk(v, key) for v in o]
    if isinstance(o, str):
        if key == 'inLanguage': return 'it'
        if o.startswith('https://www.murith.ch'): return to_it_url(o)
        if key in JSON_KEYS and LET.search(o) and not o.startswith('http'):
            t = DICT.get(o.strip())
            if t is None: missing.add(o.strip()); return o
            return t
    return o

def build_it(rel):
    s = soup_of(ROOT / rel)
    for el in s.find_all(attrs={'data-fr-only': True}): el.decompose()
    # unités de texte
    for r in unit_roots(s):
        key, els = serialize(r)
        if not key or not LET.search(re.sub(r'\{/?x?\d+\}', '', key)): continue
        t = tr_unit(key)
        if t is None: continue
        rebuild(r, t, els, s)
    # attributs
    for el, a, v in attr_items(s):
        t = DICT.get(norm(v))
        if t is None: missing.add(norm(v)); continue
        el[a] = t
    # JSON-LD
    for sc in s.find_all('script', type='application/ld+json'):
        try: j = json.loads(sc.string)
        except Exception: continue
        sc.string = json.dumps(jwalk(j), ensure_ascii=False, separators=(',', ':'))
    # langue
    s.html['lang'] = 'it'
    for m in s.find_all('meta'):
        if m.get('property') == 'og:locale': m['content'] = 'it_CH'
        if m.get('property') == 'og:url': m['content'] = to_it_url(m['content'])
    c = s.find('link', rel='canonical')
    if c: c['href'] = to_it_url(c['href'])
    # liens internes
    for a in s.find_all('a', href=True):
        if a.get('data-l'): continue
        a['href'] = prefix_href(a['href'])
    for f in s.find_all('form', action=True): f['action'] = prefix_href(f['action'])
    # sélecteur : IT actif
    lang = s.find(class_='lang')
    if lang:
        for a in lang.find_all('a'):
            if a.get('data-l') == 'it': a['aria-current'] = 'true'
            elif a.has_attr('aria-current'): del a['aria-current']
    return s

n = 0
for rel in all_pages():
    if rel.parts[0] in LANGS[1:] or rel.parts[0] == 'it': continue
    write(ROOT / 'it' / rel, build_it(rel)); n += 1
print('pages it/ générées :', n)
log = pathlib.Path(__file__).parent / 'missing.txt'
log.write_text('\n'.join(sorted(missing)), encoding='utf8')
print('chaînes sans traduction :', len(missing))
