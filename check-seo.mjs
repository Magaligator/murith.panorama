// Contrôle SEO automatique (Phase 1 / Phase 8). Échoue (code 1) si une règle bloquante est violée.
// Usage : node check-seo.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const BASE = 'https://www.murith.ch';
const LANGS = ['fr', 'en', 'de', 'it', 'es', 'pt'];
const cfg = JSON.parse(fs.readFileSync(path.join(root, 'vercel.json'), 'utf8'));
const PENDING = new Set(['/politique-de-confidentialite', '/mentions-legales']);   // pages créées en Phase 5
const errors = [], warns = [];
const err = (f, m) => errors.push(`${f} : ${m}`);
const warn = (f, m) => warns.push(`${f} : ${m}`);

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (['_archive-wix', '_build', 'node_modules', '.git', 'img', 'fonts', 'docs'].includes(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out); else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}
const files = walk(root).map(f => path.relative(root, f).split(path.sep).join('/'));
const urlOf = f => {
  let u = '/' + f.replace(/\.html$/, '').replace(/(^|\/)index$/, '');
  return u === '' ? '/' : u.replace(/\/$/, '') || '/';
};
const known = new Set(files.map(urlOf));
const redirects = (cfg.redirects || []).map(r => r.source);
const exists = u => {
  u = u.split('#')[0].split('?')[0];
  if (known.has(u) || redirects.includes(u)) return true;
  if (u === '' ) return true;
  const abs = path.join(root, decodeURIComponent(u));
  return fs.existsSync(abs) && fs.statSync(abs).isFile();
};
const attr = (tag, a) => (tag.match(new RegExp(`\\b${a}="([^"]*)"`)) || [])[1];

