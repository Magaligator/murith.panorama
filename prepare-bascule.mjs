#!/usr/bin/env node
// prepare-bascule.mjs — prépare le site Murith avant la bascule du domaine murith.ch (Wix → Vercel).
//
// Ce que fait le script (rejouable sans risque : une 2e exécution ne change plus rien) :
//   1. Crée la page « Politique de confidentialité » dans les 6 langues (nLPD) : le pied de page y pointait déjà (404).
//   2. Crée l'article /blog/cout-obseques-geneve (migration de « Comprendre le coût d'un enterrement à Genève »),
//      l'ajoute au blog (liste + données structurées).
//   3. Retire le texte rouge de relecture (classe « seo-new ») sur toutes les pages, en gardant le texte,
//      et supprime la règle CSS. La liste de ce qui était en rouge est conservée dans _build/rapport-texte-rouge.md.
//   4. Met à jour sitemap.xml et check-seo.mjs (page FR seule autorisée pour le nouvel article).
//   5. Relance migration-murith.mjs (les redirections pointent maintenant vers les vraies pages) puis check-seo.mjs.
//
// Usage, à la racine du dépôt :   node prepare-bascule.mjs
// Pour annuler avant de publier :  git restore . && git clean -fd   (attention : efface aussi vos autres changements)

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = path.dirname(fileURLToPath(import.meta.url));
process.chdir(root);
const BASE = 'https://www.murith.ch';
const DATE = '2026-11-25';                       // date de mise à jour affichée / sitemap
const LANGS = ['fr', 'en', 'de', 'it', 'es', 'pt'];
const rd = f => fs.readFileSync(path.join(root, f), 'utf8');
const wr = (f, t) => { fs.mkdirSync(path.dirname(path.join(root, f)), { recursive: true }); fs.writeFileSync(path.join(root, f), t); };
const log = [];
const say = m => { log.push(m); console.log('  ' + m); };
const esc = s => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

for (const f of ['index.html', 'vercel.json', 'blog.html', 'sitemap.xml', 'blog/cout-rapatriement-corps.html', '404.html']) {
  if (!fs.existsSync(path.join(root, f))) { console.error(`✘ ${f} introuvable : lancez ce script à la racine du dépôt murith.panorama.`); process.exit(1); }
}

/* ─────────────────────────────────────────────────────────────
   1. Page de confidentialité (6 langues)
   ───────────────────────────────────────────────────────────── */
const P = s => `<p>${s}</p>`;
const UL = a => `<ul>${a.map(x => `<li>${x}</li>`).join('')}</ul>`;
const MAIL = '<a href="mailto:murith@murith.ch">murith@murith.ch</a>';
const TEL = '+41 22 809 56 00';

