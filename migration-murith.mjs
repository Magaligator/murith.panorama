#!/usr/bin/env node
// =============================================================================
//  migration-murith.mjs — Migration Wix → Vercel du site murith.ch
//
//  Ce que fait ce fichier (aucune dépendance, Node 18+ suffit) :
//    1. GÉNÈRE vercel.json : URLs propres sans .html, redirections 301 de toutes les
//       anciennes URLs Wix vers le nouveau site, en-têtes de cache et de sécurité,
//       noindex sur les adresses *.vercel.app.
//       (murith.ch → www.murith.ch se règle dans Vercel : Settings → Domains.)
//    2. VÉRIFIE (hors ligne) que chaque destination existe dans le dépôt, qu'il n'y a
//       ni boucle ni chaîne de redirections, que chaque ancienne URL est couverte et
//       que le sitemap.xml ne liste aucune URL qui redirige.
//    3. TESTE (en ligne) un déploiement réel : chaque ancienne URL doit répondre
//       301 puis 200, en une seule étape.
//
//  Utilisation (à la racine du dépôt) :
//    node migration-murith.mjs                  → vérifie + écrit vercel.json
//    node migration-murith.mjs --check          → vérifie seulement, n'écrit rien
//    node migration-murith.mjs --test <URL>     → teste un site en ligne, ex. :
//         node migration-murith.mjs --test https://murith-panorama.vercel.app
//         node migration-murith.mjs --test https://www.murith.ch      (après la bascule)
//         node migration-murith.mjs --test http://localhost:3000      (avec dev-server.mjs)
//    Option --strict : les avertissements font aussi échouer la commande.
//
//  Ce fichier n'est pas déployé (.vercelignore exclut *.mjs).
//  Il peut être relancé autant de fois que nécessaire : il ne casse rien, et il
//  conserve les redirections que vous auriez ajoutées à la main dans vercel.json.
// =============================================================================
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const HOST = 'www.murith.ch';            // domaine canonique (comme dans les canonical et le sitemap)
const APEX = 'murith.ch';

// -----------------------------------------------------------------------------
//  1. TABLE DES REDIRECTIONS — c'est la seule partie à modifier si besoin
//     [ancienne URL Wix, nouvelle URL, (option) URL de repli si la nouvelle n'existe pas encore]
// -----------------------------------------------------------------------------
const REDIRECTS = [
  // --- pages françaises dont l'adresse change
  ['/pompes-funebres-geneve',        '/'],                       // doublon de l'accueil (décision du 10.11)
  ['/notrehistoire',                 '/notre-histoire'],
  ['/cerceuils',                     '/cercueils'],              // faute de frappe connue de Search Console
  ['/tranports',                     '/transports-funeraires'],  // idem
  ['/transports',                    '/transports-funeraires'],
  ['/prevoyancefuneraire',           '/prevoyance-funeraire'],
  ['/produits',                      '/obseques'],               // page fusionnée dans /obseques
  ['/politique-de-confidentialité',  '/politique-de-confidentialite', '/'],   // ⚠ page à créer

  // --- articles de blog (Wix : /post/... → nouveau : /blog/...)
  ['/post/comprendre-le-cout-d-un-enterrement-a-geneve-conseils-et-estimation-des-frais',
                                     '/blog/cout-obseques-geneve', '/blog'], // ⚠ meilleur article, à créer
  ['/post/pompes-funebres-geneve',   '/blog/deces-proche-suisse-10-etapes'],
  ['/post/prevoyance-funeraire-geneve',
                                     '/blog/prevoyance-funeraire-geneve'],
  ['/post/combien-coûte-un-rapatriement-de-corps-maison-murith',
                                     '/blog/cout-rapatriement-corps'],
  ['/post/how-much-does-repatriating-a-loved-one-cost-murith-funeral-services',
                                     '/en/blog/cout-rapatriement-corps'],

  // --- catégories du blog Wix (n'existent plus) → liste des articles
  ['/blog/categories/les-obsèques',          '/blog'],
  ['/blog/categories/repatriation',          '/blog'],
  ['/blog/categories/enterrement',           '/blog'],
  ['/blog/categories/prévoyance-funéraire',  '/blog'],
  ['/blog/categories/coût-d-un-enterrement', '/blog'],

  // --- version anglaise de Wix (/home-1/...) → /en/...
  ['/home-1',                              '/en'],
  ['/home-1/funerals',                     '/en/obseques'],
  ['/home-1/funerallounges',               '/en/salons'],
  ['/home-1/ourcoffins',                   '/en/cercueils'],
  ['/home-1/ourflowers',                   '/en/fleurs'],
  ['/home-1/ourhistory',                   '/en/notre-histoire'],
  ['/home-1/ourproducts',                  '/en/obseques'],
  ['/home-1/formalites-1',                 '/en/formalites'],
  ['/home-1/funeralplanning',              '/en/prevoyance-funeraire'],
  ['/home-1/tranports-1',                  '/en/transports-funeraires'],
  ['/home-1/murith-care-everywhere-en',    '/en/murith-care-everywhere'],
  ['/contact-en',                          '/en/contact'],
  ['/en/cerceuils',                        '/en/cercueils'],
];

