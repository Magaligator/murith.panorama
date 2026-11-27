/*! Magali Tshikudi - Websituation | https://www.websituation.ch */
/* consent.js : bannière de consentement et Google Analytics 4. Fichier généré par prepare-bascule.mjs.
   Google Analytics n'est chargé qu'après un clic sur « Accepter » : avant, aucune requête vers Google et aucun cookie.
   Le choix est gardé 12 mois dans le navigateur (localStorage) et modifiable par le lien du pied de page.
   Pour changer d'identifiant : relancer « GA_ID=G-XXXXXXXXXX node prepare-bascule.mjs ». */
(function () {
  var GA_ID = '';
  var T = {"fr":{"h":"Cookies et mesure d'audience","p":"Avec votre accord, nous utilisons Google Analytics pour mesurer l'audience du site et l'améliorer. Rien n'est déposé ni transmis à Google tant que vous n'avez pas accepté.","ok":"Accepter","no":"Refuser","more":"En savoir plus","manage":"Gérer les cookies"},"en":{"h":"Cookies and audience measurement","p":"With your consent, we use Google Analytics to measure and improve the site. Nothing is stored or sent to Google until you accept.","ok":"Accept","no":"Decline","more":"Learn more","manage":"Cookie settings"},"de":{"h":"Cookies und Reichweitenmessung","p":"Mit Ihrer Einwilligung nutzen wir Google Analytics, um die Website zu messen und zu verbessern. Solange Sie nicht zugestimmt haben, wird nichts gespeichert oder an Google übermittelt.","ok":"Akzeptieren","no":"Ablehnen","more":"Mehr erfahren","manage":"Cookie-Einstellungen"},"it":{"h":"Cookie e misurazione dell'audience","p":"Con il vostro consenso usiamo Google Analytics per misurare e migliorare il sito. Finché non accettate, nulla viene salvato né trasmesso a Google.","ok":"Accetta","no":"Rifiuta","more":"Scopri di più","manage":"Gestisci i cookie"},"es":{"h":"Cookies y medición de audiencia","p":"Con su consentimiento, usamos Google Analytics para medir y mejorar el sitio. No se guarda ni se envía nada a Google hasta que usted acepte.","ok":"Aceptar","no":"Rechazar","more":"Más información","manage":"Gestionar cookies"},"pt":{"h":"Cookies e medição de audiência","p":"Com o seu consentimento, usamos o Google Analytics para medir e melhorar o site. Nada é guardado nem enviado à Google enquanto não aceitar.","ok":"Aceitar","no":"Recusar","more":"Saber mais","manage":"Gerir cookies"}};
  if (!/^G-[A-Z0-9]+$/.test(GA_ID)) return;
  var KEY = 'murith-consent', MAX_AGE = 365 * 864e5;
  var lang = (document.documentElement.lang || 'fr').slice(0, 2);
  var t = T[lang] || T.fr;
  var privacy = (lang === 'fr' ? '' : '/' + lang) + '/politique-de-confidentialite';
  var mem = null;
  function read() {
    try { var v = JSON.parse(localStorage.getItem(KEY)); if (v && v.t && Date.now() - v.t < MAX_AGE) return v.a ? 'yes' : 'no'; } catch (e) {}
    if (mem && Date.now() - mem.t < MAX_AGE) return mem.a ? 'yes' : 'no';
    return null;
  }
  function save(a) { mem = { a: a, t: Date.now() }; try { localStorage.setItem(KEY, JSON.stringify(mem)); } catch (e) {} }
  var loaded = false;
  function load() {
    if (loaded) return; loaded = true;
    window['ga-disable-' + GA_ID] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { allow_google_signals: false, allow_ad_personalization_signals: false, cookie_expires: 33696000 });
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }
  function revoke() {
    window['ga-disable-' + GA_ID] = true;
    var host = location.hostname.replace(/^www\./, '');
    document.cookie.split(';').forEach(function (c) {
      var n = c.split('=')[0].trim();
      if (n === '_ga' || n.indexOf('_ga_') === 0) {
        document.cookie = n + '=; Max-Age=0; path=/';
        document.cookie = n + '=; Max-Age=0; path=/; domain=' + host;
        document.cookie = n + '=; Max-Age=0; path=/; domain=.' + host;
      }
    });
  }
  var box = null;
  function close() { if (box && box.parentNode) box.parentNode.removeChild(box); box = null; }
  function choose(a) { save(a); if (a) load(); else revoke(); close(); }
  function open() {
    if (box) return;
    box = document.createElement('div');
    box.className = 'ck-banner';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-labelledby', 'ck-t');
    box.setAttribute('aria-describedby', 'ck-d');
    box.innerHTML = '<div class="ck-in"><div class="ck-tx"><p class="ck-h" id="ck-t">' + t.h + '</p><p id="ck-d">' + t.p + ' <a href="' + privacy + '">' + t.more + '</a></p></div>' +
      '<div class="ck-bt"><button type="button" class="ck-b ck-no">' + t.no + '</button><button type="button" class="ck-b ck-ok">' + t.ok + '</button></div></div>';
    box.querySelector('.ck-no').addEventListener('click', function () { choose(false); });
    box.querySelector('.ck-ok').addEventListener('click', function () { choose(true); });
    document.body.insertBefore(box, document.body.firstChild);
  }
  var CSS = '.ck-banner{position:fixed;left:0;right:0;bottom:0;z-index:2147483000;padding:12px}' +
    '.ck-in{max-width:960px;margin:0 auto;background:var(--surface,#fff);color:var(--ink,#22262E);border:1px solid var(--line-strong,#C3CDE2);border-radius:var(--r-m,16px);box-shadow:0 12px 40px rgba(24,28,35,.2);padding:18px 20px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}' +
    '.ck-tx{flex:1 1 340px;font-size:15px;line-height:1.5}.ck-tx p{margin:0}.ck-h{font-weight:600;color:var(--head,#181C23);margin-bottom:4px!important}' +
    '.ck-tx a{color:var(--accent,#3A5796);text-decoration:underline}' +
    '.ck-bt{display:flex;gap:10px;flex:0 0 auto}' +
    '.ck-b{min-height:46px;min-width:118px;padding:0 22px;border-radius:var(--btn-r,999px);font:inherit;font-weight:500;cursor:pointer;border:1px solid var(--accent,#3A5796);background:var(--accent,#3A5796);color:var(--accent-ink,#fff)}' +
    '.ck-b.ck-no{background:var(--surface,#fff);color:var(--accent,#3A5796)}' +
    '.ck-b:focus-visible,.ck-link:focus-visible{outline:3px solid var(--accent,#3A5796);outline-offset:2px}' +
    '.ck-link{background:none;border:0;padding:0;font:inherit;color:inherit;text-decoration:underline;cursor:pointer}' +
    '@media(max-width:640px){.ck-bt{width:100%}.ck-b{flex:1}}';
  function init() {
    var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
    var fb = document.querySelector('.foot-bot');
    if (fb) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'ck-link'; b.textContent = t.manage;
      b.addEventListener('click', open);
      fb.insertBefore(b, fb.children[1] || null);
    }
    var s = read();
    if (s === null && navigator.globalPrivacyControl === true) { save(false); s = 'no'; }   // signal « Global Privacy Control » = refus
    if (s === 'yes') load(); else if (s === null) open();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
