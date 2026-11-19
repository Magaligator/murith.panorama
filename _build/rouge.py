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
    s = s.replace('target="_blank" rel="noopener">© Websituation', 'target="_blank" rel="noopener" class="rg-t">© Websituation')
    s = s.replace('class="ph-devis"', 'class="ph-devis rg"')
    # 1) libellé du menu
    s = re.sub(r'>(Transports Internationaux)</a>', r'><span class="rg-t">\1</span></a>', s)
    if name == 'index.html':
        s = s.replace('<p>La mort est une réalité que chaque être humain doit affronter', '<p class="rg">La mort est une réalité que chaque être humain doit affronter', 1)
        s = s.replace('<p>Que vous optiez pour la simplicité ou que vous ayez des exigences particulières, nos conseillers funéraires', '<p class="rg">Que vous optiez pour la simplicité ou que vous ayez des exigences particulières, nos conseillers funéraires', 1)
        s = s.replace('<section class="hero hero-pan">', '<section class="hero hero-pan"><span class="rg-tag rg-mob">CORRIGÉ (mobile et tablette) · l\'enseigne « Chapelle de la Cluse » n\'apparaît plus sur la photo, quel que soit l\'écran · textes du diaporama plus lisibles · photo plus nette · ordre des prénoms : Jacques, Jimmy, Philippe et Jean-Marc · « Demander un devis » sous « Un décès vient de survenir »</span>', 1)
        s = mark(s, r'<div [^>]*class="c3d"[^>]*>', 'NOUVEAU · « Prévoyance funéraire » passe en numéro 1 · défilement plus lent (9 s) · un appui sur la photo ouvre la page')
        s = mark(s, r'<div class="pshow reveal"[^>]*>', 'NOUVEAU · petites icônes à droite · défilement plus lent (7 s)')
        s = mark(s, r'<div class="vcard">(?=.{0,400}?video-accueil)', 'NOUVEAU · nouvelle vidéo de présentation (2 min 43), grand format HD', flags=re.S)
    if name == 'prevoyance-funeraire.html':
        s = s.replace('<details><summary>', '<div class="rg-removed"><b>SUPPRIMÉ</b> : la question « Le service public de la Ville de Genève propose-t-il encore des prévoyances funéraires ? » (le service public de la Ville de Genève n\'est plus cité qu\'une seule fois sur le site, dans l\'article de blog sur la prévoyance).</div><details><summary>', 1)
        s = s.replace('<div class="container pv-intro">', '<div class="container pv-intro">' + tag('NOUVEAU · texte centré et simple, comme sur mobile'), 1)
        s = s.replace('</div></section><section class="section alt pv-trust"',
            '<div class="rg-removed"><b>SUPPRIMÉ</b> : le bloc « Prévoyance Funéraire Genève – Maison Murith » (service public de la Ville de Genève depuis 1866, obsèques gratuites, depuis 2014 plus de nouvelles prévoyances, maîtriser le coût).</div></div></section><section class="section alt pv-trust"', 1)
        s = mark(s, r'<div class="vcard">(?=.{0,400}?video-prevoyance)', 'NOUVEAU · vidéo prévoyance (4 min 27) en meilleure qualité (720p, image nettoyée et plus nette) · sous-titres, transcription, référencement Google', flags=re.S)
        s = mark(s, r'<div class="split pv-split" id="video">', 'NOUVEAU · mise en page épurée, une seule colonne centrée (comme sur mobile)')
        s = mark(s, r'<div class="g3">(?=<div class="card reveal")', 'NOUVEAU · trois blocs empilés, texte simple (comme sur mobile)')
    s = re.sub(r'(<a class="btn [^"]*" href="/prevoyance-funeraire")(>Découvrir la prévoyance funéraire)', r'\1 style="outline:3px solid var(--rg);outline-offset:4px"\2', s)
    if name == 'blog/prevoyance-funeraire-geneve.html' or name == 'prevoyance-funeraire-geneve.html':
        s = re.sub(r"(En effet, en cas de décès à l'étranger, deux solutions possibles.*?réseau partenaire\.)(</p>)", r'<span class="rg-t" id="rg-rapat">\1</span>\2<div class="rg-removed"><b>MODIFIÉ</b> : la phrase en rouge ci-dessus (texte exact du client) remplace l\'ancienne. <b>SUPPRIMÉ</b> : « Ce service peut être intégré dans votre contrat de prévoyance funéraire à Genève pour une couverture complète, même en cas de décès à l\'étranger. »</div>', s, count=1, flags=re.S)
    s = s.replace('<b class="h24">', '<b class="h24 rg-t">')
    if name == 'conseillers.html':
        s = mark(s, r'<h3 class="adv-sub"[^>]*>', 'NOUVEAU · équipe de direction et d\'administration : photos, spécialités, présentations et langues parlées (document « version COURTE » du client)')
    if name == 'contact.html':
        s = mark(s, r'<div class="vcard">(?=.{0,400}?video-accueil)', 'NOUVEAU · nouvelle vidéo de présentation (2 min 43), HD', flags=re.S)
    if name == 'prevoyance-funeraire-geneve.html':
        s = s.replace('<article class="post-body">', '<article class="post-body">' + tag('CORRIGÉ selon le document du client : frais « dès 3 500 CHF » · section « service public de la Ville de Genève » et son entrée du sommaire supprimées · fonds « garantis par notre patrimoine » · « la plus ancienne à Genève » · rapatriement : deux solutions à l\'étranger · « paiement en un seul versement ou échelonné » · nouvelle étape « sans rencontre : questionnaire » · lien du questionnaire réparé · réponses de la FAQ (âge, fonds, hors Genève) · « Murith » en moins dans la liste'), 1)
        s = s.replace('<p>En Suisse romande, le coût de l\'enterrement est souvent sous-estimé.', '<p class="rg">En Suisse romande, le coût de l\'enterrement est souvent sous-estimé.', 1)
        s = s.replace('<h2><strong>Comment souscrire à une Prévoyance', '<div class="rg-removed"><b>SUPPRIMÉ</b> : la section « Le Service Public des Pompes Funèbres de la Ville de Genève » (gratuité) et son entrée dans la table des matières.</div><h2><strong>Comment souscrire à une Prévoyance', 1)
        s = s.replace('<li><strong>Sans rencontre :</strong>', '<li class="rg"><strong>Sans rencontre :</strong>', 1)
        s = s.replace('<div class="tbl"><table><thead><tr><th><strong>Question</strong>', '<div class="tbl rg"><table><thead><tr><th><strong>Question</strong>', 1)
    if name == 'cout-rapatriement-corps.html':
        s = s.replace('<article class="post-body">', '<article class="post-body">' + tag('CORRIGÉ selon le document du client : tableau des coûts (3 lignes) · comparaison aérien / routier · soins de conservation 450 à 510 CHF · tableau des étapes (délai, Transit\'Air, cérémonie, « Murith ») · « la plus ancienne à Genève » · « en face des Hôpitaux » · ajout : formation et Brevet Fédéral (ASSF)'), 1)
        s = re.sub(r'<div class="tbl">(?=<table>)', '<div class="tbl rg">', s, count=3)
        s = s.replace('<li>Murith forme aussi', '<li class="rg">Murith forme aussi', 1)
    if name == 'deces-proche-suisse-10-etapes.html':
        s = s.replace('<article class="post-body">', '<article class="post-body">' + tag('CORRIGÉ selon le document du client : tableau « Estimation des coûts » supprimé (frais « dès CHF 3\'500 ») · « cercueils de qualité » (sans « européens ») · titre en minuscules · « Les les » corrigé · ajout : formation et Brevet Fédéral (ASSF)'), 1)
        s = s.replace('<li><strong>La formation :</strong>', '<li class="rg"><strong>La formation :</strong>', 1)
    if name == 'cercueils.html':
        s = mark(s, r'<div class="slider per-4"[^>]*>', 'CORRIGÉ · défilement des photos au doigt sans blocage · photos suivantes préchargées')
    if name == 'notre-histoire.html':
        s = re.sub(r'(<figure>)(<img[^>]*histoire-1919-paul-murith-960)', lambda m: '<figure class="rg">' + tag('NOUVEAU · photo 1919 : corbillard et portrait de Paul Murith') + m.group(2), s, count=1)
        s = re.sub(r'(<figure>)(<img[^>]*histoire-1960-henri-murith-960)', lambda m: '<figure class="rg">' + tag('NOUVEAU · photo 1960-1981 : portrait de Henri Murith et corbillard') + m.group(2), s, count=1)
        s = re.sub(r'(<figure>)(<img[^>]*freres-murith-960)', lambda m: '<figure class="rg">' + tag('NOUVEAU · photo des trois frères (partie « Aujourd\'hui »)') + m.group(2), s, count=1)
    if name == 'salons.html':
        s = s.replace('<section class="section tight">', '<section class="section tight"><span class="rg-tag rg-mobonly">NOUVEAU (mobile) · espaces entre les sections resserrés et réguliers · galerie plus compacte</span>', 1)
        s = mark(s, r'<div [^>]*data-cyl[^>]*>', 'CORRIGÉ · galerie qui reprend plus vite après le doigt · photos suivantes préchargées')
    return s

