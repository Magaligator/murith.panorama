// Minifie _src/style.css et _src/app.js vers style.css et app.js (racine du site). Usage : node _build/minify.mjs
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const esbuild = createRequire(import.meta.url)(process.env.ESBUILD_PATH || 'esbuild');
for (const [src, out, loader] of [['_src/style.css', 'style.css', 'css'], ['_src/app.js', 'app.js', 'js']]) {
  const code = fs.readFileSync(path.join(root, src), 'utf8');
  const r = await esbuild.transform(code, { loader, minify: true, legalComments: 'none', target: loader === 'js' ? 'es2018' : undefined });
  fs.writeFileSync(path.join(root, out), '/*! Magali Tshikudi - Websituation | https://www.websituation.ch */\n' + r.code);
  console.log(`${src} ${(code.length / 1024).toFixed(0)} Ko → ${out} ${(r.code.length / 1024).toFixed(0)} Ko`);
}
