# Corrections EN/DE/ES/PT alignées sur les corrections FR (idiome « tous les saints », essences de bois, nom des HUG…)
import re, os, glob
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'panorama') + '/'
def pat(old):
    parts = []
    for ch in old:
        if ch in "'’": parts.append("['’]")
        elif ch.isspace(): parts.append(r'\s+')
        else: parts.append(re.escape(ch))
    return re.compile(''.join(parts))
def sub(lg, files, old, new, red=False):
    n = 0
    for f in files:
        p = f'{P}{lg}/{f}'; h = open(p, encoding='utf-8').read(); rx = pat(old)
        c = len(rx.findall(h))
        if c:
            h = rx.sub(lambda m: f'<span class="seo-new">{new}</span>' if red else new, h); open(p, 'w', encoding='utf-8').write(h); n += c
    print(lg, 'ok' if n else '!! introuvable', old[:55], n)
ALL = [os.path.basename(x) for x in glob.glob(P + 'en/*.html')]
O = ['obseques.html']
sub('en', O, "We work with the church, the mosque, the temple, the synagogue and our partners in the name of all the saints.", "We work with churches, mosques, temples, synagogues and our partners, with respect for all traditions.", True)
sub('en', O, "an authentic reflection of them: songs they loved", "an authentic reflection of your loved one: songs they loved", True)
sub('en', O, "oak, pine, cherry, mahogany and more", "fir, oak, ash, walnut, mahogany, frake and more", True)
sub('en', ALL, "Cantonal University Hospital (HUG)", "Geneva University Hospitals (HUG)")
sub('en', ALL, "Cantonal Hospital (HUG)", "Geneva University Hospitals (HUG)")
sub('en', ALL, "fir, poplar, oak", "fir, oak")
sub('de', O, "Wir arbeiten mit der Kirche, der Moschee, dem Tempel, der Synagoge und unseren Partnern zusammen.", "Wir arbeiten mit Kirchen, Moscheen, Tempeln, Synagogen und unseren Partnern zusammen – im Respekt vor allen Traditionen.", True)
sub('de', O, "Eiche, Kiefer, Kirsche, Mahagoni und weiteren", "Tanne, Eiche, Esche, Nussbaum, Mahagoni, Frake und weiteren", True)
for a in ["dem Kantonsspital Genf (HUG)", "dem Kantonsspital (HUG)", "dem Universitätsspital (HUG)"]:
    sub('de', ALL, a, "dem Universitätsspital Genf (HUG)")
sub('de', ALL, "Tanne, Pappel, Eiche", "Tanne, Eiche")
sub('es', O, "Colaboramos con la iglesia, la mezquita, el templo, la sinagoga y nuestros socios, en nombre de todos los santos.", "Colaboramos con iglesias, mezquitas, templos, sinagogas y nuestros socios, con respeto a todas las tradiciones.", True)
sub('es', O, "roble, pino, cerezo, caoba y otras más", "abeto, roble, fresno, nogal, caoba, frake y otras más", True)
for a in ["frente al Hospital Cantonal Universitario (HUG)", "frente al Hospital Cantonal (HUG)", "frente al Hospital Universitario de Ginebra (HUG)", "frente al hospital cantonal de Ginebra (HUG)"]:
    sub('es', ALL, a, "frente a los Hospitales Universitarios de Ginebra (HUG)")
sub('es', ALL, "abeto, álamo, roble", "abeto, roble")
sub('pt', O, "Colaboramos com a igreja, a mesquita, o templo, a sinagoga e os nossos parceiros, em nome de todos os santos.", "Colaboramos com igrejas, mesquitas, templos, sinagogas e os nossos parceiros, no respeito por todas as tradições.", True)
sub('pt', O, "carvalho, pinho, cerejeira, mogno e outras ainda", "abeto, carvalho, freixo, nogueira, mogno, frake e outras ainda", True)
for a in ["em frente ao Hospital Cantonal Universitário (HUG)", "em frente ao Hospital Cantonal (HUG)", "em frente ao Hospital Universitário de Genebra (HUG)", "em frente ao hospital cantonal de Genebra (HUG)"]:
    sub('pt', ALL, a, "em frente aos Hospitais Universitários de Genebra (HUG)")
sub('pt', ALL, "abeto, choupo, carvalho", "abeto, carvalho")
