// Magali Tshikudi - Websituation | https://www.websituation.ch
// Vercel Function : reçoit les formulaires du site (contact et devis) et les envoie par e-mail avec Resend.
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
