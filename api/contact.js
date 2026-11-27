// Magali Tshikudi - Websituation | https://www.websituation.ch
// Vercel Function : reçoit les formulaires du site (contact, et devis / questionnaire) et envoie, avec Resend :
//   1. une notification détaillée à l'entreprise (toutes les réponses, bouton « Répondre » vers le visiteur) ;
//   2. un e-mail de confirmation au visiteur, dans sa langue (fr, en, de, it, es, pt).
//
// Variables d'environnement à définir dans Vercel (Settings > Environment Variables), puis redéployer :
//   RESEND_API_KEY   clé API Resend (re_...)                                         [obligatoire]
//   CONTACT_TO       destinataire des notifications, ex. "murith@murith.ch"          [défaut ci-dessous]
//   CONTACT_FROM     expéditeur des notifications, ex. "Site Murith <site@envoi.murith.ch>"   [défaut ci-dessous]
//   CONFIRM_FROM     expéditeur de la confirmation au visiteur, ex. "Maison Murith <site@envoi.murith.ch>"   [défaut ci-dessous]
// Le domaine de l'expéditeur (envoi.murith.ch) doit être vérifié dans Resend.
'use strict';

const FROM = process.env.CONTACT_FROM || 'Site Murith <site@envoi.murith.ch>';
const FROM_VISITOR = process.env.CONFIRM_FROM || 'Maison Murith <site@envoi.murith.ch>';
const TO = process.env.CONTACT_TO || 'murith@murith.ch';
const SITE = 'https://www.murith.ch';
const TEL = '+41 22 809 56 00', TEL_HREF = '+41228095600';
const ADDR = '89, boulevard de la Cluse, 1205 Genève';
const LANGS = ['fr', 'en', 'de', 'it', 'es', 'pt'];
const LANG_NAME = { fr: 'Français', en: 'English', de: 'Deutsch', it: 'Italiano', es: 'Español', pt: 'Português' };
const MAX_FIELDS = 40, MAX_LEN = 4000;
const C = { accent: '#3A5796', head: '#181C23', ink: '#22262E', soft: '#4C5462', muted: '#6F788A', line: '#DDE4F0', bg: '#F3F6FC' };
const SANS = "Arial,Helvetica,sans-serif", SERIF = "Georgia,'Times New Roman',serif";

/* Textes de la confirmation envoyée au visiteur. Le texte libre saisi par le visiteur n'est jamais
   repris dans cet e-mail (pour qu'il ne serve pas à envoyer des messages à un tiers). */
