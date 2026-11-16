# Murith — site de production (design Panorama)

Racine du site : ce dossier (FR) + `en/`, `de/`, `es/`, `pt/`. Hébergement prévu : Vercel (`vercel.json`, URLs propres sans `.html`).

- Tester en local (imite Vercel) : `node dev-server.mjs 3000`
- Contrôle SEO automatique : `node check-seo.mjs` (échoue en cas d'erreur bloquante)
- CSS / JS : éditer `_src/style.css` et `_src/app.js`, puis `node _build/minify.mjs` (génère `style.css` et `app.js`)
- Non déployés (`.vercelignore`) : `_archive-wix/`, `_build/`, `_img-src/` (originaux), documents de suivi SEO

Suivi : `PLAN-SEO-MURITH.md`, `CHANGELOG-SEO.md`, `QUESTIONS-MURITH.md`, `INVENTAIRE-URLS.csv`.
Réalisé par © www.websituation.ch

## Dépôt de référence et publication (GitHub Pages)

- Ce dépôt (`main`) est la source de référence du site Murith Panorama.
- GitHub Pages sert la branche `gh-pages`, générée depuis `main` : `node _build/pages.mjs <dossier>` corrige les chemins (`/murith.panorama/…`) et force `noindex`. Pousser le contenu du dossier généré sur `gh-pages`, puis lancer un build Pages.
- Mise en ligne définitive (Vercel ou domaine propre) : déployer `main` tel quel (chemins à la racine, balises SEO d'origine).

## Langues (ordre : FR, EN, DE, IT, ES, PT)

- L'italien (`it/`) est généré depuis les pages françaises : `_build/it/build_it.py` (dictionnaire de traduction `_build/it/it_dict.json`). Après toute modification d'un texte français, ajouter sa traduction dans le dictionnaire puis relancer le script (Python avec `beautifulsoup4`).
- PDF de la check-list : `docs/checklist-formalites-deces-<langue>.pdf`.
