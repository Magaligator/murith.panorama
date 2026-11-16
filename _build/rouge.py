#!/usr/bin/env python3 -I
"""Génère une copie « changements en rouge » du site (revue client). Usage : python3 -I _build/rouge.py <dossier-de-sortie>
Les repères rouges ne sont jamais ajoutés au site de production. La copie se lance avec : node dev-server.mjs (voir Ouvrir.command)."""
import pathlib, re, shutil, sys
root = pathlib.Path(__file__).resolve().parent.parent
out = pathlib.Path(sys.argv[1]).resolve()
SKIP = {'.git', 'node_modules', '_archive-wix', '_img-src', '_build', '_src', '.DS_Store', '.vercelignore'}
if out.exists(): shutil.rmtree(out)
def ignore(d, names): return [n for n in names if n in SKIP or n.endswith(('.md', '.csv'))]
shutil.copytree(root, out, ignore=ignore)

def tag(txt): return f'<span class="rg-tag">{txt}</span>'
def add_rg(start):  # ajoute la classe rg à une balise ouvrante
    return re.sub(r'class="([^"]*)"', lambda m: f'class="{m.group(1)} rg"', start, count=1)
def mark(s, pattern, label, tag_before=True, flags=0):
    m = re.search(pattern, s, flags)
    if not m: print('  (repère introuvable)', label[:50]); return s
    start = m.group(0)
    return s[:m.start()] + (tag(label) if tag_before else '') + add_rg(start) + s[m.end():]

def fr_page(name, s):
    # 1) libellé du menu
    s = re.sub(r'>(Transports Internationaux)</a>', r'><span class="rg-t">\1</span></a>', s)
    if name == 'index.html':
        s = mark(s, r'<div [^>]*class="c3d"[^>]*>', 'NOUVEAU · « Prévoyance funéraire » passe en numéro 1 · défilement plus lent (9 s au lieu de 6,5 s)')
        s = mark(s, r'<div class="pshow reveal"[^>]*>', 'NOUVEAU · petites icônes à droite · défilement plus lent (7 s)')
        s = mark(s, r'<div class="vcard">(?=.{0,400}?video-accueil)', 'NOUVEAU · vidéo agrandie de 30 % et qualité HD (720p, refaite depuis le fichier 4K d\'origine)', flags=re.S)
        s = s.replace('<section class="hero hero-pan">', '<section class="hero hero-pan"><span class="rg-tag rg-mob">NOUVEAU (mobile) · barre de menu lisible, enseigne « Chapelle de la Cluse » adoucie</span>', 1)
    if name == 'prevoyance-funeraire.html':
        s = s.replace('<div class="container pv-intro">', '<div class="container pv-intro">' + tag('NOUVEAU · texte centré et simple, comme sur mobile'), 1)
        s = s.replace('</div></section><section class="section alt pv-trust"',
            '<div class="rg-removed"><b>SUPPRIMÉ</b> : le bloc « Prévoyance Funéraire Genève – Maison Murith » (service public de la Ville de Genève depuis 1866, obsèques gratuites, depuis 2014 plus de nouvelles prévoyances, maîtriser le coût).</div></div></section><section class="section alt pv-trust"', 1)
        s = mark(s, r'<div class="vcard">(?=.{0,400}?video-prevoyance)', 'NOUVEAU · vidéo prévoyance (4 min 27) : sous-titres, transcription, référencement Google', flags=re.S)
        s = mark(s, r'<div class="split pv-split" id="video">', 'NOUVEAU · mise en page épurée, une seule colonne centrée (comme sur mobile)')
        s = mark(s, r'<div class="g3">(?=<div class="card reveal")', 'NOUVEAU · trois blocs empilés, texte simple (comme sur mobile)')
    if name == 'contact.html':
        s = mark(s, r'<div class="vcard">(?=.{0,400}?video-accueil)', 'NOUVEAU · vidéo en qualité HD (720p, depuis le fichier 4K d\'origine)', flags=re.S)
    if name == 'cercueils.html':
        s = mark(s, r'<div class="slider per-4"[^>]*>', 'CORRIGÉ · défilement des photos au doigt sans blocage · photos suivantes préchargées')
    if name == 'salons.html':
        s = mark(s, r'<div [^>]*data-cyl[^>]*>', 'CORRIGÉ · galerie qui reprend plus vite après le doigt · photos suivantes préchargées')
    return s

for p in sorted(out.rglob('*.html')):
    rel = p.relative_to(out)
    s = p.read_text(encoding='utf8')
    if len(rel.parts) == 1 or rel.parts[0] == 'blog':
        s = fr_page(rel.name if len(rel.parts) == 1 else '', s)
    s = s.replace('</head>', '<link rel="stylesheet" href="/rouge.css"/></head>', 1)
    p.write_text(s, encoding='utf8')

(out / 'rouge.css').write_text('''/* Revue client : changements en rouge (jamais en production) */
:root{--rg:#E10600}
.rg{outline:3px solid var(--rg)!important;outline-offset:6px;border-radius:12px}
.rg-tag{display:block;width:fit-content;max-width:100%;margin:0 0 14px;background:var(--rg);color:#fff;font:600 13px/1.35 Inter,system-ui,sans-serif;padding:6px 12px;border-radius:8px;letter-spacing:.01em;text-transform:none}
.vid-home .rg-tag{margin-inline:auto}
.rg-mob{display:none}
@media(max-width:820px){.rg-mob{display:block;position:absolute;left:12px;right:12px;top:calc(var(--hdr-h,60px) + 52px);z-index:90;font-size:12px}
 .pan-top:has(.hero-pan) .site-header:not(.is-scrolled){box-shadow:inset 0 0 0 3px var(--rg)!important}}
.rg-t{color:var(--rg)!important;font-weight:800;background:rgba(255,255,255,.92);border-radius:6px;padding:1px 6px}
.ps-ic{outline:3px solid var(--rg);outline-offset:3px}
.rg-removed{margin:28px auto 0;max-width:760px;border:3px dashed var(--rg);border-radius:12px;padding:14px 18px;color:var(--rg);font:500 15px/1.5 Inter,system-ui,sans-serif;text-align:left}
.rg-removed b{background:var(--rg);color:#fff;border-radius:6px;padding:1px 8px;margin-right:6px}
@media(max-width:820px){''', encoding='utf8')

(out / 'Ouvrir.command').write_text('#!/bin/bash\ncd "$(dirname "$0")"\n(sleep 1.5; open http://localhost:3010/) &\nnode dev-server.mjs 3010\n', encoding='utf8')
(out / 'Ouvrir.command').chmod(0o755)
print('Copie rouge générée :', out)