for p in sorted(out.rglob('*.html')):
    rel = p.relative_to(out)
    s = p.read_text(encoding='utf8')
    if len(rel.parts) == 1 or rel.parts[0] == 'blog':
        s = fr_page(rel.name, s)
    s = s.replace('</head>', '<link rel="stylesheet" href="/rouge.css"/></head>', 1)
    p.write_text(s, encoding='utf8')

(out / 'rouge.css').write_text('''/* Revue client : changements en rouge (jamais en production) */
:root{--rg:#E10600}
.rg{outline:3px solid var(--rg)!important;outline-offset:6px;border-radius:12px}
.rg-tag{display:block;width:fit-content;max-width:100%;margin:0 0 14px;background:var(--rg);color:#fff;font:600 13px/1.35 Inter,system-ui,sans-serif;padding:6px 12px;border-radius:8px;letter-spacing:.01em;text-transform:none}
.vid-home .rg-tag{margin-inline:auto}
.rg-mob,.rg-mobonly{display:none}.rg-mobonly{margin-inline:16px}
@media(max-width:700px){.rg-mobonly{display:block}}
@media(max-width:1100px){.rg-mob{display:block;position:absolute;left:12px;right:12px;top:calc(var(--hdr-h,60px) + 52px);z-index:90;font-size:12px;max-width:none}}
.rg-t{color:var(--rg)!important;font-weight:800;background:rgba(255,255,255,.92);border-radius:6px;padding:1px 6px}
.ps-ic{outline:3px solid var(--rg);outline-offset:3px}
.rg-removed{margin:28px auto 0;max-width:760px;border:3px dashed var(--rg);border-radius:12px;padding:14px 18px;color:var(--rg);font:500 15px/1.5 Inter,system-ui,sans-serif;text-align:left}
.rg-removed b{background:var(--rg);color:#fff;border-radius:6px;padding:1px 8px;margin-right:6px}
''', encoding='utf8')

(out / 'Ouvrir.command').write_text('#!/bin/bash\ncd "$(dirname "$0")"\n(sleep 1.5; open http://localhost:3010/) &\nnode dev-server.mjs 3010\n', encoding='utf8')
(out / 'Ouvrir.command').chmod(0o755)
print('Copie rouge générée :', out)
