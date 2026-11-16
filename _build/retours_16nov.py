#!/usr/bin/env python3 -I
"""Retours client du 2026-11-16 (HTML, FR EN DE ES PT ; l'italien est régénéré par _build/it/build_it.py). Idempotent.
 1. menu : « Transport Internationaux » -> « Transports Internationaux » (FR)
 2. page prévoyance : retrait du bloc « Prévoyance Funéraire Genève – Maison Murith » (Ville de Genève 1866 + coût)
 3. accueil : carrousel de services, « Prévoyance funéraire » en numéro 1
 4. accueil : petites icônes à droite dans « Nos produits »
"""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
LANGS = ['', 'en/', 'de/', 'es/', 'pt/']
changed = []

def rw(path, fn):
    p = root / path
    s = p.read_text(encoding='utf8'); n = fn(s)
    if n != s: p.write_text(n, encoding='utf8'); changed.append(path)

# 1) libellé du menu (FR) + dictionnaire italien
for p in sorted(root.glob('*.html')) + sorted((root / 'blog').glob('*.html')):
    rw(p.relative_to(root), lambda s: s.replace('Transport Internationaux', 'Transports Internationaux'))
dp = root / '_build/it/it_dict.json'
d = json.loads(dp.read_text(encoding='utf8'))
nd = {k.replace('Transport Internationaux', 'Transports Internationaux'): v for k, v in d.items()}
if nd != d: dp.write_text('{\n' + ',\n'.join(json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False) for k, v in nd.items()) + '\n}\n', encoding='utf8'); changed.append('_build/it/it_dict.json')

# 2) page prévoyance : retire la carte d'information, texte centré sur une colonne
CARD = re.compile(r'\n?<div class="card reveal"[^>]*><span class="ico-ring">.*?</div>\n(?=</div></section><section class="section alt pv-trust")', re.S)
def prev(s):
    j = s.find('<section class="section tight">')
    if j < 0: return s
    head, tail = s[:j], s[j:]
    tail = CARD.sub('\n', tail, count=1)
    tail = re.sub(r'<div class="container split"[^>]*>', '<div class="container pv-intro">', tail, count=1)
    return head + tail
for l in LANGS: rw(l + 'prevoyance-funeraire.html', prev)

# 3) carrousel : Prévoyance en premier (data-i, numéros « 0N / 04 »)
ART = re.compile(r'<article class="c3d-card" data-i="(\d)">.*?</article>', re.S)
def carousel(s):
    cards = [m.group(0) for m in ART.finditer(s)]
    if len(cards) != 4: return s
    if re.search(r'href="[^"]*prevoyance-funeraire"', cards[0]): return s
    order = [3, 0, 1, 2]
    out = []
    for new_i, old_i in enumerate(order):
        c = cards[old_i]
        c = re.sub(r'data-i="\d"', f'data-i="{new_i}"', c, count=1)
        c = re.sub(r'<p class="eyebrow">\d\d / 04</p>', f'<p class="eyebrow">0{new_i + 1} / 04</p>', c, count=1)
        out.append(c)
    it = iter(out)
    return ART.sub(lambda m: next(it), s)
for l in LANGS: rw(l + 'index.html', carousel)

# 4) icônes « Nos produits »
SVG = {
 0: '<svg aria-hidden="true" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24"><path d="M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6M12 5V2.5M10.8 3.8h2.4"/></svg>',
 1: '<svg aria-hidden="true" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24"><path d="M8.5 3h7l3 5.5-2.5 12.5h-8L5.5 8.5 8.5 3Z"/><path d="M5.5 8.5h13M12 11v6M9.8 13.2h4.4"/></svg>',
 2: '<svg aria-hidden="true" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24"><g transform="translate(0 -1)"><ellipse cx="12" cy="6.2" rx="2.1" ry="3"/><ellipse cx="12" cy="6.2" rx="2.1" ry="3" transform="rotate(72 12 10.2)"/><ellipse cx="12" cy="6.2" rx="2.1" ry="3" transform="rotate(144 12 10.2)"/><ellipse cx="12" cy="6.2" rx="2.1" ry="3" transform="rotate(216 12 10.2)"/><ellipse cx="12" cy="6.2" rx="2.1" ry="3" transform="rotate(288 12 10.2)"/><circle cx="12" cy="10.2" r="1.3"/></g><path d="M12 14.5V22M12 19c-2.4 0-3.8-1-4.4-2.4M12 18c2.4 0 3.8-1 4.4-2.4"/></svg>',
}
def icons(s):
    s = re.sub(r'<span class="ps-ic" aria-hidden="true">.*?</span>', '', s)
    k = iter(range(3))
    return re.sub(r'(<span class="ps-t">[^<]*</span>)', lambda m: m.group(1) + f'<span class="ps-ic" aria-hidden="true">{SVG[next(k)]}</span>', s)
for l in LANGS: rw(l + 'index.html', icons)

print('modifiés :', len(changed)); [print(' ', c) for c in changed]
