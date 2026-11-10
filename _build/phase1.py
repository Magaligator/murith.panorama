# PHASE 1 (A, B, C, D, E, G) — passage en production : panorama/ devient la racine, URLs propres sans .html,
# balises de base (canonical, hreflang, robots, og:url/locale), JSON-LD, sitemap, robots.txt.
# À exécuter UNE fois depuis la racine du dépôt (avant : panorama/, img/, fonts/ ; après : racine du site).
import os, re, json, subprocess, posixpath, glob, html, datetime, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = 'https://www.murith.ch'
LANGS = ['fr', 'en', 'de', 'es', 'pt']
PFX = {'fr': '', 'en': 'en', 'de': 'de', 'es': 'es', 'pt': 'pt'}
LOCALE = {'fr': 'fr_CH', 'en': 'en_GB', 'de': 'de_CH', 'es': 'es_ES', 'pt': 'pt_PT'}
HTMLLANG = {'fr': 'fr-CH', 'en': 'en', 'de': 'de-CH', 'es': 'es', 'pt': 'pt'}
# ancien nom de fichier -> nouveau slug (None = page supprimée, 301 vers /obseques)
SLUG = {'index': '', 'transports': 'transports-funeraires', 'murith-care': 'murith-care-everywhere',
        'post-etapes': 'blog/deces-proche-suisse-10-etapes', 'post-prevoyance': 'blog/prevoyance-funeraire-geneve',
        'post-rapat': 'blog/cout-rapatriement-corps', 'produits': None}

def slug(name):
    return SLUG[name] if name in SLUG else name

def url(lang, name, frag=''):
    s = slug(name)
    if s is None: s = 'obseques'
    p = '/' + PFX[lang] if PFX[lang] else ''
    path = (p + '/' + s) if s else (p or '/')
    if path == '': path = '/'
    return path + frag

def sh(*a): return subprocess.run(a, check=True, capture_output=True, text=True).stdout

# ---------- 0. restructuration ----------
OLD = {}   # nouveau chemin de fichier -> ancien chemin (pour résoudre les liens relatifs)
def move(src, dst):
    os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
    sh('git', 'mv', src, dst)

if os.path.isdir('panorama'):
    if os.path.exists('index.html'): sh('git', 'rm', '-q', 'index.html')     # redirection de maquette
    for e in sorted(os.listdir('panorama')):
        move('panorama/' + e, e)
    shutil.rmtree('panorama', ignore_errors=True)
for lg in LANGS:
    d = PFX[lg]
    for name in list(SLUG):
        src = (d + '/' if d else '') + name + '.html'
        if not os.path.exists(src): continue
        if SLUG[name] is None:
            sh('git', 'rm', '-qf', src); continue
        if name != 'index' and slug(name) != name:
            move(src, (d + '/' if d else '') + slug(name) + '.html')
# produits supprimé partout ; vérification
assert not [f for f in glob.glob('**/produits.html', recursive=True) if not f.startswith('_archive-wix')]

pages = {}   # (lang, name) -> fichier
for lg in LANGS:
    d = PFX[lg]
    for f in glob.glob((d + '/' if d else '') + '**/*.html', recursive=True) if d else glob.glob('*.html') + glob.glob('blog/*.html'):
        if not d and f.split('/')[0] in ('en', 'de', 'es', 'pt', '_archive-wix'): continue
        rel = f[len(d) + 1:] if d else f
        name = rel[:-5]
        pages[(lg, name)] = f
# noms « anciens » équivalents pour résoudre les anciens liens relatifs
NEWNAME2OLD = {v: k for k, v in SLUG.items() if v}

def old_of(name):
    return NEWNAME2OLD.get(name, name)

# ---------- 1. réécriture des liens ----------
def resolve_old(old_dir, rel):
    return posixpath.normpath(posixpath.join(old_dir, rel))

def conv(value, lang):
    """convertit une valeur d'attribut relative de l'ancienne arborescence en chemin absolu de la nouvelle"""
    v = value.strip()
    if not v or v.startswith(('http:', 'https:', 'mailto:', 'tel:', '#', 'data:', 'javascript:', '//', '/')): return value
    path, frag = (v.split('#', 1) + [''])[:2]; frag = '#' + frag if frag else ''
    q = ''
    if '?' in path: path, q = path.split('?', 1); q = '?' + q
    old_dir = 'panorama/' + PFX[lang] if PFX[lang] else 'panorama'
    r = resolve_old(old_dir, path) if path else old_dir
    if r.endswith('.html'):
        parts = r.split('/')[1:]                       # sans « panorama »
        lg = 'fr'
        if parts and parts[0] in ('en', 'de', 'es', 'pt'): lg, parts = parts[0], parts[1:]
        name = '/'.join(parts)[:-5]
        return url(lg, name, frag) + q
    if r.startswith('panorama/'): return '/' + r[len('panorama/'):] + frag + q       # style.css, app.js, docs/…
    if r.startswith(('img/', 'fonts/')): return '/' + r + frag + q
    return value

