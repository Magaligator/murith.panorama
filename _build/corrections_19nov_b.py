#!/usr/bin/env python3 -I
"""Corrections client du 2026-11-19, partie 2 (6 langues, idempotent) : article rapatriement, article « décès d'un proche »,
phrase « formation / Brevet fédéral » dans les passages « pourquoi choisir Murith »."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
L = ['', 'en/', 'de/', 'it/', 'es/', 'pt/']
changed = set(); problems = []

def rw(path, fn):
    p = root / path
    if not p.exists(): problems.append(f'absent {path}'); return
    s = p.read_text(encoding='utf8'); n = fn(s)
    if n != s: p.write_text(n, encoding='utf8'); changed.add(path)
def must(s, old, new, label, path=''):
    if old in s: return s.replace(old, new, 1)
    if new in s: return s
    problems.append(f'{path} :: introuvable : {label}'); return s
def rx(s, pattern, repl, label, path='', flags=re.S):
    n, k = re.subn(pattern, repl, s, count=1, flags=flags)
    if k == 0: problems.append(f'{path} :: motif introuvable : {label}')
    return n

# ----------------------------------------------------------------- phrase « formation / Brevet fédéral »
ASSF = {
 '': "Murith forme aussi les entrepreneurs de pompes funèbres de demain, dans toute la Suisse romande, auprès de l’Association Suisse des Services Funéraires (ASSF), notamment pour l’obtention du Brevet Fédéral : un gage de sûreté et de clarté pour des obsèques réalisées selon les règles de l’art (seule entreprise privée à Genève détentrice du Brevet Fédéral).",
 'en/': "Murith also trains the funeral directors of tomorrow throughout French-speaking Switzerland, with the Swiss Association of Funeral Services (SVB), notably for the Federal Diploma: a guarantee of reliability and clarity for funerals carried out to the highest professional standards (the only private company in Geneva holding the Federal Diploma).",
 'de/': "Murith bildet zudem die Bestatterinnen und Bestatter von morgen in der ganzen Westschweiz beim Schweizerischen Verband der Bestattungsdienste (SVB) aus, insbesondere für den Erwerb des eidgenössischen Fachausweises: eine Garantie für Verlässlichkeit und Klarheit bei Bestattungen nach allen Regeln der Kunst (das einzige private Unternehmen in Genf mit eidgenössischem Fachausweis).",
 'it/': "Murith forma inoltre gli impresari di pompe funebri di domani, in tutta la Svizzera romanda, presso l'Associazione Svizzera dei servizi funerari (ASSF), in particolare per il conseguimento dell'attestato professionale federale: una garanzia di affidabilità e chiarezza per esequie svolte a regola d'arte (unica impresa privata a Ginevra in possesso dell'attestato professionale federale).",
 'es/': "Murith forma además a los empresarios de servicios funerarios del mañana, en toda la Suiza romanda, a través de la Asociación Suiza de Servicios Funerarios (ASSF), en particular para la obtención del diploma federal: una garantía de seguridad y claridad para unos funerales realizados conforme a las reglas del arte (única empresa privada de Ginebra que posee el diploma federal).",
 'pt/': "A Murith forma também os empresários funerários de amanhã, em toda a Suíça romanda, junto da Associação Suíça dos Serviços Funerários (ASSF), nomeadamente para a obtenção do diploma federal: uma garantia de segurança e clareza para funerais realizados segundo as regras da arte (única empresa privada em Genebra detentora do diploma federal).",
}
LBL = {'': 'La formation :', 'en/': 'Training:', 'de/': 'Ausbildung:', 'it/': 'La formazione:', 'es/': 'La formación:', 'pt/': 'A formação:'}

# ----------------------------------------------------------------- tableaux : outils
def cells(row): return re.findall(r'<td[^>]*>.*?</td>', row, re.S)
def set_cell(row, i, text):
    cs = cells(row); c = cs[i]
    new = re.sub(r'>.*</td>$', '>' + text + '</td>', c, flags=re.S)
    return row.replace(c, new, 1)
def body_rows(tbl):
    b = re.search(r'<tbody>(.*?)</tbody>', tbl, re.S)
    return b, re.findall(r'<tr>.*?</tr>', b.group(1), re.S)
def tables(s): return list(re.finditer(r'<table.*?</table>', s, re.S))

VOLS = {'': 'Vols intercontinentaux', 'en/': 'Intercontinental flights', 'de/': 'Interkontinentalflüge', 'it/': 'Voli intercontinentali', 'es/': 'Vuelos intercontinentales', 'pt/': 'Voos intercontinentais'}
NOTE = {'': " selon la destination en Europe (jusqu'au sud de l'Italie)", 'en/': " depending on the destination in Europe (up to southern Italy)",
        'de/': " je nach Zielort in Europa (bis Süditalien)", 'it/': " a seconda della destinazione in Europa (fino al Sud Italia)",
        'es/': " según el destino en Europa (hasta el sur de Italia)", 'pt/': " consoante o destino na Europa (até ao sul de Itália)"}
STRAS = {'': "Homologation Accords de Strasbourg requise", 'en/': "Strasbourg Agreement approval required", 'de/': "Zulassung nach dem Strassburger Übereinkommen erforderlich",
         'it/': "Omologazione secondo gli Accordi di Strasburgo richiesta", 'es/': "Homologación según los Acuerdos de Estrasburgo requerida", 'pt/': "Homologação segundo os Acordos de Estrasburgo exigida"}
H1 = {'': "Sous 1h", 'en/': "Within 1h", 'de/': "Innert 1 Std.", 'it/': "Entro 1 ora", 'es/': "En menos de 1 h", 'pt/': "Em 1h"}
FAM = {'': "Famille / Pompes funèbres Murith", 'en/': "Family / Murith funeral services", 'de/': "Familie / Bestattungsinstitut Murith", 'it/': "Famiglia / Pompe funebri Murith", 'es/': "Familia / Servicios funerarios Murith", 'pt/': "Família / Serviços funerários Murith"}
CONS = {'': "Pompes funèbres Murith / Consulat", 'en/': "Murith funeral services / Consulate", 'de/': "Bestattungsinstitut Murith / Konsulat", 'it/': "Pompe funebri Murith / Consolato", 'es/': "Servicios funerarios Murith / Consulado", 'pt/': "Serviços funerários Murith / Consulado"}
TRANSIT = {'': "Transit’Air, partenaire Murith", 'en/': "Transit’Air, Murith partner", 'de/': "Transit’Air, Partner von Murith", 'it/': "Transit’Air, partner di Murith", 'es/': "Transit’Air, colaborador de Murith", 'pt/': "Transit’Air, parceiro da Murith"}
CEREM = {'': "Célébration à Genève avant le départ", 'en/': "Ceremony in Geneva before departure", 'de/': "Feier in Genf vor der Abreise", 'it/': "Celebrazione a Ginevra prima della partenza", 'es/': "Celebración en Ginebra antes de la salida", 'pt/': "Celebração em Genebra antes da partida"}
OLDWHY = {
 '': ("est l'une des entreprises de pompes funèbres les plus anciennes et les plus respectées de Genève.", "est l'entreprise de pompes funèbres la plus ancienne à Genève."),
 'en/': ("is one of the oldest and most respected funeral companies in Geneva.", "is the oldest funeral company in Geneva."),
 'de/': ("ist eines der ältesten und angesehensten Bestattungsunternehmen in Genf.", "ist das älteste Bestattungsunternehmen in Genf."),
 'it/': ("è una delle imprese di pompe funebri più antiche e rispettate di Ginevra.", "è l'impresa di pompe funebri più antica di Ginevra."),
 'es/': ("es una de las empresas funerarias más antiguas y respetadas de Ginebra.", "es la empresa funeraria más antigua de Ginebra."),
 'pt/': ("é uma das empresas funerárias mais antigas e mais respeitadas de Genebra.", "é a empresa funerária mais antiga de Genebra."),
}

def rapatriement(s, l):
    P = l + 'blog/cout-rapatriement-corps.html'
    T = tables(s)
    # --- tableau des coûts
    t0 = T[0].group(0); b, rows = body_rows(t0)
    if len(rows) == 5:
        r1, r2, r3 = rows[0], rows[1], rows[2]
        sp = ' ' if False else ' '
        r1 = set_cell(r1, 2, "2 500 - 3 500"); r1 = set_cell(r1, 3, re.sub(r'\d+', lambda m, it=iter(['1', '3']): next(it), cells(r1)[3].replace('</td>', '').split('>', 1)[1], count=2))
        r2 = set_cell(r2, 2, "6 500 - 8 500"); r2 = set_cell(r2, 3, re.sub(r'\d+', lambda m, it=iter(['2', '5']): next(it), cells(r2)[3].replace('</td>', '').split('>', 1)[1], count=2))
        r3 = set_cell(r3, 0, VOLS[l]); r3 = set_cell(r3, 2, "7 500 - 10 500")
        t0n = t0.replace(b.group(1), r1 + r2 + r3)
        s = s.replace(t0, t0n, 1)
    elif '6 500 - 8 500' not in s: problems.append(f'{P} :: tableau coûts ({len(rows)} lignes)')
    # --- comparaison des modes de transport
    T = tables(s); t1 = T[1].group(0); b, rows = body_rows(t1)
    if len(rows) == 5 and NOTE[l] not in t1:
        sep = ',' if l == 'en/' else ' '
        c1 = f"2{sep}500 - 5{sep}000 CHF"; c2 = f"800 - 5{sep}000 CHF{NOTE[l]}"
        rows[1] = set_cell(set_cell(rows[1], 1, c1), 2, c2)
        rows[4] = set_cell(rows[4], 2, STRAS[l])
        s = s.replace(t1, t1.replace(b.group(1), ''.join(rows)), 1)
    elif NOTE[l] not in s: problems.append(f'{P} :: tableau comparaison')
    # --- soins de conservation : 450 – 510 CHF
    if re.search(r'\b800\D{1,16}?2[ ,\u202f\u00a0]?500', s):
        s = re.sub(r'\b800(\D{1,16}?)2[ ,\u202f\u00a0]?500', r'450\g<1>510', s, count=1)
    elif '450' not in s: problems.append(f'{P} :: soins de conservation')
    # --- étapes du rapatriement
    T = tables(s); t2 = T[2].group(0); b, rows = body_rows(t2)
    if len(rows) == 7:
        resp_murith = re.sub(r'<[^>]+>', '', cells(rows[1])[2])
        rows[0] = set_cell(rows[0], 2, FAM[l])
        rows[1] = set_cell(rows[1], 3, H1[l])
        rows[3] = set_cell(rows[3], 2, CONS[l])
        rows[5] = set_cell(rows[5], 2, TRANSIT[l])
        rows[6] = set_cell(set_cell(rows[6], 1, CEREM[l]), 2, resp_murith)
        s = s.replace(t2, t2.replace(b.group(1), ''.join(rows)), 1)
    else: problems.append(f'{P} :: tableau étapes')
    # --- pourquoi choisir : la plus ancienne + HUG + formation / brevet
    o, n = OLDWHY[l]; s = must(s, o, n, 'la plus ancienne', P)
    if l == '': s = must(s, "en face de l'Hôpitaux universitaires de Genève", "en face des Hôpitaux universitaires de Genève", 'HUG', P)
    if ASSF[l] not in s:
        m = re.search(r'(<li>[^<]*(?:<a [^>]*>www\.murith\.ch</a>)[^<]*<br role="presentation"/></li></ul>)', s)
        if m: s = s[:m.start()] + '<li>' + ASSF[l] + '</li>' + s[m.start():]
        else: problems.append(f'{P} :: liste pourquoi choisir')
    return s
for l in L: rw(l + 'blog/cout-rapatriement-corps.html', lambda s, l=l: rapatriement(s, l))

# ----------------------------------------------------------------- article « décès d'un proche »
STARTS = {'': "Les frais d’obsèques débutent dès CHF 3’500.–, selon les prestations choisies.",
          'en/': "Funeral costs start from CHF 3,500, depending on the services chosen.",
          'de/': "Die Kosten einer Bestattung beginnen ab CHF 3’500.–, je nach gewählten Leistungen.",
          'it/': "Le spese per le esequie partono da CHF 3’500.–, a seconda delle prestazioni scelte.",
          'es/': "Los gastos de los funerales comienzan desde 3 500 CHF, según las prestaciones elegidas.",
          'pt/': "Os custos de funerais começam a partir de 3 500 CHF, consoante as prestações escolhidas."}
EURO = {'': [("cercueils européens de qualité", "cercueils de qualité"), ("parmi notre gamme européenne :", "parmi notre gamme :")],
        'en/': [("quality European coffins", "quality coffins"), ("from our European range:", "from our range:")],
        'de/': [("hochwertige europäische Särge", "hochwertige Särge"), ("aus unserem europäischen Sortiment:", "aus unserem Sortiment:")],
        'it/': [("bare europee di qualità", "bare di qualità"), ("nella nostra gamma europea:", "nella nostra gamma:")],
        'es/': [("ataúdes europeos de calidad", "ataúdes de calidad"), ("entre nuestra gama europea:", "entre nuestra gama:")],
        'pt/': [("caixões europeus de qualidade", "caixões de qualidade")]}
def deces(s, l):
    P = l + 'blog/deces-proche-suisse-10-etapes.html'
    # coûts : « dès 3 500 CHF », tableau d'estimation supprimé
    m = re.search(r'(?:Il est estimé|It is estimated|Man schätzt|Si stima|Se estima|Estima-se)[^<]*(?=</p><h3>[^<]*</h3><div class="tbl"><table>)', s)
    if m:
        s = s[:m.start()] + STARTS[l] + s[m.end():]
        s = rx(s, r'(' + re.escape(STARTS[l]) + r'</p>)<h3>[^<]*</h3><div class="tbl"><table>.*?</table></div>(<blockquote>)(?:[^.]*\.){2}\s*', r'\1\2', 'tableau estimation', P)
    elif STARTS[l] not in s: problems.append(f'{P} :: phrase coûts')
    for old, new in EURO[l]: s = must(s, old, new, 'européen', P)
    if l == '':
        s = s.replace('Ce que Peut Inclure un Contrat de Prévoyance Murith', 'Ce que peut inclure un contrat de prévoyance Murith')
        s = must(s, 'Conclusion : Les les pompes funèbres', 'Conclusion : Les pompes funèbres', 'Les les', P)
    # formation / brevet : nouvelle ligne après les certifications
    if ASSF[l] not in s:
        mm = re.search(r'<li><strong>[^<]*(?:certifications|Qualifikationen|certificazioni|certificaciones|certificações|certifications)[^<]*</strong>.*?</li>', s, re.S | re.I)
        if mm: s = s[:mm.end()] + '<li><strong>' + LBL[l] + '</strong> ' + ASSF[l] + '</li>' + s[mm.end():]
        else: problems.append(f'{P} :: ligne certifications')
    return s
for l in L: rw(l + 'blog/deces-proche-suisse-10-etapes.html', lambda s, l=l: deces(s, l))

# ----------------------------------------------------------------- page prévoyance : carte « équipe » + questions « Pourquoi choisir »
def pv_page(s, l):
    P = l + 'prevoyance-funeraire.html'
    if ASSF[l] in s: return s
    m = re.search(r'(<section class="section alt pv-trust".*?<div class="g3">.*?)(</p></div></div>)(?=<div class="faq pv-tr|<p class="pv-close|</div></section>)', s, re.S)
    if m: return s[:m.end(1)] + ' ' + ASSF[l] + s[m.start(2):]
    problems.append(f'{P} :: carte équipe'); return s
for l in L: rw(l + 'prevoyance-funeraire.html', lambda s, l=l: pv_page(s, l))

def faq_why(s, l):
    P = 'faq'
    for m in re.finditer(r'<details><summary>([^<]*)<i aria-hidden="true"></i></summary><div class="ans">(<p>(?:(?!</details>).)*?</p>)(?=<p><a class="link-arrow" href="[^"]*notre-histoire")', s, re.S):
        if ASSF[l] in m.group(2): return s
        q = m.group(1); ans = m.group(2)
        s = s[:m.end(2) - 4] + ' ' + ASSF[l] + '</p>' + s[m.end(2):]
        # JSON-LD
        j = s.find('"name":"' + q + '"')
        if j >= 0:
            e = s.find('"}', s.find('"text":"', j))
            if e > 0 and ASSF[l] not in s[j:e + 40]: s = s[:e] + ' ' + ASSF[l] + s[e:]
        return s
    return s
for l in L:
    for f in ['index.html', 'contact.html', 'formalites.html', 'obseques.html']:
        rw(l + f, lambda s, l=l: faq_why(s, l))

if __name__ == '__main__':
    print('modifiés :', len(changed))
    print('problèmes :', len(problems))
    for p in problems: print('  !', p)
