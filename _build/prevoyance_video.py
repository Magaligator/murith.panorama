#!/usr/bin/env python3 -I
"""Ajoute la vidéo « prévoyance funéraire » + sections associées sur la page prévoyance (FR EN DE ES PT). Idempotent.
L'italien est généré ensuite par _build/it/build_it.py."""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
PLAY = '<svg aria-hidden="true" fill="currentColor" viewbox="0 0 24 24"><path d="M7 4.5v15l13-7.5-13-7.5Z"></path></svg>'
PLAY2 = '<svg aria-hidden="true" class="" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewbox="0 0 24 24"><path d="M7 4.500v15l13-7.500-13-7.500Z" fill="currentColor"></path></svg>'
L = {
 'fr': dict(badge='Vidéo', play='Lire la vidéo', note='', eb='En vidéo', h2='La prévoyance funéraire en 4 minutes',
   lead="Décider aujourd'hui ce que vous souhaitez pour demain : un de nos conseillers vous explique en quoi consiste une prévoyance funéraire et pourquoi la confiance en est le critère essentiel.",
   pts=["Choisir la cérémonie (laïque ou religieuse) et le mode de sépulture : inhumation ou crémation", "Fixer votre budget, avec des versements répartis dans le temps selon vos modalités", "Protéger vos proches et vous assurer que vos volontés seront respectées"],
   aria="Vidéo : la prévoyance funéraire expliquée par un conseiller Murith",
   te='La confiance avant tout', th="À qui confier sa prévoyance funéraire ?",
   tl="Une prévoyance se prépare pour dans 5, 10, 20, voire 30 ans. Au-delà de l'aspect financier, il s'agit de choisir les personnes à qui vous confierez l'organisation de vos dernières volontés.",
   cards=[("Une histoire, depuis 1888", "À Genève, les pompes funèbres Murith accompagnent les familles depuis 1888 : bientôt 140 ans d'expérience et de relation de confiance, avec la même mission, accompagner chaque famille avec dignité, respect et professionnalisme."),
          ("Un patrimoine immobilier propre", "L'entreprise possède son propre patrimoine immobilier, intégralement détenu par elle. Cet appui contribue à sa stabilité et à sa volonté de s'inscrire dans la durée, un critère fondamental quand on prépare ses obsèques plusieurs décennies à l'avance."),
          ("Une équipe qui connaît le terrain", "Plusieurs organismes proposent des solutions de prévoyance, avec des fondations indépendantes, des assurances ou des partenaires chargés d'organiser les obsèques. Chez Murith, vous connaissez concrètement l'entreprise qui sera présente le moment venu : nous maîtrisons les démarches administratives, les cérémonies et les attentes des familles.")],
   close="Parce que chaque vie est unique, chaque prévoyance doit l'être aussi : nous écoutons vos volontés pour préparer une organisation qui vous ressemble.",
   extra="Chez Murith, il est possible de répartir les versements dans le temps selon les modalités de chaque personne.",
   vname="Prévoyance funéraire à Genève : la vidéo Murith", vdesc="Un conseiller Murith explique en quoi consiste une prévoyance funéraire, ce que vous pouvez décider dès aujourd'hui et pourquoi la confiance dans l'entreprise compte. Vidéo en français."),
 'en': dict(badge='Video', play='Play the video', note='Video in French', eb='In video', h2='Funeral pre-planning in 4 minutes',
   lead="Deciding today what you want for tomorrow: one of our advisers explains what funeral pre-planning involves and why trust is the key criterion.",
   pts=["Choose the ceremony (secular or religious) and the type of burial: interment or cremation", "Set your budget, with payments spread over time to suit you", "Protect your loved ones and make sure your wishes are respected"],
   aria="Video: funeral pre-planning explained by a Murith adviser",
   te='Trust above all', th="Who should you entrust your funeral pre-planning to?",
   tl="A pre-plan is prepared for 5, 10, 20 or even 30 years ahead. Beyond the financial side, it is about choosing the people to whom you will entrust the organisation of your last wishes.",
   cards=[("A history since 1888", "In Geneva, Murith funeral services have been supporting families since 1888: soon 140 years of experience and trust, with the same mission – supporting every family with dignity, respect and professionalism."),
          ("Its own property assets", "The company owns its own real estate, entirely held by the company. This foundation contributes to its stability and its determination to last, a fundamental criterion when you prepare your funeral several decades in advance."),
          ("A team that knows the field", "Several organisations offer pre-planning solutions, with independent foundations, insurers or partners in charge of organising the funeral. At Murith, you know exactly who will be there when the time comes: we master the administrative procedures, the ceremonies and families' expectations.")],
   close="Because every life is unique, every pre-plan must be too: we listen to your wishes to prepare an organisation that reflects you.",
   extra="At Murith, payments can be spread over time to suit each person.",
   vname="Funeral pre-planning in Geneva: the Murith video", vdesc="A Murith adviser explains what funeral pre-planning involves, what you can decide today and why trust in the company matters. Video in French."),
 'de': dict(badge='Video', play='Video abspielen', note='Video auf Französisch', eb='Im Video', h2='Bestattungsvorsorge in 4 Minuten',
   lead="Heute entscheiden, was Sie für morgen wünschen: Einer unserer Berater erklärt, was eine Bestattungsvorsorge umfasst und warum Vertrauen das entscheidende Kriterium ist.",
   pts=["Die Trauerfeier (weltlich oder religiös) und die Bestattungsart wählen: Erdbestattung oder Kremation", "Ihr Budget festlegen, mit Zahlungen, die nach Ihren Möglichkeiten über die Zeit verteilt werden", "Ihre Angehörigen schützen und sicherstellen, dass Ihre Wünsche respektiert werden"],
   aria="Video: Bestattungsvorsorge, erklärt von einem Murith-Berater",
   te='Vertrauen zuerst', th="Wem vertrauen Sie Ihre Bestattungsvorsorge an?",
   tl="Eine Vorsorge wird für in 5, 10, 20 oder sogar 30 Jahren getroffen. Über den finanziellen Aspekt hinaus geht es darum, die Menschen zu wählen, denen Sie die Organisation Ihrer letzten Wünsche anvertrauen.",
   cards=[("Eine Geschichte seit 1888", "In Genf begleitet das Bestattungsinstitut Murith seit 1888 die Familien: bald 140 Jahre Erfahrung und Vertrauen, mit derselben Aufgabe – jede Familie mit Würde, Respekt und Professionalität zu begleiten."),
          ("Ein eigenes Immobilienvermögen", "Das Unternehmen besitzt eigene Immobilien, die vollständig in seinem Besitz sind. Diese Grundlage trägt zu seiner Stabilität und seinem Willen bei, dauerhaft zu bestehen – ein grundlegendes Kriterium, wenn man seine Bestattung mehrere Jahrzehnte im Voraus plant."),
          ("Ein Team, das die Praxis kennt", "Mehrere Organisationen bieten Vorsorgelösungen an, mit unabhängigen Stiftungen, Versicherungen oder Partnern, die die Bestattung organisieren. Bei Murith kennen Sie konkret das Unternehmen, das im entscheidenden Moment da sein wird: Wir beherrschen die Behördengänge, die Trauerfeiern und die Erwartungen der Familien.")],
   close="Weil jedes Leben einzigartig ist, muss es auch jede Vorsorge sein: Wir hören auf Ihre Wünsche, um eine Organisation vorzubereiten, die zu Ihnen passt.",
   extra="Bei Murith können die Zahlungen nach den Möglichkeiten jeder Person über die Zeit verteilt werden.",
   vname="Bestattungsvorsorge in Genf: das Murith-Video", vdesc="Ein Murith-Berater erklärt, was eine Bestattungsvorsorge umfasst, was Sie heute entscheiden können und warum das Vertrauen in das Unternehmen zählt. Video auf Französisch."),
 'es': dict(badge='Vídeo', play='Reproducir el vídeo', note='Vídeo en francés', eb='En vídeo', h2='La previsión funeraria en 4 minutos',
   lead="Decidir hoy lo que desea para mañana: uno de nuestros asesores le explica en qué consiste una previsión funeraria y por qué la confianza es el criterio esencial.",
   pts=["Elegir la ceremonia (laica o religiosa) y el tipo de sepultura: inhumación o cremación", "Fijar su presupuesto, con pagos repartidos en el tiempo según sus posibilidades", "Proteger a sus allegados y asegurarse de que se respeten sus voluntades"],
   aria="Vídeo: la previsión funeraria explicada por un asesor de Murith",
   te='La confianza ante todo', th="¿A quién confiar su previsión funeraria?",
   tl="Una previsión se prepara para dentro de 5, 10, 20 o incluso 30 años. Más allá del aspecto económico, se trata de elegir a las personas a quienes confiará la organización de sus últimas voluntades.",
   cards=[("Una historia desde 1888", "En Ginebra, los servicios funerarios Murith acompañan a las familias desde 1888: casi 140 años de experiencia y de relación de confianza, con la misma misión: acompañar a cada familia con dignidad, respeto y profesionalidad."),
          ("Un patrimonio inmobiliario propio", "La empresa posee su propio patrimonio inmobiliario, íntegramente suyo. Este respaldo contribuye a su estabilidad y a su voluntad de perdurar, un criterio fundamental cuando se preparan los funerales con varias décadas de antelación."),
          ("Un equipo que conoce el terreno", "Varias entidades ofrecen soluciones de previsión, con fundaciones independientes, aseguradoras o socios encargados de organizar los funerales. En Murith conoce concretamente a la empresa que estará presente llegado el momento: dominamos los trámites administrativos, las ceremonias y las expectativas de las familias.")],
   close="Porque cada vida es única, cada previsión debe serlo también: escuchamos sus voluntades para preparar una organización que se parezca a usted.",
   extra="En Murith, los pagos pueden repartirse en el tiempo según las posibilidades de cada persona.",
   vname="Previsión funeraria en Ginebra: el vídeo de Murith", vdesc="Un asesor de Murith explica en qué consiste una previsión funeraria, qué puede decidir hoy y por qué es importante la confianza en la empresa. Vídeo en francés."),
 'pt': dict(badge='Vídeo', play='Reproduzir o vídeo', note='Vídeo em francês', eb='Em vídeo', h2='A previdência funerária em 4 minutos',
   lead="Decidir hoje o que deseja para amanhã: um dos nossos conselheiros explica em que consiste uma previdência funerária e porque é que a confiança é o critério essencial.",
   pts=["Escolher a cerimónia (laica ou religiosa) e o tipo de sepultura: inumação ou cremação", "Definir o seu orçamento, com pagamentos repartidos no tempo de acordo com as suas possibilidades", "Proteger os seus familiares e garantir que as suas vontades serão respeitadas"],
   aria="Vídeo: a previdência funerária explicada por um conselheiro da Murith",
   te='A confiança acima de tudo', th="A quem confiar a sua previdência funerária?",
   tl="Uma previdência prepara-se para daqui a 5, 10, 20 ou até 30 anos. Para além do aspeto financeiro, trata-se de escolher as pessoas a quem confiará a organização das suas últimas vontades.",
   cards=[("Uma história desde 1888", "Em Genebra, os serviços funerários Murith acompanham as famílias desde 1888: quase 140 anos de experiência e de relação de confiança, com a mesma missão: acompanhar cada família com dignidade, respeito e profissionalismo."),
          ("Um património imobiliário próprio", "A empresa possui o seu próprio património imobiliário, integralmente detido por si. Esta base contribui para a sua estabilidade e para a sua vontade de perdurar, um critério fundamental quando se preparam os funerais com várias décadas de antecedência."),
          ("Uma equipa que conhece o terreno", "Várias entidades propõem soluções de previdência, com fundações independentes, seguradoras ou parceiros encarregados de organizar os funerais. Na Murith, conhece concretamente a empresa que estará presente no momento certo: dominamos as diligências administrativas, as cerimónias e as expectativas das famílias.")],
   close="Porque cada vida é única, cada previdência deve sê-lo também: ouvimos as suas vontades para preparar uma organização que se pareça consigo.",
   extra="Na Murith, os pagamentos podem ser repartidos no tempo de acordo com as possibilidades de cada pessoa.",
   vname="Previdência funerária em Genebra: o vídeo da Murith", vdesc="Um conselheiro da Murith explica em que consiste uma previdência funerária, o que pode decidir hoje e porque é importante a confiança na empresa. Vídeo em francês."),
}
FAQ_FR = [("Peut-on étaler le paiement d'une prévoyance funéraire ?", "Oui. Chez Murith, il est possible de répartir les versements dans le temps selon les modalités de chaque personne, après avoir choisi la cérémonie, le mode de sépulture et fixé son budget."),
          ("Pourquoi confier sa prévoyance à une entreprise de pompes funèbres genevoise ?", "Parce qu'une prévoyance se prépare pour dans 5, 10, 20 ou 30 ans : il est essentiel de connaître l'entreprise qui sera présente le moment venu. Les pompes funèbres Murith accompagnent les familles depuis 1888 et possèdent leur propre patrimoine immobilier, gage de stabilité dans la durée.")]
