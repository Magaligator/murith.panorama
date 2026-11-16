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
        s = mark(s, r'<div class="vcard">(?=.{0,400}?video-accueil)', 'NOUVEAU · vidéo agrandie de 30 % et qualité HD (1080p, depuis le fichier 4K d\'origine)', flags=re.S)
        s = s.replace('<section class="hero hero-pan">', '<section class="hero hero-pan"><span class="rg-tag rg-mob">NOUVEAU (mobile) · barre de menu lisible, enseigne « Chapelle de la Cluse » adoucie</span>', 1)
    if name == 'prevoyance-funeraire.html':
        s = s.replace('<div class="container pv-intro">', '<div class="container pv-intro">' + tag('NOUVEAU · texte centré et simple, comme sur mobile'), 1)
        s = s.replace('</div></section><section class="section alt pv-trust"',
            '<div class="rg-removed"><b>SUPPRIMÉ</b> : le bloc « Prévoyance Funéraire Genève – Maison Murith » (service public de la Ville de Genève depuis 1866, obsèques gratuites, depuis 2014 plus de nouvelles prévoyances, maîtriser le coût).</div></div></section><section class="section alt pv-trust"', 1)
        s = mark(s, r'<div class="split pv-split" id="video">', 'NOUVEAU · mise en page épurée, une seule colonne centrée (comme sur mobile)')
        s = mark(s, r'<div class="g3">(?=<div class="card reveal")', 'NOUVEAU · trois blocs empilés, texte simple (comme sur mobile)')
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
    s = s.replace('</body>', '<a class="rg-pill" href="/changements">Changements en rouge · voir la liste</a></body>', 1)
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
.rg-pill{position:fixed;left:12px;bottom:12px;z-index:9999;background:var(--rg);color:#fff!important;font:700 13px/1 Inter,system-ui,sans-serif;padding:11px 16px;border-radius:999px;text-decoration:none;box-shadow:0 8px 24px -8px rgba(0,0,0,.5)}
@media(max-width:820px){.rg-pill{bottom:auto;top:calc(var(--hdr-h,60px) + 10px);left:auto;right:10px;font-size:11px;padding:8px 12px}}
''', encoding='utf8')

ROWS = [
 ('Menu', '« Manque un s à transport »', 'Le menu (ordinateur, mobile, pied de page) affiche maintenant <b>Transports Internationaux</b>.', '/'),
 ('Accueil · carrousels', '« Les photos défilent trop vite, on n\'a pas le temps de lire le petit texte, il manque 1 à 2 secondes minimum »', 'Carrousel des services : 6,5 s → <b>9 s</b> par carte. Diaporama du haut : 5,6 s → <b>7,6 s</b>. Liste « Nos produits » : 5,2 s → <b>7,2 s</b>.', '/'),
 ('Salons et cercueils', '« Les photos ne circulent pas bien avec le doigt, ça se bloque à un moment donné »', 'Défilement tactile libre (plus d\'accroche de fin de course sur les cercueils), photos suivantes préchargées dans la visionneuse, galerie des salons qui reprend plus vite.', '/cercueils'),
 ('Accueil mobile', '« Comment réduire ce gros Chapelle de la Cluse tout en le préservant afin de voir correctement la barre de menu »', 'Barre de menu bleu marine (logo et menu lisibles), la photo démarre sous la barre et l\'enseigne est adoucie par un dégradé : elle reste visible.', '/'),
 ('Accueil · Nos produits', '« On avait parlé de petites icônes sur la droite afin d\'attirer plus l\'œil »', 'Une icône ronde à droite de chaque ligne : salons, cercueils, fleurs (6 langues).', '/'),
 ('Accueil mobile · carrousel', '« En numéro 1 svp » (Prévoyance funéraire)', 'La carte <b>Prévoyance funéraire</b> est désormais la première (01 / 04) dans toutes les langues.', '/'),
 ('Page prévoyance', '« On peut enlever cette information »', 'Le bloc « Prévoyance Funéraire Genève – Maison Murith » (Ville de Genève 1866, obsèques gratuites, coût) est <b>supprimé</b>. Le budget étalé reste dit dans la section « La confiance avant tout ».', '/prevoyance-funeraire'),
 ('Page prévoyance · ordinateur', '« Dans la version mobile la simplicité du texte est très bien, merci de faire pareil dans la version informatique »', 'Texte centré sur une seule colonne, vidéo au-dessus, puces puis trois blocs empilés : même simplicité que sur mobile.', '/prevoyance-funeraire'),
 ('Accueil · vidéo', '« Si on peut agrandir la vidéo de 30 % et arranger la qualité »', 'Largeur 920 px → <b>1 196 px (+30 %)</b>. Nouvelle vidéo 1080p refaite depuis le fichier 4K d\'origine (l\'ancienne était en 480p) et nouvelle image d\'aperçu HD (aussi sur la page Contact).', '/#video'),
 ('Page prévoyance · vidéo', 'Nouvelle vidéo envoyée (VIDEO-2026-11-13)', 'Vidéo de 4 min 27 intégrée dans « La confiance avant tout » : sous-titres français, transcription repliable, balisage VideoObject, titre/description optimisés « prévoyance funéraire Genève ». Le fichier d\'origine est en 576p : la qualité s\'améliorera avec le fichier du Drive de Jean-Marc.', '/prevoyance-funeraire#video'),
]
rows = ''.join(f'<tr><td><b>{a}</b></td><td class="q">{b}</td><td>{c}</td><td><a href="{d}">Voir</a></td></tr>' for a, b, c, d in ROWS)
(out / 'changements.html').write_text(f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><meta name="robots" content="noindex,nofollow"/><title>Changements en rouge</title>
<style>body{{margin:0;font:16px/1.55 Inter,system-ui,sans-serif;color:#142B46;background:#F5F8FD}}main{{max-width:1080px;margin:0 auto;padding:32px 16px 80px}}h1{{font-family:"Playfair Display",Georgia,serif;font-weight:400;color:#E10600;margin:0 0 6px}}p.s{{margin:0 0 24px}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #D5DEEA;border-radius:12px;overflow:hidden}}th,td{{text-align:left;vertical-align:top;padding:12px 14px;border-bottom:1px solid #E3EAF3}}th{{background:#E10600;color:#fff;font-size:13px;letter-spacing:.04em}}td.q{{font-style:italic;color:#4A5B74}}b{{color:#E10600}}a{{color:#142B46;font-weight:600}}
@media(max-width:760px){{table,thead,tbody,tr,td,th{{display:block}}thead{{display:none}}tr{{border-bottom:6px solid #F5F8FD;padding:6px 0}}td{{border:0;padding:4px 14px}}}}</style></head><body><main>
<h1>Changements en rouge</h1><p class="s">Retours du client du 16 novembre 2026. Sur chaque page, les éléments modifiés sont entourés ou écrits en rouge.</p>
<table><thead><tr><th>Où</th><th>Retour du client</th><th>Ce qui a changé</th><th></th></tr></thead><tbody>{rows}</tbody></table>
<p class="s" style="margin-top:20px"><a href="/">← Retour au site</a></p></main></body></html>''', encoding='utf8')
(out / 'Ouvrir.command').write_text('#!/bin/bash\ncd "$(dirname "$0")"\n(sleep 1.5; open http://localhost:3010/) &\nnode dev-server.mjs 3010\n', encoding='utf8')
(out / 'Ouvrir.command').chmod(0o755)
print('Copie rouge générée :', out)
