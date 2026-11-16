#!/usr/bin/env python3 -I
"""Ajoute le bandeau « Partenaires et affiliations » (accueil + Notre histoire, 5 langues). Idempotent."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
T = {
 'fr': ('Partenaires et affiliations', 'Des partenaires de confiance à nos côtés',
        "Nous travaillons avec Exit Suisse romande et la Résidence de la Champagne, et nous sommes membres de l'Association Suisse des services funéraires.",
        ('Partenaire', 'Partenaire', 'Membre de'), 'Logo Exit Suisse romande', 'Logo Résidence de la Champagne EMS', 'Logo Association Suisse des services funéraires', 'Association Suisse des services funéraires', 'https://bestatter.ch/fr/'),
 'en': ('Partners and affiliations', 'Trusted partners by our side',
        'We work with Exit Suisse romande and the Résidence de la Champagne, and we are members of the Swiss Association of Funeral Services.',
        ('Partner', 'Partner', 'Member of'), 'Exit Suisse romande logo', 'Résidence de la Champagne nursing home logo', 'Swiss Association of Funeral Services logo', 'Swiss Association of Funeral Services', 'https://bestatter.ch/fr/'),
 'de': ('Partner und Mitgliedschaften', 'Vertrauensvolle Partner an unserer Seite',
        'Wir arbeiten mit Exit Suisse romande und der Résidence de la Champagne zusammen und sind Mitglied des Schweizerischen Verbands der Bestattungsdienste.',
        ('Partner', 'Partner', 'Mitglied von'), 'Logo Exit Suisse romande', 'Logo Résidence de la Champagne Pflegeheim', 'Logo Schweizerischer Verband der Bestattungsdienste', 'Schweizerischer Verband der Bestattungsdienste', 'https://bestatter.ch/fr/'),
 'es': ('Socios y afiliaciones', 'Socios de confianza a nuestro lado',
        'Trabajamos con Exit Suisse romande y la Résidence de la Champagne, y somos miembros de la Asociación Suiza de Servicios Funerarios.',
        ('Socio', 'Socio', 'Miembro de'), 'Logotipo de Exit Suisse romande', 'Logotipo de la Résidence de la Champagne', 'Logotipo de la Asociación Suiza de Servicios Funerarios', 'Asociación Suiza de Servicios Funerarios', 'https://bestatter.ch/fr/'),
 'pt': ('Parceiros e filiações', 'Parceiros de confiança ao nosso lado',
        'Trabalhamos com a Exit Suisse romande e a Résidence de la Champagne, e somos membros da Associação Suíça dos Serviços Funerários.',
        ('Parceiro', 'Parceiro', 'Membro de'), 'Logótipo da Exit Suisse romande', 'Logótipo da Résidence de la Champagne', 'Logótipo da Associação Suíça dos Serviços Funerários', 'Associação Suíça dos Serviços Funerários', 'https://bestatter.ch/fr/'),
}
def block(lang):
    eb, h2, lead, caps, a1, a2, a3, n3, u3 = T[lang]
    def card(img, w, h, alt, cap, name, href=None):
        im = f'<img alt="{alt}" decoding="async" height="{h}" loading="lazy" src="/img/partenaires/{img}" width="{w}"/>'
        inner = f'<span class="pt-logo">{im}</span><span class="pt-cap">{cap}</span><b class="pt-name">{name}</b>'
        if href:
            return f'<li><a class="pt-card" href="{href}" rel="noopener" target="_blank">{inner}</a></li>'
        return f'<li><div class="pt-card">{inner}</div></li>'
    return ('<section class="section alt partners" data-partners="" id="partenaires"><div class="container">'
            f'<div class="sec-head reveal"><p class="eyebrow">{eb}</p><h2>{h2}</h2><p class="lead">{lead}</p></div>'
            '<ul class="pt-list reveal">'
            + card('exit-suisse-romande.png', 318, 159, a1, caps[0], 'Exit Suisse romande', 'https://www.exit-romandie.ch/')
            + card('residence-de-la-champagne.jpg', 480, 213, a2, caps[1], 'Résidence de la Champagne (EMS)')
            + card('assf.svg', 1350, 450, a3, caps[2], n3, u3)
            + '</ul></div></section>\n')
SD = {'fr': '', 'en': 'en/', 'de': 'de/', 'es': 'es/', 'pt': 'pt/'}
n = 0
for lang, d in SD.items():
    for page in ('index.html', 'notre-histoire.html'):
        p = root / d / page
        h = p.read_text(encoding='utf8')
        if 'data-partners' in h: continue
        # insérer juste avant la dernière section « tight » (bandeau d'appel) ou le pied de page
        i = h.rfind('<section class="section tight">')
        if i < 0: i = h.find('<footer class="site-footer">')
        h = h[:i] + block(lang) + h[i:]
        if page == 'index.html' and '"memberOf"' not in h:
            h = h.replace('"hasMap"', '"memberOf":{"@type":"Organization","name":"Association Suisse des services funéraires","url":"https://bestatter.ch/fr/"},"hasMap"', 1)
        p.write_text(h, encoding='utf8'); n += 1
print('pages modifiées :', n)