TRANSCRIPT_FR = [
 "Mesdames et messieurs, bonjour ! Nous sommes ici aux pompes funèbres Murith et nous allons aujourd'hui parler un petit peu de prévoyance funéraire. On pense souvent que prévoir ses obsèques à l'avance, c'est quelque chose qu'on peut remettre à demain. Cependant, la démarche est très importante, avant tout pour protéger ses proches mais surtout pour que ses volontés soient respectées.",
 "Mais une question essentielle se pose : à qui confier cette prévoyance ? Avant d'y répondre, il faut comprendre en quoi consiste cette prestation. Une prévoyance funéraire permet de décider aujourd'hui ce que l'on souhaite pour demain. Quel type de cérémonie ? Laïque ou religieuse ? Quel type de sépulture ? Une crémation ou une mise en terre du corps, que l'on appelle dans le jargon une inhumation ? Et surtout, critère important, quel budget allouer pour le service ? Chez Murith, il est possible de répartir les versements dans le temps selon les modalités de chaque personne. Finalement, c'est une démarche de sérénité pour soi et surtout pour sa famille.",
 "Pour prévoir un projet sur le long terme, un critère est très important : la confiance. Lorsqu'on organise une telle démarche, on prévoit quelque chose qui peut se passer dans 5, 10, 20 ou même 30 ans. Il est donc essentiel de choisir une entreprise de pompes funèbres sérieuse qui a su s'inscrire dans la durée. Car une prévoyance funéraire ne se résume pas à une simple question financière : c'est surtout choisir les personnes à qui l'on confiera l'organisation de ses dernières volontés.",
 "À Genève, les pompes funèbres Murith accompagnent les familles depuis 1888. Cela représente bientôt 140 ans d'histoire, d'expérience et de relation de confiance avec les Genevois. Au fil des générations, notre entreprise a traversé de nombreuses évolutions, tout en conservant sa mission première : accompagner les familles avec dignité, respect et professionnalisme. Cette histoire est aujourd'hui l'un des fondements de notre engagement.",
 "Notre entreprise s'appuie également sur un autre élément fondamental : son patrimoine. Les pompes funèbres Murith possèdent leur propre patrimoine immobilier, intégralement détenu par l'entreprise. Cette assise patrimoniale contribue à notre stabilité et à notre volonté de nous inscrire dans la durée. Et lorsque l'on prépare ses obsèques plusieurs décennies à l'avance, la stabilité d'une entreprise est un critère fondamental.",
 "Aujourd'hui, plusieurs organismes proposent des solutions de prévoyance funéraire. Certains fonctionnent avec des fondations indépendantes, d'autres avec des assurances ou des partenaires chargés d'organiser les obsèques. Bien que ces modèles répondent à des besoins différents, chez Murith, nous pensons qu'il est également essentiel de connaître concrètement l'entreprise qui sera présente le moment venu. Car au-delà du financement, il y a des personnes, un savoir-faire et surtout une responsabilité envers les familles.",
 "Faire une prévoyance chez Murith, c'est avant tout établir un lien de confiance avec une entreprise de pompes funèbres qui connaît son métier. Nous connaissons les réalités du terrain, les différentes démarches administratives, les contraintes liées aux cérémonies, mais aussi et surtout les attentes des familles. Notre objectif est simple : écouter chaque personne, comprendre ses volontés et préparer une organisation qui lui ressemble. Parce que chaque vie est unique, chaque prévoyance doit l'être également.",
 "Prévoir ses obsèques, c'est une décision très importante pour soi, mais aussi et surtout pour ceux que l'on aime. C'est pourquoi nous pensons qu'au-delà des offres, des assurances et des différentes formules, la confiance doit rester au cœur de cette démarche. Depuis 1888, les pompes funèbres Murith accompagnent les familles genevoises, et c'est avec ce même engagement que nous souhaitons les accompagner demain."]
