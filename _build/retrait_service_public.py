#!/usr/bin/env python3 -I
"""Retrait des mentions répétées du service public de la Ville de Genève / de la gratuité.
Une seule mention est conservée : la section « Le Service Public des Pompes Funèbres de la Ville de Genève » de l'article de blog sur la prévoyance. Idempotent."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
L = ['', 'en/', 'de/', 'it/', 'es/', 'pt/']
TEASER = {
 '': "Comment organiser et financer vos obsèques à l'avance : tarifs bloqués dès la souscription, démarches et conseils des pompes funèbres Murith.",
 'en/': "How to organise and pay for your funeral in advance: prices fixed at signing, step-by-step guidance and advice from Murith funeral directors.",
 'de/': "So organisieren und finanzieren Sie Ihre Bestattung im Voraus: Preise ab Vertragsabschluss garantiert, Beratung und Begleitung durch Murith.",
 'it/': "Come organizzare e finanziare in anticipo le proprie esequie: prezzi bloccati alla sottoscrizione, passi da seguire e consigli di Pompe Funebri Murith.",
 'es/': "Cómo organizar y financiar sus exequias por adelantado: precios bloqueados desde la contratación, gestiones y consejos de las pompas fúnebres Murith.",
 'pt/': "Como organizar e financiar as suas exéquias com antecedência: preços fixos desde a subscrição, diligências e conselhos da Murith.",
}
ART_DESC = {
 '': "Prévoyance funéraire à Genève : comment organiser et financer vos obsèques à l'avance, tarifs bloqués dès la souscription, démarches et conseils de la Maison Murith.",
 'en/': "Funeral pre-planning in Geneva: how to organise and pay for your funeral in advance, prices fixed at signing, step-by-step guidance from Maison Murith.",
 'de/': "Bestattungsvorsorge in Genf: So organisieren und finanzieren Sie Ihre Bestattung im Voraus – Preise ab Vertragsabschluss garantiert, mit Beratung der Maison Murith.",
 'it/': "Previdenza funeraria a Ginevra: come organizzare e finanziare in anticipo le proprie esequie, prezzi bloccati alla sottoscrizione, consigli della Maison Murith.",
 'es/': "Previsión funeraria en Ginebra: cómo organizar y financiar sus exequias por adelantado, precios bloqueados desde la contratación y consejos de la Maison Murith.",
 'pt/': "Previdência funerária em Genebra: como organizar e financiar as suas exéquias com antecedência, preços fixos desde a subscrição e conselhos da Maison Murith.",
}
GUIDE = {'': "Nous vous guidons pas à pas.", 'en/': "We guide you step by step.", 'de/': "Wir begleiten Sie Schritt für Schritt.", 'it/': "Vi guidiamo passo dopo passo.", 'es/': "Le guiamos paso a paso.", 'pt/': "Guiamo-lo passo a passo."}
GE_H3 = {'': "Genève et la Maison Murith", 'en/': "Geneva and Maison Murith", 'de/': "Genf und die Maison Murith", 'it/': "Ginevra e la Maison Murith", 'es/': "Ginebra y la Maison Murith", 'pt/': "Genebra e a Maison Murith"}
changed = []
def rw(path, fn):
    p = root / path
    s = p.read_text(encoding='utf8'); n = fn(s)
    if n != s: p.write_text(n, encoding='utf8'); changed.append(path)
def p_with(s, *keys):
    return [m for m in re.finditer(r'<p>(?:(?!</p>).)*</p>', s, re.S) if all(k in m.group(0) for k in keys)]

for l in L:
    # 1) cartes d'articles (accueil, blog, articles) : résumé neutre
    def teaser(s, l=l):
        for m in reversed(p_with(s, '1866', '2014')):
            s = s[:m.start()] + '<p>' + TEASER[l] + '</p>' + s[m.end():]
        return s
    for f in ['index.html', 'blog.html', 'blog/cout-rapatriement-corps.html', 'blog/deces-proche-suisse-10-etapes.html']:
        rw(l + f, teaser)

    # 2) article « prévoyance funéraire à Genève » : une seule mention (la section dédiée), meta neutres
    def art(s, l=l):
        ps = p_with(s, '1866')
        if len(ps) == 3:                                   # intro, section dédiée (conservée), conclusion
            for m in (ps[2], ps[0]): s = s[:m.start()] + s[m.end():]
        d = re.search(r'<meta content="([^"]*)" name="description"/>', s).group(1)
        if '2014' in d: s = s.replace(d, ART_DESC[l])
        return s
    rw(l + 'blog/prevoyance-funeraire-geneve.html', art)

    # 3) article « décès d'un proche » : ligne du tableau, aides, section Ville, colonne service municipal
    def dec(s, l=l):
        # a) ligne « Ville de Genève » du comparatif des prestataires (2e ligne du 1er tableau)
        t = re.search(r'<table>.*?</table>', s, re.S)
        rows = re.findall(r'<tr>.*?</tr>', t.group(0), re.S)
        if len(rows) == 5 and 'tbody' in t.group(0):
            new = t.group(0).replace(rows[2], '', 1)
            s = s.replace(t.group(0), new, 1)
        # b) « Aides et gratuités » : titre + 2 paragraphes jusqu'à la liste suivante
        s = re.sub(r'<h3>[^<]*(?:gratuit|Gratuit|free|Free|kostenlos|Gratis|gratuidad|gratuidade|Gratuit)[^<]*</h3><p>.*?</p><p>.*?</p>(?=<ol>)', '', s, count=1, flags=re.S)
        # c) section « service municipal historique » : on ne garde que la phrase sur Murith
        m = re.search(r'<h3><strong>([^<]*)</strong></h3><p>((?:(?!</p>).)*1866(?:(?!</p>).)*)</p>', s, re.S)
        if m:
            body = m.group(2); k = body.find('<strong>')
            s = s[:m.start()] + f'<h3><strong>{GE_H3[l]}</strong></h3><p>' + body[k:] + '</p>' + s[m.end():]
        # d) colonne « Service municipal » du tableau des cantons
        def drop_col(mt):
            tb = mt.group(0)
            if '1866' not in tb: return tb
            return re.sub(r'<(td|th)[^>]*>(?:(?!</\1>).)*</\1>(</tr>)', r'\2', tb, flags=re.S).replace('(1866)', '')
        s = re.sub(r'<table>.*?</table>', drop_col, s, flags=re.S)
        s = re.sub(r'(Gratuité des obsèques de base pour les résidents / |Free basic funeral for residents / )', '', s)
        return s
    rw(l + 'blog/deces-proche-suisse-10-etapes.html', dec)

    # 4) page prévoyance : méta sans la Ville + question FAQ retirée (HTML + JSON-LD)
    def prev(s, l=l):
        for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            mm = re.search(r'<meta content="([^"]*)" ' + re.escape(attr) + r'/>', s)
            if mm and '2014' in mm.group(1):
                old = mm.group(1); sents = re.split(r'(?<=[.:]) ', old)
                keep = [x for x in re.split(r'(?<=\.) ', old) if '2014' not in x]
                new = ' '.join(keep) + ' ' + GUIDE[l]
                s = s.replace(old, new)
        s = re.sub(r',\{"@type":"Question","name":"[^"]*","acceptedAnswer":\{"@type":"Answer","text":"[^"]*2014[^"]*"\}\}', '', s)
        s = re.sub(r'<details><summary>(?:(?!</details>).)*?</summary><div class="ans"><p><b>[^<]*2014[^<]*</b>.*?</details>', '', s, count=1, flags=re.S)
        return s
    rw(l + 'prevoyance-funeraire.html', prev)

# 5) pied de page : le lien « Pompes funèbres Ville de Genève » (2e élément des sujets d'information)
for p in sorted(root.rglob('*.html')):
    if any(x in p.parts for x in ('node_modules', '_archive-wix', '_img-src')): continue
    s = p.read_text(encoding='utf8')
    m = re.search(r'(<div class="container foot-topics">.*?<ul>)(<li>.*?</li>)(<li>.*?</li>)(<li>.*?</li>)', s, re.S)
    if m and re.search(r'Ville|City|Stadt|Città|Ciudad|Cidade', m.group(3)):
        p.write_text(s[:m.start(3)] + s[m.end(3):], encoding='utf8'); changed.append(str(p.relative_to(root)))
print('modifiés :', len(changed))
