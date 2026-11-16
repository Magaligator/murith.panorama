"""Outils de traduction des pages FR -> IT : extraction / réinjection des textes (blocs, attributs, JSON-LD)."""
import copy, json, pathlib, re
from bs4 import BeautifulSoup, NavigableString, Comment, Doctype, Declaration

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
SKIP_DIRS = ('_archive-wix', '_build', '_img-src', '_src', 'docs', '.git', 'en', 'de', 'es', 'pt', 'it', 'node_modules')
INLINE = {'a', 'b', 'strong', 'em', 'i', 'span', 'small', 'sup', 'sub', 'abbr', 'mark', 'u', 'time', 'label'}
NOTEXT = {'script', 'style', 'svg', 'code', 'noscript'}
ATTRS = ('alt', 'title', 'aria-label', 'placeholder', 'content', 'data-label', 'data-more', 'data-less', 'data-t')
LET = re.compile(r'[A-Za-zÀ-ÿ]{2}')

def fr_pages():
    out = []
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS: continue
        out.append(rel)
    return out

def soup_of(path): return BeautifulSoup(pathlib.Path(path).read_text(encoding='utf8'), 'html.parser')

def has_direct_text(el):
    return any(isinstance(c, NavigableString) and not isinstance(c, Comment) and c.strip() for c in el.children)

def in_skip(el):
    return any(getattr(a, 'name', None) in NOTEXT or (hasattr(a, 'get') and (a.get('class') or []) and ('lang' in a.get('class') or 'm-lang' in a.get('class'))) for a in [el] + list(el.parents))

def unit_roots(soup):
    """Racines d'unités de traduction, dans l'ordre du document, sans doublon."""
    seen, roots = set(), []
    for t in soup.find_all(string=True):
        if isinstance(t, (Comment, Doctype, Declaration)) or not t.strip(): continue
        if in_skip(t.parent): continue
        r = t.parent
        while r.parent is not None and r.parent.name not in ('[document]', 'html', 'body', 'head') and (r.name in INLINE and (r.parent.name in INLINE or has_direct_text(r.parent))):
            r = r.parent
        # remonter aussi quand r est inline et son parent a du texte direct
        if id(r) not in seen:
            seen.add(id(r)); roots.append(r)
    return roots

def is_inline_child(c): return c.name in INLINE

def serialize(root):
    """Texte de l'unité avec marqueurs {n}..{/n} (inline) et {xn} (atomes). Renvoie (chaîne, liste d'éléments)."""
    els = []
    def rec(node):
        s = ''
        for c in node.children:
            if isinstance(c, Comment): continue
            if isinstance(c, NavigableString):
                s += re.sub(r'\s+', ' ', str(c)); continue
            els.append(c); n = len(els)
            if c.name in INLINE and not in_skip(c):
                s += '{%d}%s{/%d}' % (n, rec(c), n)
            else:
                s += '{x%d}' % n
        return s
    s = rec(root)
    return re.sub(r'\s+', ' ', s).strip(), els

TOK = re.compile(r'\{(/?)(x?)(\d+)\}')
def rebuild(root, tr, els, soup):
    """Remplace le contenu de root par la traduction tr (mêmes marqueurs)."""
    for c in list(root.children): c.extract()
    def build(s, parent):
        pos = 0; stack = []
        cur = parent
        for m in TOK.finditer(s):
            if m.start() > pos: cur.append(NavigableString(s[pos:m.start()]))
            pos = m.end(); close, x, n = m.group(1), m.group(2), int(m.group(3))
            if x:
                cur.append(copy.copy(els[n - 1]) if False else els[n - 1])
            elif not close:
                shell = soup.new_tag(els[n - 1].name, attrs=dict(els[n - 1].attrs))
                cur.append(shell); stack.append(cur); cur = shell
            else:
                cur = stack.pop()
        if pos < len(s): cur.append(NavigableString(s[pos:]))
    build(tr, root)

def check_markers(src, tr):
    f = lambda s: sorted(re.findall(r'\{/?x?\d+\}', s))
    return f(src) == f(tr)

def attr_items(soup):
    out = []
    for el in soup.find_all(True):
        if in_skip(el) and el.name != 'svg': continue
        for a in ATTRS:
            v = el.get(a)
            if isinstance(v, str) and LET.search(v):
                if a == 'content' and el.name == 'meta':
                    k = el.get('name') or el.get('property') or ''
                    if k not in ('description', 'og:title', 'og:description', 'twitter:title', 'twitter:description', 'og:image:alt'): continue
                elif a == 'content': continue
                out.append((el, a, v))
    return out

JSON_KEYS = {'name', 'description', 'text', 'headline', 'caption', 'alternativeHeadline', 'articleSection', 'abstract', 'about'}
def json_strings(obj, key=None, out=None):
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items(): json_strings(v, k, out)
    elif isinstance(obj, list):
        for v in obj: json_strings(v, key, out)
    elif isinstance(obj, str) and key in JSON_KEYS and LET.search(obj) and not obj.startswith('http'):
        out.append(obj)
    return out