def esc(s): return s.replace('&', '&amp;')
def video_section(lg):
    t = L[lg]
    track = '<track kind="captions" label="Français" src="/img/video-prevoyance-fr.vtt" srclang="fr"/>' if lg == 'fr' else ''
    note = f'<p class="pv-note">{t["note"]}</p>' if t['note'] else ''
    tr = ''
    if lg == 'fr':
        tr = ('<div class="faq pv-tr reveal" data-fr-only=""><details><summary>Lire la transcription de la vidéo<i aria-hidden="true"></i></summary><div class="ans">'
              + ''.join(f'<p>{esc(p)}</p>' for p in TRANSCRIPT_FR) + '</div></details></div>')
    return ('<section class="section prev-video" id="video"><div class="container"><div class="split pv-split">'
            f'<div class="reveal"><div class="vcard"><span class="v-badge">{PLAY}<b>{t["badge"]}</b><i class="v-dur" data-dur="">4:27</i></span>'
            f'<video aria-label="{esc(t["aria"])}" playsinline="" poster="/img/video-prevoyance-poster.jpg" preload="none"><source src="/img/video-prevoyance.mp4" type="video/mp4"/>{track}</video>'
            f'<button aria-label="{t["play"]}" class="vplay" type="button">{PLAY2}</button><span class="v-cap">{t["play"]}</span></div>{note}</div>'
            f'<div class="reveal" style="--d:.1s"><p class="eyebrow">{t["eb"]}</p><h2>{esc(t["h2"])}</h2><p class="lead">{esc(t["lead"])}</p>'
            '<ul class="pv-points">' + ''.join(f'<li>{esc(x)}</li>' for x in t['pts']) + '</ul></div></div>' + tr + '</div></section>')