const V = {
  fr: {
    hi: n => n ? 'Bonjour ' + n + ',' : 'Bonjour,',
    contact: { subject: 'Nous avons bien reçu votre message', h: 'Nous avons bien reçu votre message', p: 'Merci de nous avoir écrit. Votre message est bien arrivé et un membre de notre équipe vous répondra dans les meilleurs délais.' },
    devis: { subject: 'Nous avons bien reçu votre demande de devis', h: 'Nous avons bien reçu votre demande de devis', p: 'Merci pour votre demande. Elle est bien arrivée et un conseiller vous répondra sous 24 h, sans engagement.' },
    urgent: 'Si votre situation est urgente, appelez-nous : nous sommes à votre écoute 24 h/24, 7 j/7.',
    call: 'Appeler le ', sign: 'Avec toute notre sympathie,', team: 'La Maison Murith, pompes funèbres à Genève depuis 1888',
    foot: 'Vous recevez ce message car un formulaire a été envoyé depuis murith.ch avec cette adresse e-mail. Si ce n\'est pas vous, vous pouvez l\'ignorer. Vous pouvez répondre directement à cet e-mail.',
    pre: 'Votre demande est bien arrivée chez Murith.'
  },
  en: {
    hi: n => n ? 'Hello ' + n + ',' : 'Hello,',
    contact: { subject: 'We have received your message', h: 'We have received your message', p: 'Thank you for writing to us. Your message has arrived and a member of our team will reply as soon as possible.' },
    devis: { subject: 'We have received your quote request', h: 'We have received your quote request', p: 'Thank you for your request. It has arrived and an advisor will reply within 24 hours, with no commitment.' },
    urgent: 'If your situation is urgent, please call us: we are here for you 24 hours a day, 7 days a week.',
    call: 'Call ', sign: 'With our deepest sympathy,', team: 'The Maison Murith, funeral directors in Geneva since 1888',
    foot: 'You are receiving this message because a form was submitted on murith.ch with this email address. If this was not you, you can ignore it. You can reply directly to this email.',
    pre: 'Your request has reached Murith.'
  },
  de: {
    hi: n => n ? 'Guten Tag ' + n + ',' : 'Guten Tag,',
    contact: { subject: 'Wir haben Ihre Nachricht erhalten', h: 'Wir haben Ihre Nachricht erhalten', p: 'Vielen Dank für Ihre Nachricht. Sie ist bei uns angekommen, und ein Mitglied unseres Teams antwortet Ihnen so schnell wie möglich.' },
    devis: { subject: 'Wir haben Ihre Offertanfrage erhalten', h: 'Wir haben Ihre Offertanfrage erhalten', p: 'Vielen Dank für Ihre Anfrage. Sie ist bei uns angekommen, und ein Berater antwortet Ihnen innerhalb von 24 Stunden, unverbindlich.' },
    urgent: 'Wenn Ihre Situation dringend ist, rufen Sie uns an: Wir sind rund um die Uhr für Sie da.',
    call: 'Anrufen: ', sign: 'In aufrichtiger Anteilnahme,', team: 'Die Maison Murith, Bestattungsinstitut in Genf seit 1888',
    foot: 'Sie erhalten diese Nachricht, weil über murith.ch ein Formular mit dieser E-Mail-Adresse abgesendet wurde. Falls Sie das nicht waren, können Sie sie ignorieren. Sie können direkt auf diese E-Mail antworten.',
    pre: 'Ihre Anfrage ist bei Murith angekommen.'
  },
  it: {
    hi: n => n ? 'Buongiorno ' + n + ',' : 'Buongiorno,',
    contact: { subject: 'Abbiamo ricevuto il vostro messaggio', h: 'Abbiamo ricevuto il vostro messaggio', p: 'Grazie per averci scritto. Il vostro messaggio ci è arrivato e un membro del nostro team vi risponderà il prima possibile.' },
    devis: { subject: 'Abbiamo ricevuto la vostra richiesta di preventivo', h: 'Abbiamo ricevuto la vostra richiesta di preventivo', p: 'Grazie per la vostra richiesta. È arrivata e un consulente vi risponderà entro 24 ore, senza impegno.' },
    urgent: 'Se la vostra situazione è urgente, chiamateci: siamo a vostra disposizione 24 ore su 24, 7 giorni su 7.',
    call: 'Chiamare lo ', sign: 'Con profonda partecipazione,', team: 'La Maison Murith, pompe funebri a Ginevra dal 1888',
    foot: 'Ricevete questo messaggio perché è stato inviato un modulo su murith.ch con questo indirizzo e-mail. Se non siete stati voi, potete ignorarlo. Potete rispondere direttamente a questa e-mail.',
    pre: 'La vostra richiesta è arrivata a Murith.'
  },
  es: {
    hi: n => n ? 'Buenos días ' + n + ',' : 'Buenos días,',
    contact: { subject: 'Hemos recibido su mensaje', h: 'Hemos recibido su mensaje', p: 'Gracias por escribirnos. Su mensaje ha llegado y un miembro de nuestro equipo le responderá lo antes posible.' },
    devis: { subject: 'Hemos recibido su solicitud de presupuesto', h: 'Hemos recibido su solicitud de presupuesto', p: 'Gracias por su solicitud. Ha llegado y un asesor le responderá en 24 horas, sin compromiso.' },
    urgent: 'Si su situación es urgente, llámenos: estamos a su disposición las 24 horas, los 7 días de la semana.',
    call: 'Llamar al ', sign: 'Con nuestro más sentido pésame,', team: 'La Maison Murith, pompas fúnebres en Ginebra desde 1888',
    foot: 'Recibe este mensaje porque se envió un formulario en murith.ch con esta dirección de correo. Si no fue usted, puede ignorarlo. Puede responder directamente a este correo.',
    pre: 'Su solicitud ha llegado a Murith.'
  },
  pt: {
    hi: n => n ? 'Bom dia ' + n + ',' : 'Bom dia,',
    contact: { subject: 'Recebemos a sua mensagem', h: 'Recebemos a sua mensagem', p: 'Obrigado por nos ter escrito. A sua mensagem chegou e um membro da nossa equipa responderá o mais depressa possível.' },
    devis: { subject: 'Recebemos o seu pedido de orçamento', h: 'Recebemos o seu pedido de orçamento', p: 'Obrigado pelo seu pedido. Chegou e um conselheiro responderá em 24 horas, sem compromisso.' },
    urgent: 'Se a sua situação for urgente, ligue-nos: estamos ao seu dispor 24 horas por dia, 7 dias por semana.',
    call: 'Ligar para o ', sign: 'Com as nossas sentidas condolências,', team: 'A Maison Murith, pompas fúnebres em Genebra desde 1888',
    foot: 'Recebe esta mensagem porque foi enviado um formulário em murith.ch com este endereço de e-mail. Se não foi você, pode ignorá-la. Pode responder diretamente a este e-mail.',
    pre: 'O seu pedido chegou à Murith.'
  }
};

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (s, n) => String(s == null ? '' : s).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').slice(0, n);
const oneLine = (s, n) => clean(s, n).replace(/[\r\n]+/g, ' ').trim();
const nameOnly = s => oneLine(s, 60).replace(/[^\p{L}\p{M}' .-]/gu, '').replace(/\s+/g, ' ').trim().slice(0, 40);

/* Gabarit commun : en-tête avec logo, carte blanche, pied de page. Mise en page en tableaux et styles en ligne
   (seule méthode qui fonctionne partout : Gmail, Outlook, Apple Mail). */
function layout(o) {
  const btn = (href, label) => '<a href="' + esc(href) + '" style="display:inline-block;background:' + C.accent + ';color:#ffffff;text-decoration:none;font-family:' + SANS + ';font-size:15px;font-weight:bold;line-height:1;padding:14px 26px;border-radius:999px">' + esc(label) + '</a>';
  return '<!DOCTYPE html><html lang="' + o.lang + '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>' + esc(o.title) + '</title></head>' +
    '<body style="margin:0;padding:0;background:' + C.bg + '">' +
    '<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:' + C.bg + ';font-size:1px;line-height:1px">' + esc(o.pre) + '</div>' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:' + C.bg + '"><tr><td align="center" style="padding:28px 12px">' +
    '<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:#ffffff;border:1px solid ' + C.line + ';border-top:4px solid ' + C.accent + ';border-radius:14px">' +
    '<tr><td style="padding:28px 36px 8px"><a href="' + SITE + '" style="text-decoration:none"><img src="' + SITE + '/img/logo-marine.png" width="190" alt="A. Murith SA, pompes funèbres depuis 1888" style="display:block;border:0;height:auto;width:190px;max-width:100%"></a></td></tr>' +
    '<tr><td style="padding:12px 36px 32px;font-family:' + SANS + ';font-size:16px;line-height:1.6;color:' + C.ink + '">' + o.body(btn) + '</td></tr>' +
    '<tr><td style="padding:20px 36px 26px;border-top:1px solid ' + C.line + ';font-family:' + SANS + ';font-size:13px;line-height:1.55;color:' + C.muted + '">' +
    '<b style="color:' + C.soft + '">A. Murith SA</b> · ' + esc(ADDR) + '<br><a href="tel:' + TEL_HREF + '" style="color:' + C.muted + '">' + TEL + '</a> · <a href="mailto:' + esc(TO) + '" style="color:' + C.muted + '">' + esc(TO) + '</a> · <a href="' + SITE + '" style="color:' + C.muted + '">www.murith.ch</a>' +
    (o.foot ? '<br><br>' + esc(o.foot) : '') + '</td></tr>' +
    '</table></td></tr></table></body></html>';
}

/* E-mail de confirmation envoyé au visiteur */
function visitorMail(lang, kind, name) {
  const t = V[lang] || V.fr, k = t[kind];
  const html = layout({
    lang: lang, title: k.subject, pre: t.pre, foot: t.foot,
    body: btn => '<p style="margin:0 0 18px">' + esc(t.hi(name)) + '</p>' +
      '<h1 style="margin:0 0 16px;font-family:' + SERIF + ';font-size:26px;line-height:1.25;font-weight:normal;color:' + C.head + '">' + esc(k.h) + '</h1>' +
      '<p style="margin:0 0 16px">' + esc(k.p) + '</p>' +
      '<p style="margin:0 0 22px">' + esc(t.urgent) + '</p>' +
      '<p style="margin:0 0 28px">' + btn('tel:' + TEL_HREF, t.call + TEL) + '</p>' +
      '<p style="margin:0;color:' + C.soft + '">' + esc(t.sign) + '<br><b style="color:' + C.head + '">' + esc(t.team) + '</b></p>'
  });
  const text = [t.hi(name), '', k.p, '', t.urgent + ' ' + TEL, '', t.sign, t.team, '', 'A. Murith SA · ' + ADDR + ' · ' + TEL + ' · ' + SITE, '', t.foot].join('\n');
  return { subject: k.subject + ' · Murith', html: html, text: text };
}

/* E-mail de notification pour l'entreprise : toutes les réponses */
function staffMail(o) {
  const phoneField = o.fields.find(f => /t[eé]l|phone|telef/i.test(f.label));
  const phone = phoneField ? phoneField.value.replace(/[^\d+]/g, '') : '';
  const when = new Date().toLocaleString('fr-CH', { timeZone: 'Europe/Zurich', dateStyle: 'full', timeStyle: 'short' });
  const heading = o.kind === 'devis' ? 'Nouvelle demande de devis' : 'Nouveau message';
  const who = o.name || o.email || 'Visiteur';
  const rows = o.fields.map(f => '<tr><td style="padding:9px 14px 9px 0;vertical-align:top;border-bottom:1px solid ' + C.line + ';font-family:' + SANS + ';font-size:13px;color:' + C.muted + ';width:34%">' + esc(f.label) + '</td>' +
    '<td style="padding:9px 0;vertical-align:top;border-bottom:1px solid ' + C.line + ';font-family:' + SANS + ';font-size:15px;color:' + C.ink + ';white-space:pre-wrap">' + esc(f.value) + '</td></tr>').join('');
  const subject = '[murith.ch] ' + heading + ' — ' + who + (o.lang !== 'fr' ? ' [' + o.lang.toUpperCase() + ']' : '');
  const html = layout({
    lang: 'fr', title: subject, pre: heading + ' de ' + who, foot: 'Cet e-mail a été envoyé automatiquement par le site murith.ch. Une confirmation est envoyée au visiteur dans sa langue (' + LANG_NAME[o.lang] + ').',
    body: btn => '<h1 style="margin:0 0 6px;font-family:' + SERIF + ';font-size:26px;line-height:1.25;font-weight:normal;color:' + C.head + '">' + esc(heading) + '</h1>' +
      '<p style="margin:0 0 20px;font-size:14px;color:' + C.muted + '">' + esc(when) + ' · langue du visiteur : <b style="color:' + C.soft + '">' + esc(LANG_NAME[o.lang]) + '</b></p>' +
      '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid ' + C.line + '">' + rows + '</table>' +
      '<p style="margin:26px 0 0">' + (o.email ? btn('mailto:' + o.email + '?subject=' + encodeURIComponent('Re: ' + (o.kind === 'devis' ? 'Votre demande de devis' : 'Votre message') + ' — Murith'), 'Répondre à ' + o.email) : '') +
      (phone ? ' &nbsp; <a href="tel:' + esc(phone) + '" style="display:inline-block;font-family:' + SANS + ';font-size:15px;font-weight:bold;color:' + C.accent + ';text-decoration:none;padding:12px 8px">Appeler ' + esc(phoneField.value) + '</a>' : '') + '</p>' +
      '<p style="margin:20px 0 0;font-size:12px;color:' + C.muted + '">Page : ' + esc(o.page) + '</p>'
  });
  const text = heading + ' — ' + when + '\nLangue du visiteur : ' + LANG_NAME[o.lang] + '\n\n' + o.fields.map(f => f.label + ' : ' + f.value).join('\n') + '\n\nPage : ' + o.page;
  return { subject: subject, html: html, text: text };
}

/* Accepte le site (murith.ch, www.murith.ch) ; les adresses .vercel.app et localhost seulement hors production. */
function originOk(req) {
  const o = req.headers.origin || '';
  if (!o) return true;
  let host; try { host = new URL(o).hostname; } catch (e) { return false; }
  if (host === 'murith.ch' || host === 'www.murith.ch') return true;
  // l'adresse de test du projet (murith-panorama.vercel.app) reste autorisée pour pouvoir tester avant la bascule du domaine
  if (host === 'murith-panorama.vercel.app' || (process.env.VERCEL_PROJECT_PRODUCTION_URL && host === process.env.VERCEL_PROJECT_PRODUCTION_URL)) return true;
  return process.env.VERCEL_ENV !== 'production' && (host.endsWith('.vercel.app') || host === 'localhost');
}

/* Limite simple : 6 envois par adresse IP et par tranche de 10 minutes (par instance, au mieux). */
const hits = new Map();
function limited(req) {
  const ip = String(req.headers['x-forwarded-for'] || (req.socket && req.socket.remoteAddress) || '').split(',')[0].trim() || 'x';
  const now = Date.now(), win = 10 * 60 * 1000, arr = (hits.get(ip) || []).filter(t => now - t < win);
  if (arr.length >= 6) { hits.set(ip, arr); return true; }
  arr.push(now); hits.set(ip, arr);
  if (hits.size > 500) hits.forEach((v, k) => { if (!v.some(t => now - t < win)) hits.delete(k); });
  return false;
}

async function send(payload) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + process.env.RESEND_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!r.ok) throw new Error('Resend ' + r.status + ' ' + (await r.text()));
}

