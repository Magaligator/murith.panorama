#!/usr/bin/env python3 -I
"""Ligne discrète « Partenaires et affiliations » dans le pied de page de toutes les pages (5 langues). Idempotent."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
T = {
 'fr': ('Partenaires et affiliations', 'Des partenaires de confiance à nos côtés',
        "Nous travaillons avec Exit Suisse romande et la Résidence de la Champagne, et nous sommes membres de l'Association Suisse des services funéraires.",
        ('Partenaire', 'Partenaire', 'Membre de'), 'Logo Exit Suisse romande', 'Logo Résidence de la Champagne EMS', 'Logo Association Suisse des services funéraires', 'Association Suisse des services funéraires (ASSF)', 'https://bestatter.ch/fr/'),
 'en': ('Partners and affiliations', 'Trusted partners by our side',
        'We work with Exit Suisse romande and the Résidence de la Champagne, and we are members of the Swiss Association of Funeral Services.',
        ('Partner', 'Partner', 'Member of'), 'Exit Suisse romande logo', 'Résidence de la Champagne nursing home logo', 'Swiss Association of Funeral Services logo', 'Swiss Association of Funeral Services (SVB)', 'https://bestatter.ch/fr/'),
 'de': ('Partner und Mitgliedschaften', 'Vertrauensvolle Partner an unserer Seite',
        'Wir arbeiten mit Exit Suisse romande und der Résidence de la Champagne zusammen und sind Mitglied des Schweizerischen Verbands der Bestattungsdienste.',
        ('Partner', 'Partner', 'Mitglied von'), 'Logo Exit Suisse romande', 'Logo Résidence de la Champagne Pflegeheim', 'Logo Schweizerischer Verband der Bestattungsdienste', 'Schweizerischer Verband der Bestattungsdienste (SVB)', 'https://bestatter.ch/fr/'),
 'es': ('Socios y afiliaciones', 'Socios de confianza a nuestro lado',
        'Trabajamos con Exit Suisse romande y la Résidence de la Champagne, y somos miembros de la Asociación Suiza de Servicios Funerarios.',
        ('Socio', 'Socio', 'Miembro de'), 'Logotipo de Exit Suisse romande', 'Logotipo de la Résidence de la Champagne', 'Logotipo de la Asociación Suiza de Servicios Funerarios', 'Asociación Suiza de Servicios Funerarios', 'https://bestatter.ch/fr/'),
 'pt': ('Parceiros e filiações', 'Parceiros de confiança ao nosso lado',
        'Trabalhamos com a Exit Suisse romande e a Résidence de la Champagne, e somos membros da Associação Suíça dos Serviços Funerários.',
        ('Parceiro', 'Parceiro', 'Membro de'), 'Logótipo da Exit Suisse romande', 'Logótipo da Résidence de la Champagne', 'Logótipo da Associação Suíça dos Serviços Funerários', 'Associação Suíça dos Serviços Funerários', 'https://bestatter.ch/fr/'),
}
LBL = {'fr': 'Partenaires et affiliations', 'en': 'Partners and affiliations', 'de': 'Partner und Mitgliedschaften', 'es': 'Socios y afiliaciones', 'pt': 'Parceiros e filiações'}
def row(lang):
    eb, h2, lead, caps, a1, a2, a3, n3, u3 = T[lang]
    def li(img, w, h, alt, title, href=None):
        im = f'<img alt="{alt}" decoding="async" height="{h}" loading="lazy" src="/img/partenaires/{img}" width="{w}"/>'
        if href: return f'<li><a href="{href}" rel="noopener" target="_blank" title="{title}">{im}</a></li>'
        return f'<li><span title="{title}">{im}</span></li>'
    return ('<div class="container foot-partners" data-fp=""><span class="fp-t">' + LBL[lang] + '</span><ul>'
            + li('exit-suisse-romande.png', 318, 159, a1, 'Exit Suisse romande', 'https://www.exit-romandie.ch/')
            + li('residence-de-la-champagne.jpg', 480, 213, a2, 'Résidence de la Champagne (EMS)')
            + li('assf.svg', 855, 305, a3, n3, u3) + '</ul></div>\n')
n = 0
for p in root.rglob('*.html'):
    if p.relative_to(root).parts[0] in ('_archive-wix', '_build', '_img-src', '_src', 'docs', '.git'): continue
    rel = p.relative_to(root).parts
    lang = rel[0] if rel[0] in T else 'fr'
    h = p.read_text(encoding='utf8'); o = h
    h = re.sub(r'<section class="section alt partners".*?</section>\n?', '', h, flags=re.S)
    if 'data-fp' not in h:
        i = h.find('<div class="container foot-topics">')
        if i < 0: continue
        h = h[:i] + row(lang) + h[i:]
    if h != o: p.write_text(h, encoding='utf8'); n += 1
print('pages modifiées :', n)