const PRIV = {
  fr: {
    title: 'Politique de confidentialité | Murith',
    desc: 'Comment A. Murith SA, pompes funèbres à Genève, traite vos données personnelles : formulaires, hébergement, cookies et vos droits selon la nLPD.',
    home: 'Accueil', crumbAria: "Fil d'Ariane", h1: 'Politique de confidentialité',
    lead: 'Quelles données nous traitons, pourquoi, et comment vous gardez la maîtrise de vos informations.',
    updated: 'Dernière mise à jour : 25 novembre 2026.',
    sec: [
      ['Qui est responsable de vos données ?', P(`Le responsable du traitement est A. Murith SA, pompes funèbres, 89, boulevard de la Cluse, 1205 Genève, Suisse (téléphone ${TEL}, e-mail ${MAIL}). Cette politique s'applique à ce site et suit la loi fédérale sur la protection des données (nLPD).`)],
      ['Quelles données traitons-nous ?', UL([
        'Lorsque vous visitez le site : adresse IP, date et heure, pages consultées, type de navigateur et d\'appareil. Ces données techniques sont enregistrées par notre hébergeur pour assurer le fonctionnement et la sécurité du site.',
        'Lorsque vous nous écrivez (formulaires de contact et de devis, e-mail, téléphone) : nom, prénom, adresse e-mail, numéro de téléphone et contenu de votre message.']) +
        P('Nous vous invitons à n\'indiquer dans les formulaires que l\'essentiel. Les informations plus sensibles (situation du défunt, volontés, convictions religieuses) sont échangées de vive voix ou lors d\'un entretien.')],
      ['Pourquoi utilisons-nous ces données ?', UL([
        'répondre à vos demandes et vous rappeler ;',
        'établir un devis et préparer l\'accompagnement de votre famille ;',
        'assurer la sécurité et le bon fonctionnement du site ;',
        'respecter nos obligations légales.']) +
        P('En envoyant un formulaire, vous acceptez que nous utilisions vos données pour traiter votre demande. Nous ne les vendons pas et ne les utilisons pas à des fins publicitaires.')],
      ['Qui reçoit vos données ?', P('Seules les personnes de notre équipe qui en ont besoin y accèdent. Nous faisons aussi appel à des prestataires techniques, tenus de protéger vos données :') +
        UL(['Vercel Inc. : hébergement du site (États-Unis) ;',
          'Resend : envoi des messages de nos formulaires vers notre messagerie (États-Unis) ;',
          'contenus intégrés : certaines pages affichent une carte OpenStreetMap, un catalogue en ligne (FlipBuilder) ou une vidéo (YouTube, mode sans cookies). Quand ces contenus s\'affichent, votre adresse IP est transmise à ces services, qui appliquent leurs propres règles.']) +
        P('Les liens vers Google Maps, LinkedIn, Instagram ou d\'autres sites vous mènent hors de notre site : leur politique de confidentialité s\'applique alors.')],
      ['Vos données à l\'étranger', P('Certains prestataires (hébergement, envoi d\'e-mails) sont établis hors de Suisse, notamment aux États-Unis. Lorsque le pays n\'offre pas un niveau de protection reconnu comme adéquat, nous nous appuyons sur des garanties appropriées, telles que les clauses contractuelles types.')],
      ['Cookies et stockage dans votre navigateur', P('Ce site n\'utilise ni cookies publicitaires, ni outil de suivi ou de mesure d\'audience. Il peut enregistrer dans votre navigateur (stockage local ou de session) des réglages d\'affichage et l\'avancement de nos listes de contrôle. Ces informations restent sur votre appareil, ne vous identifient pas et ne servent pas à vous suivre. Si nous ajoutons un outil de mesure d\'audience, cette page sera mise à jour.')],
      ['Durée de conservation', P('Nous conservons vos données le temps nécessaire pour traiter votre demande et respecter nos obligations légales, puis nous les supprimons ou les anonymisons. Les journaux techniques de l\'hébergeur sont conservés pour une durée limitée.')],
      ['Sécurité', P('Le site est servi en connexion chiffrée (HTTPS). Nous prenons des mesures techniques et organisationnelles raisonnables pour protéger vos données contre l\'accès non autorisé, la perte ou l\'altération.')],
      ['Vos droits', P(`Vous pouvez demander l'accès à vos données, leur rectification, leur suppression, la limitation ou l'opposition à leur traitement, ainsi que leur remise dans un format courant. Si vous avez donné votre consentement, vous pouvez le retirer à tout moment. Écrivez-nous à ${MAIL} ; nous pouvons vous demander une pièce d'identité pour traiter votre demande.`) +
        P('Vous pouvez aussi vous adresser au Préposé fédéral à la protection des données et à la transparence (PFPDT) : <a href="https://www.edoeb.admin.ch" rel="noopener" target="_blank">www.edoeb.admin.ch</a>.')],
      ['Modifications', P('Nous pouvons adapter cette politique, par exemple si nous ajoutons un service au site. La version en ligne fait foi.')],
    ],
  },
  en: {
    title: 'Privacy policy | Murith Funeral Services Geneva',
    desc: 'How A. Murith SA, funeral directors in Geneva, handles your personal data: forms, hosting, cookies and your rights under the Swiss FADP.',
    home: 'Home', crumbAria: 'Breadcrumb', h1: 'Privacy policy',
    lead: 'Which data we process, why, and how you stay in control of your information.',
    updated: 'Last updated: 25 November 2026.',
    sec: [
      ['Who is responsible for your data?', P(`The controller is A. Murith SA, funeral directors, 89 boulevard de la Cluse, 1205 Geneva, Switzerland (phone ${TEL}, e-mail ${MAIL}). This policy applies to this website and follows the Swiss Federal Act on Data Protection (FADP).`)],
      ['Which data do we process?', UL([
        'When you visit the site: IP address, date and time, pages viewed, browser and device type. Our hosting provider records these technical data to keep the site running and secure.',
        'When you contact us (contact and quote forms, e-mail, phone): first name, last name, e-mail address, phone number and the content of your message.']) +
        P('Please share only what is essential in the forms. More sensitive information (the situation of the deceased, wishes, religious beliefs) is discussed by phone or in a meeting.')],
      ['Why do we use these data?', UL([
        'to answer your requests and call you back;',
        'to prepare a quote and plan support for your family;',
        'to keep the site secure and working;',
        'to meet our legal obligations.']) +
        P('By sending a form, you agree that we use your data to handle your request. We do not sell them and do not use them for advertising.')],
      ['Who receives your data?', P('Only the members of our team who need them have access. We also use technical providers, who must protect your data:') +
        UL(['Vercel Inc.: website hosting (United States);',
          'Resend: delivery of our form messages to our mailbox (United States);',
          'embedded content: some pages show an OpenStreetMap map, an online catalogue (FlipBuilder) or a video (YouTube, no-cookie mode). When this content loads, your IP address is sent to these services, which apply their own rules.']) +
        P('Links to Google Maps, LinkedIn, Instagram or other sites take you away from our site: their own privacy policies then apply.')],
      ['Your data abroad', P('Some providers (hosting, e-mail delivery) are based outside Switzerland, notably in the United States. Where the country does not offer a level of protection recognised as adequate, we rely on appropriate safeguards such as standard contractual clauses.')],
      ['Cookies and browser storage', P('This site uses no advertising cookies and no tracking or analytics tool. It may save display settings and the progress of our checklists in your browser (local or session storage). This information stays on your device, does not identify you and is not used to track you. If we add an analytics tool, this page will be updated.')],
      ['How long we keep your data', P('We keep your data as long as needed to handle your request and meet our legal obligations, then we delete or anonymise it. The hosting provider keeps technical logs for a limited period.')],
      ['Security', P('The site is served over an encrypted connection (HTTPS). We take reasonable technical and organisational measures to protect your data against unauthorised access, loss or alteration.')],
      ['Your rights', P(`You may ask for access to your data, its correction or deletion, restriction of or objection to its processing, and a copy in a common format. If you gave consent, you may withdraw it at any time. Write to us at ${MAIL}; we may ask for proof of identity to handle your request.`) +
        P('You can also contact the Federal Data Protection and Information Commissioner (FDPIC): <a href="https://www.edoeb.admin.ch" rel="noopener" target="_blank">www.edoeb.admin.ch</a>.')],
      ['Changes', P('We may update this policy, for example when we add a service to the site. The online version prevails.')],
    ],
  },
  de: {
    title: 'Datenschutzerklärung | Bestattungen Murith Genf',
    desc: 'Wie A. Murith SA, Bestattungsinstitut in Genf, Ihre Personendaten bearbeitet: Formulare, Hosting, Cookies und Ihre Rechte nach dem Schweizer DSG.',
    home: 'Startseite', crumbAria: 'Brotkrumennavigation', h1: 'Datenschutzerklärung',
    lead: 'Welche Daten wir bearbeiten, warum, und wie Sie die Kontrolle über Ihre Angaben behalten.',
    updated: 'Letzte Aktualisierung: 25. November 2026.',
    sec: [
      ['Wer ist für Ihre Daten verantwortlich?', P(`Verantwortlich ist die A. Murith SA, Bestattungsinstitut, 89, boulevard de la Cluse, 1205 Genf, Schweiz (Telefon ${TEL}, E-Mail ${MAIL}). Diese Erklärung gilt für diese Website und richtet sich nach dem Schweizer Bundesgesetz über den Datenschutz (DSG).`)],
      ['Welche Daten bearbeiten wir?', UL([
        'Beim Besuch der Website: IP-Adresse, Datum und Uhrzeit, aufgerufene Seiten, Browser- und Gerätetyp. Unser Hosting-Anbieter zeichnet diese technischen Daten auf, um den Betrieb und die Sicherheit der Website zu gewährleisten.',
        'Wenn Sie uns schreiben (Kontakt- und Offertformulare, E-Mail, Telefon): Vorname, Name, E-Mail-Adresse, Telefonnummer und Inhalt Ihrer Nachricht.']) +
        P('Bitte geben Sie in den Formularen nur das Wesentliche an. Sensiblere Informationen (Situation der verstorbenen Person, Wünsche, religiöse Überzeugungen) besprechen wir telefonisch oder im persönlichen Gespräch.')],
      ['Wozu verwenden wir diese Daten?', UL([
        'um Ihre Anfragen zu beantworten und Sie zurückzurufen;',
        'um eine Offerte zu erstellen und die Begleitung Ihrer Familie vorzubereiten;',
        'um die Sicherheit und den Betrieb der Website zu gewährleisten;',
        'um unsere gesetzlichen Pflichten zu erfüllen.']) +
        P('Mit dem Absenden eines Formulars sind Sie damit einverstanden, dass wir Ihre Daten zur Bearbeitung Ihrer Anfrage verwenden. Wir verkaufen sie nicht und nutzen sie nicht für Werbung.')],
      ['Wer erhält Ihre Daten?', P('Nur die Mitglieder unseres Teams, die sie benötigen, haben Zugriff. Wir setzen ausserdem technische Dienstleister ein, die Ihre Daten schützen müssen:') +
        UL(['Vercel Inc.: Hosting der Website (USA);',
          'Resend: Zustellung der Nachrichten aus unseren Formularen an unser Postfach (USA);',
          'eingebettete Inhalte: Einige Seiten zeigen eine OpenStreetMap-Karte, einen Online-Katalog (FlipBuilder) oder ein Video (YouTube, Modus ohne Cookies). Beim Laden dieser Inhalte wird Ihre IP-Adresse an diese Dienste übermittelt, die ihre eigenen Regeln anwenden.']) +
        P('Links zu Google Maps, LinkedIn, Instagram oder anderen Websites führen Sie aus unserer Website hinaus: Dort gelten deren eigene Datenschutzbestimmungen.')],
      ['Ihre Daten im Ausland', P('Einige Dienstleister (Hosting, E-Mail-Versand) haben ihren Sitz ausserhalb der Schweiz, insbesondere in den USA. Wenn das Land kein als angemessen anerkanntes Datenschutzniveau bietet, stützen wir uns auf geeignete Garantien, etwa Standardvertragsklauseln.')],
      ['Cookies und Speicher im Browser', P('Diese Website verwendet weder Werbe-Cookies noch Tracking- oder Analysetools. Sie kann Anzeigeeinstellungen und den Fortschritt unserer Checklisten im Browser speichern (lokaler Speicher oder Sitzungsspeicher). Diese Angaben bleiben auf Ihrem Gerät, identifizieren Sie nicht und dienen nicht der Verfolgung. Falls wir ein Analysetool einsetzen, wird diese Seite angepasst.')],
      ['Aufbewahrungsdauer', P('Wir bewahren Ihre Daten so lange auf, wie es zur Bearbeitung Ihrer Anfrage und zur Erfüllung unserer gesetzlichen Pflichten nötig ist, und löschen oder anonymisieren sie danach. Die technischen Protokolle des Hosting-Anbieters werden nur für eine begrenzte Dauer aufbewahrt.')],
      ['Sicherheit', P('Die Website wird über eine verschlüsselte Verbindung (HTTPS) ausgeliefert. Wir treffen angemessene technische und organisatorische Massnahmen, um Ihre Daten vor unbefugtem Zugriff, Verlust oder Veränderung zu schützen.')],
      ['Ihre Rechte', P(`Sie können Auskunft über Ihre Daten, deren Berichtigung oder Löschung, die Einschränkung oder den Widerspruch gegen die Bearbeitung sowie die Herausgabe in einem gängigen Format verlangen. Eine erteilte Einwilligung können Sie jederzeit widerrufen. Schreiben Sie uns an ${MAIL}; zur Bearbeitung Ihrer Anfrage können wir einen Identitätsnachweis verlangen.`) +
        P('Sie können sich auch an den Eidgenössischen Datenschutz- und Öffentlichkeitsbeauftragten (EDÖB) wenden: <a href="https://www.edoeb.admin.ch" rel="noopener" target="_blank">www.edoeb.admin.ch</a>.')],
      ['Änderungen', P('Wir können diese Erklärung anpassen, zum Beispiel wenn wir der Website einen Dienst hinzufügen. Es gilt die Online-Version.')],
    ],
  },
  it: {
    title: 'Informativa sulla privacy | Pompe funebri Murith',
    desc: 'Come A. Murith SA, pompe funebri a Ginevra, tratta i vostri dati personali: moduli, hosting, cookie e i vostri diritti secondo la LPD svizzera.',
    home: 'Home', crumbAria: 'Percorso di navigazione', h1: 'Informativa sulla privacy',
    lead: 'Quali dati trattiamo, perché, e come mantenete il controllo delle vostre informazioni.',
    updated: 'Ultimo aggiornamento: 25 novembre 2026.',
    sec: [
      ['Chi è responsabile dei vostri dati?', P(`Il titolare del trattamento è A. Murith SA, pompe funebri, 89, boulevard de la Cluse, 1205 Ginevra, Svizzera (telefono ${TEL}, e-mail ${MAIL}). La presente informativa si applica a questo sito e segue la legge federale sulla protezione dei dati (LPD).`)],
      ['Quali dati trattiamo?', UL([
        'Quando visitate il sito: indirizzo IP, data e ora, pagine consultate, tipo di browser e di dispositivo. Questi dati tecnici sono registrati dal nostro fornitore di hosting per garantire il funzionamento e la sicurezza del sito.',
        'Quando ci scrivete (moduli di contatto e di preventivo, e-mail, telefono): nome, cognome, indirizzo e-mail, numero di telefono e contenuto del messaggio.']) +
        P('Vi invitiamo a indicare nei moduli solo l\'essenziale. Le informazioni più sensibili (situazione del defunto, volontà, convinzioni religiose) vengono scambiate a voce o durante un colloquio.')],
      ['Perché usiamo questi dati?', UL([
        'per rispondere alle vostre richieste e richiamarvi;',
        'per preparare un preventivo e l\'accompagnamento della vostra famiglia;',
        'per garantire la sicurezza e il funzionamento del sito;',
        'per rispettare i nostri obblighi di legge.']) +
        P('Inviando un modulo, accettate che usiamo i vostri dati per trattare la richiesta. Non li vendiamo e non li usiamo a fini pubblicitari.')],
      ['Chi riceve i vostri dati?', P('Vi accedono solo i membri del nostro team che ne hanno bisogno. Ci avvaliamo anche di fornitori tecnici, tenuti a proteggere i vostri dati:') +
        UL(['Vercel Inc.: hosting del sito (Stati Uniti);',
          'Resend: invio dei messaggi dei nostri moduli alla nostra casella di posta (Stati Uniti);',
          'contenuti incorporati: alcune pagine mostrano una mappa OpenStreetMap, un catalogo online (FlipBuilder) o un video (YouTube, modalità senza cookie). Quando questi contenuti si caricano, il vostro indirizzo IP viene trasmesso a questi servizi, che applicano le proprie regole.']) +
        P('I link verso Google Maps, LinkedIn, Instagram o altri siti vi portano fuori dal nostro sito: si applica allora la loro informativa sulla privacy.')],
      ['I vostri dati all\'estero', P('Alcuni fornitori (hosting, invio di e-mail) hanno sede fuori dalla Svizzera, in particolare negli Stati Uniti. Quando il Paese non offre un livello di protezione riconosciuto come adeguato, ci basiamo su garanzie appropriate, come le clausole contrattuali tipo.')],
      ['Cookie e memoria del browser', P('Questo sito non usa cookie pubblicitari né strumenti di tracciamento o di misurazione dell\'audience. Può salvare nel browser (memoria locale o di sessione) impostazioni di visualizzazione e l\'avanzamento delle nostre checklist. Queste informazioni restano sul vostro dispositivo, non vi identificano e non servono a tracciarvi. Se aggiungeremo uno strumento di misurazione dell\'audience, questa pagina sarà aggiornata.')],
      ['Durata di conservazione', P('Conserviamo i vostri dati per il tempo necessario a trattare la richiesta e a rispettare i nostri obblighi di legge, poi li cancelliamo o li rendiamo anonimi. I log tecnici del fornitore di hosting sono conservati per un periodo limitato.')],
      ['Sicurezza', P('Il sito è servito tramite una connessione cifrata (HTTPS). Adottiamo misure tecniche e organizzative ragionevoli per proteggere i vostri dati da accessi non autorizzati, perdita o alterazione.')],
      ['I vostri diritti', P(`Potete chiedere l'accesso ai vostri dati, la loro rettifica o cancellazione, la limitazione o l'opposizione al trattamento, nonché la consegna in un formato di uso comune. Se avete dato il consenso, potete revocarlo in qualsiasi momento. Scriveteci a ${MAIL}; per trattare la richiesta possiamo chiedervi un documento d'identità.`) +
        P('Potete anche rivolgervi all\'Incaricato federale della protezione dei dati e della trasparenza (IFPDT): <a href="https://www.edoeb.admin.ch" rel="noopener" target="_blank">www.edoeb.admin.ch</a>.')],
      ['Modifiche', P('Possiamo adeguare questa informativa, ad esempio se aggiungiamo un servizio al sito. Fa fede la versione online.')],
    ],
  },
  es: {
    title: 'Política de privacidad | Pompas fúnebres Murith',
    desc: 'Cómo A. Murith SA, pompas fúnebres en Ginebra, trata sus datos personales: formularios, alojamiento, cookies y sus derechos según la LPD suiza.',
    home: 'Inicio', crumbAria: 'Ruta de navegación', h1: 'Política de privacidad',
    lead: 'Qué datos tratamos, por qué, y cómo conserva usted el control de su información.',
    updated: 'Última actualización: 25 de noviembre de 2026.',
    sec: [
      ['¿Quién es responsable de sus datos?', P(`El responsable del tratamiento es A. Murith SA, pompas fúnebres, 89, boulevard de la Cluse, 1205 Ginebra, Suiza (teléfono ${TEL}, correo electrónico ${MAIL}). Esta política se aplica a este sitio web y se rige por la ley federal suiza de protección de datos (LPD).`)],
      ['¿Qué datos tratamos?', UL([
        'Cuando visita el sitio: dirección IP, fecha y hora, páginas consultadas, tipo de navegador y de dispositivo. Nuestro proveedor de alojamiento registra estos datos técnicos para garantizar el funcionamiento y la seguridad del sitio.',
        'Cuando nos escribe (formularios de contacto y de presupuesto, correo electrónico, teléfono): nombre, apellidos, dirección de correo electrónico, número de teléfono y contenido de su mensaje.']) +
        P('Le invitamos a indicar en los formularios solo lo esencial. La información más sensible (situación del difunto, voluntades, creencias religiosas) se trata de viva voz o en una entrevista.')],
      ['¿Para qué usamos estos datos?', UL([
        'responder a sus solicitudes y llamarle;',
        'elaborar un presupuesto y preparar el acompañamiento de su familia;',
        'garantizar la seguridad y el buen funcionamiento del sitio;',
        'cumplir nuestras obligaciones legales.']) +
        P('Al enviar un formulario, usted acepta que utilicemos sus datos para tramitar su solicitud. No los vendemos ni los utilizamos con fines publicitarios.')],
      ['¿Quién recibe sus datos?', P('Solo acceden a ellos los miembros de nuestro equipo que los necesitan. También recurrimos a proveedores técnicos, obligados a proteger sus datos:') +
        UL(['Vercel Inc.: alojamiento del sitio (Estados Unidos);',
          'Resend: envío de los mensajes de nuestros formularios a nuestro buzón (Estados Unidos);',
          'contenidos incrustados: algunas páginas muestran un mapa de OpenStreetMap, un catálogo en línea (FlipBuilder) o un vídeo (YouTube, modo sin cookies). Cuando se cargan estos contenidos, su dirección IP se transmite a esos servicios, que aplican sus propias normas.']) +
        P('Los enlaces a Google Maps, LinkedIn, Instagram u otros sitios le llevan fuera de nuestro sitio: se aplica entonces su propia política de privacidad.')],
      ['Sus datos en el extranjero', P('Algunos proveedores (alojamiento, envío de correos) están establecidos fuera de Suiza, en particular en Estados Unidos. Cuando el país no ofrece un nivel de protección reconocido como adecuado, nos basamos en garantías apropiadas, como las cláusulas contractuales tipo.')],
      ['Cookies y almacenamiento en su navegador', P('Este sitio no utiliza cookies publicitarias ni herramientas de seguimiento o de medición de audiencia. Puede guardar en su navegador (almacenamiento local o de sesión) ajustes de visualización y el avance de nuestras listas de tareas. Esta información permanece en su dispositivo, no le identifica y no sirve para seguirle. Si añadimos una herramienta de medición de audiencia, esta página se actualizará.')],
      ['Plazo de conservación', P('Conservamos sus datos el tiempo necesario para tramitar su solicitud y cumplir nuestras obligaciones legales; después los eliminamos o los anonimizamos. Los registros técnicos del proveedor de alojamiento se conservan durante un tiempo limitado.')],
      ['Seguridad', P('El sitio se sirve mediante una conexión cifrada (HTTPS). Adoptamos medidas técnicas y organizativas razonables para proteger sus datos frente al acceso no autorizado, la pérdida o la alteración.')],
      ['Sus derechos', P(`Puede solicitar el acceso a sus datos, su rectificación o supresión, la limitación o la oposición a su tratamiento, así como su entrega en un formato de uso común. Si ha dado su consentimiento, puede retirarlo en cualquier momento. Escríbanos a ${MAIL}; para tramitar su solicitud podemos pedirle un documento de identidad.`) +
        P('También puede dirigirse al Comisionado Federal de Protección de Datos y de Transparencia (PFPDT): <a href="https://www.edoeb.admin.ch" rel="noopener" target="_blank">www.edoeb.admin.ch</a>.')],
      ['Modificaciones', P('Podemos adaptar esta política, por ejemplo si añadimos un servicio al sitio. Prevalece la versión en línea.')],
    ],
  },
  pt: {
    title: 'Política de privacidade | Pompas fúnebres Murith',
    desc: 'Como a A. Murith SA, pompas fúnebres em Genebra, trata os seus dados pessoais: formulários, alojamento, cookies e os seus direitos segundo a LPD suíça.',
    home: 'Início', crumbAria: 'Caminho de navegação', h1: 'Política de privacidade',
    lead: 'Que dados tratamos, porquê, e como mantém o controlo das suas informações.',
    updated: 'Última atualização: 25 de novembro de 2026.',
    sec: [
      ['Quem é responsável pelos seus dados?', P(`O responsável pelo tratamento é a A. Murith SA, pompas fúnebres, 89, boulevard de la Cluse, 1205 Genebra, Suíça (telefone ${TEL}, e-mail ${MAIL}). Esta política aplica-se a este site e segue a lei federal suíça de proteção de dados (LPD).`)],
      ['Que dados tratamos?', UL([
        'Quando visita o site: endereço IP, data e hora, páginas consultadas, tipo de navegador e de dispositivo. O nosso fornecedor de alojamento regista estes dados técnicos para garantir o funcionamento e a segurança do site.',
        'Quando nos escreve (formulários de contacto e de orçamento, e-mail, telefone): nome, apelido, endereço de e-mail, número de telefone e conteúdo da sua mensagem.']) +
        P('Convidamo-lo a indicar nos formulários apenas o essencial. As informações mais sensíveis (situação do falecido, vontades, convicções religiosas) são tratadas de viva voz ou numa entrevista.')],
      ['Para que usamos estes dados?', UL([
        'responder aos seus pedidos e voltar a contactá-lo;',
        'elaborar um orçamento e preparar o acompanhamento da sua família;',
        'garantir a segurança e o bom funcionamento do site;',
        'cumprir as nossas obrigações legais.']) +
        P('Ao enviar um formulário, aceita que utilizemos os seus dados para tratar o seu pedido. Não os vendemos nem os utilizamos para fins publicitários.')],
      ['Quem recebe os seus dados?', P('Só têm acesso os membros da nossa equipa que deles precisam. Recorremos também a prestadores técnicos, obrigados a proteger os seus dados:') +
        UL(['Vercel Inc.: alojamento do site (Estados Unidos);',
          'Resend: envio das mensagens dos nossos formulários para a nossa caixa de correio (Estados Unidos);',
          'conteúdos incorporados: algumas páginas mostram um mapa OpenStreetMap, um catálogo em linha (FlipBuilder) ou um vídeo (YouTube, modo sem cookies). Quando estes conteúdos são carregados, o seu endereço IP é transmitido a esses serviços, que aplicam as suas próprias regras.']) +
        P('As ligações para o Google Maps, LinkedIn, Instagram ou outros sites levam-no para fora do nosso site: aplica-se então a política de privacidade desses sites.')],
      ['Os seus dados no estrangeiro', P('Alguns prestadores (alojamento, envio de e-mails) estão estabelecidos fora da Suíça, nomeadamente nos Estados Unidos. Quando o país não oferece um nível de proteção reconhecido como adequado, recorremos a garantias apropriadas, como as cláusulas contratuais-tipo.')],
      ['Cookies e armazenamento no navegador', P('Este site não utiliza cookies publicitários nem ferramentas de seguimento ou de medição de audiência. Pode guardar no seu navegador (armazenamento local ou de sessão) definições de visualização e o progresso das nossas listas de verificação. Estas informações ficam no seu dispositivo, não o identificam e não servem para o seguir. Se acrescentarmos uma ferramenta de medição de audiência, esta página será atualizada.')],
      ['Prazo de conservação', P('Conservamos os seus dados durante o tempo necessário para tratar o seu pedido e cumprir as nossas obrigações legais; depois eliminamo-los ou tornamo-los anónimos. Os registos técnicos do fornecedor de alojamento são conservados por um período limitado.')],
      ['Segurança', P('O site é servido através de uma ligação cifrada (HTTPS). Tomamos medidas técnicas e organizativas razoáveis para proteger os seus dados contra o acesso não autorizado, a perda ou a alteração.')],
      ['Os seus direitos', P(`Pode pedir o acesso aos seus dados, a sua retificação ou eliminação, a limitação ou a oposição ao seu tratamento, bem como a sua entrega num formato de uso corrente. Se deu o seu consentimento, pode retirá-lo a qualquer momento. Escreva-nos para ${MAIL}; para tratar o seu pedido, podemos pedir-lhe um documento de identificação.`) +
        P('Pode também dirigir-se ao Encarregado Federal da Proteção de Dados e da Transparência (PFPDT): <a href="https://www.edoeb.admin.ch" rel="noopener" target="_blank">www.edoeb.admin.ch</a>.')],
      ['Alterações', P('Podemos adaptar esta política, por exemplo se acrescentarmos um serviço ao site. Prevalece a versão em linha.')],
    ],
  },
};