ATTR = re.compile(r'\b(href|src|poster|data-src|data-href)="([^"]*)"')
SRCSET = re.compile(r'\bsrcset="([^"]*)"')
def rewrite_links(s, lang):
    s = ATTR.sub(lambda m: f'{m.group(1)}="{conv(m.group(2), lang)}"', s)
    def ss(m):
        items = [it.strip() for it in m.group(1).split(',') if it.strip()]
        out = []
        for it in items:
            u, *w = it.split(None, 1)
            out.append(' '.join([conv(u, lang)] + w))
        return 'srcset="' + ', '.join(out) + '"'
    return SRCSET.sub(ss, s)

def clean_jsonld_urls(s):
    def f(m):
        lg = m.group(1)[:-1] if m.group(1) else 'fr'
        name = m.group(2)
        if name in ('politique-de-confidentialité',): return m.group(0)
        return BASE + url(lg, name) + (m.group(3) or '')
    return re.sub(r'https://www\.murith\.ch/((?:en|de|es|pt)/)?([a-z0-9\-]+)\.html(#[a-z]+)?', f, s)

# ---------- 2. balises de base ----------
def head_block(lang, name):
    path = url(lang, name)
    canon = BASE + path
    alts = ''
    if name != '404':
        for lg in LANGS:
            alts += f'<link rel="alternate" hreflang="{lg}" href="{BASE}{url(lg, name)}"/>'
        alts += f'<link rel="alternate" hreflang="x-default" href="{BASE}{url("fr", name)}"/>'
    robots = 'noindex,follow' if name == '404' else 'index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1'
    return f'<meta name="robots" content="{robots}"/><link rel="canonical" href="{canon}"/>{alts}<link rel="manifest" href="/manifest.webmanifest"/>'

def fix_head(s, lang, name):
    head_end = s.index('</head>')
    h, rest = s[:head_end], s[head_end:]
    h = re.sub(r'<meta[^>]*name="robots"[^>]*>', '', h)
    h = re.sub(r'<link[^>]*rel="canonical"[^>]*>', '', h)
    h = re.sub(r'<link[^>]*rel="alternate"[^>]*hreflang[^>]*>', '', h)
    h = re.sub(r'<link[^>]*hreflang[^>]*>', '', h)
    h = re.sub(r'<link[^>]*rel="manifest"[^>]*>', '', h)
    h = re.sub(r'\n{2,}', '\n', h)
    h = re.sub(r'(<meta content=")[^"]*(" property="og:url"/?>)', lambda m: m.group(1) + BASE + url(lang, name) + m.group(2), h)
    h = re.sub(r'(<meta content=")[^"]*(" property="og:locale"/?>)', lambda m: m.group(1) + LOCALE[lang] + m.group(2), h)
    h = h.rstrip() + '\n' + head_block(lang, name) + '\n'
    s = h + rest
    s = re.sub(r'<html([^>]*?) lang="[^"]*"', lambda m: f'<html{m.group(1)} lang="{HTMLLANG[lang]}"', s, count=1)
    return s

# ---------- 3. contenu technique (G) ----------
FB = re.compile(r'<li><a aria-label="Facebook" href="https://www\.facebook\.com/"[^>]*>.*?</a></li>', re.S)
def fix_content(s, lang):
    s = FB.sub('', s)
    s = re.sub(r'(<a[^>]*href=")https://www\.murith\.ch/politique-de-confidentialité(")', lambda m: m.group(1) + (('/' + PFX[lang]) if PFX[lang] else '') + '/politique-de-confidentialite' + m.group(2), s)
    s = s.replace('© 2023 créé par', '© 1888–2026 · créé par').replace('© 2023 created by', '© 1888–2026 · created by')
    s = re.sub(r'© 2023 ', '© 1888–2026 · ', s)
    return s

