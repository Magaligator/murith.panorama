// Phase 1-F : conversion des JPG référencés en WebP (480/960/1600) + écriture d'un manifeste.
// Usage : node _build/phase1_images.mjs   (sharp est cherché dans le projet voisin)
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const sharp = require(process.env.SHARP_PATH || '/Users/magalitshikudi/Desktop/Murith site new 2026/node_modules/sharp');
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
process.chdir(root);
const WIDTHS = [480, 960, 1600];

function walk(d, out = []) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    if (e.name.startsWith('_') || ['node_modules', '.git', 'img', 'fonts'].includes(e.name)) continue;
    const p = path.join(d, e.name); if (e.isDirectory()) walk(p, out); else if (/\.(html)$/.test(e.name)) out.push(p);
  }
  return out;
}
const refs = new Set();
for (const f of walk('.')) {
  const h = fs.readFileSync(f, 'utf8');
  for (const m of h.matchAll(/(?:src|poster|data-src)="(\/img\/[^"]+\.jpe?g)"/g)) refs.add(m[1]);
  for (const m of h.matchAll(/srcset="([^"]*)"/g)) for (const it of m[1].split(',')) { const u = it.trim().split(/\s+/)[0]; if (/^\/img\/.+\.jpe?g$/.test(u)) refs.add(u); }
}
// le « -m.jpg » (1100 px) est une variante réduite d'une image déjà listée : on part de l'original
const bases = new Set();
for (const r of refs) {
  const mm = r.replace(/-m\.jpg$/, '.jpg');
  bases.add(fs.existsSync('.' + mm) ? mm : r);
}
const manifest = {};
let n = 0, before = 0, after = 0;
for (const b of [...bases].sort()) {
  const src = '.' + b;
  const meta = await sharp(src).metadata();
  const stem = b.replace(/\.jpe?g$/, '');
  const out = [];
  before += fs.statSync(src).size;
  for (const w of WIDTHS) {
    if (w > meta.width && !(out.length === 0)) continue;            // pas d'agrandissement (sauf si l'image est plus petite que 480)
    const ww = Math.min(w, meta.width);
    const file = `${stem}-${w}.webp`;
    await sharp(src).rotate().resize({ width: ww, withoutEnlargement: true }).webp({ quality: w <= 480 ? 72 : 76, effort: 5 }).toFile('.' + file);
    out.push({ file, w: ww }); after += fs.statSync('.' + file).size; n++;
    if (ww === meta.width) break;
  }
  manifest[b] = { width: meta.width, height: meta.height, variants: out };
}
fs.writeFileSync('_build/images-manifest.json', JSON.stringify(manifest, null, 1));
console.log(`${Object.keys(manifest).length} images → ${n} fichiers WebP ; ${(before / 1e6).toFixed(1)} Mo (JPG de référence) → ${(after / 1e6).toFixed(1)} Mo`);