const privPath = l => (l === 'fr' ? '' : `/${l}`) + '/politique-de-confidentialite';
const setMeta = (h, key, val, content) => h.replace(new RegExp(`<meta[^>]*(?:name|property)="${key}"[^>]*>`), m => m.replace(/content="[^"]*"/, `content="${esc(content)}"`));

function buildPrivacy(l) {
  const D = PRIV[l];
  const shellFile = l === 'fr' ? '404.html' : `${l}/404.html`;
  let h = rd(shellFile);
  const url = BASE + privPath(l);
  h = h.replace(/<title>[\s\S]*?<\/title>/, `<title>${esc(D.title)}</title>`);
  h = setMeta(h, 'description', 'x', D.desc);
  h = setMeta(h, 'og:title', 'x', D.title); h = setMeta(h, 'og:description', 'x', D.desc); h = setMeta(h, 'og:url', 'x', url);
  h = setMeta(h, 'twitter:title', 'x', D.title); h = setMeta(h, 'twitter:description', 'x', D.desc);
  const alts = LANGS.map(x => `<link rel="alternate" hreflang="${x}" href="${BASE + privPath(x)}"/>`).join('') + `<link rel="alternate" hreflang="x-default" href="${BASE + privPath('fr')}"/>`;
  const homeHref = l === 'fr' ? '/' : `/${l}`;
  const ld = `<script type="application/ld+json">${JSON.stringify({ '@context': 'https://schema.org', '@type': 'WebPage', '@id': url + '#page', url, name: D.title, description: D.desc, inLanguage: h.match(/<html[^>]*lang="([^"]*)"/)[1], isPartOf: { '@id': BASE + '/#site' }, about: { '@id': BASE + '/#entreprise' } })}</script>\n` +
    `<script type="application/ld+json">${JSON.stringify({ '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [{ '@type': 'ListItem', position: 1, name: D.home, item: BASE + (l === 'fr' ? '/' : homeHref) }, { '@type': 'ListItem', position: 2, name: D.h1, item: url }] })}</script>\n`;
  h = h.replace(/<meta name="robots"[^>]*\/>/, '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>')
       .replace(/<link rel="canonical"[^>]*\/>/, `<link rel="canonical" href="${url}"/>${alts}`)
       .replace('<meta content="#F6F8FB" name="theme-color"/>', ld + '<meta content="#F6F8FB" name="theme-color"/>');
  h = h.replace(/(<meta content="[^"]*" property="og:type"\/>)/, '<meta content="website" property="og:type"/>');
  // sélecteur de langue : chaque langue pointe vers sa version de cette page
  h = h.replace(/(data-l="(\w\w)"\s+href=")[^"]*(")/g, (m, a, x, c) => a + privPath(x) + c);
  const body = D.sec.map(([t, html]) => `<h2>${t}</h2>${html}`).join('') + `<p><em>${D.updated}</em></p>`;
  const main = `<main id="main">
<section class="phead noimg"><div class="container"><div class="phead-text reveal"><nav aria-label="${D.crumbAria}" class="crumb"><a href="${homeHref}">${D.home}</a><span aria-hidden="true">/</span><span>${D.h1}</span></nav><h1>${D.h1}</h1><p class="lead">${D.lead}</p></div></div></section>
<section class="section tight"><div class="container"><article class="post-body">${body}</article></div></section>
</main>`;
  h = h.replace(/<main[\s\S]*<\/main>/, () => main);
  return h;
}

/* ─────────────────────────────────────────────────────────────
   2. Article /blog/cout-obseques-geneve (6 langues)
   ───────────────────────────────────────────────────────────── */
const ART = {
  slug: 'cout-obseques-geneve',
  published: '2024-04-29T00:00:00+02:00', modified: DATE + 'T09:00:00+01:00',
  img: { base: 'cercueil-bougie', w: 1600, h: 1066 },
};
const artPath = l => (l === 'fr' ? '' : `/${l}`) + `/blog/${ART.slug}`;
const A = (l, slug, txt) => `<a href="${l === 'fr' ? '' : '/' + l}/${slug}">${txt}</a>`;
const TELA = '<a href="tel:+41228095600">+41 22 809 56 00</a>';

const ARTL = {
  fr: {
    title: "Coût d'un enterrement à Genève : estimation | Murith",
    h1: "Comprendre le coût d'un enterrement à Genève : conseils et estimation des frais",
    short: "Comprendre le coût d'un enterrement à Genève",
    desc: "Découvrez le coût d'un enterrement à Genève : tarifs, prestations funéraires, frais à prévoir et conseils pour organiser des obsèques adaptées à votre budget.",
    tag: "Coût d'un enterrement", dateLabel: '25 novembre', read: '6 min de lecture', imgAlt: 'Poignée de cercueil et bougie allumée',
    card: "Quel est le coût d'un enterrement ? En règle générale, en Suisse, il faut s'attendre à des coûts allant de 3 000 à 10 000 CHF. Panorama des frais essentiels, des choix optionnels et de nos conseils pour un budget maîtrisé.",
    body: l => `<p><strong>Table des matières :</strong></p><ol><li>Démarches administratives et leurs coûts</li><li>Choix entre inhumation et crémation</li><li>Analyse des coûts d'un enterrement à Genève</li><li>Repères de prix indicatifs</li><li>Arrangements floraux pour des funérailles à Genève</li><li>Chambres funéraires</li><li>En résumé, le coût des funérailles à Genève</li></ol>
<p>Quel est le coût d'un enterrement ? Cette question préoccupe souvent les familles dans les moments les plus difficiles. En règle générale, en Suisse, il faut s'attendre à des coûts allant de 3 000 à 10 000 CHF. Cet article présente un panorama des frais essentiels, des choix optionnels qui peuvent influencer votre budget, et des recommandations pour trouver un équilibre entre le respect des dernières volontés et un budget maîtrisé.</p>
<h2>1. Démarches administratives et leurs coûts</h2>
<p>À Genève, plusieurs démarches administratives suivent un décès : l'établissement du certificat médical de décès, la déclaration du décès à l'état civil et l'obtention de l'acte de décès. Elles sont encadrées par la réglementation cantonale. Pour le détail, consultez notre page sur ${A(l, 'formalites', 'les formalités de décès')}.</p>
<p>Lorsque vous confiez les obsèques aux pompes funèbres Murith, toutes les formalités de décès sont prises en charge, pour vous alléger dans ce moment difficile.</p>
<h2>2. Choix entre inhumation et crémation</h2>
<p>Le choix entre l'inhumation et la crémation est un autre facteur clé du coût d'un enterrement, avec des conséquences notables sur le budget des funérailles. Comprendre les coûts associés à chaque option aide à choisir en connaissance de cause et facilite la prise de décision.</p>
<p><strong>Le prix d'une inhumation.</strong> Pour une inhumation, plusieurs coûts sont à considérer. Le premier est le cercueil, puis l'achat d'une concession et d'une parcelle dans un cimetière de Genève pour 20 ans, avec la possibilité de renouveler cette concession. Ces coûts varient selon la durée de la concession et l'emplacement du cimetière.</p>
<p><strong>Le coût d'une crémation.</strong> Pour une crémation, le coût varie aussi selon plusieurs facteurs. Le choix du cercueil et de l'urne sont les principaux éléments qui l'influencent. Il est également important de savoir que les crématoriums en Suisse n'acceptent pas les cercueils en carton.</p>
<h2>3. Analyse des coûts d'un enterrement à Genève</h2>
<p>À Genève, les frais d'un enterrement varient selon plusieurs éléments et peuvent différer d'un service funéraire à l'autre. On y trouve notamment :</p>
<ul><li>les fournitures funéraires (cercueils) ;</li><li>les prestations de services tiers (crématorium, cimetière, avis de décès, etc.) ;</li><li>les taxes liées à l'enterrement ;</li><li>les arrangements floraux ;</li><li>un rassemblement après le service funéraire (cérémonie, réception, etc.).</li></ul>
<p>Pour une estimation précise, le plus simple est de s'adresser directement à une entreprise de services funéraires du canton de Genève : elle connaît en détail les frais et peut vous aider à les comprendre. ${A(l, 'devis', 'Recevoir mon devis')}.</p>
<p>La planification des funérailles implique de nombreuses décisions et des coûts variés. Il est donc essentiel de savoir quels sont les frais incontournables.</p>
<h3>Frais incontournables</h3>
<p>La première dépense incontournable est le cercueil. En Suisse, un cercueil en sapin coûte environ 1 000 CHF. Aux pompes funèbres Murith, le cercueil en sapin est à 940 CHF, mais le prix d'un cercueil varie selon le type de bois et la qualité : de 1 000 CHF à 10 000 CHF pour les modèles les plus élaborés. Découvrez ${A(l, 'cercueils', 'nos modèles de cercueils')}.</p>
<h3>Services funéraires optionnels</h3>
<p>En plus des frais incontournables, des services optionnels peuvent augmenter le coût total : les services d'un thanatopracteur, la location d'un funérarium pour le dernier adieu, la publication des avis de décès. Ces services varient d'une entreprise à l'autre.</p>
<p>Les pompes funèbres Murith ont plus de 135 ans d'expérience dans le domaine funéraire et un savoir-faire transmis depuis cinq générations, de père en fils.</p>
<p>Les services optionnels lors d'un enterrement peuvent aussi inclure :</p>
<ul><li>un officiant, pour personnaliser l'adieu et rendre hommage à la personne défunte ;</li><li>des musiciens pour jouer de la musique en direct ;</li><li>des fleurs supplémentaires pour décorer le lieu de la cérémonie ;</li><li>des services de photographie ou de vidéo pour garder le souvenir des moments importants.</li></ul>
<p>Ces services complémentaires ajoutent une touche personnelle à la cérémonie, mais ils augmentent aussi le coût total. Pour aller plus loin, voyez comment ${A(l, 'obseques', 'nous organisons les obsèques')}.</p>
<h2>4. Repères de prix indicatifs</h2>
<div class="tbl"><table><thead><tr><th scope="col">Poste</th><th scope="col">Repère</th></tr></thead><tbody>
<tr><td>Enterrement, ensemble des frais en Suisse</td><td>de 3 000 à 10 000 CHF</td></tr>
<tr><td>Cercueil en sapin</td><td>environ 1 000 CHF en Suisse ; 940 CHF chez Murith</td></tr>
<tr><td>Cercueil plus élaboré</td><td>jusqu'à 10 000 CHF</td></tr>
<tr><td>Concession dans un cimetière genevois</td><td>20 ans, renouvelable ; tarif selon la durée et le cimetière</td></tr>
<tr><td>Arrangements floraux</td><td>de 100 à 900 CHF</td></tr>
<tr><td>Crématorium, cimetière, avis de décès, taxes</td><td>variables : sur devis</td></tr>
</tbody></table></div>
<p>Ces montants sont indicatifs. Pour votre situation, ${A(l, 'devis', 'demandez un devis sans engagement')}.</p>
<h2>5. Arrangements floraux pour des funérailles à Genève</h2>
<p>Les arrangements floraux sont une autre dépense à prévoir. À Genève, leur prix varie généralement entre 100 CHF et 900 CHF.</p>
<p>Ils font partie intégrante de la cérémonie funéraire et se personnalisent selon vos souhaits. Qu'il s'agisse d'une simple couronne ou d'une composition plus élaborée, il faut les intégrer au budget des funérailles. ${A(l, 'fleurs', 'Découvrez nos arrangements floraux à Genève')}.</p>
<h2>6. Chambres funéraires</h2>
<p>Une chambre funéraire est un lieu où le corps du défunt est gardé avant les funérailles et la mise en terre. Aux pompes funèbres Murith, nos chambres funéraires sont ouvertes aux familles et à leurs proches, 24 h sur 24 et 7 jours sur 7. ${A(l, 'salons', 'Découvrir nos salons et la chapelle de la Cluse')}.</p>
<p>Si le décès survient dans une maison de retraite, une clinique ou à l'hôpital, le transfert du défunt est effectué dans les heures qui suivent par notre service jusqu'à nos locaux.</p>
<h2>7. En résumé, le coût des funérailles à Genève</h2>
<p>Comprendre les coûts d'un enterrement aide à planifier et à gérer les dépenses. Qu'il s'agisse de choisir entre inhumation et crémation, de comprendre les frais incontournables ou les services optionnels, être bien informé permet de faire des choix éclairés. Pour anticiper ces frais, vous pouvez aussi découvrir ${A(l, 'prevoyance-funeraire', 'la prévoyance funéraire')}.</p>
<p>Les pompes funèbres Murith assurent une permanence 24 h sur 24, 7 jours sur 7, pour répondre à toutes vos questions : ${TELA}. L'objectif reste de rendre hommage à un être cher de manière respectueuse et digne, dans le respect de vos contraintes budgétaires.</p>`,
  },

  en: {
    title: 'Cost of a Funeral in Geneva: Estimate | Murith',
    h1: 'Understanding the cost of a funeral in Geneva: advice and cost estimate',
    short: 'Understanding the cost of a funeral in Geneva',
    desc: 'Find out what a funeral costs in Geneva: prices, funeral services, expenses to plan for and advice on organising a funeral that fits your budget.',
    tag: 'Cost of a funeral', dateLabel: '25 November', read: '6 min read', imgAlt: 'Coffin handle and lit candle',
    card: 'How much does a funeral cost? In Switzerland, expect costs of roughly 3,000 to 10,000 CHF. An overview of the essential expenses, optional choices and our advice for keeping a budget under control.',
    body: l => `<p><strong>Table of contents:</strong></p><ol><li>Administrative procedures and their costs</li><li>Burial or cremation</li><li>Breaking down the cost of a funeral in Geneva</li><li>Indicative price guide</li><li>Floral arrangements for a funeral in Geneva</li><li>Funeral rooms</li><li>In summary: the cost of a funeral in Geneva</li></ol>
<p>How much does a funeral cost? This question often weighs on families at the most difficult times. As a general rule, in Switzerland, you should expect costs of 3,000 to 10,000 CHF. This article gives an overview of the essential expenses, the optional choices that can affect your budget, and recommendations for balancing respect for final wishes with a controlled budget.</p>
<h2>1. Administrative procedures and their costs</h2>
<p>In Geneva, several administrative steps follow a death: issuing the medical death certificate, declaring the death to the civil registry and obtaining the death certificate. They are governed by cantonal regulations. For details, see our page on ${A(l, 'formalites', 'death formalities')}.</p>
<p>When you entrust the funeral to Murith funeral services, all death formalities are taken care of, to ease your burden at a difficult time.</p>
<h2>2. Burial or cremation</h2>
<p>The choice between burial and cremation is another key factor in the cost of a funeral, with a significant impact on the funeral budget. Understanding the costs of each option helps you choose with full knowledge and makes the decision easier.</p>
<p><strong>The price of a burial.</strong> For a burial, several costs have to be considered. The first is the coffin, then the purchase of a concession and a plot in a Geneva cemetery for 20 years, with the possibility of renewing it. These costs vary with the length of the concession and the location of the cemetery.</p>
<p><strong>The cost of a cremation.</strong> For a cremation, the cost also depends on several factors. The choice of coffin and urn are the main ones. It is also worth knowing that crematoria in Switzerland do not accept cardboard coffins.</p>
<h2>3. Breaking down the cost of a funeral in Geneva</h2>
<p>In Geneva, the cost of a funeral depends on several elements and can differ from one funeral service to another. These include:</p>
<ul><li>funeral supplies (coffins);</li><li>third-party services (crematorium, cemetery, death notices, etc.);</li><li>taxes related to the funeral;</li><li>floral arrangements;</li><li>a gathering after the funeral service (ceremony, reception, etc.).</li></ul>
<p>For an accurate estimate, the simplest way is to contact a funeral service in the canton of Geneva directly: it knows the costs in detail and can help you understand them. ${A(l, 'devis', 'Get my quote')}.</p>
<p>Planning a funeral involves many decisions and varied costs. It is therefore essential to know which expenses cannot be avoided.</p>
<h3>Unavoidable costs</h3>
<p>The first unavoidable expense is the coffin. In Switzerland, a fir coffin costs about 1,000 CHF. At Murith funeral services, the fir coffin is 940 CHF, but the price of a coffin varies with the type of wood and the quality: from 1,000 CHF to 10,000 CHF for the most elaborate models. Discover ${A(l, 'cercueils', 'our coffin models')}.</p>
<h3>Optional funeral services</h3>
<p>On top of the unavoidable costs, optional services can increase the total: the services of a thanatopractor, the rental of a funeral home for the last farewell, the publication of death notices. These services vary from one company to another.</p>
<p>Murith funeral services have more than 135 years of experience in the funeral field and know-how passed down through five generations, from father to son.</p>
<p>Optional services during a funeral can also include:</p>
<ul><li>an officiant, to personalise the farewell and pay tribute to the deceased;</li><li>musicians to play live music;</li><li>additional flowers to decorate the ceremony venue;</li><li>photography or video services to keep a record of important moments.</li></ul>
<p>These additional services add a personal touch to the ceremony, but they also increase the total cost. To find out more, see how ${A(l, 'obseques', 'we organise funerals')}.</p>
<h2>4. Indicative price guide</h2>
<div class="tbl"><table><thead><tr><th scope="col">Item</th><th scope="col">Guide figure</th></tr></thead><tbody>
<tr><td>Funeral, total costs in Switzerland</td><td>3,000 to 10,000 CHF</td></tr>
<tr><td>Fir coffin</td><td>about 1,000 CHF in Switzerland; 940 CHF at Murith</td></tr>
<tr><td>More elaborate coffin</td><td>up to 10,000 CHF</td></tr>
<tr><td>Concession in a Geneva cemetery</td><td>20 years, renewable; price depends on the length and the cemetery</td></tr>
<tr><td>Floral arrangements</td><td>100 to 900 CHF</td></tr>
<tr><td>Crematorium, cemetery, death notices, taxes</td><td>variable: on quote</td></tr>
</tbody></table></div>
<p>These amounts are indicative. For your situation, ${A(l, 'devis', 'request a no-obligation quote')}.</p>
<h2>5. Floral arrangements for a funeral in Geneva</h2>
<p>Floral arrangements are another expense to plan for. In Geneva, their price generally ranges between 100 CHF and 900 CHF.</p>
<p>They are an integral part of the funeral ceremony and can be personalised to your wishes. Whether it is a simple wreath or a more elaborate composition, they should be included in the funeral budget. ${A(l, 'fleurs', 'Discover our floral arrangements in Geneva')}.</p>
<h2>6. Funeral rooms</h2>
<p>A funeral room is a place where the body of the deceased is kept before the funeral and burial. At Murith funeral services, our funeral rooms are open to families and their loved ones, 24 hours a day, 7 days a week. ${A(l, 'salons', 'Discover our rooms and the Chapelle de la Cluse')}.</p>
<p>If the death occurs in a retirement home, a clinic or a hospital, the deceased is transferred to our premises by our service within hours.</p>
<h2>7. In summary: the cost of a funeral in Geneva</h2>
<p>Understanding the costs of a funeral helps you plan and manage expenses. Whether choosing between burial and cremation, or understanding the unavoidable costs and optional services, being well informed lets you make sound choices. To plan these costs ahead, you can also discover ${A(l, 'prevoyance-funeraire', 'funeral pre-planning')}.</p>
<p>Murith funeral services are available 24 hours a day, 7 days a week, to answer all your questions: ${TELA}. The goal remains to pay tribute to a loved one in a respectful and dignified way, within your budget.</p>`,
  },

  de: {
    title: 'Kosten einer Bestattung in Genf: Schätzung | Murith',
    h1: 'Die Kosten einer Bestattung in Genf verstehen: Ratschläge und Kostenschätzung',
    short: 'Die Kosten einer Bestattung in Genf verstehen',
    desc: 'Was kostet eine Bestattung in Genf? Preise, Bestattungsleistungen, einzuplanende Kosten und Tipps für eine Trauerfeier, die zu Ihrem Budget passt.',
    tag: 'Kosten einer Bestattung', dateLabel: '25. November', read: '6 Min. Lesezeit', imgAlt: 'Sarggriff und brennende Kerze',
    card: "Was kostet eine Bestattung? In der Schweiz muss man in der Regel mit 3'000 bis 10'000 CHF rechnen. Ein Überblick über die wesentlichen Kosten, optionale Leistungen und unsere Tipps für ein überschaubares Budget.",
    body: l => `<p><strong>Inhaltsverzeichnis:</strong></p><ol><li>Behördengänge und ihre Kosten</li><li>Erdbestattung oder Kremation</li><li>Die Kosten einer Bestattung in Genf im Überblick</li><li>Preisrichtwerte</li><li>Blumenschmuck für eine Trauerfeier in Genf</li><li>Abdankungs- und Aufbahrungsräume</li><li>Zusammenfassung: die Kosten einer Bestattung in Genf</li></ol>
<p>Was kostet eine Bestattung? Diese Frage beschäftigt Familien oft in den schwersten Momenten. In der Schweiz muss man in der Regel mit Kosten von 3'000 bis 10'000 CHF rechnen. Dieser Artikel gibt einen Überblick über die wesentlichen Kosten, die optionalen Entscheidungen, die Ihr Budget beeinflussen können, und Empfehlungen, um den letzten Willen zu achten und das Budget im Griff zu behalten.</p>
<h2>1. Behördengänge und ihre Kosten</h2>
<p>In Genf folgen auf einen Todesfall mehrere administrative Schritte: die Ausstellung des ärztlichen Todesscheins, die Meldung des Todesfalls beim Zivilstandsamt und die Beschaffung der Sterbeurkunde. Sie unterliegen den kantonalen Vorschriften. Einzelheiten finden Sie auf unserer Seite zu den ${A(l, 'formalites', 'Formalitäten bei einem Todesfall')}.</p>
<p>Wenn Sie die Bestattung dem Bestattungsinstitut Murith anvertrauen, übernehmen wir alle Formalitäten, um Sie in dieser schwierigen Zeit zu entlasten.</p>
<h2>2. Erdbestattung oder Kremation</h2>
<p>Die Wahl zwischen Erdbestattung und Kremation ist ein weiterer wichtiger Kostenfaktor und wirkt sich spürbar auf das Budget aus. Wer die Kosten jeder Möglichkeit kennt, kann bewusst entscheiden, und die Entscheidung fällt leichter.</p>
<p><strong>Der Preis einer Erdbestattung.</strong> Bei einer Erdbestattung fallen mehrere Kosten an. Zuerst der Sarg, dann der Erwerb einer Konzession und einer Grabstätte auf einem Genfer Friedhof für 20 Jahre, mit der Möglichkeit der Verlängerung. Diese Kosten hängen von der Dauer der Konzession und vom Standort des Friedhofs ab.</p>
<p><strong>Die Kosten einer Kremation.</strong> Auch bei einer Kremation hängen die Kosten von mehreren Faktoren ab. Die Wahl von Sarg und Urne beeinflusst sie am stärksten. Wichtig zu wissen: Die Krematorien in der Schweiz akzeptieren keine Kartonsärge.</p>
<h2>3. Die Kosten einer Bestattung in Genf im Überblick</h2>
<p>In Genf hängen die Kosten einer Bestattung von mehreren Elementen ab und können sich von einem Bestattungsinstitut zum anderen unterscheiden. Dazu gehören insbesondere:</p>
<ul><li>Bestattungsbedarf (Särge);</li><li>Leistungen Dritter (Krematorium, Friedhof, Todesanzeigen usw.);</li><li>Gebühren und Abgaben im Zusammenhang mit der Bestattung;</li><li>Blumenschmuck;</li><li>ein Zusammenkommen nach der Trauerfeier (Zeremonie, Empfang usw.).</li></ul>
<p>Für eine genaue Schätzung wenden Sie sich am besten direkt an ein Bestattungsinstitut im Kanton Genf: Es kennt die Kosten im Detail und kann Ihnen helfen, sie zu verstehen. ${A(l, 'devis', 'Offerte anfordern')}.</p>
<p>Die Planung einer Trauerfeier erfordert viele Entscheidungen und verursacht unterschiedliche Kosten. Daher ist es wichtig zu wissen, welche Ausgaben sich nicht vermeiden lassen.</p>
<h3>Unvermeidbare Kosten</h3>
<p>Die erste unvermeidbare Ausgabe ist der Sarg. In der Schweiz kostet ein Tannensarg etwa 1'000 CHF. Beim Bestattungsinstitut Murith kostet der Tannensarg 940 CHF; der Preis eines Sargs hängt jedoch von der Holzart und der Qualität ab: von 1'000 CHF bis 10'000 CHF für die aufwendigsten Modelle. Entdecken Sie ${A(l, 'cercueils', 'unsere Sargmodelle')}.</p>
<h3>Optionale Bestattungsleistungen</h3>
<p>Zusätzlich zu den unvermeidbaren Kosten können optionale Leistungen die Gesamtkosten erhöhen: die Dienste eines Thanatopraktikers, die Miete eines Abschiedsraums für den letzten Abschied, die Veröffentlichung von Todesanzeigen. Diese Leistungen unterscheiden sich von Unternehmen zu Unternehmen.</p>
<p>Das Bestattungsinstitut Murith verfügt über mehr als 135 Jahre Erfahrung im Bestattungswesen und ein Wissen, das seit fünf Generationen vom Vater an den Sohn weitergegeben wird.</p>
<p>Zu den optionalen Leistungen bei einer Bestattung können ausserdem gehören:</p>
<ul><li>eine Trauerredner- oder Zeremonienleitung, um den Abschied persönlich zu gestalten und der verstorbenen Person zu gedenken;</li><li>Musiker, die live spielen;</li><li>zusätzliche Blumen zur Dekoration des Zeremonieorts;</li><li>Foto- oder Videoaufnahmen, um wichtige Momente festzuhalten.</li></ul>
<p>Diese zusätzlichen Leistungen verleihen der Zeremonie eine persönliche Note, erhöhen aber auch die Gesamtkosten. Weitere Informationen dazu, wie ${A(l, 'obseques', 'wir Bestattungen organisieren')}.</p>
<h2>4. Preisrichtwerte</h2>
<div class="tbl"><table><thead><tr><th scope="col">Posten</th><th scope="col">Richtwert</th></tr></thead><tbody>
<tr><td>Bestattung, Gesamtkosten in der Schweiz</td><td>3'000 bis 10'000 CHF</td></tr>
<tr><td>Tannensarg</td><td>etwa 1'000 CHF in der Schweiz; 940 CHF bei Murith</td></tr>
<tr><td>Aufwendigerer Sarg</td><td>bis zu 10'000 CHF</td></tr>
<tr><td>Konzession auf einem Genfer Friedhof</td><td>20 Jahre, verlängerbar; Preis je nach Dauer und Friedhof</td></tr>
<tr><td>Blumenschmuck</td><td>100 bis 900 CHF</td></tr>
<tr><td>Krematorium, Friedhof, Todesanzeigen, Gebühren</td><td>variabel: auf Offerte</td></tr>
</tbody></table></div>
<p>Diese Beträge sind Richtwerte. Für Ihre Situation ${A(l, 'devis', 'fordern Sie eine unverbindliche Offerte an')}.</p>
<h2>5. Blumenschmuck für eine Trauerfeier in Genf</h2>
<p>Blumenschmuck ist eine weitere Ausgabe, die man einplanen sollte. In Genf liegt sein Preis in der Regel zwischen 100 CHF und 900 CHF.</p>
<p>Er gehört fest zur Trauerfeier und lässt sich nach Ihren Wünschen gestalten. Ob ein einfacher Kranz oder ein aufwendigeres Gesteck: Er sollte im Budget der Bestattung berücksichtigt werden. ${A(l, 'fleurs', 'Entdecken Sie unseren Blumenschmuck in Genf')}.</p>
<h2>6. Abdankungs- und Aufbahrungsräume</h2>
<p>Ein Aufbahrungsraum ist ein Ort, an dem der Leichnam vor der Trauerfeier und der Beisetzung aufbewahrt wird. Beim Bestattungsinstitut Murith stehen unsere Räume den Familien und ihren Angehörigen rund um die Uhr an 7 Tagen pro Woche offen. ${A(l, 'salons', 'Unsere Räume und die Chapelle de la Cluse entdecken')}.</p>
<p>Erfolgt der Todesfall in einem Altersheim, einer Klinik oder im Spital, wird die verstorbene Person innerhalb weniger Stunden von unserem Dienst in unsere Räumlichkeiten überführt.</p>
<h2>7. Zusammenfassung: die Kosten einer Bestattung in Genf</h2>
<p>Wer die Kosten einer Bestattung versteht, kann Ausgaben besser planen und steuern. Ob Wahl zwischen Erdbestattung und Kremation oder Verständnis der unvermeidbaren Kosten und optionalen Leistungen: Gut informiert lassen sich überlegte Entscheidungen treffen. Um diese Kosten im Voraus zu regeln, können Sie auch die ${A(l, 'prevoyance-funeraire', 'Bestattungsvorsorge')} entdecken.</p>
<p>Das Bestattungsinstitut Murith ist rund um die Uhr, an 7 Tagen pro Woche, für alle Ihre Fragen erreichbar: ${TELA}. Das Ziel bleibt, einem geliebten Menschen respektvoll und würdig die letzte Ehre zu erweisen und dabei Ihr Budget zu respektieren.</p>`,
  },

  it: {
    title: 'Costo di una sepoltura a Ginevra: stima | Murith',
    h1: 'Capire il costo di una sepoltura a Ginevra: consigli e stima delle spese',
    short: 'Capire il costo di una sepoltura a Ginevra',
    desc: 'Scoprite il costo di una sepoltura a Ginevra: tariffe, servizi funebri, spese da prevedere e consigli per organizzare esequie adatte al vostro budget.',
    tag: 'Costo di una sepoltura', dateLabel: '25 novembre', read: '6 min di lettura', imgAlt: 'Maniglia di una bara e candela accesa',
    card: "Quanto costa una sepoltura? In Svizzera, di regola, ci si deve aspettare costi da 3'000 a 10'000 CHF. Una panoramica delle spese essenziali, delle scelte facoltative e dei nostri consigli per un budget sotto controllo.",
    body: l => `<p><strong>Indice:</strong></p><ol><li>Pratiche amministrative e relativi costi</li><li>Inumazione o cremazione</li><li>Analisi dei costi di una sepoltura a Ginevra</li><li>Prezzi indicativi</li><li>Composizioni floreali per un funerale a Ginevra</li><li>Camere funerarie</li><li>In sintesi: il costo di un funerale a Ginevra</li></ol>
<p>Quanto costa una sepoltura? Questa domanda preoccupa spesso le famiglie nei momenti più difficili. Di regola, in Svizzera, ci si deve aspettare costi da 3'000 a 10'000 CHF. Questo articolo offre una panoramica delle spese essenziali, delle scelte facoltative che possono incidere sul budget e dei consigli per conciliare il rispetto delle ultime volontà con un budget sotto controllo.</p>
<h2>1. Pratiche amministrative e relativi costi</h2>
<p>A Ginevra, dopo un decesso occorre svolgere diverse pratiche amministrative: il rilascio del certificato medico di morte, la dichiarazione del decesso allo stato civile e l'ottenimento dell'atto di morte. Sono disciplinate dalla normativa cantonale. Per i dettagli, consultate la nostra pagina sulle ${A(l, 'formalites', 'pratiche in caso di decesso')}.</p>
<p>Quando affidate le esequie alle pompe funebri Murith, tutte le pratiche sono a nostro carico, per alleggerirvi in un momento difficile.</p>
<h2>2. Inumazione o cremazione</h2>
<p>La scelta tra inumazione e cremazione è un altro fattore chiave del costo di una sepoltura, con conseguenze rilevanti sul budget del funerale. Conoscere i costi di ciascuna opzione aiuta a scegliere con cognizione di causa e rende la decisione più semplice.</p>
<p><strong>Il prezzo di un'inumazione.</strong> Per un'inumazione vanno considerati diversi costi. Il primo è la bara, poi l'acquisto di una concessione e di un lotto in un cimitero di Ginevra per 20 anni, con la possibilità di rinnovare la concessione. Questi costi variano in base alla durata della concessione e alla posizione del cimitero.</p>
<p><strong>Il costo di una cremazione.</strong> Anche per una cremazione il costo varia in base a diversi fattori. La scelta della bara e dell'urna sono gli elementi principali. È inoltre importante sapere che i crematori in Svizzera non accettano bare di cartone.</p>
<h2>3. Analisi dei costi di una sepoltura a Ginevra</h2>
<p>A Ginevra, le spese di una sepoltura variano in base a diversi elementi e possono differire da un servizio funebre all'altro. Tra questi:</p>
<ul><li>le forniture funebri (bare);</li><li>i servizi di terzi (crematorio, cimitero, annunci funebri, ecc.);</li><li>le tasse legate alla sepoltura;</li><li>le composizioni floreali;</li><li>un momento di ritrovo dopo il servizio funebre (cerimonia, rinfresco, ecc.).</li></ul>
<p>Per una stima precisa, la cosa più semplice è rivolgersi direttamente a un'impresa di servizi funebri del Cantone di Ginevra: conosce nel dettaglio le spese e può aiutarvi a comprenderle. ${A(l, 'devis', 'Richiedere il mio preventivo')}.</p>
<p>L'organizzazione di un funerale comporta molte decisioni e costi diversi. È quindi essenziale sapere quali sono le spese ineludibili.</p>
<h3>Spese ineludibili</h3>
<p>La prima spesa ineludibile è la bara. In Svizzera, una bara in abete costa circa 1'000 CHF. Presso le pompe funebri Murith la bara in abete costa 940 CHF, ma il prezzo di una bara varia in base al tipo di legno e alla qualità: da 1'000 CHF a 10'000 CHF per i modelli più elaborati. Scoprite ${A(l, 'cercueils', 'i nostri modelli di bare')}.</p>
<h3>Servizi funebri facoltativi</h3>
<p>Oltre alle spese ineludibili, alcuni servizi facoltativi possono aumentare il costo totale: i servizi di un tanatoprassista, l'affitto di una camera funeraria per l'ultimo saluto, la pubblicazione degli annunci funebri. Questi servizi variano da un'impresa all'altra.</p>
<p>Le pompe funebri Murith vantano oltre 135 anni di esperienza nel settore funerario e un sapere tramandato da cinque generazioni, di padre in figlio.</p>
<p>I servizi facoltativi durante una sepoltura possono includere anche:</p>
<ul><li>un officiante, per personalizzare l'addio e rendere omaggio alla persona defunta;</li><li>musicisti per eseguire musica dal vivo;</li><li>fiori supplementari per decorare il luogo della cerimonia;</li><li>servizi fotografici o video per conservare il ricordo dei momenti importanti.</li></ul>
<p>Questi servizi complementari aggiungono un tocco personale alla cerimonia, ma aumentano anche il costo totale. Per saperne di più, scoprite come ${A(l, 'obseques', 'organizziamo le esequie')}.</p>
<h2>4. Prezzi indicativi</h2>
<div class="tbl"><table><thead><tr><th scope="col">Voce</th><th scope="col">Valore indicativo</th></tr></thead><tbody>
<tr><td>Sepoltura, insieme delle spese in Svizzera</td><td>da 3'000 a 10'000 CHF</td></tr>
<tr><td>Bara in abete</td><td>circa 1'000 CHF in Svizzera; 940 CHF da Murith</td></tr>
<tr><td>Bara più elaborata</td><td>fino a 10'000 CHF</td></tr>
<tr><td>Concessione in un cimitero ginevrino</td><td>20 anni, rinnovabile; tariffa in base alla durata e al cimitero</td></tr>
<tr><td>Composizioni floreali</td><td>da 100 a 900 CHF</td></tr>
<tr><td>Crematorio, cimitero, annunci funebri, tasse</td><td>variabili: su preventivo</td></tr>
</tbody></table></div>
<p>Questi importi sono indicativi. Per la vostra situazione, ${A(l, 'devis', 'richiedete un preventivo senza impegno')}.</p>
<h2>5. Composizioni floreali per un funerale a Ginevra</h2>
<p>Le composizioni floreali sono un'altra spesa da prevedere. A Ginevra il loro prezzo varia in genere tra 100 CHF e 900 CHF.</p>
<p>Fanno parte integrante della cerimonia funebre e si personalizzano secondo i vostri desideri. Che si tratti di una semplice corona o di una composizione più elaborata, vanno inserite nel budget del funerale. ${A(l, 'fleurs', 'Scoprite le nostre composizioni floreali a Ginevra')}.</p>
<h2>6. Camere funerarie</h2>
<p>Una camera funeraria è un luogo in cui la salma viene custodita prima del funerale e della sepoltura. Presso le pompe funebri Murith, le nostre camere funerarie sono aperte alle famiglie e ai loro cari 24 ore su 24 e 7 giorni su 7. ${A(l, 'salons', 'Scoprite i nostri saloni e la cappella della Cluse')}.</p>
<p>Se il decesso avviene in una casa di riposo, in una clinica o in ospedale, il trasferimento della salma presso i nostri locali viene effettuato dal nostro servizio nelle ore successive.</p>
<h2>7. In sintesi: il costo di un funerale a Ginevra</h2>
<p>Capire i costi di una sepoltura aiuta a pianificare e a gestire le spese. Che si tratti di scegliere tra inumazione e cremazione, di conoscere le spese ineludibili o i servizi facoltativi, essere ben informati permette di fare scelte consapevoli. Per anticipare queste spese, potete anche scoprire la ${A(l, 'prevoyance-funeraire', 'previdenza funeraria')}.</p>
<p>Le pompe funebri Murith garantiscono una reperibilità 24 ore su 24, 7 giorni su 7, per rispondere a tutte le vostre domande: ${TELA}. L'obiettivo resta rendere omaggio a una persona cara in modo rispettoso e dignitoso, nel rispetto del vostro budget.</p>`,
  },

  es: {
    title: 'Coste de un entierro en Ginebra: estimación | Murith',
    h1: 'Entender el coste de un entierro en Ginebra: consejos y estimación de gastos',
    short: 'Entender el coste de un entierro en Ginebra',
    desc: 'Descubra el coste de un entierro en Ginebra: tarifas, servicios funerarios, gastos a prever y consejos para organizar un funeral acorde con su presupuesto.',
    tag: 'Coste de un entierro', dateLabel: '25 de noviembre', read: '6 min de lectura', imgAlt: 'Asa de ataúd y vela encendida',
    card: '¿Cuánto cuesta un entierro? En Suiza, por lo general, hay que contar con costes de 3000 a 10 000 CHF. Un panorama de los gastos esenciales, de las opciones adicionales y de nuestros consejos para mantener el presupuesto bajo control.',
    body: l => `<p><strong>Índice:</strong></p><ol><li>Trámites administrativos y sus costes</li><li>Inhumación o cremación</li><li>Análisis de los costes de un entierro en Ginebra</li><li>Precios orientativos</li><li>Arreglos florales para un funeral en Ginebra</li><li>Salas funerarias</li><li>En resumen: el coste de un funeral en Ginebra</li></ol>
<p>¿Cuánto cuesta un entierro? Esta pregunta suele preocupar a las familias en los momentos más difíciles. Por lo general, en Suiza, hay que contar con costes de 3000 a 10 000 CHF. Este artículo ofrece un panorama de los gastos esenciales, de las opciones adicionales que pueden influir en su presupuesto y de recomendaciones para conciliar el respeto de las últimas voluntades con un presupuesto controlado.</p>
<h2>1. Trámites administrativos y sus costes</h2>
<p>En Ginebra, tras un fallecimiento hay que realizar varios trámites administrativos: la expedición del certificado médico de defunción, la declaración del fallecimiento en el registro civil y la obtención del acta de defunción. Están regulados por la normativa cantonal. Para más detalles, consulte nuestra página sobre los ${A(l, 'formalites', 'trámites tras un fallecimiento')}.</p>
<p>Cuando confía el funeral a los servicios funerarios Murith, nos encargamos de todos los trámites para aliviarle en un momento difícil.</p>
<h2>2. Inhumación o cremación</h2>
<p>La elección entre inhumación y cremación es otro factor clave del coste de un entierro, con consecuencias notables en el presupuesto del funeral. Conocer los costes de cada opción ayuda a elegir con conocimiento de causa y facilita la decisión.</p>
<p><strong>El precio de una inhumación.</strong> En una inhumación hay que tener en cuenta varios costes. El primero es el ataúd, y después la compra de una concesión y de una parcela en un cementerio de Ginebra por 20 años, con la posibilidad de renovar la concesión. Estos costes varían según la duración de la concesión y la ubicación del cementerio.</p>
<p><strong>El coste de una cremación.</strong> En una cremación, el coste también depende de varios factores. La elección del ataúd y de la urna son los principales. También es importante saber que los crematorios de Suiza no aceptan ataúdes de cartón.</p>
<h2>3. Análisis de los costes de un entierro en Ginebra</h2>
<p>En Ginebra, los gastos de un entierro varían según varios elementos y pueden diferir de un servicio funerario a otro. Entre ellos:</p>
<ul><li>los suministros funerarios (ataúdes);</li><li>los servicios de terceros (crematorio, cementerio, esquelas, etc.);</li><li>las tasas relacionadas con el entierro;</li><li>los arreglos florales;</li><li>una reunión tras el servicio funerario (ceremonia, recepción, etc.).</li></ul>
<p>Para obtener una estimación precisa, lo más sencillo es dirigirse directamente a una empresa de servicios funerarios del cantón de Ginebra: conoce los gastos al detalle y puede ayudarle a entenderlos. ${A(l, 'devis', 'Recibir mi presupuesto')}.</p>
<p>La planificación de un funeral implica muchas decisiones y costes diversos. Por eso es esencial saber cuáles son los gastos ineludibles.</p>
<h3>Gastos ineludibles</h3>
<p>El primer gasto ineludible es el ataúd. En Suiza, un ataúd de abeto cuesta alrededor de 1000 CHF. En los servicios funerarios Murith, el ataúd de abeto cuesta 940 CHF, pero el precio de un ataúd varía según el tipo de madera y la calidad: de 1000 CHF a 10 000 CHF para los modelos más elaborados. Descubra ${A(l, 'cercueils', 'nuestros modelos de ataúdes')}.</p>
<h3>Servicios funerarios opcionales</h3>
<p>Además de los gastos ineludibles, algunos servicios opcionales pueden aumentar el coste total: los servicios de un tanatopractor, el alquiler de una sala funeraria para la última despedida, la publicación de esquelas. Estos servicios varían de una empresa a otra.</p>
<p>Los servicios funerarios Murith cuentan con más de 135 años de experiencia en el ámbito funerario y un saber hacer transmitido durante cinco generaciones, de padre a hijo.</p>
<p>Los servicios opcionales durante un entierro también pueden incluir:</p>
<ul><li>un oficiante, para personalizar la despedida y rendir homenaje a la persona fallecida;</li><li>músicos que toquen en directo;</li><li>flores adicionales para decorar el lugar de la ceremonia;</li><li>servicios de fotografía o de vídeo para conservar el recuerdo de los momentos importantes.</li></ul>
<p>Estos servicios complementarios aportan un toque personal a la ceremonia, pero también aumentan el coste total. Para saber más, descubra cómo ${A(l, 'obseques', 'organizamos los funerales')}.</p>
<h2>4. Precios orientativos</h2>
<div class="tbl"><table><thead><tr><th scope="col">Concepto</th><th scope="col">Referencia</th></tr></thead><tbody>
<tr><td>Entierro, conjunto de gastos en Suiza</td><td>de 3000 a 10 000 CHF</td></tr>
<tr><td>Ataúd de abeto</td><td>alrededor de 1000 CHF en Suiza; 940 CHF en Murith</td></tr>
<tr><td>Ataúd más elaborado</td><td>hasta 10 000 CHF</td></tr>
<tr><td>Concesión en un cementerio ginebrino</td><td>20 años, renovable; tarifa según la duración y el cementerio</td></tr>
<tr><td>Arreglos florales</td><td>de 100 a 900 CHF</td></tr>
<tr><td>Crematorio, cementerio, esquelas, tasas</td><td>variables: bajo presupuesto</td></tr>
</tbody></table></div>
<p>Estos importes son orientativos. Para su situación, ${A(l, 'devis', 'solicite un presupuesto sin compromiso')}.</p>
<h2>5. Arreglos florales para un funeral en Ginebra</h2>
<p>Los arreglos florales son otro gasto a prever. En Ginebra, su precio suele situarse entre 100 CHF y 900 CHF.</p>
<p>Forman parte integrante de la ceremonia fúnebre y se personalizan según sus deseos. Ya se trate de una sencilla corona o de una composición más elaborada, conviene incluirlos en el presupuesto del funeral. ${A(l, 'fleurs', 'Descubra nuestros arreglos florales en Ginebra')}.</p>
<h2>6. Salas funerarias</h2>
<p>Una sala funeraria es un lugar donde se vela el cuerpo del difunto antes del funeral y del enterramiento. En los servicios funerarios Murith, nuestras salas están abiertas a las familias y a sus allegados las 24 horas del día, los 7 días de la semana. ${A(l, 'salons', 'Descubra nuestras salas y la capilla de la Cluse')}.</p>
<p>Si el fallecimiento se produce en una residencia, una clínica o un hospital, nuestro servicio realiza el traslado del difunto a nuestras instalaciones en las horas siguientes.</p>
<h2>7. En resumen: el coste de un funeral en Ginebra</h2>
<p>Entender los costes de un entierro ayuda a planificar y gestionar los gastos. Ya se trate de elegir entre inhumación y cremación, de conocer los gastos ineludibles o los servicios opcionales, estar bien informado permite tomar decisiones acertadas. Para anticipar estos gastos, también puede descubrir la ${A(l, 'prevoyance-funeraire', 'previsión funeraria')}.</p>
<p>Los servicios funerarios Murith atienden las 24 horas del día, los 7 días de la semana, para responder a todas sus preguntas: ${TELA}. El objetivo sigue siendo rendir homenaje a un ser querido de forma respetuosa y digna, respetando su presupuesto.</p>`,
  },

  pt: {
    title: 'Custo de um enterro em Genebra: estimativa | Murith',
    h1: 'Compreender o custo de um enterro em Genebra: conselhos e estimativa das despesas',
    short: 'Compreender o custo de um enterro em Genebra',
    desc: 'Descubra o custo de um enterro em Genebra: tarifas, serviços funerários, despesas a prever e conselhos para organizar um funeral adequado ao seu orçamento.',
    tag: 'Custo de um enterro', dateLabel: '25 de novembro', read: '6 min de leitura', imgAlt: 'Pega de caixão e vela acesa',
    card: 'Quanto custa um enterro? Na Suíça, em regra, deve contar-se com custos de 3 000 a 10 000 CHF. Um panorama das despesas essenciais, das escolhas opcionais e dos nossos conselhos para um orçamento controlado.',
    body: l => `<p><strong>Índice:</strong></p><ol><li>Diligências administrativas e respetivos custos</li><li>Inumação ou cremação</li><li>Análise dos custos de um enterro em Genebra</li><li>Preços indicativos</li><li>Arranjos florais para um funeral em Genebra</li><li>Câmaras funerárias</li><li>Em resumo: o custo de um funeral em Genebra</li></ol>
<p>Quanto custa um enterro? Esta pergunta preocupa frequentemente as famílias nos momentos mais difíceis. Em regra, na Suíça, deve contar-se com custos de 3 000 a 10 000 CHF. Este artigo apresenta um panorama das despesas essenciais, das escolhas opcionais que podem influenciar o seu orçamento e de recomendações para conciliar o respeito pelas últimas vontades com um orçamento controlado.</p>
<h2>1. Diligências administrativas e respetivos custos</h2>
<p>Em Genebra, após um falecimento é preciso tratar de várias diligências administrativas: a emissão do certificado médico de óbito, a declaração do óbito no registo civil e a obtenção da certidão de óbito. Estas diligências são enquadradas pela regulamentação cantonal. Para mais detalhes, consulte a nossa página sobre as ${A(l, 'formalites', 'formalidades em caso de falecimento')}.</p>
<p>Quando confia o funeral aos serviços funerários Murith, tratamos de todas as formalidades para o aliviar num momento difícil.</p>
<h2>2. Inumação ou cremação</h2>
<p>A escolha entre inumação e cremação é outro fator-chave do custo de um enterro, com consequências notáveis no orçamento do funeral. Conhecer os custos de cada opção ajuda a escolher com conhecimento de causa e facilita a decisão.</p>
<p><strong>O preço de uma inumação.</strong> Numa inumação, há vários custos a considerar. O primeiro é o caixão, depois a compra de uma concessão e de uma parcela num cemitério de Genebra por 20 anos, com a possibilidade de renovar a concessão. Estes custos variam consoante a duração da concessão e a localização do cemitério.</p>
<p><strong>O custo de uma cremação.</strong> Numa cremação, o custo também varia consoante vários fatores. A escolha do caixão e da urna são os principais. É igualmente importante saber que os crematórios na Suíça não aceitam caixões de cartão.</p>
<h2>3. Análise dos custos de um enterro em Genebra</h2>
<p>Em Genebra, as despesas de um enterro variam consoante vários elementos e podem diferir de um serviço funerário para outro. Entre eles:</p>
<ul><li>os fornecimentos funerários (caixões);</li><li>os serviços de terceiros (crematório, cemitério, avisos de falecimento, etc.);</li><li>as taxas relacionadas com o enterro;</li><li>os arranjos florais;</li><li>um encontro após o serviço fúnebre (cerimónia, receção, etc.).</li></ul>
<p>Para obter uma estimativa precisa, o mais simples é dirigir-se diretamente a uma empresa de serviços funerários do cantão de Genebra: conhece as despesas em detalhe e pode ajudá-lo a compreendê-las. ${A(l, 'devis', 'Receber o meu orçamento')}.</p>
<p>O planeamento de um funeral implica muitas decisões e custos variados. É por isso essencial saber quais são as despesas inevitáveis.</p>
<h3>Despesas inevitáveis</h3>
<p>A primeira despesa inevitável é o caixão. Na Suíça, um caixão de abeto custa cerca de 1 000 CHF. Nos serviços funerários Murith, o caixão de abeto custa 940 CHF, mas o preço de um caixão varia consoante o tipo de madeira e a qualidade: de 1 000 CHF a 10 000 CHF para os modelos mais elaborados. Descubra ${A(l, 'cercueils', 'os nossos modelos de caixões')}.</p>
<h3>Serviços funerários opcionais</h3>
<p>Além das despesas inevitáveis, alguns serviços opcionais podem aumentar o custo total: os serviços de um tanatopraxista, o aluguer de uma câmara funerária para a última despedida, a publicação de avisos de falecimento. Estes serviços variam de empresa para empresa.</p>
<p>Os serviços funerários Murith têm mais de 135 anos de experiência no setor funerário e um saber-fazer transmitido ao longo de cinco gerações, de pai para filho.</p>
<p>Os serviços opcionais durante um enterro podem também incluir:</p>
<ul><li>um oficiante, para personalizar a despedida e prestar homenagem à pessoa falecida;</li><li>músicos para tocar ao vivo;</li><li>flores adicionais para decorar o local da cerimónia;</li><li>serviços de fotografia ou de vídeo para guardar a memória dos momentos importantes.</li></ul>
<p>Estes serviços complementares dão um toque pessoal à cerimónia, mas também aumentam o custo total. Para saber mais, veja como ${A(l, 'obseques', 'organizamos os funerais')}.</p>
<h2>4. Preços indicativos</h2>
<div class="tbl"><table><thead><tr><th scope="col">Item</th><th scope="col">Referência</th></tr></thead><tbody>
<tr><td>Enterro, conjunto das despesas na Suíça</td><td>de 3 000 a 10 000 CHF</td></tr>
<tr><td>Caixão de abeto</td><td>cerca de 1 000 CHF na Suíça; 940 CHF na Murith</td></tr>
<tr><td>Caixão mais elaborado</td><td>até 10 000 CHF</td></tr>
<tr><td>Concessão num cemitério genebrino</td><td>20 anos, renovável; tarifa consoante a duração e o cemitério</td></tr>
<tr><td>Arranjos florais</td><td>de 100 a 900 CHF</td></tr>
<tr><td>Crematório, cemitério, avisos de falecimento, taxas</td><td>variáveis: sob orçamento</td></tr>
</tbody></table></div>
<p>Estes montantes são indicativos. Para a sua situação, ${A(l, 'devis', 'peça um orçamento sem compromisso')}.</p>
<h2>5. Arranjos florais para um funeral em Genebra</h2>
<p>Os arranjos florais são outra despesa a prever. Em Genebra, o seu preço situa-se geralmente entre 100 CHF e 900 CHF.</p>
<p>Fazem parte integrante da cerimónia fúnebre e personalizam-se de acordo com os seus desejos. Quer se trate de uma simples coroa ou de uma composição mais elaborada, convém incluí-los no orçamento do funeral. ${A(l, 'fleurs', 'Descubra os nossos arranjos florais em Genebra')}.</p>
<h2>6. Câmaras funerárias</h2>
<p>Uma câmara funerária é um local onde o corpo do falecido é velado antes do funeral e da sepultura. Nos serviços funerários Murith, as nossas câmaras estão abertas às famílias e aos seus familiares 24 horas por dia, 7 dias por semana. ${A(l, 'salons', 'Descubra os nossos salões e a capela da Cluse')}.</p>
<p>Se o falecimento ocorrer num lar, numa clínica ou no hospital, o nosso serviço efetua a transferência do falecido para as nossas instalações nas horas seguintes.</p>
<h2>7. Em resumo: o custo de um funeral em Genebra</h2>
<p>Compreender os custos de um enterro ajuda a planear e a gerir as despesas. Quer se trate de escolher entre inumação e cremação, de conhecer as despesas inevitáveis ou os serviços opcionais, estar bem informado permite tomar decisões esclarecidas. Para antecipar estas despesas, pode também descobrir a ${A(l, 'prevoyance-funeraire', 'previdência funerária')}.</p>
<p>Os serviços funerários Murith asseguram um atendimento 24 horas por dia, 7 dias por semana, para responder a todas as suas perguntas: ${TELA}. O objetivo continua a ser prestar homenagem a um ente querido de forma respeitosa e digna, respeitando o seu orçamento.</p>`,
  },
};

const tplArticle = l => (l === 'fr' ? 'blog/cout-rapatriement-corps.html' : `${l}/blog/cout-rapatriement-corps.html`);
const readMoreHead = l => l;

function buildArticle(l) {
  const D = ARTL[l];
  let h = rd(tplArticle(l));
  const url = BASE + artPath(l);
  const lang = h.match(/<html[^>]*lang="([^"]*)"/)[1];
  h = h.replace(/<title>[\s\S]*?<\/title>/, `<title>${esc(D.title)}</title>`);
  h = setMeta(h, 'description', 'x', D.desc);
  for (const k of ['og:title', 'twitter:title']) h = setMeta(h, k, 'x', D.title);
  for (const k of ['og:description', 'twitter:description']) h = setMeta(h, k, 'x', D.desc);
  h = setMeta(h, 'og:url', 'x', url);
  // données structurées : on reprend celles du modèle (noms de fil d'Ariane déjà traduits) et on change l'essentiel
  h = h.replace(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g, (m, json) => {
    const o = JSON.parse(json);
    if (o['@type'] === 'WebPage') Object.assign(o, { '@id': url + '#page', url, name: D.title, description: D.desc });
    else if (o['@type'] === 'BreadcrumbList') { const it = o.itemListElement; it[it.length - 1].name = D.short; it[it.length - 1].item = url; }
    else if (o['@type'] === 'Article') Object.assign(o, { headline: D.h1, description: D.desc, mainEntityOfPage: url, datePublished: ART.published, dateModified: ART.modified });
    return `<script type="application/ld+json">${JSON.stringify(o)}</script>`;
  });
  const alts = LANGS.map(x => `<link rel="alternate" hreflang="${x}" href="${BASE + artPath(x)}"/>`).join('') + `<link rel="alternate" hreflang="x-default" href="${BASE + artPath('fr')}"/>`;
  h = h.replace(/<link rel="canonical"[^>]*\/>(?:<link rel="alternate"[^>]*\/>)+/, `<link rel="canonical" href="${url}"/>${alts}`);
  h = h.replace(/(data-l="(\w\w)"\s+href=")[^"]*(")/g, (m, a, x, c) => a + artPath(x) + c);
  // en-tête : on garde le gabarit de la langue et on change photo, dernier élément du fil d'Ariane, étiquette, titre
  const I = ART.img, src = `/img/${I.base}`;
  const i0 = h.indexOf('<main id="main">'), i1 = h.indexOf('<article class="post-body">'), i2 = h.indexOf('<div class="btns" style="margin-top:2.6rem">');
  if (i0 < 0 || i1 < 0 || i2 < 0) throw new Error("structure inattendue du modèle d'article : " + tplArticle(l));
  let head = h.slice(i0, i1);
  head = head.replace(/<img [^>]*class="pan-ph-img"[^>]*\/?>/, `<img decoding="async" width="${I.w}" height="${I.h}" alt="${esc(D.imgAlt)}" class="pan-ph-img" fetchpriority="high" src="${src}-960.webp" srcset="${src}-480.webp 480w, ${src}-960.webp 960w, ${src}-1600.webp 1600w" sizes="100vw" style="object-position:50% 45%"/>`)
    .replace(/<span>[^<]*<\/span><\/nav>/, `<span>${esc(D.short)}</span></nav>`)
    .replace(/<span class="tag">[^<]*<\/span><span>[^<]*<\/span><span>[^<]*<\/span>/, `<span class="tag">${esc(D.tag)}</span><span>${D.dateLabel}</span><span>${D.read}</span>`)
    .replace(/<h1>[\s\S]*?<\/h1>/, `<h1>${esc(D.h1)}</h1>`);
  h = h.slice(0, i0) + head + '<article class="post-body">\n' + D.body(l) + '\n' + h.slice(i2);
  return h;
}

function patchBlogIndex(l, h) {
  const D = ARTL[l], href = artPath(l);
  if (h.includes(`href="${href}"`)) return h;
  const model = new RegExp(`<a class="post reveal" data-cats="Les obsèques" href="${l === 'fr' ? '' : '/' + l}/blog/deces-proche-suisse-10-etapes"[\\s\\S]*?</a>`);
  const m = h.match(model);
  if (!m) throw new Error(`carte modèle introuvable dans ${l === 'fr' ? '' : l + '/'}blog.html`);
  const card = m[0].replace('data-cats="Les obsèques"', `data-cats="Coût d'un enterrement|Les obsèques"`)
    .replace(/href="[^"]*deces-proche-suisse-10-etapes"/, `href="${href}"`)
    .replace('style="--d:0.08s"', 'style="--d:0.16s"')
    .replace(/<span class="tag">[^<]*<\/span><span>[^<]*<\/span><span>[^<]*<\/span>/, `<span class="tag">${esc(D.tag)}</span><span>${D.dateLabel}</span><span>${D.read}</span>`)
    .replace(/<h3>[\s\S]*?<\/h3><p>[\s\S]*?<\/p>/, `<h3>${esc(D.short)}</h3><p>${esc(D.card)}</p>`);
  const key = `<a class="post reveal" data-cats="Repatriation|Coût d'un enterrement" href="${l === 'fr' ? '' : '/' + l}/blog/cout-rapatriement-corps"`;
  const k = h.indexOf(key);
  if (k < 0) throw new Error('carte rapatriement introuvable dans le blog ' + l);
  h = h.slice(0, k) + card + h.slice(k);
  h = h.replace(/\{"@type":"ListItem","position":3,"url":"[^"]*cout-rapatriement-corps","name":"([^"]*)"\}/, (x, name) =>
    `{"@type":"ListItem","position":3,"url":"${BASE + href}","name":${JSON.stringify(D.short)}},{"@type":"ListItem","position":4,"url":"${BASE + (l === 'fr' ? '' : '/' + l)}/blog/cout-rapatriement-corps","name":"${name}"}`);
  return h;
}

/* ─────────────────────────────────────────────────────────────
   3. Retrait du texte rouge (classe seo-new)
   ───────────────────────────────────────────────────────────── */
const SKIP_DIRS = new Set(['_archive-wix', '_build', '_src', 'node_modules', '.git', 'img', 'fonts', 'docs', '_img-src']);
function htmlFiles(dir = '', out = []) {
  for (const e of fs.readdirSync(path.join(root, dir), { withFileTypes: true })) {
    if (SKIP_DIRS.has(e.name)) continue;
    const rel = path.join(dir, e.name);
    if (e.isDirectory()) htmlFiles(rel, out); else if (e.name.endsWith('.html')) out.push(rel.split(path.sep).join('/'));
  }
  return out;
}
const textOf = s => s.replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();

function stripRed(html, collect) {
  const open = /<([a-z][a-z0-9]*)\b[^>]*?\bclass="([^"]*?\bseo-new\b[^"]*?)"[^>]*>/i;
  let n = 0, guard = 0;
  for (;;) {
    const m = open.exec(html);
    if (!m || ++guard > 5000) break;
    const tag = m[1].toLowerCase(), tokens = m[2].split(/\s+/).filter(t => t && t !== 'seo-new');
    const onlyClass = new RegExp(`^<${tag}\\s+class="[^"]*">$`, 'i').test(m[0]);
    n++;
    if ((tag === 'span' || tag === 'div') && onlyClass && tokens.length === 0) {
      // retire la balise ouvrante et la fermante correspondante, garde le contenu
      const re = new RegExp(`<(/?)${tag}\\b[^>]*>`, 'gi'); re.lastIndex = m.index + m[0].length;
      let depth = 1, end = -1, mm;
      while ((mm = re.exec(html))) { depth += mm[1] ? -1 : 1; if (depth === 0) { end = mm.index; break; } }
      if (end < 0) throw new Error('balise fermante introuvable pour ' + m[0]);
      const inner = html.slice(m.index + m[0].length, end);
      if (collect) collect(textOf(inner));
      html = html.slice(0, m.index) + inner + html.slice(end + `</${tag}>`.length);
    } else {
      const cls = tokens.length ? `class="${tokens.join(' ')}"` : '';
      const repl = m[0].replace(/\s*\bclass="[^"]*"/, cls ? ' ' + cls : '');
      if (collect) collect('(attribut sur <' + tag + '>)');
      html = html.slice(0, m.index) + repl + html.slice(m.index + m[0].length);
    }
  }
  return [html, n];
}


/* ─────────────────────────────────────────────────────────────
   4. Sitemap et contrôle SEO
   ───────────────────────────────────────────────────────────── */
function sitemapUrl(loc, lastmod, alts, images = []) {
  return `<url><loc>${loc}</loc><lastmod>${lastmod}</lastmod>${alts.map(([l, u]) => `<xhtml:link rel="alternate" hreflang="${l}" href="${u}"/>`).join('')}${images.map(i => `<image:image><image:loc>${i}</image:loc></image:image>`).join('')}</url>`;
}
const dropUrl = (sm, loc) => sm.replace(new RegExp(`<url><loc>${loc.replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&')}</loc>[\\s\\S]*?</url>\\n?`), '');
function patchSitemap(sm) {
  // pages de confidentialité (6 langues)
  if (!sm.includes('/politique-de-confidentialite</loc>')) {
    const alts = [...LANGS.map(l => [l, BASE + privPath(l)]), ['x-default', BASE + privPath('fr')]];
    const add = LANGS.map(l => sitemapUrl(BASE + privPath(l), DATE, alts)).join('\n');
    sm = sm.replace('</urlset>', add + '\n</urlset>');
  }
  // article du coût d'un enterrement (6 langues) : on remplace d'éventuelles anciennes entrées
  const alts = [...LANGS.map(l => [l, BASE + artPath(l)]), ['x-default', BASE + artPath('fr')]];
  for (const l of LANGS) {
    const loc = BASE + artPath(l);
    sm = dropUrl(sm, loc);
    const entry = sitemapUrl(loc, DATE, alts, [`${BASE}/img/${ART.img.base}-1600.webp`]) + '\n';
    const at = sm.indexOf(`<url><loc>${BASE + (l === 'fr' ? '' : '/' + l)}/blog/cout-rapatriement-corps</loc>`);
    sm = at >= 0 ? sm.slice(0, at) + entry + sm.slice(at) : sm.replace('</urlset>', entry + '</urlset>');
  }
  // les pages « blog » ont changé
  for (const l of LANGS) sm = sm.replace(new RegExp(`(<url><loc>${BASE}${l === 'fr' ? '' : '/' + l}/blog</loc><lastmod>)[^<]*`), `$1${DATE}`);
  return sm;
}

/* check-seo.mjs : l'ancienne version du script autorisait une page française seule ; ce n'est plus nécessaire */
function patchCheckSeo(t) {
  return t.replace("new Set(['/blog/cout-obseques-geneve'])", 'new Set([])');
}

/* ─────────────────────────────────────────────────────────────
   5. Formulaires : branchement sur /api/contact (Resend)
   ───────────────────────────────────────────────────────────── */
const API_CONTACT = String.raw`// Vercel Function : reçoit les formulaires du site (contact et devis) et les envoie par e-mail avec Resend.
//
// Variables d'environnement à définir dans Vercel (Settings > Environment Variables), puis redéployer :
//   RESEND_API_KEY   clé API Resend (re_...)                                   [obligatoire]
//   CONTACT_FROM     expéditeur, ex. "Site Murith <site@envoi.murith.ch>"      [défaut ci-dessous]
//   CONTACT_TO       destinataire, ex. "murith@murith.ch"                      [défaut ci-dessous]
'use strict';

const FROM = process.env.CONTACT_FROM || 'Site Murith <site@envoi.murith.ch>';
const TO = process.env.CONTACT_TO || 'murith@murith.ch';
const MAX_FIELDS = 40, MAX_LEN = 4000;

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (s, n) => String(s == null ? '' : s).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').slice(0, n);
const oneLine = (s, n) => clean(s, n).replace(/[\r\n]+/g, ' ').trim();

// Accepte le site (murith.ch, www.murith.ch) ; les adresses .vercel.app et localhost seulement hors production.
function originOk(req) {
  const o = req.headers.origin || '';
  if (!o) return true;
  let host; try { host = new URL(o).hostname; } catch (e) { return false; }
  if (host === 'murith.ch' || host === 'www.murith.ch') return true;
  return process.env.VERCEL_ENV !== 'production' && (host.endsWith('.vercel.app') || host === 'localhost');
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ ok: false }); }
  if (!originOk(req)) return res.status(403).json({ ok: false });
  if (!process.env.RESEND_API_KEY) return res.status(500).json({ ok: false, error: 'not-configured' });

  let b;
  try { b = req.body; } catch (e) { return res.status(400).json({ ok: false }); }
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch (e) { b = null; } }
  if (!b || typeof b !== 'object') return res.status(400).json({ ok: false });

  // Champ piège (invisible) : seuls les robots le remplissent. On répond « ok » sans rien envoyer.
  if (b.website) return res.status(200).json({ ok: true });

  const fields = (Array.isArray(b.fields) ? b.fields : []).slice(0, MAX_FIELDS)
    .map(f => ({ label: oneLine(f && f.label, 80), value: clean(f && f.value, MAX_LEN) }))
    .filter(f => f.label && f.value);
  if (!fields.length) return res.status(400).json({ ok: false });

  const email = oneLine(b.email, 200);
  const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
  const subject = '[murith.ch] ' + (oneLine(b.subject, 120) || 'Message depuis le site');
  const rows = fields.map(f => '<tr><td style="padding:4px 12px 4px 0;vertical-align:top;color:#555"><b>' + esc(f.label) + '</b></td><td style="padding:4px 0;white-space:pre-wrap">' + esc(f.value) + '</td></tr>').join('');
  const html = '<table style="font-family:Arial,sans-serif;font-size:14px;border-collapse:collapse">' + rows + '</table>' +
    '<p style="font-family:Arial,sans-serif;font-size:12px;color:#888">Envoyé depuis ' + esc(oneLine(b.page, 200)) + ' (langue : ' + esc(oneLine(b.lang, 5)) + ')</p>';
  const text = fields.map(f => f.label + ' : ' + f.value).join('\n') + '\n\nEnvoyé depuis ' + oneLine(b.page, 200);

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + process.env.RESEND_API_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.assign({ from: FROM, to: [TO], subject: subject, html: html, text: text }, emailOk ? { reply_to: email } : {}))
    });
    if (!r.ok) { console.error('Resend', r.status, await r.text()); return res.status(502).json({ ok: false }); }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('Resend', e);
    return res.status(502).json({ ok: false });
  }
};
`;

// textes de confirmation : l'ancien message annonçait « votre messagerie s'ouvre »
const DONE_JS = {   // [ancien titre, nouveau titre, nouveau texte]
  fr: ['Merci, votre message est prêt', 'Merci pour votre message', "Nous vous répondons dans les meilleurs délais. Pour une réponse immédiate, appelez-nous au 022 809 56 00, 24h/24."],
  en: ['Thank you, your message is ready', 'Thank you for your message', 'We will reply as soon as possible. For an immediate answer, call us on 022 809 56 00, 24/7.'],
  de: ['Danke, Ihre Nachricht ist bereit', 'Danke für Ihre Nachricht', 'Wir antworten Ihnen so schnell wie möglich. Für eine sofortige Antwort rufen Sie uns an: 022 809 56 00, rund um die Uhr.'],
  es: ['Gracias, su mensaje está listo', 'Gracias por su mensaje', 'Le responderemos lo antes posible. Para una respuesta inmediata, llámenos al 022 809 56 00, 24 h/24.'],
  pt: ['Obrigado, a sua mensagem está pronta', 'Obrigado pela sua mensagem', 'Responderemos o mais depressa possível. Para uma resposta imediata, ligue 022 809 56 00, 24h/24.'],
  it: ['Grazie, il vostro messaggio è pronto', 'Grazie per il vostro messaggio', 'Vi risponderemo il prima possibile. Per una risposta immediata, chiamateci allo 022 809 56 00, 24 ore su 24.'],
};
const SENT_HTML = [   // paragraphe affiché sous les formulaires de contact
  ["Votre messagerie s'ouvre pour envoyer votre message.", 'Merci pour votre message.'],
  ['Your email client is opening to send your message.', 'Thank you for your message.'],
  ['Ihr E-Mail-Programm öffnet sich, um Ihre Nachricht zu senden.', 'Danke für Ihre Nachricht.'],
  ['Si aprirà il vostro programma di posta per inviare il messaggio.', 'Grazie per il vostro messaggio.'],
  ['Se abre su aplicación de correo para enviar su mensaje.', 'Gracias por su mensaje.'],
  ['A sua aplicação de e-mail abre-se para enviar a mensagem.', 'Obrigado pela sua mensagem.'],
];
const DEVIS_HTML = {  // confirmation de la page devis, par langue
  '': [['Votre demande est prête', "Votre messagerie s'ouvre pour envoyer votre demande à murith@murith.ch. Nous vous répondons sous 24h, sans engagement."], ['Merci pour votre demande', 'Nous vous répondons sous 24h, sans engagement. Pour une réponse immédiate, appelez-nous au 022 809 56 00, 24h/24.']],
  en: [['Your request is ready', 'Your email client is opening to send your request to murith@murith.ch. We will reply within 24h, with no commitment.'], ['Thank you for your request', 'We will reply within 24h, with no commitment. For an immediate answer, call us on 022 809 56 00, 24/7.']],
  de: [['Ihre Anfrage ist bereit', 'Ihr E-Mail-Programm öffnet sich, um Ihre Anfrage an murith@murith.ch zu senden. Wir antworten innerhalb von 24 Std., unverbindlich.'], ['Danke für Ihre Anfrage', 'Wir antworten innerhalb von 24 Std., unverbindlich. Für eine sofortige Antwort rufen Sie uns an: 022 809 56 00, rund um die Uhr.']],
  it: [['La vostra richiesta è pronta', 'Si aprirà il vostro programma di posta per inviare la richiesta a murith@murith.ch. Vi rispondiamo entro 24 ore, senza impegno.'], ['Grazie per la vostra richiesta', 'Vi rispondiamo entro 24 ore, senza impegno. Per una risposta immediata, chiamateci allo 022 809 56 00, 24 ore su 24.']],
  es: [['Su solicitud está lista', 'Se abre su aplicación de correo para enviar su solicitud a murith@murith.ch. Le respondemos en 24 h, sin compromiso.'], ['Gracias por su solicitud', 'Le respondemos en 24 h, sin compromiso. Para una respuesta inmediata, llámenos al 022 809 56 00, 24 h/24.']],
  pt: [['O seu pedido está pronto', 'A sua aplicação de e-mail abre-se para enviar o pedido para murith@murith.ch. Respondemos em 24h, sem compromisso.'], ['Obrigado pelo seu pedido', 'Respondemos em 24h, sem compromisso. Para uma resposta imediata, ligue 022 809 56 00, 24h/24.']],
};

function patchAppSource(js) {
  if (js.includes('function sendForm(')) return js;
  const must = (a, b) => { if (!js.includes(a)) throw new Error('app.js : repère introuvable : ' + a.slice(0, 70)); js = js.replace(a, () => b); };
  must("/* Formulaires (prototype : mailto — renseigner FORM_ENDPOINT pour un envoi réel) */\n  var FORM_ENDPOINT = '';",
    "/* Formulaires : envoi par e-mail via la fonction /api/contact (Resend) ; repli sur la messagerie de l'internaute si l'envoi échoue */\n  var FORM_ENDPOINT = '/api/contact';");
  must("    return out.join('\\n');\n  }\n  $$('form[data-mail]:not(#devis-form)').forEach(function (form) {",
    `    return out.join('\\n');
  }
  function sendForm(form, subj) {
    var fields = [], email = '', hp = form.querySelector('input[name=website]');
    $$('input,textarea,select', form).forEach(function (f) {
      if (!f.name || f.name === 'website') return;
      if ((f.type === 'radio' || f.type === 'checkbox') && !f.checked) return;
      if (!f.value) return;
      if (f.name === 'email') email = f.value;
      fields.push({ label: f.getAttribute('data-label') || f.name, value: f.value });
    });
    var fallback = function () { window.location.href = 'mailto:murith@murith.ch?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(formText(form)); };
    try {
      fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subject: subj, page: location.pathname, lang: (d.documentElement.lang || 'fr').slice(0, 2), email: email, fields: fields, website: hp ? hp.value : '' }) })
        .then(function (r) { if (!r.ok) fallback(); }, fallback);
    } catch (e) { fallback(); }
  }
  /* champ piège invisible contre les robots (rempli par les robots seulement) */
  function addHoneypot(form) {
    var h = d.createElement('input'); h.type = 'text'; h.name = 'website'; h.tabIndex = -1; h.autocomplete = 'off'; h.setAttribute('aria-hidden', 'true');
    h.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;opacity:0'; form.appendChild(h);
  }
  $$('form[data-mail]:not(#devis-form)').forEach(function (form) {
    addHoneypot(form);`);
  must("      if (FORM_ENDPOINT) { fetch(FORM_ENDPOINT, { method: 'POST', body: new FormData(form) }); }\n      else { window.location.href = 'mailto:murith@murith.ch?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(formText(form)); }",
    '      sendForm(form, subj);');
  must("      if (FORM_ENDPOINT) { fetch(FORM_ENDPOINT, { method: 'POST', body: new FormData(qf) }); }\n      else { window.location.href = 'mailto:murith@murith.ch?subject=' + encodeURIComponent(qf.getAttribute('data-mail')) + '&body=' + encodeURIComponent(formText(qf)); }",
    "      sendForm(qf, qf.getAttribute('data-mail'));");
  must("  var qf = $('#devis-form');\n  if (qf) {", "  var qf = $('#devis-form');\n  if (qf) {\n    addHoneypot(qf);");
  // textes de confirmation du formulaire de contact
  for (const l of Object.keys(DONE_JS)) {
    const [oldT, newT, newP] = DONE_JS[l];
    const re = new RegExp(`done: '${oldT.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}', doneP: '(?:[^'\\\\]|\\\\.)*'`);
    if (!re.test(js)) throw new Error('app.js : texte de confirmation introuvable (' + l + ')');
    js = js.replace(re, () => `done: '${newT.replace(/'/g, "\\'")}', doneP: '${newP.replace(/'/g, "\\'")}'`);
  }
  return js;
}

/* ─────────────────────────────────────────────────────────────
   Exécution
   ───────────────────────────────────────────────────────────── */
console.log('\n=== prepare-bascule : préparation du site avant la bascule ===\n');

console.log('1. Texte rouge (seo-new)');
{
  const report = []; let pages = 0, total = 0;
  for (const f of htmlFiles()) {
    const h0 = rd(f);
    if (!h0.includes('seo-new')) continue;
    const found = [];
    const [h1, n] = stripRed(h0, t => found.push(t));
    if (n) { wr(f, h1); pages++; total += n; report.push([f, found]); }
  }
  if (total) {
    const md = ['# Texte qui était en rouge avant la bascule', '', `Retiré le ${DATE} par prepare-bascule.mjs. Le texte est conservé sur le site ; seule la couleur rouge est supprimée.`, `${total} repères sur ${pages} pages.`, '']
      .concat(...report.map(([f, a]) => [`## ${f}`, ...a.filter(x => x).map(x => `- ${x.length > 300 ? x.slice(0, 300) + '…' : x}`), '']));
    wr('_build/rapport-texte-rouge.md', md.join('\n'));
    say(`${total} repères retirés sur ${pages} pages (liste : _build/rapport-texte-rouge.md)`);
  } else say('aucun texte rouge restant');
  for (const f of ['_src/style.css', 'style.css']) {
    if (!fs.existsSync(path.join(root, f))) continue;
    let c = rd(f); if (!c.includes('seo-new')) continue;
    c = c.replace(/\.seo-new,\.seo-new\s*\*\s*\{[^}]*\}\s*/g, '').replace(/^.*\.seo-new.*\n?/gm, '');
    if (c.includes('seo-new')) say(`⚠ ${f} : une règle seo-new subsiste, à retirer à la main`); else { wr(f, c); say(`règle CSS retirée : ${f}`); }
  }
  const left = htmlFiles().filter(f => rd(f).includes('seo-new'));
  if (left.length) say(`⚠ seo-new encore présent dans : ${left.join(', ')}`);
}

console.log('2. Pages de confidentialité (6 langues)');
for (const l of LANGS) {
  const f = (l === 'fr' ? '' : l + '/') + 'politique-de-confidentialite.html';
  const html = buildPrivacy(l);
  if (fs.existsSync(path.join(root, f)) && rd(f) === html) say(`déjà à jour : ${f}`);
  else { wr(f, html); say(`créé ou mis à jour : ${f}`); }
}

console.log("3. Article du coût d'un enterrement (6 langues) et blog");
for (const l of LANGS) {
  const f = (l === 'fr' ? '' : l + '/') + `blog/${ART.slug}.html`, html = buildArticle(l);
  if (fs.existsSync(path.join(root, f)) && rd(f) === html) say(`déjà à jour : ${f}`); else { wr(f, html); say(`créé ou mis à jour : ${f}`); }
  const bf = (l === 'fr' ? '' : l + '/') + 'blog.html', b0 = rd(bf), b1 = patchBlogIndex(l, b0);
  if (b0 !== b1) { wr(bf, b1); say(`${bf} : carte et données structurées ajoutées`); }
}

console.log('4. Formulaires : branchement sur /api/contact (Resend)');
{
  if (!fs.existsSync(path.join(root, 'api/contact.js')) || rd('api/contact.js') !== API_CONTACT) { wr('api/contact.js', API_CONTACT); say('créé ou mis à jour : api/contact.js'); } else say('déjà à jour : api/contact.js');
  const j0 = rd('_src/app.js'), j1 = patchAppSource(j0);
  if (j0 !== j1) { wr('_src/app.js', j1); say('_src/app.js : envoi par /api/contact, avec repli sur la messagerie'); }
  if (!rd('app.js').includes('/api/contact')) {
    // même commande que _build/minify.mjs (résultat identique octet pour octet au fichier actuel)
    const r = spawnSync('npx', ['--yes', 'esbuild@0.28.2', '_src/app.js', '--minify', '--target=es2018', '--legal-comments=none', '--outfile=app.js'], { cwd: root, encoding: 'utf8', shell: process.platform === 'win32' });
    if (r.status === 0 && rd('app.js').includes('/api/contact')) say('app.js régénéré (esbuild)');
    else { say('⚠ app.js non régénéré (esbuild indisponible ?). Lancez « npx --yes esbuild@0.28.2 _src/app.js --minify --target=es2018 --legal-comments=none --outfile=app.js » puis relancez ce script.'); console.log((r.stderr || '').split('\n').slice(0, 4).join('\n')); }
  } else say('déjà à jour : app.js');
  // textes statiques de confirmation (6 langues)
  let n = 0;
  for (const f of htmlFiles()) {
    let h = rd(f), h0 = h;
    if (f.endsWith('contact.html') || f.endsWith('index.html')) for (const [a, b] of SENT_HTML) h = h.split(`class="sent" role="status">${a}`).join(`class="sent" role="status">${b}`);
    if (f.endsWith('devis.html')) { const d = DEVIS_HTML[f.includes('/') ? f.split('/')[0] : '']; if (d) h = h.replace(`<h3>${d[0][0]}</h3><p>${d[0][1]}</p>`, () => `<h3>${d[1][0]}</h3><p>${d[1][1]}</p>`); }
    if (h !== h0) { wr(f, h); n++; }
  }
  say(n ? `${n} pages : messages de confirmation mis à jour` : 'messages de confirmation : déjà à jour');
}

console.log('5. Sitemap et contrôle SEO');
{
  const s0 = rd('sitemap.xml'), s1 = patchSitemap(s0);
  if (s0 !== s1) { wr('sitemap.xml', s1); say('sitemap.xml : mis à jour (confidentialité ×6, article ×6)'); } else say('sitemap.xml : déjà à jour');
  const c0 = rd('check-seo.mjs'), c1 = patchCheckSeo(c0);
  if (c0 !== c1) { wr('check-seo.mjs', c1); say('check-seo.mjs : mis à jour'); }
}

console.log('6. Descriptions trop courtes ou trop longues (7 pages signalées par check-seo)');
{
  const FIX = {
    'prevoyance-funeraire.html': ["Préparez vos obsèques de votre vivant à Genève : volontés, cérémonie, financement. Nous vous guidons pas à pas.", "Préparez vos obsèques de votre vivant à Genève : volontés, cérémonie, financement. Murith vous guide pas à pas, avec le soin d'une maison genevoise depuis 1888."],
    'en/prevoyance-funeraire.html': ["Plan your funeral in advance in Geneva: wishes, ceremony, financing. We guide you step by step.", "Plan your funeral in advance in Geneva: wishes, ceremony, financing. Murith guides you step by step, with the care of a Geneva family firm since 1888."],
    'es/prevoyance-funeraire.html': ["Prepare su funeral en vida en Ginebra: voluntades, ceremonia y financiación. Le guiamos paso a paso.", "Prepare su funeral en vida en Ginebra: voluntades, ceremonia y financiación. Murith le guía paso a paso, con el cuidado de una casa ginebrina desde 1888."],
    'it/prevoyance-funeraire.html': ["Preparate le vostre esequie in vita a Ginevra: volontà, cerimonia, finanziamento. Vi guidiamo passo dopo passo.", "Preparate le vostre esequie in vita a Ginevra: volontà, cerimonia, finanziamento. Murith vi guida passo dopo passo, con la cura di una casa ginevrina dal 1888."],
    'pt/prevoyance-funeraire.html': ["Prepare o seu funeral em vida em Genebra: vontades, cerimónia e financiamento. Guiamo-lo passo a passo.", "Prepare o seu funeral em vida em Genebra: vontades, cerimónia e financiamento. A Murith guia-o passo a passo, com o cuidado de uma casa genebrina desde 1888."],
    'blog/prevoyance-funeraire-geneve.html': ["Prévoyance funéraire à Genève : comment organiser et financer vos obsèques à l'avance, tarifs bloqués dès la souscription, démarches et conseils de la Maison Murith.", "Prévoyance funéraire à Genève : organisez et financez vos obsèques à l'avance, tarifs bloqués dès la souscription. Démarches et conseils de la Maison Murith."],
    'de/blog/prevoyance-funeraire-geneve.html': ["Bestattungsvorsorge in Genf: So organisieren und finanzieren Sie Ihre Bestattung im Voraus – Preise ab Vertragsabschluss garantiert, mit Beratung der Maison Murith.", "Bestattungsvorsorge in Genf: So organisieren und finanzieren Sie Ihre Bestattung im Voraus – Preise ab Vertragsabschluss garantiert. Beratung der Maison Murith."],
  };
  let n = 0;
  for (const [f, [a, b]] of Object.entries(FIX)) {
    if (b.length < 120 || b.length > 160) { say(`⚠ description hors limites (${b.length}) : ${f}`); continue; }
    const h = rd(f); if (!h.includes(a)) continue;
    wr(f, h.split(a).join(b)); n++;
  }
  say(n ? `${n} descriptions corrigées (balise, Open Graph, Twitter et données structurées)` : 'déjà à jour');
}

console.log('7. Redirections et vérifications');
const run = (args, label) => { const r = spawnSync(process.execPath, args, { cwd: root, encoding: 'utf8' }); say(`${label} : ${r.status === 0 ? 'OK' : 'ÉCHEC (code ' + r.status + ')'}`); return r; };
if (fs.existsSync(path.join(root, 'migration-murith.mjs'))) {
  const r = run(['migration-murith.mjs'], 'migration-murith.mjs (vercel.json régénéré)');
  (r.stdout.match(/⚠[^\n]*/g) || []).forEach(w => console.log('     ' + w));
} else say('⚠ migration-murith.mjs absent : copiez-le à la racine puis relancez');
const seo = run(['check-seo.mjs'], 'check-seo.mjs');
console.log((seo.stdout + seo.stderr).split('\n').filter(l => /ERREUR|OK :|Pages contrôlées|Avertissements/.test(l) || (seo.status !== 0 && /^ +- /.test(l))).slice(0, 30).map(l => '     ' + l).join('\n'));

console.log('\nTerminé. Prochaines étapes :');
console.log('  git status                      # relire les fichiers modifiés');
console.log('  node dev-server.mjs 3000        # tester http://localhost:3000/politique-de-confidentialite et /blog/cout-obseques-geneve');
console.log('  git add -A && git commit -m "Bascule SEO : confidentialité, article ×6, formulaires, redirections" && git push');
console.log('  Dans Vercel : ajouter RESEND_API_KEY (et CONTACT_TO / CONTACT_FROM), puis redéployer.\n');
process.exit(seo.status === 0 ? 0 : 1);
