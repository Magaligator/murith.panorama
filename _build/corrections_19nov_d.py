#!/usr/bin/env python3 -I
"""Corrections client du 2026-11-19, partie 4 (6 langues, idempotent) :
page « Nos conseillers funéraires » : 4 fiches réelles (photo, spécialité, texte, langues) d'après
« Notre équipe de direction version COURTE.docx » à la place des fiches à compléter."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
L = ['', 'en/', 'de/', 'it/', 'es/', 'pt/']
problems = []; changed = []

# (nom, fichier photo, [langues]) ; ordre du document client
PEOPLE = [
 ('Philippe Murith', 'conseiller-philippe-murith', ['fr', 'en', 'es']),
 ('Jacques Murith', 'conseiller-jacques-murith', ['fr', 'en', 'es', 'de']),
 ('Jean-Marc Murith', 'conseiller-jean-marc-murith', ['fr', 'es', 'en', 'de']),
 ('Jimmy Nydegger', 'conseiller-jimmy-nydegger', ['fr', 'en']),
]
LANG = {
 '':    dict(fr='Français', en='Anglais', es='Espagnol', de='Allemand'),
 'en/': dict(fr='French', en='English', es='Spanish', de='German'),
 'de/': dict(fr='Französisch', en='Englisch', es='Spanisch', de='Deutsch'),
 'it/': dict(fr='Francese', en='Inglese', es='Spagnolo', de='Tedesco'),
 'es/': dict(fr='Francés', en='Inglés', es='Español', de='Alemán'),
 'pt/': dict(fr='Francês', en='Inglês', es='Espanhol', de='Alemão'),
}
TXT = {  # par langue : [(spécialité, présentation)] dans l'ordre de PEOPLE
 '': [
  ("Droits et accompagnement des familles", "Spécialisé dans les droits des proches, l'accompagnement des familles, le respect des droits des personnes LGBTQ+, la gestion des conflits et la protection de la personnalité des collaborateurs."),
  ("Administration, finances et engagement environnemental", "Responsable financier et chef de service, chargé de la gestion administrative, de la politique environnementale et du développement de pratiques funéraires écoresponsables."),
  ("Prévoyance funéraire et relations extérieures", "Spécialisé dans la prévoyance funéraire, la gestion des contrats, la communication et les relations publiques et institutionnelles. Formateur officiel au sein de l'Association suisse des services funéraires (ASSF)."),
  ("Informatique et coordination", "Spécialisé dans les outils informatiques, la gestion numérique des dossiers, l'assistance administrative et la coordination des services funéraires."),
 ],
 'en/': [
  ("Family rights and support", "Specialised in the rights of relatives, family support, respect for the rights of LGBTQ+ people, conflict management and the protection of staff members' personal integrity."),
  ("Administration, finance and environmental commitment", "Financial manager and head of department, in charge of administrative management, environmental policy and the development of eco-responsible funeral practices."),
  ("Funeral pre-planning and external relations", "Specialised in funeral pre-planning, contract management, communication, and public and institutional relations. Official trainer at the Swiss Association of Funeral Services (SVB)."),
  ("IT and coordination", "Specialised in IT tools, digital file management, administrative support and the coordination of funeral services."),
 ],
 'de/': [
  ("Rechte und Begleitung der Familien", "Spezialisiert auf die Rechte der Angehörigen, die Begleitung von Familien, die Achtung der Rechte von LGBTQ+-Personen, das Konfliktmanagement und den Persönlichkeitsschutz der Mitarbeitenden."),
  ("Administration, Finanzen und Umweltengagement", "Finanzverantwortlicher und Abteilungsleiter, zuständig für die administrative Führung, die Umweltpolitik und die Entwicklung umweltverantwortlicher Bestattungspraktiken."),
  ("Bestattungsvorsorge und externe Beziehungen", "Spezialisiert auf die Bestattungsvorsorge, die Vertragsverwaltung, die Kommunikation sowie die öffentlichen und institutionellen Beziehungen. Offizieller Ausbilder beim Schweizerischen Verband der Bestattungsdienste (SVB)."),
  ("Informatik und Koordination", "Spezialisiert auf IT-Werkzeuge, die digitale Aktenführung, die administrative Unterstützung und die Koordination der Bestattungsdienste."),
 ],
 'it/': [
  ("Diritti e accompagnamento delle famiglie", "Specializzato nei diritti dei familiari, nell'accompagnamento delle famiglie, nel rispetto dei diritti delle persone LGBTQ+, nella gestione dei conflitti e nella tutela della personalità dei collaboratori."),
  ("Amministrazione, finanze e impegno ambientale", "Responsabile finanziario e capo servizio, incaricato della gestione amministrativa, della politica ambientale e dello sviluppo di pratiche funerarie ecosostenibili."),
  ("Previdenza funeraria e relazioni esterne", "Specializzato nella previdenza funeraria, nella gestione dei contratti, nella comunicazione e nelle relazioni pubbliche e istituzionali. Formatore ufficiale presso l'Associazione Svizzera dei servizi funerari (ASSF)."),
  ("Informatica e coordinamento", "Specializzato negli strumenti informatici, nella gestione digitale dei fascicoli, nell'assistenza amministrativa e nel coordinamento dei servizi funerari."),
 ],
 'es/': [
  ("Derechos y acompañamiento de las familias", "Especializado en los derechos de los allegados, el acompañamiento de las familias, el respeto de los derechos de las personas LGBTQ+, la gestión de conflictos y la protección de la personalidad de los colaboradores."),
  ("Administración, finanzas y compromiso medioambiental", "Responsable financiero y jefe de servicio, encargado de la gestión administrativa, de la política medioambiental y del desarrollo de prácticas funerarias ecorresponsables."),
  ("Previsión funeraria y relaciones externas", "Especializado en la previsión funeraria, la gestión de contratos, la comunicación y las relaciones públicas e institucionales. Formador oficial de la Asociación Suiza de Servicios Funerarios (ASSF)."),
  ("Informática y coordinación", "Especializado en herramientas informáticas, la gestión digital de expedientes, la asistencia administrativa y la coordinación de los servicios funerarios."),
 ],
 'pt/': [
  ("Direitos e acompanhamento das famílias", "Especializado nos direitos dos familiares, no acompanhamento das famílias, no respeito pelos direitos das pessoas LGBTQ+, na gestão de conflitos e na proteção da personalidade dos colaboradores."),
  ("Administração, finanças e compromisso ambiental", "Responsável financeiro e chefe de serviço, encarregado da gestão administrativa, da política ambiental e do desenvolvimento de práticas funerárias ecorresponsáveis."),
  ("Previdência funerária e relações externas", "Especializado na previdência funerária, na gestão de contratos, na comunicação e nas relações públicas e institucionais. Formador oficial da Associação Suíça dos Serviços Funerários (ASSF)."),
  ("Informática e coordenação", "Especializado nas ferramentas informáticas, na gestão digital de processos, na assistência administrativa e na coordenação dos serviços funerários."),
 ],
}
SUB = {  # titre de l'équipe, au-dessus des fiches
 '': "Notre équipe de direction et d'administration",
 'en/': "Our management and administration team",
 'de/': "Unser Führungs- und Verwaltungsteam",
 'it/': "Il nostro team di direzione e amministrazione",
 'es/': "Nuestro equipo de dirección y administración",
 'pt/': "A nossa equipa de direção e administração",
}
ALT = {
 '': "{n}, {r} – Maison Murith, Genève", 'en/': "{n}, {r} – Maison Murith, Geneva",
 'de/': "{n}, {r} – Maison Murith, Genf", 'it/': "{n}, {r} – Maison Murith, Ginevra",
 'es/': "{n}, {r} – Maison Murith, Ginebra", 'pt/': "{n}, {r} – Maison Murith, Genebra",
}
esc = lambda t: t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def page(s, l):
    m = re.search(r'(<div class="s-item"><article class="card adv".*?</article></div>)(?=<div class="s-item">|</div><div class="s-ctrl">)', s, re.S)
    if not m: problems.append(l + 'conseillers.html :: fiche modèle introuvable'); return s
    tpl = re.search(r'<article class="card adv".*?</article>', m.group(1), re.S).group(0)
    a = s.index('<div class="s-item"><article class="card adv"'); b = s.index('</div><div class="s-ctrl">', a)
    items = []
    for (name, f, langs), (role, bio) in zip(PEOPLE, TXT[l]):
        c = tpl.replace(' data-placeholder="1"', '')
        img = (f'<div class="adv-photo"><img alt="{esc(ALT[l].format(n=name, r=role[0].lower() + role[1:]))}" decoding="async" height="960" loading="lazy" '
               f'sizes="(max-width:700px) 80vw, 25vw" src="/img/{f}-960.webp" srcset="/img/{f}-480.webp 480w, /img/{f}-960.webp 960w" width="960"/></div>')
        c, n1 = re.subn(r'<div class="adv-photo">.*?</div>(?=<div class="adv-body">)', lambda _: img, c, count=1, flags=re.S)
        c, n2 = re.subn(r'<h3>[^<]*</h3>', lambda _: f'<h3>{esc(name)}</h3>', c, count=1)
        c, n3 = re.subn(r'<p class="adv-bio">[^<]*</p>', lambda _: f'<p class="adv-bio">{esc(bio)}</p>', c, count=1)
        dds = [''.join(f'<span class="chipl">{LANG[l][k]}</span>' for k in langs), f'<span class="chipl solid">{esc(role)}</span>']
        it = iter(dds)
        c, n4 = re.subn(r'(<dd>).*?(</dd>)', lambda mm: mm.group(1) + next(it) + mm.group(2), c, flags=re.S)
        if (n1, n2, n3, n4) != (1, 1, 1, 2): problems.append(f'{l}conseillers.html :: {name} {(n1, n2, n3, n4)}')
        items.append(f'<div class="s-item">{c}</div>')
    s = s[:a] + ''.join(items) + s[b:]
    if 'class="adv-sub"' not in s:
        s = s.replace('<div class="slider per-4" data-slider="">', f'<h3 class="adv-sub" style="text-align:center;margin-bottom:clamp(20px,3vw,36px)">{esc(SUB[l])}</h3><div class="slider per-4" data-slider="">', 1)
        if 'class="adv-sub"' not in s: problems.append(l + 'conseillers.html :: slider introuvable')
    return s

for l in L:
    p = root / f'{l}conseillers.html'
    s = p.read_text(encoding='utf8'); n = page(s, l)
    if n != s: p.write_text(n, encoding='utf8'); changed.append(str(p.relative_to(root)))

if __name__ == '__main__':
    print('modifiés :', len(changed), changed); print('problèmes :', len(problems))
    for p in problems: print('  !', p)