const pages = {};
for (const f of files) {
  const h = fs.readFileSync(path.join(root, f), 'utf8');
  pages[f] = h;
  const u = urlOf(f);
  const is404 = f.endsWith('404.html');
  // robots
  const rb = h.match(/<meta[^>]*name="robots"[^>]*>/);
  const rc = rb ? attr(rb[0], 'content') : '';
  if (is404) { if (!/noindex/.test(rc)) err(f, '404 doit être noindex'); }
  else if (/noindex/.test(rc) || /noindex/.test(h.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<!--[\s\S]*?-->/g, ''))) err(f, 'contient « noindex » (page publique)');
  else if (!/index,follow/.test(rc)) err(f, 'meta robots index,follow absente');
  // title / description
  const t = (h.match(/<title>([\s\S]*?)<\/title>/) || [])[1]?.trim() || '';
  if (!t) err(f, 'title manquant'); else if (t.length > 60) err(f, `title ${t.length} > 60`);
  const dm = h.match(/<meta[^>]*name="description"[^>]*>/); const d = dm ? attr(dm[0], 'content') : '';
  if (!d) err(f, 'description manquante'); else if (d.length < 120 || d.length > 160) err(f, `description ${d.length} hors 120-160`);
  // H1 et hiérarchie
  const heads = [...h.matchAll(/<h([1-6])[\s>]/g)].map(m => +m[1]);
  if (heads.filter(x => x === 1).length !== 1) err(f, `${heads.filter(x => x === 1).length} H1`);
  for (let i = 1; i < heads.length; i++) if (heads[i] - heads[i - 1] > 1) { err(f, `saut de titre h${heads[i - 1]} → h${heads[i]}`); break; }
  // canonical
  const cn = h.match(/<link[^>]*rel="canonical"[^>]*>/);
  const cu = cn ? attr(cn[0], 'href') : '';
  const expected = BASE + (u === '/' ? '/' : u);
  if (!cu) err(f, 'canonical manquant'); else if (cu !== expected) err(f, `canonical ${cu} ≠ ${expected}`);
  const og = h.match(/<meta[^>]*property="og:url"[^>]*>/);
  if (og && attr(og[0], 'content') !== cu) err(f, 'og:url ≠ canonical');
  // lang
  const lg = (h.match(/<html[^>]*\blang="([^"]*)"/) || [])[1];
  const dirLang = ['en', 'de', 'it', 'es', 'pt'].includes(f.split('/')[0]) ? f.split('/')[0] : 'fr';
  if (!lg || lg.slice(0, 2) !== dirLang) err(f, `lang="${lg}" incohérent`);
  // JSON-LD
  for (const m of h.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try { JSON.parse(m[1]); } catch (e) { err(f, 'JSON-LD invalide : ' + e.message); }
  }
  // images
  for (const m of h.matchAll(/<img\b[^>]*>/g)) if (!/\balt="/.test(m[0])) err(f, 'image sans alt : ' + (attr(m[0], 'src') || '?'));
  // liens
  for (const m of h.matchAll(/\b(?:href|src|poster|data-src)="([^"]*)"/g)) {
    const v = m[1];
    if (/github\.io|magaligator|localhost/.test(v)) err(f, 'lien interdit : ' + v);
    if (!v.startsWith('/') || v.startsWith('//')) {
      if (/^[a-z0-9_\-]+\.html(#|$)/i.test(v) || /\.html(#|$)/.test(v) && !/^https?:/.test(v)) err(f, 'lien relatif .html : ' + v);
      continue;
    }
    if (/\.html(#|\?|$)/.test(v)) { err(f, 'URL en .html : ' + v); continue; }
    const p0 = v.split('#')[0].split('?')[0];
    if (!exists(p0)) { if (PENDING.has(p0.replace(/^\/(en|de|it|es|pt)/, ''))) warn(f, 'page à créer (Phase 5) : ' + p0); else err(f, 'lien cassé : ' + v); }
  }
}
// hreflang
for (const [f, h] of Object.entries(pages)) {
  if (f.endsWith('404.html')) continue;
  const alts = [...h.matchAll(/<link[^>]*rel="alternate"[^>]*hreflang="([^"]*)"[^>]*href="([^"]*)"|<link[^>]*hreflang="([^"]*)"[^>]*href="([^"]*)"/g)].map(m => [m[1] || m[3], m[2] || m[4]]);
  const map = Object.fromEntries(alts);
  for (const l of [...LANGS, 'x-default']) if (!map[l]) err(f, 'hreflang manquant : ' + l);
  const self = map[LANGS.find(l => (l === 'fr' ? !['en', 'de', 'it', 'es', 'pt'].includes(f.split('/')[0]) : f.split('/')[0] === l))];
  if (self !== BASE + (urlOf(f) === '/' ? '/' : urlOf(f))) err(f, 'hreflang auto-référent incorrect');
  for (const [l, hu] of alts) {
    const tu = hu.replace(BASE, '') || '/';
    const tf = Object.keys(pages).find(x => urlOf(x) === tu);
    if (!tf) { err(f, `hreflang ${l} → page inexistante ${tu}`); continue; }
    const back = [...pages[tf].matchAll(/hreflang="([^"]*)"[^>]*href="([^"]*)"|href="([^"]*)"[^>]*hreflang="([^"]*)"/g)].map(m => m[2] || m[3]);
    if (!back.includes(BASE + (urlOf(f) === '/' ? '/' : urlOf(f)))) err(f, `hreflang non réciproque avec ${tu}`);
  }
}
// sitemap
const sm = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
for (const m of sm.matchAll(/<loc>([^<]*)<\/loc>/g)) {
  const u = m[1].replace(BASE, '') || '/';
  if (/\.html/.test(u)) err('sitemap.xml', '.html dans ' + u);
  else if (!exists(u)) err('sitemap.xml', 'URL inexistante ' + u);
}
const rt = fs.readFileSync(path.join(root, 'robots.txt'), 'utf8');
if (/Disallow:\s*\/(img|fonts)/.test(rt)) err('robots.txt', 'bloque /img ou /fonts');
if (!/Sitemap: https:\/\/www\.murith\.ch\/sitemap\.xml/.test(rt)) err('robots.txt', 'Sitemap absent');

console.log(`Pages contrôlées : ${files.length}`);
if (warns.length) console.log(`\nAvertissements (${warns.length}, ex. ${warns[0]})`);
if (errors.length) { console.log(`\n${errors.length} ERREUR(S) :`); const seen = new Map(); for (const e of errors) { const k = e.replace(/^[^:]*: /, ''); seen.set(k, (seen.get(k) || 0) + 1); } for (const [k, n] of [...seen].slice(0, 40)) console.log(` - ${k}${n > 1 ? ` (×${n})` : ''}`); process.exit(1); }
console.log('\nOK : 0 erreur');
