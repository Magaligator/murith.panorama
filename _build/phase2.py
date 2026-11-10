# PHASE 2 — titles, meta descriptions et H1 (FR + EN/DE/ES/PT). Rejouable (idempotent).
import re, os, json, html, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = ROOT + '/panorama/'
R = lambda t: f'<span class="seo-new">{t}</span>'

# page : {lang: (title, description, h1)}
D = {
'index.html': {
 'fr': ("Pompes funèbres Genève 24h/24 | Maison Murith depuis 1888", "Pompes funèbres à Genève depuis 1888, face aux HUG. Obsèques, crémation, salons funéraires et rapatriements. Une famille à vos côtés 24h/24 : 022 809 56 00.", None),
 'en': ("Funeral Directors Geneva 24/7 | Maison Murith since 1888", "Funeral directors in Geneva since 1888, opposite the HUG. Funerals, cremation, funeral rooms and repatriation. A family by your side 24/7: +41 22 809 56 00.", None),
 'de': ("Bestattungsinstitut Genf 24/7 | Maison Murith seit 1888", "Bestattungsinstitut in Genf seit 1888, gegenüber dem HUG. Bestattungen, Kremation, Abschiedsräume und Überführungen. Eine Familie an Ihrer Seite: 022 809 56 00.", None),
 'es': ("Funeraria en Ginebra 24h | Casa Murith desde 1888", "Funeraria en Ginebra desde 1888, frente a los HUG. Funerales, cremación, salas funerarias y repatriaciones. Una familia a su lado 24h/24: 022 809 56 00.", None),
 'pt': ("Agência funerária Genebra 24h | Casa Murith desde 1888", "Agência funerária em Genebra desde 1888, em frente aos HUG. Funerais, cremação, salas funerárias e repatriamentos. Ao seu lado 24h/24: 022 809 56 00.", None)},
'obseques.html': {
 'fr': ("Obsèques à Genève : enterrement et crémation | Murith", "Organiser des obsèques à Genève : inhumation, crémation, cérémonie laïque ou religieuse. Un conseiller dédié et un devis sous 24h. Joignable 24h/24.", "Organiser des obsèques à Genève"),
 'en': ("Funerals in Geneva: burial and cremation | Murith", "Arranging a funeral in Geneva: burial, cremation, secular or religious ceremony. A dedicated advisor and a quote within 24h. Reachable 24/7.", "Arranging a funeral in Geneva"),
 'de': ("Bestattung in Genf: Beisetzung und Kremation | Murith", "Eine Bestattung in Genf organisieren: Erdbestattung, Kremation, weltliche oder religiöse Feier. Ein fester Berater und eine Offerte innert 24 Stunden.", "Eine Bestattung in Genf organisieren"),
 'es': ("Funerales en Ginebra: entierro y cremación | Murith", "Organizar un funeral en Ginebra: inhumación, cremación, ceremonia laica o religiosa. Un asesor dedicado y un presupuesto en 24 horas. Disponibles 24h/24.", "Organizar un funeral en Ginebra"),
 'pt': ("Funerais em Genebra: enterro e cremação | Murith", "Organizar um funeral em Genebra: inumação, cremação, cerimónia laica ou religiosa. Um conselheiro dedicado e um orçamento em 24 horas. Disponível 24h/24.", "Organizar um funeral em Genebra")},
'formalites.html': {
 'fr': ("Décès à Genève : démarches et acte de décès | Murith", "Un décès à Genève ? Déclaration, acte de décès, documents à préparer : téléchargez notre check-list gratuite. Nous nous chargeons des formalités.", "Décès à Genève : les démarches à effectuer"),
 'en': ("Death in Geneva: formalities and death certificate | Murith", "A death in Geneva? Declaration, death certificate, documents to prepare: use our free checklist. We take care of the formalities for you.", "Death in Geneva: the formalities to complete"),
 'de': ("Todesfall in Genf: Formalitäten und Todesschein | Murith", "Ein Todesfall in Genf? Todesmeldung, Todesschein, nötige Unterlagen: nutzen Sie unsere kostenlose Checkliste. Wir übernehmen die Formalitäten für Sie.", "Todesfall in Genf: die zu erledigenden Formalitäten"),
 'es': ("Fallecimiento en Ginebra: trámites y acta | Murith", "¿Un fallecimiento en Ginebra? Declaración, acta de defunción, documentos que preparar: use nuestra lista gratuita. Nos encargamos de los trámites por usted.", "Fallecimiento en Ginebra: los trámites a realizar"),
 'pt': ("Óbito em Genebra: formalidades e certidão | Murith", "Um óbito em Genebra? Declaração, certidão de óbito, documentos a preparar: use a nossa lista gratuita. Tratamos das formalidades por si.", "Óbito em Genebra: as formalidades a cumprir")},
'prevoyance-funeraire.html': {
 'fr': ("Prévoyance funéraire à Genève : vos obsèques | Murith", "Préparez vos obsèques de votre vivant à Genève : volontés, cérémonie, financement. La Ville n'accepte plus de prévoyance depuis 2014 : nous vous guidons.", "Prévoyance funéraire à Genève"),
 'en': ("Funeral pre-planning in Geneva: plan ahead | Murith", "Plan your funeral in advance in Geneva: wishes, ceremony, financing. The City no longer accepts new pre-planning since 2014: we guide you.", "Funeral pre-planning in Geneva"),
 'de': ("Bestattungsvorsorge in Genf: vorsorgen | Murith", "Bestattungsvorsorge in Genf: Wünsche, Feier und Finanzierung zu Lebzeiten regeln. Die Stadt nimmt seit 2014 keine neue Vorsorge mehr an: wir beraten Sie.", "Bestattungsvorsorge in Genf"),
 'es': ("Previsión funeraria en Ginebra: planificar | Murith", "Prepare su funeral en vida en Ginebra: voluntades, ceremonia y financiación. La Ciudad ya no acepta nuevas previsiones desde 2014: le guiamos.", "Previsión funeraria en Ginebra"),
 'pt': ("Previdência funerária em Genebra: planear | Murith", "Prepare o seu funeral em vida em Genebra: vontades, cerimónia e financiamento. A Cidade já não aceita novas previdências desde 2014: nós orientamos.", "Previdência funerária em Genebra")},
'transports.html': {
 'fr': ("Rapatriement de corps depuis Genève | Pompes funèbres Murith", "Rapatriement funéraire depuis Genève vers la Suisse et l'étranger : formalités, consulats, transport aérien ou routier. Organisation rapide, 24h/24.", "Rapatriement de corps et transports internationaux"),
 'en': ("Repatriation of remains from Geneva | Murith", "Funeral repatriation from Geneva to Switzerland and abroad: formalities, consulates, air or road transport. Fast organisation by Murith, available 24/7.", "Repatriation of remains and international transport"),
 'de': ("Überführung Verstorbener ab Genf | Murith", "Überführung ab Genf in die Schweiz und ins Ausland: Formalitäten, Konsulate, Transport per Flugzeug oder Strasse. Rasche Organisation, rund um die Uhr.", "Überführung und internationale Transporte"),
 'es': ("Repatriación de restos desde Ginebra | Murith", "Repatriación funeraria desde Ginebra a Suiza y al extranjero: trámites, consulados, transporte aéreo o por carretera. Organización rápida, 24h/24.", "Repatriación de restos y transportes internacionales"),
 'pt': ("Repatriamento de corpos a partir de Genebra | Murith", "Repatriamento funerário a partir de Genebra para a Suíça e o estrangeiro: formalidades, consulados, transporte aéreo ou rodoviário. Rápido, 24h/24.", "Repatriamento de corpos e transportes internacionais")},
'salons.html': {
 'fr': ("Salons funéraires à Genève – Chapelle de la Cluse | Murith", "Salons funéraires privés au centre de Genève, accessibles 24h/24 avec un code, et chapelle de la Cluse jusqu'à 60 personnes pour les cérémonies.", "Nos salons funéraires et la chapelle de la Cluse"),
 'en': ("Funeral viewing rooms in Geneva – La Cluse chapel | Murith", "Private viewing rooms in central Geneva, accessible 24/7 with a code, and the La Cluse chapel for up to 60 people for ceremonies.", "Our viewing rooms and the La Cluse chapel"),
 'de': ("Abschiedsräume in Genf – Kapelle La Cluse | Murith", "Private Abschiedsräume im Zentrum von Genf, rund um die Uhr mit Code zugänglich, und die Kapelle La Cluse für bis zu 60 Personen bei Trauerfeiern.", "Unsere Abschiedsräume und die Kapelle La Cluse"),
 'es': ("Salas funerarias en Ginebra – Capilla de La Cluse | Murith", "Salas funerarias privadas en el centro de Ginebra, accesibles 24h/24 con código, y capilla de La Cluse para hasta 60 personas en las ceremonias.", "Nuestras salas funerarias y la capilla de La Cluse"),
 'pt': ("Salas funerárias em Genebra – Capela de La Cluse | Murith", "Salas funerárias privadas no centro de Genebra, acessíveis 24h/24 com código, e capela de La Cluse para até 60 pessoas nas cerimónias.", "As nossas salas funerárias e a capela de La Cluse")},
'cercueils.html': {
 'fr': ("Cercueils à Genève : modèles et essences de bois | Murith", "Choisissez un cercueil pour une inhumation ou une crémation : chêne, sapin, finitions et capitonnages. Modèles de fabrication européenne, conseil personnalisé.", "Nos cercueils"),
 'en': ("Coffins in Geneva: models and wood types | Murith", "Choose a coffin for burial or cremation: oak, fir, finishes and interior linings. European-made models, with personal advice from our advisors.", "Our coffins"),
 'de': ("Särge in Genf: Modelle und Holzarten | Murith", "Wählen Sie einen Sarg für Erdbestattung oder Kremation: Eiche, Tanne, Ausführungen und Innenausstattung. Europäische Fertigung, persönliche Beratung.", "Unsere Särge"),
 'es': ("Ataúdes en Ginebra: modelos y maderas | Murith", "Elija un ataúd para inhumación o cremación: roble, abeto, acabados y acolchado interior. Modelos de fabricación europea y asesoramiento personal.", "Nuestros ataúdes"),
 'pt': ("Caixões em Genebra: modelos e madeiras | Murith", "Escolha um caixão para inumação ou cremação: carvalho, abeto, acabamentos e forro interior. Modelos de produção europeia e aconselhamento personalizado.", "Os nossos caixões")},
'fleurs.html': {
 'fr': ("Fleurs d'enterrement à Genève : gerbes, couronnes | Murith", "Fleurs pour un enterrement à Genève : couronnes, gerbes, coussins et dessus de cercueil, livrés au lieu de la cérémonie. Composez votre arrangement.", "Fleurs pour un enterrement à Genève"),
 'en': ("Funeral flowers in Geneva: sprays, wreaths | Murith", "Funeral flowers in Geneva: wreaths, sprays, cushions and coffin pieces, delivered to the ceremony venue. Create your own arrangement with our advisors.", "Funeral flowers in Geneva"),
 'de': ("Trauerblumen in Genf: Gestecke, Kränze | Murith", "Trauerblumen in Genf: Kränze, Gestecke, Kissen und Sargschmuck, geliefert zum Ort der Feier. Stellen Sie Ihr Arrangement zusammen.", "Trauerblumen in Genf"),
 'es': ("Flores para funeral en Ginebra: coronas | Murith", "Flores para un funeral en Ginebra: coronas, ramos, cojines y piezas para el ataúd, entregados en el lugar de la ceremonia. Componga su arreglo.", "Flores para un funeral en Ginebra"),
 'pt': ("Flores para funeral em Genebra: coroas | Murith", "Flores para um funeral em Genebra: coroas, ramos, almofadas e peças para o caixão, entregues no local da cerimónia. Componha o seu arranjo.", "Flores para um funeral em Genebra")},
'contact.html': {
 'fr': ("Contact et urgence décès 24h/24 à Genève | Murith", "Un décès vient de survenir ? Appelez le 022 809 56 00, jour et nuit. Boulevard de la Cluse 89, 1205 Genève, face aux HUG. Rendez-vous à domicile possible.", "Nous contacter, 24h/24"),
 'en': ("Contact and 24/7 death assistance in Geneva | Murith", "A death has just occurred? Call 022 809 56 00, day and night. Boulevard de la Cluse 89, 1205 Geneva, opposite the HUG. Home visits possible.", "Contact us, 24/7"),
 'de': ("Kontakt und Todesfall 24/7 in Genf | Murith", "Ein Todesfall ist eingetreten? Rufen Sie 022 809 56 00 an, Tag und Nacht. Boulevard de la Cluse 89, 1205 Genf, gegenüber dem HUG. Hausbesuche möglich.", "Kontakt, rund um die Uhr"),
 'es': ("Contacto y urgencia 24h/24 en Ginebra | Murith", "¿Ha ocurrido un fallecimiento? Llame al 022 809 56 00, de día y de noche. Boulevard de la Cluse 89, 1205 Ginebra, frente a los HUG. Visitas a domicilio.", "Contacte con nosotros, 24h/24"),
 'pt': ("Contacto e urgência 24h/24 em Genebra | Murith", "Ocorreu um óbito? Ligue para o 022 809 56 00, dia e noite. Boulevard de la Cluse 89, 1205 Genebra, em frente aos HUG. Visitas ao domicílio possíveis.", "Contacte-nos, 24h/24")},
'devis.html': {
 'fr': ("Devis d'obsèques à Genève sous 24h | Murith", "Recevez sans engagement un devis détaillé pour des obsèques à Genève (crémation ou inhumation), sous 24h et en toute transparence. Équipe disponible 24h/24.", "Demander un devis d'obsèques"),
 'en': ("Funeral quote in Geneva within 24h | Murith", "Receive a detailed funeral quote in Geneva (cremation or burial) within 24h, with full transparency and no commitment. Our team is available 24/7.", "Request a funeral quote"),
 'de': ("Offerte für eine Bestattung in Genf in 24h | Murith", "Erhalten Sie in 24 Stunden eine detaillierte, transparente und unverbindliche Offerte für eine Bestattung in Genf (Kremation oder Erdbestattung).", "Offerte für eine Bestattung anfragen"),
 'es': ("Presupuesto de funeral en Ginebra en 24h | Murith", "Reciba en 24 horas un presupuesto detallado, transparente y sin compromiso para un funeral en Ginebra (cremación o inhumación). Disponible 24h/24.", "Solicitar un presupuesto de funeral"),
 'pt': ("Orçamento de funeral em Genebra em 24h | Murith", "Receba em 24 horas um orçamento detalhado, transparente e sem compromisso para um funeral em Genebra (cremação ou inumação). Disponível 24h/24.", "Pedir um orçamento de funeral")},
'notre-histoire.html': {
 'fr': ("Notre histoire : la famille Murith à Genève depuis 1888", "Cinq générations de la famille Murith au service des familles genevoises depuis 1888. Découvrez l'histoire de notre maison, boulevard de la Cluse.", "Notre histoire depuis 1888"),
 'en': ("Our history: the Murith family in Geneva since 1888", "Five generations of the Murith family serving Geneva families since 1888. Discover the history of our house on Boulevard de la Cluse.", "Our history since 1888"),
 'de': ("Unsere Geschichte: Familie Murith in Genf seit 1888", "Fünf Generationen der Familie Murith im Dienst der Genfer Familien seit 1888. Entdecken Sie die Geschichte unseres Hauses am Boulevard de la Cluse.", "Unsere Geschichte seit 1888"),
 'es': ("Nuestra historia: la familia Murith en Ginebra", "Cinco generaciones de la familia Murith al servicio de las familias ginebrinas desde 1888. Descubra la historia de nuestra casa en Boulevard de la Cluse.", "Nuestra historia desde 1888"),
 'pt': ("A nossa história: a família Murith em Genebra", "Cinco gerações da família Murith ao serviço das famílias genebrinas desde 1888. Descubra a história da nossa casa no Boulevard de la Cluse.", "A nossa história desde 1888")},
'conseillers.html': {
 'fr': ("Nos conseillers funéraires à Genève | Murith", "Rencontrez les conseillers et maîtres de cérémonie de la Maison Murith, qui vous accompagnent avec écoute à chaque étape des obsèques à Genève.", "Nos conseillers funéraires"),
 'en': ("Our funeral advisors in Geneva | Murith", "Meet the advisors and masters of ceremony of Maison Murith, who support you attentively at every stage of the funeral in Geneva.", "Our funeral advisors"),
 'de': ("Unsere Bestattungsberater in Genf | Murith", "Lernen Sie die Berater und Zeremonienleiter des Hauses Murith kennen, die Sie bei jedem Schritt der Bestattung in Genf aufmerksam begleiten.", "Unsere Bestattungsberater"),
 'es': ("Nuestros asesores funerarios en Ginebra | Murith", "Conozca a los asesores y maestros de ceremonia de la Casa Murith, que le acompañan con atención en cada etapa de los funerales en Ginebra.", "Nuestros asesores funerarios"),
 'pt': ("Os nossos conselheiros funerários em Genebra", "Conheça os conselheiros e mestres de cerimónia da Casa Murith, que o acompanham com atenção em cada etapa do funeral em Genebra.", "Os nossos conselheiros funerários")},
'remerciements.html': {
 'fr': ("Cartes de remerciements après un décès | Murith Genève", "Cartes de remerciements et faire-part de deuil personnalisés : modèles, textes et impression pour remercier vos proches après les obsèques.", "Cartes de remerciements"),
 'en': ("Thank-you cards after a bereavement | Murith Geneva", "Personalised thank-you cards: models, texts and printing to thank your loved ones after the funeral. Matching announcements available on request.", "Thank-you cards"),
 'de': ("Dankeskarten nach einem Todesfall | Murith Genf", "Persönliche Dankeskarten: Modelle, Texte und Druck, um Ihren Angehörigen nach der Trauerfeier zu danken. Passende Trauerkarten auf Anfrage erhältlich.", "Dankeskarten"),
 'es': ("Tarjetas de agradecimiento tras un duelo | Murith", "Tarjetas de agradecimiento personalizadas: modelos, textos e impresión para dar las gracias a sus allegados tras el funeral. Esquelas a juego disponibles.", "Tarjetas de agradecimiento"),
 'pt': ("Cartões de agradecimento após um luto | Murith", "Cartões de agradecimento personalizados: modelos, textos e impressão para agradecer aos seus familiares após o funeral. Convites a condizer disponíveis.", "Cartões de agradecimento")},
'murith-care.html': {
 'fr': ("Murith Care Everywhere : assistance à l'étranger | Murith", "Murith Care Everywhere : prévoyance funéraire pour les familles suisses résidant à l'étranger. Rapatriement à Genève et obsèques organisées par Murith.", "Murith Care Everywhere"),
 'en': ("Murith Care Everywhere: assistance abroad | Murith", "Murith Care Everywhere: funeral pre-planning for Swiss families living abroad. Repatriation to Geneva and funeral organised by Murith.", "Murith Care Everywhere"),
 'de': ("Murith Care Everywhere: Hilfe im Ausland | Murith", "Murith Care Everywhere: Bestattungsvorsorge für Schweizer Familien im Ausland. Überführung nach Genf und Bestattung durch Murith, wie vertraglich vereinbart.", "Murith Care Everywhere"),
 'es': ("Murith Care Everywhere: asistencia en el extranjero", "Murith Care Everywhere: previsión funeraria para familias suizas residentes en el extranjero. Repatriación a Ginebra y funeral organizado por Murith.", "Murith Care Everywhere"),
 'pt': ("Murith Care Everywhere: assistência no estrangeiro", "Murith Care Everywhere: previdência funerária para famílias suíças residentes no estrangeiro. Repatriamento para Genebra e funeral organizado pela Murith.", "Murith Care Everywhere")},
'blog.html': {
 'fr': ("Obsèques et deuil à Genève : guides pratiques | Murith", "Démarches après un décès, coût des obsèques, prévoyance, rapatriement : nos guides pratiques pour les familles genevoises.", "Guides et conseils pour les familles"),
 'en': ("Funerals and bereavement in Geneva: guides | Murith", "Formalities after a death, funeral costs, pre-planning, repatriation: our practical guides for families in Geneva, by Maison Murith.", "Guides and advice for families"),
 'de': ("Bestattung und Trauer in Genf: Ratgeber | Murith", "Formalitäten nach einem Todesfall, Bestattungskosten, Vorsorge, Überführung: unsere praktischen Ratgeber für Genfer Familien vom Haus Murith.", "Ratgeber für Familien"),
 'es': ("Funerales y duelo en Ginebra: guías | Murith", "Trámites tras un fallecimiento, coste de los funerales, previsión funeraria, repatriación: nuestras guías prácticas para las familias de Ginebra.", "Guías y consejos para las familias"),
 'pt': ("Funerais e luto em Genebra: guias | Murith", "Formalidades após um óbito, custo dos funerais, previdência funerária, repatriamento: os nossos guias práticos para as famílias de Genebra.", "Guias e conselhos para as famílias")},
}
LANG = {'fr': '', 'en': 'en/', 'de': 'de/', 'es': 'es/', 'pt': 'pt/'}