async function handler(req, res) {
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
  if (limited(req)) return res.status(429).json({ ok: false });

  const fields = (Array.isArray(b.fields) ? b.fields : []).slice(0, MAX_FIELDS)
    .map(f => ({ label: oneLine(f && f.label, 80), value: clean(f && f.value, MAX_LEN) }))
    .filter(f => f.label && f.value);
  if (!fields.length) return res.status(400).json({ ok: false });

  const email = oneLine(b.email, 200);
  const emailOk = /^[^\s@<>"]+@[^\s@<>"]+\.[^\s@<>"]{2,}$/.test(email);
  const lang = LANGS.indexOf(b.lang) >= 0 ? b.lang : 'fr';
  const kind = b.kind === 'devis' ? 'devis' : 'contact';
  const name = nameOnly(b.name);

  // 1. notification à l'entreprise : si elle échoue, on renvoie une erreur (le site propose alors la messagerie)
  const staff = staffMail({ fields: fields, email: emailOk ? email : '', name: name, lang: lang, kind: kind, page: oneLine(b.page, 200) });
  try {
    await send(Object.assign({ from: FROM, to: [TO], subject: staff.subject, html: staff.html, text: staff.text }, emailOk ? { reply_to: email } : {}));
  } catch (e) {
    console.error(e);
    return res.status(502).json({ ok: false });
  }

  // 2. confirmation au visiteur : au mieux (la demande est déjà bien reçue par l'entreprise)
  let confirmed = false;
  if (emailOk) {
    const v = visitorMail(lang, kind, name);
    try {
      await send({ from: FROM_VISITOR, to: [email], reply_to: TO, subject: v.subject, html: v.html, text: v.text, headers: { 'Auto-Submitted': 'auto-generated' } });
      confirmed = true;
    } catch (e) { console.error(e); }
  }
  return res.status(200).json({ ok: true, confirmed: confirmed });
}

module.exports = handler;