def trust_section(lg):
    t = L[lg]
    cards = ''.join(f'<div class="card reveal" style="--d:{i*.08:.2f}s"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for i, (a, b) in enumerate(t['cards']))
    return (f'<section class="section alt pv-trust"><div class="container"><div class="sec-head reveal"><p class="eyebrow">{esc(t["te"])}</p><h2>{esc(t["th"])}</h2><p class="lead">{esc(t["tl"])}</p></div>'
            f'<div class="g3">{cards}</div><p class="pv-close reveal">{esc(t["close"])}</p></div></section>')
def video_ld(lg):
    t = L[lg]
    j = {"@context": "https://schema.org", "@type": "VideoObject", "name": t['vname'], "description": t['vdesc'],
         "thumbnailUrl": "https://www.murith.ch/img/video-prevoyance-poster.jpg", "uploadDate": "2026-11-13", "duration": "PT4M27S",
         "contentUrl": "https://www.murith.ch/img/video-prevoyance.mp4", "inLanguage": "fr",
         "publisher": {"@id": "https://www.murith.ch/#entreprise"}}
    return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(',', ':')) + '</script>'
n = 0
for lg in L:
    p = root / (('' if lg == 'fr' else lg + '/') + 'prevoyance-funeraire.html')
    h = p.read_text(encoding='utf8')
    if 'prev-video' in h: continue
    t = L[lg]
    # 1) vidéo après le héros
    i = h.find('</section>', h.find('class="phead pan-ph"')) + len('</section>')
    h = h[:i] + video_section(lg) + h[i:]
    # 2) phrase « versements étalés » dans la carte
    m = re.search(r'(<p style="margin:0">)(.*?)(</p></div>\n</div></section>)', h, re.S)
    h = h[:m.start()] + m.group(1) + m.group(2) + ' ' + esc(t['extra']) + m.group(3) + h[m.end():]
    # 3) section confiance (avant la FAQ en FR, avant l'appel final sinon)
    anchor = '<section class="section" id="faq">' if lg == 'fr' else '<section class="section tight cta-prev-sec">'
    j = h.find(anchor); h = h[:j] + trust_section(lg) + h[j:]
    # 4) FAQ (FR) + JSON-LD
    if lg == 'fr':
        items = ''.join(f'<details><summary>{esc(q)}<i aria-hidden="true"></i></summary><div class="ans"><p>{esc(a)}</p></div></details>' for q, a in FAQ_FR)
        k = h.find('</div>', h.rfind('</details>', 0, h.find('<section class="section tight rel-sec"'))) 
        k = h.rfind('</details>', 0, h.find('<section class="section tight rel-sec"')) + len('</details>')
        h = h[:k] + items + h[k:]
        qs = ','.join(json.dumps({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}, ensure_ascii=False, separators=(',', ':')) for q, a in FAQ_FR)
        h = re.sub(r'(\{"@context":"https://schema.org","@type":"FAQPage","mainEntity":\[.*?)\]\}</script>', lambda mm: mm.group(1) + ',' + qs + ']}</script>', h, count=1, flags=re.S)
    h = h.replace('</head>', video_ld(lg) + '\n</head>', 1)
    p.write_text(h, encoding='utf8'); n += 1
print('pages modifiées :', n)