// Filets de sécurité : tout ce que Wix pouvait encore servir et que la liste ci-dessus ne cite pas.
// (placés APRÈS les règles précises ; jamais vers l'accueil, toujours vers la page la plus proche)
const WILDCARDS = [
  ['/blog/categories/:path*', '/blog'],
  ['/blog/page/:path*',       '/blog'],
  ['/post/:path*',            '/blog'],
  ['/home-1/:path*',          '/en'],
];

// Toutes les URLs connues de l'ancien site (sitemaps Wix du 24.11.2026 + Search Console).
// Sert au contrôle « aucune ancienne URL n'est oubliée ».
const OLD_URLS = [
  '/', '/obseques', '/salons', '/fleurs', '/formalites', '/contact', '/cercueils', '/blog',
  '/transports-funeraires', '/murith-care-everywhere', '/politique-de-confidentialite',
  '/notrehistoire', '/pompes-funebres-geneve', '/prevoyancefuneraire', '/produits',
  '/cerceuils', '/tranports', '/transports', '/politique-de-confidentialité', '/en', '/en/cerceuils',
  '/home-1', '/home-1/ourproducts', '/home-1/ourhistory', '/home-1/funerals', '/home-1/ourcoffins',
  '/home-1/tranports-1', '/home-1/formalites-1', '/home-1/funeralplanning', '/home-1/ourflowers',
  '/home-1/funerallounges', '/home-1/murith-care-everywhere-en', '/contact-en',
  '/post/comprendre-le-cout-d-un-enterrement-a-geneve-conseils-et-estimation-des-frais',
  '/post/pompes-funebres-geneve', '/post/prevoyance-funeraire-geneve',
  '/post/combien-coûte-un-rapatriement-de-corps-maison-murith',
  '/post/how-much-does-repatriating-a-loved-one-cost-murith-funeral-services',
  '/blog/categories/les-obsèques', '/blog/categories/repatriation', '/blog/categories/enterrement',
  '/blog/categories/prévoyance-funéraire', '/blog/categories/coût-d-un-enterrement',
];

// -----------------------------------------------------------------------------
//  Outils
// -----------------------------------------------------------------------------
const args = process.argv.slice(2);
const CHECK_ONLY = args.includes('--check');
const STRICT = args.includes('--strict');
const testIdx = args.indexOf('--test');
const TEST_URL = testIdx >= 0 ? args[testIdx + 1] : null;

