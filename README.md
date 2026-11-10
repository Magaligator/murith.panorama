# Murith — site de production (design Panorama)

Racine du site : ce dossier (FR) + `en/`, `de/`, `es/`, `pt/`. Hébergement prévu : Vercel (`vercel.json`, URLs propres sans `.html`).

- Tester en local (imite Vercel) : `node dev-server.mjs 3000`
- Contrôle SEO automatique : `node check-seo.mjs` (échoue en cas d'erreur bloquante)
- CSS / JS : éditer `_src/style.css` et `_src/app.js`, puis `node _build/minify.mjs` (génère `style.css` et `app.js`)
- Non déployés (`.vercelignore`) : `_archive-wix/`, `_build/`, `_img-src/` (originaux), documents de suivi SEO

Suivi : `PLAN-SEO-MURITH.md`, `CHANGELOG-SEO.md`, `QUESTIONS-MURITH.md`, `INVENTAIRE-URLS.csv`.
Réalisé par © www.websituation.ch
