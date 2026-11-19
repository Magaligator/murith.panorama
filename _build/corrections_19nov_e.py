#!/usr/bin/env python3 -I
"""Corrections client du 2026-11-19, partie 5 (idempotent) :
 - retrait du bandeau « Prévoyance funéraire » (remise comme avant) ;
 - bouton « Personnaliser la cérémonie » -> « Découvrir la prévoyance funéraire » (page prévoyance), 6 langues ;
 - phrase rapatriement : formulation exacte du client (page prévoyance Genève, FR) ;
 - français : espaces insécables avant : ; ? ! et dans « », les milliers, CHF, % et les numéros de téléphone."""
import pathlib, re, glob
root = pathlib.Path(__file__).resolve().parent.parent
L = ['', 'en/', 'de/', 'it/', 'es/', 'pt/']
changed = set(); problems = []
def rw(path, fn):
    p = root / path
    s = p.read_text(encoding='utf8'); n = fn(s)
    if n != s: p.write_text(n, encoding='utf8'); changed.add(path)
pages = [str(p.relative_to(root)) for p in root.rglob('*.html') if not any(x in p.parts for x in ('_build', '_src', 'node_modules', '_archive-wix', '.git'))]

# 1) bandeau retiré
for f in pages: rw(f, lambda s: re.sub(r'<section class="pv-strip-sec">.*?</section>', '', s, flags=re.S))

# 2) bouton -> prévoyance
BTN = {'': ('Personnaliser la cérémonie', 'Découvrir la prévoyance funéraire'),
 'en/': ('Personalise the ceremony', 'Discover funeral pre-planning'),
 'de/': ('Die Trauerfeier gestalten', 'Bestattungsvorsorge entdecken'),
 'it/': ('Personalizza la cerimonia', 'Scopri la previdenza funeraria'),
 'es/': ('Personalizar la ceremonia', 'Descubrir la previsión funeraria'),
 'pt/': ('Personalizar a cerimónia', 'Descobrir a previdência funerária')}
def btn(s, l):
    old, new = BTN[l]
    return re.sub(r'(<a class="btn [^"]*" href=")/' + re.escape(l) + r'obseques(">)' + re.escape(old), lambda m: f'{m.group(1)}/{l}prevoyance-funeraire{m.group(2)}{new}', s)
for l in L:
    for f in pages:
        if (f.startswith(l) if l else '/' not in f or f.startswith('blog/')): rw(f, lambda s, l=l: btn(s, l))

# 2b) page Obsèques : le bouton de la section « À vos côtés depuis 1888 » est retiré (celui du haut reste)
for l in L:
    rw(f'{l}obseques.html', lambda s, l=l: re.sub(r'<a class="btn btn-ghost" href="/' + re.escape(l) + r'prevoyance-funeraire">' + re.escape(BTN[l][1]) + r'(?:<svg.*?</svg>)?</a>', '', s))

# 3) phrase rapatriement (formulation du client)
NEW = "En effet, en cas de décès à l'étranger, deux solutions possibles : la famille peut mandater directement l'assurance rapatriement inclus dans la police du défunt ; si ce paramètre n'existe pas, alors nous pouvons conseiller à la famille une entreprise sur site à mandater, grâce à notre réseau partenaire."
OLD = re.compile(r"En effet, en cas de décès à l'étranger, deux solutions (?:sont )?possibles\s*(?: )?: la famille peut mandater[^<]*?réseau (?:de )?partenaires?\.")
def repat(s):
    n = OLD.sub(lambda m: NEW, s, count=1)
    return n
rw('blog/prevoyance-funeraire-geneve.html', repat)

# 4) typographie française
NB = ' '
def typo(t):
    t = re.sub(r'(?<=\S) ([:;?!])(?=\s|$)', NB + r'\1', t)
    t = re.sub(r'«[  ]', '«' + NB, t); t = re.sub(r'[  ]»', NB + '»', t)
    t = re.sub(r'(\d) (\d{3})(?!\d)', r'\1' + NB + r'\2', t)
    t = re.sub(r'(\d) (CHF|%|€|km|kg|h\b)', r'\1' + NB + r'\2', t)
    t = re.sub(r'(CHF) (\d)', r'\1' + NB + r'\2', t)
    t = re.sub(r'(\+41) (22) (809) (56) (00)', lambda m: NB.join(m.groups()), t)
    t = re.sub(r'\b(022) (809) (56) (00)\b', lambda m: NB.join(m.groups()), t)
    return t
def typo_html(s):
    parts = re.split(r'(<script.*?</script>|<style.*?</style>|<!--.*?-->|<head>.*?</head>)', s, flags=re.S)
    out = []
    for p in parts:
        if p.startswith(('<script', '<style', '<!--', '<head>')): out.append(p); continue
        out.append(re.sub(r'>([^<>]+)<', lambda m: '>' + typo(m.group(1)) + '<', p))
    return ''.join(out)
def typo_other(t):
    t = re.sub(r'(\d) %', r'\1' + NB + '%', t)
    t = re.sub(r'«[ \u202f]', '«' + NB, t); t = re.sub(r'[ \u202f]»', NB + '»', t)
    return t
def typo_other_html(s):
    parts = re.split(r'(<script.*?</script>|<style.*?</style>|<!--.*?-->|<head>.*?</head>)', s, flags=re.S)
    return ''.join(p if p.startswith(('<script', '<style', '<!--', '<head>')) else re.sub(r'>([^<>]+)<', lambda m: '>' + typo_other(m.group(1)) + '<', p) for p in parts)
for f in pages:
    rw(f, typo_other_html if f.split('/')[0] in ('en', 'de', 'it', 'es', 'pt') else typo_html)

# 5) pied de page : années retirées devant la mention « Site réalisé par Websituation »
for f in pages: rw(f, lambda s: re.sub(r'(<div class="container foot-bot">.*?<span>)© 1888[–-]2026 · ', r'\1', s, flags=re.S))

if __name__ == '__main__':
    print('modifiés :', len(changed), sorted(changed)[:5]); print('problèmes :', len(problems))