const errors = [], warnings = [], infos = [];
const err = (m) => errors.push(m), warn = (m) => warnings.push(m), info = (m) => infos.push(m);
const dec = (s) => { try { return decodeURIComponent(s); } catch { return s; } };
const norm = (p) => dec(p).normalize('NFC');
const isAscii = (s) => /^[\x00-\x7F]*$/.test(s);

function fileExists(p) { try { return fs.statSync(p).isFile(); } catch { return false; } }
// Une route existe si Vercel (cleanUrls) la servirait : /x → x.html ou x/index.html, ou un fichier exact.
function routeExists(route) {
  const rel = norm(route.split(/[?#]/)[0]).replace(/^\/+/, '').replace(/\/+$/, '');
  if (rel === '') return fileExists(path.join(ROOT, 'index.html'));
  const abs = path.join(ROOT, rel);
  if (!abs.startsWith(ROOT)) return false;
  if (/\.[a-z0-9]{2,5}$/i.test(rel) && !rel.endsWith('.html')) return fileExists(abs);
  return fileExists(abs + '.html') || fileExists(path.join(abs, 'index.html'));
}

// -----------------------------------------------------------------------------
//  2. Construction et vérifications
// -----------------------------------------------------------------------------
function build() {
  const generated = [];            // {source, destination, statusCode}
  const sources = new Map();       // source normalisée → destination

  for (const [from, to, fallback] of REDIRECTS) {
    let dest = to;
    if (!routeExists(to)) {
      if (fallback && routeExists(fallback)) {
        warn(`CIBLE ABSENTE  ${from}  →  ${to}  (page pas encore créée). Repli provisoire vers ${fallback}. Relancez ce script quand la page existera.`);
        dest = fallback;
      } else {
        err(`CIBLE ABSENTE  ${from}  →  ${to}  : cette page n'existe pas dans le dépôt (et aucun repli valable).`);
        continue;
      }
    }
    if (norm(from) === norm(dest)) { err(`BOUCLE  ${from} redirige vers lui-même`); continue; }
    sources.set(norm(from), dest);
    generated.push({ source: from, destination: dest, statusCode: 301 });
    // Variante encodée (%C3%A9) pour les URLs avec accents : on ne sait pas laquelle Vercel compare, on met les deux.
    if (!isAscii(from)) generated.push({ source: encodeURI(from), destination: dest, statusCode: 301 });
  }
  // Chaînes : la destination d'une règle ne doit pas être elle-même redirigée
  for (const [from, dest] of sources) {
    if (sources.has(norm(dest))) err(`CHAÎNE  ${from} → ${dest} → ${sources.get(norm(dest))}  : une seule étape par redirection.`);
  }

  const wild = [];
  for (const [src, to] of WILDCARDS) {
    if (!routeExists(to)) { err(`CIBLE ABSENTE (filet de sécurité)  ${src} → ${to}`); continue; }
    wild.push({ source: src, destination: to, statusCode: 301 });
  }

  // Redirections déjà présentes dans vercel.json et non gérées ici : conservées
  const vpath = path.join(ROOT, 'vercel.json');
  let existing = {};
  try { existing = JSON.parse(fs.readFileSync(vpath, 'utf8')); } catch { /* pas de fichier */ }
  const mineKeys = new Set([...generated, ...wild].map((r) => norm(r.source)));
  const kept = (existing.redirects || []).filter((r) => !mineKeys.has(norm(r.source)));
  if (kept.length) info(`${kept.length} redirection(s) déjà présente(s) dans vercel.json conservée(s) : ${kept.map((r) => r.source).join(', ')}`);

  // murith.ch → www.murith.ch : se règle dans Vercel (Settings → Domains), pas ici,
  // pour que le serveur local dev-server.mjs reste compatible avec ce fichier.

  const headers = [
    { source: '/fonts/(.*)', headers: [{ key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }] },
    { source: '/img/(.*)',   headers: [{ key: 'Cache-Control', value: 'public, max-age=2592000' }] },
    { source: '/(.*)', headers: [
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
        { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains' },
        { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
        { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=(), payment=()' } ] },
    // Les adresses de test *.vercel.app ne doivent JAMAIS être indexées (évite le contenu dupliqué avec murith.ch)
    { source: '/(.*)', has: [{ type: 'host', value: '.*\\.vercel\\.app' }],
      headers: [{ key: 'X-Robots-Tag', value: 'noindex, nofollow' }] },
  ];

  const out = {
    ...existing,
    cleanUrls: true,
    trailingSlash: false,
    redirects: [...generated, ...kept, ...wild],
    headers,
  };
  return { out, sources, vpath };
}

function checkCoverage(sources, redirectsOut) {
  const srcSet = new Set(redirectsOut.map((r) => norm(r.source)));
  let covered = 0, same = 0, todo = 0;
  for (const old of OLD_URLS) {
    if (srcSet.has(norm(old)) || sources.has(norm(old))) { covered++; continue; }
    if (routeExists(old)) { same++; continue; }
    // couvert par un filet de sécurité ?
    const wildOk = WILDCARDS.some(([s]) => old.startsWith(s.replace(':path*', '')));
    if (wildOk) { covered++; warn(`Ancienne URL ${old} : couverte seulement par un filet de sécurité (vers ${WILDCARDS.find(([s]) => old.startsWith(s.replace(':path*', '')))[1]}).`); continue; }
    if (old === '/politique-de-confidentialite') {
      warn(`BLOQUANT AVANT LA BASCULE  ${old} : l'ancienne page légale n'existe pas dans le nouveau site, et le pied de page y pointe déjà (→ 404). À créer (nLPD).`);
      todo++;
      continue;
    }
    err(`ANCIENNE URL NON COUVERTE  ${old} : ni redirection, ni page identique dans le nouveau site.`);
  }
  info(`Anciennes URLs : ${OLD_URLS.length} connues = ${covered} redirigées + ${same} identiques conservées + ${todo} page à créer.`);
}

function checkSitemap(redirectsOut) {
  const sm = path.join(ROOT, 'sitemap.xml');
  if (!fileExists(sm)) { warn('sitemap.xml introuvable.'); return; }
  const xml = fs.readFileSync(sm, 'utf8');
  const locs = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
  const srcSet = new Set(redirectsOut.filter((r) => !r.has && !r.source.includes(':')).map((r) => norm(r.source)));
  let missing = 0, redirecting = 0;
  for (const loc of locs) {
    const u = new URL(loc);
    if (u.host !== HOST) err(`SITEMAP  ${loc} : le domaine n'est pas ${HOST}.`);
    if (srcSet.has(norm(u.pathname))) { err(`SITEMAP  ${loc} : cette URL redirige — un sitemap ne doit lister que des pages qui répondent 200.`); redirecting++; }
    else if (!routeExists(u.pathname)) { err(`SITEMAP  ${loc} : la page n'existe pas dans le dépôt.`); missing++; }
  }
  info(`sitemap.xml : ${locs.length} URLs, ${redirecting} qui redirigent, ${missing} sans page.`);
}

function checkInventaireCsv(sources) {
  const f = path.join(ROOT, 'INVENTAIRE-URLS.csv');
  if (!fileExists(f)) return;
  const rows = fs.readFileSync(f, 'utf8').replace(/^﻿/, '').split(/\r?\n/).slice(1).filter(Boolean);
  for (const line of rows) {
    const c = line.split(';');
    const old = c[0], eq = (c[6] || '').split(' ')[0], action = c[7] || '';
    if (!/301/.test(action)) continue;
    const mine = sources.get(norm(old));
    if (!mine) { if (!routeExists(old)) warn(`INVENTAIRE-URLS.csv : ${old} est marquée « ${action} » mais n'a pas de redirection ici.`); continue; }
    if (eq.startsWith('/') && norm(eq).replace(/\/$/, '') !== norm(mine).replace(/\/$/, '') && !/index/.test(c[6] || '')) {
      info(`Écart avec INVENTAIRE-URLS.csv : ${old}  csv→${eq}  script→${mine}`);
    }
  }
}

// -----------------------------------------------------------------------------
//  3. Test en ligne d'un déploiement
// -----------------------------------------------------------------------------
async function hop(url) {
  const r = await fetch(url, { redirect: 'manual', headers: { 'user-agent': 'migration-murith/1.0' } });
  return { status: r.status, loc: r.headers.get('location'), headers: r.headers, res: r };
}

async function liveTest(base) {
  base = base.replace(/\/+$/, '');
  const host = new URL(base).host;
  const isVercelPreview = host.endsWith('.vercel.app');
  const isLocal = /^(localhost|127\.)/.test(host);
  console.log(`\nTest en ligne sur ${base}   (${isVercelPreview ? 'adresse de test Vercel' : isLocal ? 'serveur local' : 'domaine de production'})\n`);

  const { out } = build();
  const exact = out.redirects.filter((r) => !r.has && !r.source.includes(':') && isAscii(r.source));
  let ok = 0, ko = 0;
  const line = (good, msg) => { console.log(`${good ? '  ✔' : '  ✘'} ${msg}`); good ? ok++ : ko++; };

  console.log('Anciennes URLs → doivent répondre 301/308 puis 200, en une seule étape :');
  for (const [from, to, fb] of REDIRECTS) {
    const expected = out.redirects.find((r) => norm(r.source) === norm(from))?.destination ?? to;
    let r1;
    try { r1 = await hop(base + encodeURI(from)); } catch (e) { line(false, `${from} : site injoignable (${e.cause?.code || e.message})`); continue; }
    if (![301, 308].includes(r1.status)) { line(false, `${from} : attendu 301, reçu ${r1.status}`); continue; }
    const target = new URL(r1.loc, base);
    if (norm(target.pathname) !== norm(expected)) { line(false, `${from} : redirige vers ${target.pathname} au lieu de ${expected}`); continue; }
    const r2 = await hop(target.href);
    if (r2.status >= 300 && r2.status < 400) { line(false, `${from} → ${target.pathname} → ${r2.loc} : chaîne de redirections`); continue; }
    if (r2.status !== 200) { line(false, `${from} → ${target.pathname} : la destination répond ${r2.status}`); continue; }
    line(true, `${from}  →  ${target.pathname}   (${r1.status}, puis 200)`);
  }

  console.log('\nURLs Wix inconnues (filets de sécurité : page la plus proche, jamais un 404) :');
  for (const [pattern, to] of WILDCARDS) {
    const sample = pattern.replace(':path*', 'exemple-inconnu/2');
    const r1 = await hop(base + sample).catch(() => null);
    const good = r1 && [301, 308].includes(r1.status) && new URL(r1.loc, base).pathname === to;
    line(good, `${sample}  →  ${to}${good ? '' : '  (reçu ' + (r1 ? r1.status + ' ' + r1.loc : 'rien') + ')'}`);
  }

  console.log('\nURLs conservées (doivent répondre 200 directement) :');
  for (const p of ['/', '/obseques', '/salons', '/fleurs', '/formalites', '/contact', '/cercueils', '/blog', '/transports-funeraires', '/murith-care-everywhere', '/en', '/de', '/it', '/es', '/pt', '/sitemap.xml', '/robots.txt']) {
    const r = await hop(base + p).catch(() => null);
    line(r && r.status === 200, `${p}${r ? '' : ' (injoignable)'}${r && r.status !== 200 ? '  reçu ' + r.status : ''}`);
  }
  const pc = await hop(base + '/politique-de-confidentialite').catch(() => null);
  line(pc && pc.status === 200, `/politique-de-confidentialite  ${pc ? (pc.status === 200 ? '' : 'reçu ' + pc.status + '  ← page légale à créer') : '(injoignable)'}`);

  console.log('\nURLs propres et erreurs :');
  const h = await hop(base + '/obseques.html').catch(() => null);
  line(h && [301, 308].includes(h.status) && new URL(h.loc, base).pathname === '/obseques', '/obseques.html  →  /obseques (le .html disparaît)');
  const nf = await hop(base + '/cette-page-nexiste-pas').catch(() => null);
  line(nf && nf.status === 404, '/cette-page-nexiste-pas  →  vrai statut 404');

  console.log('\nIndexation :');
  const home = await fetch(base + '/', { headers: { 'user-agent': 'migration-murith/1.0' } }).catch(() => null);
  if (home) {
    const html = await home.text();
    const xrobots = home.headers.get('x-robots-tag') || '';
    const metaNoindex = /<meta[^>]+name=["']robots["'][^>]*noindex/i.test(html);
    const canonical = (html.match(/<link[^>]+rel=["']canonical["'][^>]*href=["']([^"']+)/i) || [])[1];
    if (isVercelPreview) line(/noindex/i.test(xrobots), `adresse de test : en-tête X-Robots-Tag = « ${xrobots || 'absent'} » (doit contenir noindex)`);
    else if (!isLocal) line(!/noindex/i.test(xrobots) && !metaNoindex, `production : aucun noindex (en-tête « ${xrobots || 'absent'} », balise meta ${metaNoindex ? 'PRÉSENTE ✘' : 'absente'})`);
    line(canonical === `https://${HOST}/`, `canonical de l'accueil = ${canonical || 'absent'}`);
  } else line(false, 'accueil injoignable');

  console.log(`\nRésultat : ${ok} ✔  /  ${ko} ✘\n`);
  if (!isLocal && !isVercelPreview) console.log(`À tester à la main sur le domaine : curl -sI http://${APEX}/obseques | grep -i -E "^HTTP|^location"   (doit donner 301 vers https://${HOST}/obseques)\n`);
  process.exit(ko ? 1 : 0);
}

// -----------------------------------------------------------------------------
//  Programme principal
// -----------------------------------------------------------------------------
if (TEST_URL) { await liveTest(TEST_URL); }
else {
  const { out, sources, vpath } = build();
  checkCoverage(sources, out.redirects);
  checkSitemap(out.redirects);
  checkInventaireCsv(sources);

  console.log('\n=== migration-murith : vérifications ===');
  infos.forEach((m) => console.log('  ·', m));
  warnings.forEach((m) => console.log('  ⚠', m));
  errors.forEach((m) => console.log('  ✘', m));

  const json = JSON.stringify(out, null, 2) + '\n';
  const old = fileExists(vpath) ? fs.readFileSync(vpath, 'utf8') : '';
  if (errors.length) {
    console.log(`\n✘ ${errors.length} erreur(s) : vercel.json n'a PAS été modifié. Corrigez, puis relancez.\n`);
    process.exit(1);
  }
  if (CHECK_ONLY) console.log('\n✔ Vérifications terminées (mode --check : rien n\'a été écrit).\n');
  else if (json === old) console.log('\n✔ vercel.json est déjà à jour.\n');
  else { fs.writeFileSync(vpath, json); console.log(`\n✔ vercel.json écrit : ${out.redirects.length} redirections, ${out.headers.length} blocs d'en-têtes.\n`); }
  console.log(`  Prochaine étape : git add vercel.json && git commit -m "Redirections 301 Wix → Vercel" && git push`);
  console.log('  Puis, après le déploiement Vercel :  node migration-murith.mjs --test https://VOTRE-PROJET.vercel.app\n');
  if (warnings.length) console.log(`  ${warnings.length} avertissement(s) ci-dessus : à traiter avant la bascule du domaine.\n`);
  process.exit(STRICT && warnings.length ? 1 : 0);
}
