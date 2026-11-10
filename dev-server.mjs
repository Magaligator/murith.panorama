// Serveur local qui imite Vercel (cleanUrls, trailingSlash:false, redirects de vercel.json, 404.html avec statut 404).
// Usage : node dev-server.mjs [port]
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const port = +process.argv[2] || 3000;
const cfg = JSON.parse(fs.readFileSync(path.join(root, 'vercel.json'), 'utf8'));
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.xml': 'application/xml', '.txt': 'text/plain', '.webmanifest': 'application/manifest+json', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif', '.svg': 'image/svg+xml', '.mp4': 'video/mp4', '.woff2': 'font/woff2', '.pdf': 'application/pdf', '.ico': 'image/x-icon' };

function matchRedirect(p) {
  for (const r of cfg.redirects || []) {
    const re = new RegExp('^' + r.source.replace(/:([a-zA-Z]+)\*/g, '(?<$1>.*)').replace(/:([a-zA-Z]+)/g, '(?<$1>[^/]+)') + '$');
    const m = p.match(re);
    if (m) {
      let dest = r.destination;
      for (const [k, v] of Object.entries(m.groups || {})) dest = dest.replace(':' + k + '*', v).replace(':' + k, v);
      return { to: dest, code: r.permanent === false ? 307 : 308 };
    }
  }
  return null;
}
function file(p) { try { return fs.statSync(p).isFile() ? p : null; } catch { return null; } }
function resolve(p) {
  const rel = decodeURIComponent(p).replace(/^\/+/, '');
  const abs = path.join(root, rel);
  if (!abs.startsWith(root)) return null;
  if (rel === '') return file(path.join(root, 'index.html'));
  if (file(abs) && !abs.endsWith('.html')) return abs;            // asset
  if (abs.endsWith('.html')) return null;                           // cleanUrls : /x.html n'existe pas
  return file(abs + '.html') || file(path.join(abs, 'index.html'));
}
http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  let p = u.pathname;
  // cleanUrls : /x.html -> /x (308) ; trailingSlash:false : /x/ -> /x
  if (p.endsWith('.html')) { const t = p.replace(/\/index\.html$/, '/').replace(/\.html$/, ''); res.writeHead(308, { Location: t || '/' }); return res.end(); }
  if (p.length > 1 && p.endsWith('/')) { res.writeHead(308, { Location: p.slice(0, -1) + u.search }); return res.end(); }
  const rd = matchRedirect(p);
  if (rd) { res.writeHead(rd.code, { Location: rd.to }); return res.end(); }
  const f = resolve(p);
  if (!f) { const nf = file(path.join(root, 'en' === p.split('/')[1] ? 'en/404.html' : '404.html')) || file(path.join(root, '404.html')); res.writeHead(404, { 'Content-Type': types['.html'] }); return res.end(nf ? fs.readFileSync(nf) : 'Not found'); }
  const ext = path.extname(f), type = types[ext] || 'application/octet-stream';
  const long = /^\/(img|fonts)\//.test(p);
  const hdr = { 'Content-Type': type, 'Cache-Control': long ? 'public, max-age=31536000, immutable' : 'public, max-age=0, must-revalidate' };
  const text = /^(text\/|application\/(json|xml|manifest|javascript))/.test(type) || ext === '.webmanifest';
  if (text && /\bgzip\b/.test(req.headers['accept-encoding'] || '')) { hdr['Content-Encoding'] = 'gzip'; hdr['Vary'] = 'Accept-Encoding'; res.writeHead(200, hdr); return fs.createReadStream(f).pipe(zlib.createGzip()).pipe(res); }
  res.writeHead(200, hdr);
  fs.createReadStream(f).pipe(res);
}).listen(port, () => console.log('http://localhost:' + port));