LOG = []
for (lg, name), f in sorted(pages.items()):
    s = open(f, encoding='utf-8').read()
    s = rewrite_links(s, lg)
    s = clean_jsonld_urls(s)
    s = fix_head(s, lg, name)
    s = fix_content(s, lg)
    open(f, 'w', encoding='utf-8').write(s)
print('pages réécrites :', len(pages))

# ---------- 4. feuille de style / scripts ----------
p = 'style.css'; s = open(p, encoding='utf-8').read()
s = s.replace('url(../fonts/', 'url(/fonts/'); open(p, 'w', encoding='utf-8').write(s)
p = 'app.js'; s = open(p, encoding='utf-8').read()
s = s.replace("var pdfBase = (lang === 'fr' ? 'docs/' : '../docs/') + 'checklist-formalites-deces-' + lang + '.pdf';", "var pdfBase = '/docs/checklist-formalites-deces-' + lang + '.pdf';")
s = s.replace("HREF = ['obseques.html', 'salons.html', 'fleurs.html'];", "HREF = ['obseques', 'salons', 'fleurs'].map(function (x) { return (lang === 'fr' ? '' : '/' + lang) + '/' + x; });")
s = s.replace("a.l[href$=\"contact.html\"]", "a.l[href$=\"/contact\"]")
s = s.replace("h.indexOf('.html') < 0) return;", "h.charAt(0) !== '/' || /\\.[a-z0-9]{2,5}($|[?#])/i.test(h)) return;")
open(p, 'w', encoding='utf-8').write(s)

# ---------- 5. manifest, robots, vercel ----------
json.dump({'name': 'A. Murith SA — Pompes funèbres Genève', 'short_name': 'Murith', 'lang': 'fr-CH', 'start_url': '/', 'display': 'standalone',
           'background_color': '#F6F8FB', 'theme_color': '#F6F8FB',
           'icons': [{'src': '/img/favicon.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': '/img/apple-touch-icon.png', 'sizes': '180x180', 'type': 'image/png'}]},
          open('manifest.webmanifest', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open('robots.txt', 'w').write('User-agent: *\nAllow: /\n\nSitemap: https://www.murith.ch/sitemap.xml\n')
vj = {'cleanUrls': True, 'trailingSlash': False,
      'redirects': [{'source': '/produits', 'destination': '/obseques', 'permanent': True}] + [{'source': f'/{l}/produits', 'destination': f'/{l}/obseques', 'permanent': True} for l in ('en', 'de', 'es', 'pt')]}
json.dump(vj, open('vercel.json', 'w'), indent=2)
open('.vercelignore', 'w').write('_archive-wix\n_build\nPLAN-SEO-MURITH.md\nINVENTAIRE-URLS.csv\nQUESTIONS-MURITH.md\nCHANGELOG-SEO.md\nREADME.md\n*.mjs\n')

# ---------- 6. sitemap ----------
TODAY = datetime.date.today().isoformat()
def lastmod(f):
    try: return sh('git', 'log', '-1', '--format=%cs', '--', f).strip() or TODAY
    except Exception: return TODAY
def images(f):
    s = open(f, encoding='utf-8').read(); m = re.search(r'<main.*?</main>', s, re.S)
    out = []
    for im in re.findall(r'<img[^>]*src="(/img/[^"]+\.(?:jpg|jpeg|png|webp))"', m.group(0) if m else s):
        if im not in out: out.append(im)
    return out[:3]
names = sorted({n for (_, n) in pages if n != '404'}, key=lambda n: (n != 'index', n))
x = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for n in names:
    for lg in LANGS:
        if (lg, n) not in pages: continue
        f = pages[(lg, n)]
        e = [f'<url><loc>{BASE}{url(lg, n)}</loc><lastmod>{lastmod(f)}</lastmod>']
        for l2 in LANGS:
            if (l2, n) in pages: e.append(f'<xhtml:link rel="alternate" hreflang="{l2}" href="{BASE}{url(l2, n)}"/>')
        e.append(f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{url("fr", n)}"/>')
        for im in images(f): e.append(f'<image:image><image:loc>{BASE}{im}</image:loc></image:image>')
        e.append('</url>'); x.append(''.join(e))
for pdf in sorted(glob.glob('docs/*.pdf')):
    x.append(f'<url><loc>{BASE}/{pdf}</loc><lastmod>{lastmod(pdf)}</lastmod></url>')
x.append('</urlset>')
open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(x) + '\n')
print('sitemap :', sum(1 for l in x if l.startswith('<url>')), 'URLs')