def check_lengths():
    bad = 0
    for f, d in D.items():
        for lg, (t, de, h1) in d.items():
            if len(t) > 60 or not (120 <= len(de) <= 160): print(f'  {f} {lg}: title {len(t)} | desc {len(de)}'); bad += 1
    return bad

LOG = []
def apply():
    for f, d in D.items():
        for lg, (t, de, h1) in d.items():
            p = P + LANG[lg] + f
            s = open(p, encoding='utf-8').read()
            ot = re.search(r'<title>(.*?)</title>', s, re.S).group(1).strip()
            od = (re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', s) or re.search(r'<meta[^>]*content="([^"]*)"[^>]*name="description"', s)).group(1)
            ntit, nd = html.escape(t, quote=False), html.escape(de, quote=True).replace('&#x27;', "'")
            if ot != ntit: s = s.replace(ot, ntit); LOG.append((f, lg, 'title', ot, t))
            if od != nd:
                s = s.replace(od, nd); LOG.append((f, lg, 'meta description', od, de))
            if h1:
                m = re.search(r'(<h1[^>]*>)(.*?)(</h1>)', s, re.S)
                old = re.sub(r'<[^>]+>', ' ', m.group(2)); old = ' '.join(html.unescape(old).split())
                if old != h1:
                    s = s[:m.start()] + m.group(1) + R(html.escape(h1, quote=False)) + m.group(3) + s[m.end():]
                    LOG.append((f, lg, 'H1', old, h1))
            open(p, 'w', encoding='utf-8').write(s)
    json.dump(LOG, open(ROOT + '/_build/phase2.log.json', 'w'), ensure_ascii=False, indent=1)
    print('modifications:', len(LOG))

if __name__ == '__main__':
    n = check_lengths(); print('hors limites:', n)
    if '--apply' in sys.argv: apply()
