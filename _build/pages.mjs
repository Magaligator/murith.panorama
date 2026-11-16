// Génère la copie de prévisualisation GitHub Pages (sous-chemin /murith.panorama/) à partir de la source de production.
// Usage : node _build/pages.mjs <dossier-de-sortie>
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.resolve(process.argv[2] || '');
if (!process.argv[2]) { console.error('Dossier de sortie manquant'); process.exit(1); }
import crypto from 'node:crypto';
const BASE = '/murith.panorama';
const ver = f => crypto.createHash('md5').update(fs.readFileSync(path.join(root, f))).digest('hex').slice(0, 8);
const V = { 'style.css': ver('style.css'), 'app.js': ver('app.js') };
const SKIP = new Set(['.git', '.gitignore', '.vercelignore', '_archive-wix', '_build', '_img-src', '_src', 'node_modules', 'vercel.json', '.DS_Store']);
const SKIP_FILES = /\.(md|csv|mjs)$/;
function walk(src, dst, top) {
  fs.mkdirSync(dst, { recursive: true });
  for (const e of fs.readdirSync(src, { withFileTypes: true })) {
    if (top && (SKIP.has(e.name) || SKIP_FILES.test(e.name))) continue;
    if (e.name === '.DS_Store') continue;
    const s = path.join(src, e.name), d = path.join(dst, e.name);
    if (e.isDirectory()) walk(s, d, false);
    else copy(s, d);
  }
}
function copy(s, d) {
  if (!/\.(html|css|js|webmanifest|xml)$/.test(s)) { fs.copyFileSync(s, d); return; }
  let t = fs.readFileSync(s, 'utf8');
  if (s.endsWith('.xml') || s.endsWith('.webmanifest')) { fs.writeFileSync(d, t); return; }
  if (s.endsWith('.html')) {
    t = t.replace(/(\s(?:href|src|action|poster|data-[a-z-]+)=")\/(?!\/)/g, `$1${BASE}/`)
         .replace(/(\s(?:srcset|imagesrcset)=")([^"]*)"/g, (m, a, v) => a + v.replace(/(^|,\s*)\/(?!\/)/g, `$1${BASE}/`) + '"')
         .replace(/(href|src)="(\/murith\.panorama\/(style\.css|app\.js))"/g, (m, a, u, f) => `${a}="${u}?v=${V[f]}"`)
         .replace(/<meta name="robots" content="[^"]*"\s*\/?>/g, '<meta name="robots" content="noindex,nofollow"/>');
  } else if (s.endsWith('.css')) {
    t = t.replace(/url\((['"]?)\/(?!\/)/g, `url($1${BASE}/`);
  } else if (s.endsWith('.js')) {
    t = t.replace(/(["'])\/(img|fonts|docs|contact|devis|blog|en|de|it|es|pt|obseques|salons|fleurs|cercueils|formalites|conseillers|remerciements|transports-funeraires|prevoyance-funeraire|murith-care-everywhere|notre-histoire)(?=[\/"'?#-])/g, `$1${BASE}/$2`);
  }
  fs.writeFileSync(d, t);
}
walk(root, out, true);
fs.writeFileSync(path.join(out, 'robots.txt'), 'User-agent: *\nDisallow: /\n');
fs.writeFileSync(path.join(out, '.nojekyll'), '');
console.log('Copie GitHub Pages générée dans', out);
