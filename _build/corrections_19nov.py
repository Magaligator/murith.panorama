#!/usr/bin/env python3 -I
"""Corrections client du 2026-11-19 (document « Correction nouveau site » + retours WhatsApp), 6 langues. Idempotent.
Partie 1 (ce fichier) : lien du questionnaire, carrousel d'accueil, cartes d'articles, article « prévoyance funéraire ».
Partie 2 : _build/corrections_19nov_b.py (rapatriement, décès d'un proche, pages, textes « Pourquoi choisir »)."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
L = ['', 'en/', 'de/', 'it/', 'es/', 'pt/']
changed = set()
problems = []

def rw(path, fn):
    p = root / path
    if not p.exists(): problems.append(f'absent {path}'); return
    s = p.read_text(encoding='utf8'); n = fn(s)
    if n != s: p.write_text(n, encoding='utf8'); changed.add(path)

def must(s, old, new, label, path='', count=1):
    """remplace old par new ; idempotent (si old est absent et new présent : rien)"""
    if old in s: return s.replace(old, new, count)
    if new in s: return s
    problems.append(f'{path} :: introuvable : {label}')
    return s

def rx(s, pattern, repl, label, path='', flags=re.S, count=1):
    n, k = re.subn(pattern, repl, s, count=count, flags=flags)
    if k == 0: problems.append(f'{path} :: motif introuvable : {label}')
    return n

# ---------------------------------------------------------------- 1) lien du questionnaire (le .html renvoyait une erreur 400)
for p in sorted(root.rglob('*')):
    if p.suffix in ('.html', '.js') and not any(x in p.parts for x in ('_archive-wix', '_build', 'node_modules', '.git')):
        rw(str(p.relative_to(root)), lambda s: s.replace('murithprevoyance.ch/questionnaire.html', 'murithprevoyance.ch/questionnaire'))

# ---------------------------------------------------------------- 2) cartes d'article « prévoyance » : texte de l'article (plus de gratuité)
INTRO = {
 '': "La mort est une réalité que chaque être humain doit affronter, pourtant rares sont ceux qui prennent le temps de s'y préparer concrètement. À Genève, la prévoyance funéraire, parfois appelée testament d'obsèques ou contrat de prévoyance funéraire, représente une démarche de plus en plus répandue. Elle permet d'organiser et de financer ses propres funérailles de son vivant, soulageant ainsi ses proches d'un double fardeau : émotionnel et financier.",
 'en/': "Death is a reality that every human being must face, yet few take the time to prepare for it in concrete terms. In Geneva, funeral pre-planning, sometimes called a funeral will or funeral pre-planning contract, is an increasingly common step. It allows you to organise and finance your own funeral during your lifetime, sparing your loved ones a double burden: emotional and financial.",
 'de/': "Der Tod ist eine Realität, der sich jeder Mensch stellen muss – und doch nehmen sich nur wenige die Zeit, sich konkret darauf vorzubereiten. In Genf ist die Bestattungsvorsorge, manchmal auch Bestattungstestament oder Bestattungsvorsorgevertrag genannt, ein immer verbreiteterer Schritt. Sie ermöglicht es, die eigene Bestattung zu Lebzeiten zu organisieren und zu finanzieren und so die Angehörigen von einer doppelten Last zu befreien: der emotionalen und der finanziellen.",
 'it/': "La morte è una realtà che ogni essere umano deve affrontare, eppure sono pochi coloro che si prendono il tempo di prepararvisi concretamente. A Ginevra la previdenza funeraria, talvolta chiamata testamento funerario o contratto di previdenza funeraria, è un passo sempre più diffuso. Permette di organizzare e finanziare in vita i propri funerali, sollevando così i propri cari da un duplice fardello: emotivo e finanziario.",
 'es/': "La muerte es una realidad que todo ser humano debe afrontar y, sin embargo, pocos se toman el tiempo de prepararse concretamente. En Ginebra, la previsión funeraria, a veces llamada testamento de exequias o contrato de previsión funeraria, es una gestión cada vez más extendida. Permite organizar y financiar los propios funerales en vida, aliviando así a los allegados de una doble carga: emocional y financiera.",
 'pt/': "A morte é uma realidade que todo o ser humano tem de enfrentar e, no entanto, são poucos os que dedicam tempo a preparar-se concretamente. Em Genebra, a previdência funerária, por vezes chamada testamento de funerais ou contrato de previdência funerária, representa uma iniciativa cada vez mais difundida. Permite organizar e financiar os próprios funerais em vida, aliviando assim os familiares de um duplo fardo: emocional e financeiro.",
}
TEASER = {  # texte neutre posé par retrait_service_public.py
 '': "Comment organiser et financer vos obsèques à l'avance : tarifs bloqués dès la souscription, démarches et conseils des pompes funèbres Murith.",
 'en/': "How to organise and pay for your funeral in advance: prices fixed at signing, step-by-step guidance and advice from Murith funeral directors.",
 'de/': "So organisieren und finanzieren Sie Ihre Bestattung im Voraus: Preise ab Vertragsabschluss garantiert, Beratung und Begleitung durch Murith.",
 'it/': "Come organizzare e finanziare in anticipo le proprie esequie: prezzi bloccati alla sottoscrizione, passi da seguire e consigli di Pompe Funebri Murith.",
 'es/': "Cómo organizar y financiar sus exequias por adelantado: precios bloqueados desde la contratación, gestiones y consejos de las pompas fúnebres Murith.",
 'pt/': "Como organizar e financiar as suas exéquias com antecedência: preços fixos desde a subscrição, diligências e conselhos da Murith.",
}
for l in L:
    for f in ['index.html', 'blog.html', 'blog/cout-rapatriement-corps.html', 'blog/deces-proche-suisse-10-etapes.html']:
        rw(l + f, lambda s, l=l: s.replace('<p>' + TEASER[l] + '</p>', '<p>' + INTRO[l] + '</p>'))

# ---------------------------------------------------------------- 3) accueil : carte « Les Obsèques » + mot « Repatriation » (FR)
rw('index.html', lambda s: must(s,
    "Que vous optiez pour la simplicité ou que vous ayez des exigences particulières. Nos conseillers en pompes funèbres sauront répondre à toutes vos demandes.",
    "Que vous optiez pour la simplicité ou que vous ayez des exigences particulières, nos conseillers funéraires sauront répondre à toutes vos demandes.",
    'carte Les Obsèques', 'index.html'))
rw('it/index.html', lambda s: must(s, 'i nostri consulenti di pompe funebri sapranno', 'i nostri consulenti funerari sapranno', 'carte esequie IT', 'it/index.html'))
for f in ['index.html', 'blog.html', 'blog/cout-rapatriement-corps.html', 'blog/prevoyance-funeraire-geneve.html', 'blog/deces-proche-suisse-10-etapes.html']:
    rw(f, lambda s: s.replace('>Repatriation<', '>Rapatriement<'))

# ---------------------------------------------------------------- 4) article « prévoyance funéraire à Genève » (6 langues)
COST = {  # 1er paragraphe de la section coût : « dès 3 500 CHF » au lieu d'une fourchette
 '': ("En Suisse romande, le coût de l'enterrement est souvent sous-estimé. Les frais d'<a href=\"/obseques\">obsèques</a> débutent dès 3 500 CHF, selon les prestations choisies."),
 'en/': ("In French-speaking Switzerland, the cost of a funeral is often underestimated. <a href=\"/en/obseques\">Funeral</a> costs start from CHF 3,500, depending on the services chosen."),
 'de/': ("In der Westschweiz werden die Kosten einer Bestattung oft unterschätzt. Die Kosten für eine <a href=\"/de/obseques\">Bestattung</a> beginnen ab 3 500 CHF, je nach gewählten Leistungen."),
 'it/': ("Nella Svizzera romanda il costo di un funerale è spesso sottostimato. Le spese per le <a href=\"/it/obseques\">esequie</a> partono da 3 500 CHF, a seconda delle prestazioni scelte."),
 'es/': ("En la Suiza romanda, el coste del entierro suele subestimarse. Los gastos de los <a href=\"/es/obseques\">funerales</a> comienzan desde 3 500 CHF, según las prestaciones elegidas."),
 'pt/': ("Na Suíça romanda, o custo do enterro é muitas vezes subestimado. Os custos de <a href=\"/pt/obseques\">funerais</a> começam a partir de 3 500 CHF, consoante as prestações escolhidas."),
}
PAY = {  # « paiement comptant » -> « en un seul versement »
 '': [("un paiement comptant ou échelonné", "un paiement en un seul versement ou échelonné"), ("paiement comptant ou échelonné sur plusieurs années", "paiement en un seul versement ou échelonné sur plusieurs années")],
 'en/': [("payment in full or by instalments", "a single payment or instalments"), ("payment in full or in instalments over several years", "a single payment or instalments over several years")],
 'de/': [("Barzahlung oder Ratenzahlung wählen", "Einmalzahlung oder Ratenzahlung wählen"), ("Barzahlung oder Ratenzahlung über mehrere Jahre", "Einmalzahlung oder Ratenzahlung über mehrere Jahre")],
 'it/': [("un pagamento in contanti o rateale", "un pagamento in un'unica soluzione o rateale"), ("pagamento in contanti o rateale su più anni", "pagamento in un'unica soluzione o rateale su più anni")],
 'es/': [("un pago al contado o escalonado", "un pago único o escalonado"), ("pago al contado o escalonado durante varios años", "pago en un único desembolso o escalonado durante varios años")],
 'pt/': [("um pagamento à vista ou faseado", "um pagamento único ou faseado"), ("pagamento à vista ou faseado ao longo de vários anos", "pagamento numa única prestação ou faseado ao longo de vários anos")],
}
FUNDS = {  # fonds « garantis par notre patrimoine » (sans « immobilier » : voir mémoire du 16/11)
 '': ("sont sécurisés dans une structure indépendante.", "sont garantis par notre patrimoine, intégralement détenu par l'entreprise."),
 'en/': ("are secured in an independent structure.", "are guaranteed by our assets, wholly owned by the company."),
 'de/': ("in einer unabhängigen Struktur gesichert.", "durch unser Vermögen garantiert, das sich vollständig im Besitz des Unternehmens befindet."),
 'it/': ("sono messi al sicuro in una struttura indipendente.", "sono garantiti dal nostro patrimonio, interamente detenuto dall'azienda."),
 'es/': ("están asegurados en una estructura independiente.", "están garantizados por nuestro patrimonio, íntegramente en manos de la empresa."),
 'pt/': ("estão protegidos numa estrutura independente.", "estão garantidos pelo nosso património, integralmente detido pela empresa."),
}
CELL = {
 '': ("Structure indépendante certifiée", "Garantis par notre patrimoine"),
 'en/': ("Certified independent structure", "Guaranteed by our assets"),
 'de/': ("Zertifizierte unabhängige Struktur", "Durch unser Vermögen garantiert"),
 'it/': ("Struttura indipendente certificata", "Garantiti dal nostro patrimonio"),
 'es/': ("Estructura independiente certificada", "Garantizados por nuestro patrimonio"),
 'pt/': ("Estrutura independente certificada", "Garantidos pelo nosso património"),
}
OLDEST = {
 '': ("Les pompes funèbres Murith (www.murith.ch) sont l'une des plus anciennes entreprises funéraires, forte de plus de 135 ans d'expérience.", "La Maison Murith est l'entreprise de pompes funèbres la plus ancienne à Genève, forte de plus de 135 ans d'expérience."),
 'en/': ("Murith funeral services (www.murith.ch) is one of the oldest funeral companies, with more than 135 years of experience.", "Maison Murith is the oldest funeral company in Geneva, with more than 135 years of experience."),
 'de/': ("Das Bestattungsinstitut Murith (www.murith.ch) ist eines der ältesten Bestattungsunternehmen mit mehr als 135 Jahren Erfahrung.", "Das Haus Murith ist das älteste Bestattungsunternehmen in Genf mit mehr als 135 Jahren Erfahrung."),
 'it/': ("Le pompe funebri Murith (www.murith.ch) sono una delle più antiche imprese funerarie, forte di oltre 135 anni di esperienza.", "La Maison Murith è la più antica impresa di pompe funebri di Ginevra, forte di oltre 135 anni di esperienza."),
 'es/': ("Los servicios funerarios Murith (www.murith.ch) son una de las empresas funerarias más antiguas y cuentan con más de 135 años de experiencia.", "La Casa Murith es la empresa funeraria más antigua de Ginebra y cuenta con más de 135 años de experiencia."),
 'pt/': ("Os serviços funerários Murith (www.murith.ch) são uma das empresas funerárias mais antigas, com mais de 135 anos de experiência.", "A Casa Murith é a empresa funerária mais antiga de Genebra, com mais de 135 anos de experiência."),
}
REPAT = {  # dernière phrase de « Rapatriement et transport international »
 '': " En effet, en cas de décès à l'étranger, deux solutions sont possibles : la famille peut mandater directement l'assurance rapatriement incluse dans la police du défunt ; si cette couverture n'existe pas, nous pouvons conseiller à la famille une entreprise sur place à mandater, grâce à notre réseau de partenaires.",
 'en/': " Indeed, if a death occurs abroad, two solutions are possible: the family can directly instruct the repatriation insurance included in the deceased's policy; if no such cover exists, we can recommend a local company for the family to appoint, thanks to our partner network.",
 'de/': " Bei einem Todesfall im Ausland gibt es nämlich zwei Möglichkeiten: Die Familie kann direkt die in der Police der verstorbenen Person enthaltene Rückführungsversicherung beauftragen; besteht diese Deckung nicht, können wir der Familie dank unseres Partnernetzes ein Unternehmen vor Ort empfehlen, das sie beauftragen kann.",
 'it/': " In caso di decesso all'estero esistono infatti due soluzioni: la famiglia può incaricare direttamente l'assicurazione di rimpatrio inclusa nella polizza del defunto; se tale copertura non esiste, possiamo consigliare alla famiglia un'impresa sul posto da incaricare, grazie alla nostra rete di partner.",
 'es/': " En efecto, en caso de fallecimiento en el extranjero hay dos soluciones posibles: la familia puede encargar directamente el seguro de repatriación incluido en la póliza del fallecido; si esa cobertura no existe, podemos aconsejar a la familia una empresa local a la que encargarlo, gracias a nuestra red de colaboradores.",
 'pt/': " Com efeito, em caso de óbito no estrangeiro, há duas soluções possíveis: a família pode mandatar diretamente o seguro de repatriamento incluído na apólice do falecido; se essa cobertura não existir, podemos aconselhar à família uma empresa no local a mandatar, graças à nossa rede de parceiros.",
}
STEP_Q = {  # nouvelle étape « sans rencontre »
 '': '<li><strong>Sans rencontre :</strong> si vous préférez ne pas venir nous voir, remplissez le questionnaire en ligne sur <a href="https://www.murithprevoyance.ch/questionnaire" rel="noopener" target="_blank">notre site de prévoyance</a></li>',
 'en/': '<li><strong>No meeting needed:</strong> if you would rather not meet an advisor, complete the online questionnaire on <a href="https://www.murithprevoyance.ch/questionnaire" rel="noopener" target="_blank">our pre-planning website</a></li>',
 'de/': '<li><strong>Ohne Treffen:</strong> Wenn Sie lieber kein Gespräch führen möchten, füllen Sie den Online-Fragebogen auf <a href="https://www.murithprevoyance.ch/questionnaire" rel="noopener" target="_blank">unserer Vorsorge-Website</a> aus</li>',
 'it/': '<li><strong>Senza incontro:</strong> se preferite non incontrare un consulente, compilate il questionario online sul <a href="https://www.murithprevoyance.ch/questionnaire" rel="noopener" target="_blank">nostro sito di previdenza</a></li>',
 'es/': '<li><strong>Sin reunión:</strong> si prefiere no reunirse con un asesor, rellene el cuestionario en línea en <a href="https://www.murithprevoyance.ch/questionnaire" rel="noopener" target="_blank">nuestro sitio de previsión</a></li>',
 'pt/': '<li><strong>Sem reunião:</strong> se preferir não se reunir com um conselheiro, preencha o questionário em linha no <a href="https://www.murithprevoyance.ch/questionnaire" rel="noopener" target="_blank">nosso site de previdência</a></li>',
}
ELEM = {  # liste « éléments à définir » : crémation, « Murith » en trop, rapatriement
 '': [("plus de 80 % des défunts suisses optent pour la crémation", "plus de 80 % des défunts en Suisse optent pour la crémation"),
      ("du maître de cérémonie Murith", "du maître de cérémonie"), ("parmi la gamme complète Murith (", "parmi la gamme complète ("),
      ("salons Murith, église", "salons, église"), ("(service proposé par l'entreprise Murith)", "(service proposé par l'entreprise)"),
      ("couverture internationale.", "vers tous les pays du monde.")],
 'en/': [("more than 80% of Swiss deceased opt for cremation", "more than 80% of people who die in Switzerland opt for cremation"),
      ("Murith master of ceremonies", "master of ceremonies"), ("from the complete Murith range (", "from the complete range ("),
      ("Murith rooms, church", "the rooms, church"), ("(service offered by Murith)", "(service offered by the company)"),
      ("international cover.", "to any country in the world.")],
 'de/': [("des Zeremonienmeisters von Murith", "des Zeremonienmeisters"), ("vollständigen Sortiment von Murith (", "vollständigen Sortiment ("),
      ("Räume von Murith, Kirche", "Räume, Kirche"), ("(von Murith angebotener Service)", "(vom Unternehmen angebotener Service)"),
      ("internationale Absicherung.", "in alle Länder der Welt.")],
 'it/': [("più dell'80 % dei defunti svizzeri opta per la cremazione", "più dell'80 % dei defunti in Svizzera opta per la cremazione"),
      ("maestro di cerimonia Murith", "maestro di cerimonia"), ("nell'intera gamma Murith (", "nell'intera gamma ("),
      ("sale Murith, chiesa", "sale, chiesa"), ("(servizio proposto dall'azienda Murith)", "(servizio proposto dall'azienda)"),
      ("copertura internazionale.", "verso tutti i paesi del mondo.")],
 'es/': [("más del 80 % de los fallecidos suizos optan por la cremación", "más del 80 % de los fallecidos en Suiza optan por la cremación"),
      ("maestro de ceremonias de Murith", "maestro de ceremonias"), ("gama completa de Murith (", "gama completa ("),
      ("salas Murith, iglesia", "salas, iglesia"), ("(servicio ofrecido por la empresa Murith)", "(servicio ofrecido por la empresa)"),
      ("cobertura internacional.", "hacia todos los países del mundo.")],
 'pt/': [("mais de 80 % dos falecidos suíços optam pela cremação", "mais de 80 % dos falecidos na Suíça optam pela cremação"),
      ("mestre de cerimónias da Murith", "mestre de cerimónias"), ("gama completa da Murith (", "gama completa ("),
      ("salas Murith, igreja", "salas, igreja"), ("(serviço oferecido pela empresa Murith)", "(serviço oferecido pela empresa)"),
      ("cobertura internacional.", "para todos os países do mundo.")],
}
FAQ = {  # (ancienne réponse – début, nouvelle réponse)
 '': [("Aucune limite d'âge. Plus tôt vous agissez, plus les mensualités sont accessibles et les tarifs bloqués.", "Aucune limite d'âge. Il n'y a pas de répercussion tarifaire à la hausse ou à la baisse selon l'âge de la souscription."),
      ("Oui, ils sont logés dans une structure indépendante. En cas de circonstances imprévues, vos fonds restent protégés.", "Oui, ces derniers sont intégrés dans un compte exclusivement dédié, garanti par notre patrimoine."),
      ("Oui. En cas de déménagement, le réseau partenaire de la Maison Murith assure la prise en charge à l'échelle nationale et internationale.", "Oui. En cas de décès à l'étranger, la famille aura deux options : mandater l'assurance rapatriement du défunt, ou mandater une entreprise sur place, conseillée par nos soins grâce à notre réseau de partenaires. Une provision à ce titre peut être prévue dans le contrat Murith."),
      (" Dans certains cantons, jusqu'à CHF 10’000 à 15’000.", "")],
 'en/': [("No age limit. The earlier you act, the more affordable the monthly payments and the prices locked in.", "No age limit. There is no price increase or decrease depending on the age at which you take out the contract."),
      ("Yes, they are held in an independent structure. In the event of unforeseen circumstances, your funds remain protected.", "Yes, they are paid into an exclusively dedicated account, guaranteed by our assets."),
      ("Yes. If you move, Maison Murith's partner network ensures coverage nationally and internationally.", "Yes. If a death occurs abroad, the family has two options: instruct the deceased's repatriation insurance, or appoint a local company recommended by us thanks to our partner network. A provision for this can be included in the Murith contract."),
      (" In some cantons, up to CHF 10,000 - 15,000.", "")],
 'de/': [("Keine Altersgrenze. Je früher Sie handeln, desto günstiger sind die monatlichen Raten und desto früher sind die Preise festgeschrieben.", "Keine Altersgrenze. Das Alter beim Abschluss wirkt sich weder nach oben noch nach unten auf den Preis aus."),
      ("Ja, sie werden in einer unabhängigen Struktur verwahrt. Bei unvorhergesehenen Umständen bleiben Ihre Gelder geschützt.", "Ja, sie werden auf ein ausschliesslich dafür vorgesehenes Konto einbezahlt, das durch unser Vermögen garantiert ist."),
      ("Ja. Bei einem Umzug übernimmt das Partnernetz des Hauses Murith die Betreuung national und international.", "Ja. Bei einem Todesfall im Ausland hat die Familie zwei Möglichkeiten: die Rückführungsversicherung der verstorbenen Person beauftragen oder ein von uns dank unseres Partnernetzes empfohlenes Unternehmen vor Ort. Dafür kann im Murith-Vertrag eine Rückstellung vorgesehen werden."),
      (" In einigen Kantonen bis zu CHF 10’000 - 15’000.", "")],
 'it/': [("Nessun limite di età. Prima agite, più le rate sono accessibili e le tariffe bloccate.", "Nessun limite di età. L'età di sottoscrizione non comporta alcuna variazione di prezzo, né in aumento né in diminuzione."),
      ("Sì, sono collocati in una struttura indipendente. In caso di circostanze impreviste, i vostri fondi restano protetti.", "Sì, sono versati su un conto esclusivamente dedicato, garantito dal nostro patrimonio."),
      ("Sì. In caso di trasloco, la rete partner della Maison Murith assicura la presa in carico a livello nazionale e internazionale.", "Sì. In caso di decesso all'estero, la famiglia avrà due opzioni: incaricare l'assicurazione di rimpatrio del defunto oppure un'impresa sul posto, da noi consigliata grazie alla nostra rete di partner. Un accantonamento a tale scopo può essere previsto nel contratto Murith."),
      (" In alcuni cantoni, fino a CHF 10’000–15’000.", "")],
 'es/': [("Sin límite de edad. Cuanto antes actúe, más accesibles son las mensualidades y más tempranas las tarifas bloqueadas.", "Sin límite de edad. La edad de contratación no supone ninguna variación de precio, ni al alza ni a la baja."),
      ("Sí, están depositados en una estructura independiente. En caso de circunstancias imprevistas, sus fondos permanecen protegidos.", "Sí, se ingresan en una cuenta exclusivamente dedicada, garantizada por nuestro patrimonio."),
      ("Sí. En caso de mudanza, la red de colaboradores de la Casa Murith asegura la atención a escala nacional e internacional.", "Sí. En caso de fallecimiento en el extranjero, la familia tendrá dos opciones: encargar el seguro de repatriación del fallecido o una empresa local aconsejada por nosotros gracias a nuestra red de colaboradores. Puede preverse una provisión a tal efecto en el contrato Murith."),
      (" En algunos cantones, hasta 10 000 - 15 000 CHF.", "")],
 'pt/': [("Sem limite de idade. Quanto mais cedo agir, mais acessíveis são as mensalidades e mais cedo ficam bloqueadas as tarifas.", "Sem limite de idade. A idade de subscrição não tem qualquer repercussão no preço, nem para mais nem para menos."),
      ("Sim, estão alojados numa estrutura independente. Em caso de circunstâncias imprevistas, os seus fundos permanecem protegidos.", "Sim, são depositados numa conta exclusivamente dedicada, garantida pelo nosso património."),
      ("Sim. Em caso de mudança, a rede de parceiros da Casa Murith assegura a tomada a cargo a nível nacional e internacional.", "Sim. Em caso de óbito no estrangeiro, a família terá duas opções: mandatar o seguro de repatriamento do falecido ou uma empresa no local, aconselhada por nós graças à nossa rede de parceiros. Pode ser prevista uma provisão para esse efeito no contrato Murith."),
      (" Em alguns cantões, até 10 000 - 15 000 CHF.", "")],
}

def prevoyance(s, l):
    P = l + 'blog/prevoyance-funeraire-geneve.html'
    # table des matières : retire l'entrée du service public (4e point) et la section elle-même
    i = s.find('1866')
    if i >= 0:
        h = s.rfind('<h2', 0, i); e = s.find('<h2', i)
        titre = re.sub(r'<[^>]+>', '', s[h:s.find('</h2>', h)])
        s = s[:h] + s[e:]
        s = re.sub(r'<li>' + re.escape(titre) + r'</li>', '', s, count=1)
    # section coût : nouveau paragraphe « dès 3 500 CHF »
    m = re.search(r'(<h2><strong>[^<]*</strong></h2>)<p>((?:(?!</p>).)*CHF(?:(?!</p>).)*)</p>(<p><strong>)', s, re.S)
    if m and '3 500 CHF' not in m.group(2) and '3,500' not in m.group(2):
        s = s[:m.start(2)] + COST[l] + s[m.end(2):]
    elif not m and COST[l] not in s: problems.append(f'{P} :: paragraphe coût')
    for old, new in PAY[l]: s = must(s, old, new, 'paiement', P)
    o, n = FUNDS[l]; s = must(s, o, n, 'fonds garantis', P)
    o, n = CELL[l]; s = must(s, o, n, 'cellule tableau', P)
    n = OLDEST[l][1]
    if n not in s:
        s = rx(s, r'(?<=<p>)[^<]*\(<a href="[^"]*">www\.murith\.ch</a>\)\s*(?:<span class="seo-new">)?[^<]*?135[^<]*?\.(?:</span>)?', n, 'plus ancienne', P)
    if l == '': s = must(s, "l'Hôpitaux universitaires de Genève", "des Hôpitaux universitaires de Genève", 'HUG', P)
    # rapatriement : dernière phrase du paragraphe qui précède la section coût
    h2 = s.find('<h2>', s.find('rapatriement' if l == '' else '<h3>'))
    mm = re.search(r'<h3><strong>[^<]*</strong></h3><p>((?:(?!</p>).)*)</p>(?=<h2><strong>[^<]*</strong></h2><p>(?:(?!</p>).)*CHF)', s, re.S)
    if mm:
        txt = mm.group(1)
        sent = re.split(r'(?<=\.)\s+', txt)
        if len(sent) >= 3 and REPAT[l].strip() not in txt:
            s = s[:mm.start(1)] + ' '.join(sent[:2]) + REPAT[l] + s[mm.end(1):]
    elif REPAT[l].strip() not in s: problems.append(f'{P} :: paragraphe rapatriement')
    # étape « sans rencontre » après l'entretien confidentiel
    if STEP_Q[l] not in s:
        mu = re.search(r'<ul>(<li><strong> [^<]*</strong>.*?</li>)</ul>', s, re.S)
        if mu:
            lis = re.findall(r'<li>.*?</li>', mu.group(0), re.S)
            if len(lis) == 7:
                lis.insert(3, STEP_Q[l]); s = s[:mu.start()] + '<ul>' + ''.join(lis) + '</ul>' + s[mu.end():]
        else: problems.append(f'{P} :: liste des étapes')
    for old, new in ELEM[l]: s = must(s, old, new, 'éléments ' + old[:25], P)
    for old, new in FAQ[l]: s = must(s, old, new, 'FAQ ' + old[:25], P)
    # titres avec majuscules inutiles (FR)
    return s
for l in L:
    rw(l + 'blog/prevoyance-funeraire-geneve.html', lambda s, l=l: prevoyance(s, l))

if __name__ == '__main__':
    print('modifiés :', len(changed))
    for p in sorted(changed)[:80]: print(' ', p)
    print('problèmes :', len(problems))
    for p in problems: print('  !', p)
