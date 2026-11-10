# Questions à confirmer par Murith (liste vivante)

> Alimentée à chaque phase. Rien n'est inventé : tant qu'une réponse manque, la mention [À CONFIRMER PAR MURITH] reste en rouge sur le site.

## Décidé le 10.11.2026
- `/transports-funeraires` : on garde l'URL actuelle (le fichier `transports.html` sera renommé en Phase 1/6).
- `/murith-care-everywhere` : on garde l'URL actuelle (`murith-care.html` sera renommé).
- `/post/pompes-funebres-geneve` : c'est l'article « 10 étapes » déjà présent → 301 vers `/blog/deces-proche-suisse-10-etapes`.
- `/pompes-funebres-geneve` : doublon de la home → 301 vers `/` (recommandation SEO, à confirmer).

## Encore ouvert
1. **Article EN « How much does repatriating a loved one cost? » (27.08.2026)** : à reprendre dans la version anglaise du blog (`/en/blog/…`) ?
2. ~~Page `/produits`~~ : **fusionnée** dans `/obseques` (301) — décision du 10.11.
3. **Blog actuel en `noindex`** : confirmer qu'il doit être indexé dans le nouveau site (c'est ce que prévoit le plan).

## Retours du client à confirmer (10.11)
4. « Notre société perpétue. » : appliqué au bloc « Savoir-faire » de l'accueil (« Située au centre-ville de Genève, notre société perpétue depuis 5 générations… »). C'est notre interprétation : est-ce bien la phrase visée ?
5. « Deux cérémonies ne peuvent pas être pareilles, car deux vies ne sont jamais identiques. » : remplace la phrase « Puisque deux vies ne se ressemblent jamais… » (page Obsèques, panneau Cérémonie). Une phrase voisine dit déjà la même chose (« Il n'y a pas deux cérémonies identiques, parce qu'il n'y a pas deux vies identiques ») : laquelle remplacer ?
6. « Supprimer le Et et remplacer par une virgule » : appliqué tel quel (« …les couleurs qu'il aimait, c'est une manière simple… »). Un deux-points (« : ») serait plus correct en français : à valider.
7. **« privilégeons »** : forme inexistante en français (verbe privilégier → « nous privilégions »). Corrigé en « privilégions » conformément au plan (Phase 1-G) : le client doit être informé.
8. **Essences de bois** (page Obsèques) : l'ancien texte citait « pin, cerisier » et un article cite le « peuplier », absents du catalogue des cercueils. Alignés sur le catalogue (sapin, chêne, frêne, noyer, acajou, fraké). Murith peut-il confirmer que le catalogue est complet ?

## Phase 2 — à confirmer
9. **Check-list « gratuite »** (description de /formalites) : le plan indique « téléchargez notre check-list gratuite ». Les PDF existent dans `docs/` mais la page propose surtout une check-list interactive : confirmer que les PDF sont bien en libre accès et gratuits.
10. **Devis « gratuit »** : le plan titrait « Devis obsèques à Genève gratuit sous 24h ». Le site dit « sans engagement » mais jamais « gratuit » : j'ai écrit « sans engagement ». Le devis est-il gratuit ?
11. **Murith Care Everywhere** : la description du plan était « [À CONFIRMER] ». J'ai rédigé à partir du texte de la page (familles suisses résidant à l'étranger, rapatriement à Genève, obsèques par Murith). À valider.
12. **Appellation « HUG »** dans les descriptions (« face aux HUG ») : on retrouve déjà cette formule sur le site ; OK pour l'utiliser dans les balises ?

## Phase 1 — à confirmer / à décider
13. **Envoi des formulaires (contact et devis)** : aujourd'hui ils ouvrent la messagerie de l'internaute (`mailto:`), donc beaucoup de demandes se perdent. Trois options : (a) fonction serverless Vercel + envoi par e-mail (Resend ou SMTP Infomaniak) ; (b) Formspree (service tiers, plus simple, gratuit jusqu'à un quota) ; (c) SMTP Infomaniak via une fonction Vercel (e-mails murith.ch). Dans tous les cas : message de confirmation et événement de conversion. **Laquelle choisir ?**
14. **Page Facebook** : le lien du site menait à `facebook.com` (aucune page) ; je l'ai retiré. Murith a-t-elle une page Facebook ? URL ?
15. **`sameAs` / fiches externes** : URL de la fiche Google (Google Business Profile), local.ch, search.ch, bestatter.ch, Apple Business, Bing Places.
16. **`priceRange`** (fourchette indicative de prix pour Google) : à fournir ou à ne pas renseigner.
17. **Distinction avec Murith Fribourg (pfmurith.ch)** : formulation validée par Murith (« entreprise genevoise indépendante, sans lien avec… ») avant publication dans les données structurées.
18. **Auteur des articles** : personne (ex. Jean-Marc Murith) ou « A. Murith SA » ? L'archive Wix indique « Magali Murith K » et un pseudonyme ; j'ai mis l'entreprise comme auteur.
19. **Accueils de langue** : `/en`, `/de`, `/es`, `/pt` (sans slash final, car `trailingSlash:false`). OK ?
