# PLAN D'ACTION SEO — Refonte murith.ch

> **Comment l'utiliser :** placez ce fichier à la racine du projet du nouveau site, ouvrez Claude Code dans ce dossier, puis collez le **prompt de démarrage** ci-dessous. Ensuite, lancez chaque phase l'une après l'autre avec la phrase « Exécute la PHASE X du fichier PLAN-SEO-MURITH.md ». Validez chaque phase avant de passer à la suivante.

Préparé le 10.11.2026 à partir de :
- l'audit du code du nouveau site (dépôt `magaligator/murith.panorama`, version V75) ;
- les données Google Search Console du site actuel (rapport de classement du 19 au 25.05.2026) ;
- le fichier `Finale_Mots_clés_Prio_260529.xlsx` ;
- les 3 backlinks Linkuma commandés en août 2026 ;
- l'analyse des concurrents : Ville de Genève (SPF), Pompes Funèbres Générales (PFG), Other Ways, Everlife.

---

## PROMPT DE DÉMARRAGE (à coller tel quel dans Claude Code)

```
Tu es mon développeur SEO technique pour le site des Pompes funèbres A. Murith SA (www.murith.ch, Genève).
Lis entièrement le fichier PLAN-SEO-MURITH.md et respecte ces règles pendant toute la session :

1. Ne travaille que sur le site actuel (dossier panorama/ + img/ + fonts/). Ne supprime aucun fichier sans me demander.
2. RÈGLE DU TEXTE ROUGE : chaque texte VISIBLE que tu ajoutes ou reformules doit être entouré de
   <span class="seo-new">…</span> (dans une phrase) ou de <div class="seo-new">…</div> (pour un bloc entier).
   Ajoute une seule fois dans style.css : .seo-new{color:#C00000 !important;}
   Les éléments invisibles (title, meta description, alt, JSON-LD, slugs) ne peuvent pas être en rouge :
   note-les dans CHANGELOG-SEO.md sous la forme d'un tableau « Page | Élément | Avant | Après ».
3. N'invente jamais un fait (prix, services, langues parlées, pays desservis, distinctions, nombre d'avis).
   Si une information manque, écris [À CONFIRMER PAR MURITH] en rouge et liste-la dans QUESTIONS-MURITH.md.
4. Ton : sobre, empathique, respectueux du deuil. Pas de bourrage de mots-clés et pas de superlatifs commerciaux.
5. Termine chaque phase par un récapitulatif de ce qui a été modifié, puis attends ma validation.
6. Fais un commit git par phase (message : « SEO Phase X — résumé »).

Commence par la PHASE 0.
```

---

## CONSTATS CLÉS (pour comprendre le plan)

| # | Constat | Impact |
|---|---------|--------|
| 1 | La copie GitHub est en `noindex,nofollow`, **sans balise canonical ni hreflang `<link>`** (le README indique que la version V75 de production les contient). | 🔴 Bloquant au lancement s'il en reste un |
| 2 | Les URLs du site actuel (Wix) sont **sans `.html`** et parfois avec des fautes : `/cerceuils`, `/notrehistoire`, `/prevoyancefuneraire`, `/tranports`, `/post/…`. Le nouveau site utilise `cercueils.html`, `notre-histoire.html`, etc. | 🔴 Sans redirections 301, perte du référencement |
| 3 | Le meilleur article actuel, *« Comprendre le coût d'un enterrement à Genève »* (10 clics/semaine, position 8), **n'existe pas dans le nouveau site**. | 🔴 Trafic perdu |
| 4 | « pompes funèbres genève » (avec accents) : position **5,3** sur la home. « pompes funebres geneve » (sans accents) : position **35,5**. « pompe funebre geneve » : **38**. | 🎯 Objectif n° 1 |
| 5 | Taux de clic très faible sur des requêtes à fort volume : « pompes funèbres murith avis de décès » = 1 346 impressions et **0 clic**, « décès murith » = 532 impressions et 1 clic. Une partie de ces recherches vise **Murith Fribourg (pfmurith.ch)**, une autre entreprise. | 🟠 Confusion de marque |
| 6 | Aucune page « Politique de confidentialité » ni « Mentions légales » dans le nouveau site (le lien pointe vers l'ancienne page Wix). | 🔴 Exigence légale (nLPD) et facteur de confiance |
| 7 | Le formulaire de contact ouvre la messagerie (`mailto`) au lieu d'envoyer le message. | 🟠 Perte de demandes |
| 8 | Le bloc « Sujets d'informations » du pied de page contient 20 liens remplis de mots-clés qui pointent souvent vers la même page (3 vers la home). | 🟠 Sur-optimisation |
| 9 | Les images pèsent 35 Mo au total, dont la vidéo `murith.mp4` (13,6 Mo), et sont en JPG. | 🟠 Vitesse (Core Web Vitals) |
| 10 | Le lien Facebook pointe vers `https://www.facebook.com/` (aucune page). On trouve aussi « privilégeons » (×2) et un « © 2023 ». | 🟡 Détails de qualité |
| 11 | Les 3 backlinks Linkuma utilisent tous l'ancre exacte « pompes funèbres à Genève » sur des blogs français généralistes. | 🟠 Risque pour le profil de liens |
| 12 | Le fichier de mots-clés prévoit des pages au nom des concurrents (`/pfg-geneve/`, `/pompes-funebres-generales-geneve-sa/`, `/service-des-pompes-funèbres…/`), des slugs avec accents et une coquille (« **Pommes** Funèbres »). | ⚠️ À ne pas reproduire (voir Phase 4) |

**Points forts à exploiter :** 135 ans d'histoire, entreprise familiale sur 5 générations, emplacement en centre-ville face aux HUG, chapelle de la Cluse, salons accessibles 24h/24, note Google de 4,8 (40 avis), site en 5 langues (PFG en a 5, les autres moins), FAQ déjà présentes et schéma `FuneralHome` déjà en place.

---

## PHASE 0 — Sauvegarde et inventaire (ne rien modifier)

```
PHASE 0 :
1. Crée une branche git « seo-refonte » et vérifie que le dépôt est propre.
2. Récupère la liste COMPLÈTE des URLs du site actuel www.murith.ch :
   - https://www.murith.ch/sitemap.xml et tous les sous-sitemaps Wix (pages-sitemap.xml, blog-posts-sitemap.xml,
     blog-categories-sitemap.xml, et les versions /en/) ;
   - ajoute ces URLs connues par Search Console même si elles manquent au sitemap :
     /, /notrehistoire, /obseques, /salons, /cerceuils, /fleurs, /formalites, /contact, /prevoyancefuneraire,
     /tranports, /blog, /politique-de-confidentialité, /en, /en/cerceuils,
     /post/comprendre-le-cout-d-un-enterrement-a-geneve-conseils-et-estimation-des-frais
   Si tu ne peux pas accéder au web, crée le fichier et demande-moi de coller l'export « Pages » de Search Console.
3. Pour chaque article de blog actuel, sauvegarde le texte complet dans /_archive-wix/ (titre, H1, texte, date).
4. Produis INVENTAIRE-URLS.csv : ancienne_url | titre actuel | page équivalente dans le nouveau site | action (garder / 301 / à créer).
5. Ne modifie aucune page. Montre-moi l'inventaire.
```

---

## PHASE 1 — Audit et corrections SEO techniques

```
PHASE 1 — fondations techniques. Vérifie et corrige page par page (FR, EN, DE, ES, PT) :

A. INDEXATION
 - meta robots : « index,follow,max-image-preview:large » sur toutes les pages publiques ;
   « noindex,follow » uniquement sur 404.html et devis.html (étape de confirmation, s'il y en a une).
   ⚠️ Ajoute un contrôle automatique (script check-seo.mjs) qui ÉCHOUE si une page publique contient « noindex ».
 - Supprime la redirection meta-refresh du index.html racine du dépôt (maquette uniquement) : en production,
   le contenu de panorama/ devient la racine du site.
 - Vérifie que les chemins ../img/ et ../fonts/ fonctionnent quand panorama/ est à la racine (img/ et fonts/ copiés à la racine).

B. URLS PROPRES (décision : garder les anciennes URLs autant que possible)
 - Passe à des URLs SANS .html (cleanUrls Vercel) : /salons, /fleurs, /formalites, /contact, /obseques, /blog
   sont alors IDENTIQUES aux URLs actuelles, ce qui conserve 100 % de leur historique.
 - Mets à jour TOUS les liens internes, canonicals, hreflang, og:url et sitemap.xml dans ce format sans .html.
 - Pas de slash final sauf pour les dossiers de langue : /en/, /de/, /es/, /pt/.
 - Domaine canonique : https://www.murith.ch (avec www, comme aujourd'hui).

C. BALISES DE BASE (dans chaque <head>)
 - <html lang="fr-CH"> (en, de-CH, es, pt selon le dossier).
 - <link rel="canonical" href="https://www.murith.ch/…"> auto-référent et absolu.
 - <link rel="alternate" hreflang="fr|en|de|es|pt|x-default"> réciproques sur chaque page traduite.
 - <meta name="description"> unique ; og:title, og:description, og:url, og:image, og:locale cohérents par langue
   (og:locale fr_CH, en_GB, de_CH, es_ES, pt_PT).
 - Un seul H1 par page ; hiérarchie H2 → H3 sans saut.
 - favicon + apple-touch-icon + manifest.

D. DONNÉES STRUCTURÉES (JSON-LD)
 - FuneralHome (home) : garder ; ajouter "priceRange", "hasMap" (lien Google Maps),
   "sameAs" (+ fiche Google, local.ch, search.ch, bestatter.ch ; RETIRER le Facebook vide),
   "disambiguatingDescription": "Entreprise genevoise indépendante, sans lien avec les pompes funèbres Murith de Fribourg." [À CONFIRMER PAR MURITH],
   "areaServed" : liste des communes du canton (voir Phase 3).
   ⚠️ Ne pas ajouter d'aggregateRating sur ses propres avis (non éligible en étoiles et contraire aux règles de Google).
 - BreadcrumbList sur toutes les pages internes (déjà présent : à vérifier).
 - Article + author (Person : Jean-Marc Murith, etc.) + datePublished/dateModified sur les articles du blog.
 - Service sur obsèques, prévoyance, transports, salons (déjà présent : à vérifier).
 - FAQPage : garder, mais chaque question ne doit apparaître que sur UNE page
   (les 6 FAQ de la home sont dupliquées sur /obseques : différencie-les).
 - Valide chaque bloc JSON (syntaxe) et liste les erreurs.

E. SITEMAP / ROBOTS
 - sitemap.xml : URLs sans .html, lastmod réel, hreflang xhtml:link, images ; exclure 404 et pages noindex.
 - robots.txt : Allow /, Sitemap: https://www.murith.ch/sitemap.xml ; ne PAS bloquer /img/, /fonts/, *.css, *.js.
 - Ajoute les PDF /docs/checklist-formalites-deces-*.pdf au sitemap s'ils sont utiles et vérifie qu'ils ont un titre PDF.

F. PERFORMANCE (Core Web Vitals)
 - Convertis les images en WebP (et AVIF si possible) avec <picture> + srcset (480/960/1600 px), width/height explicites.
 - Image principale (LCP) de la home : fetchpriority="high", pas de lazy ; toutes les autres en loading="lazy".
 - Vidéo murith.mp4 (13,6 Mo) : poster en WebP, preload="none", chargement au clic ; version compressée < 4 Mo (H.264 720p).
 - Polices : woff2, font-display:swap, preload de la police du titre uniquement.
 - Minifie style.css et app.js ; cache long sur /img, /fonts (voir vercel.json en Phase 6).
 - Objectif Lighthouse mobile : Performance ≥ 90, SEO = 100, Accessibilité ≥ 95.

G. CORRECTIONS DE CONTENU TECHNIQUES
 - « privilégeons » → « privilégions » (×2 sur la home, et partout ailleurs) — en rouge.
 - © 2023 → année courante générée en JS ou © 1888–2026.
 - Lien Facebook : vraie URL de la page ou suppression [À CONFIRMER PAR MURITH].
 - Lien « Politique de confidentialité » : pointer vers la nouvelle page /politique-de-confidentialite (Phase 5).
 - Formulaire de contact : remplacer le mailto par un vrai envoi (fonction serverless Vercel, Formspree
   ou SMTP Infomaniak) avec message de confirmation et événement de conversion. Propose-moi les options avant de coder.
 - Vérifie tous les liens internes et externes (aucun lien cassé ni lien vers magaligator.github.io).

Livrables : rapport AUDIT-TECHNIQUE.md (avant/après), check-seo.mjs, commit.
```

---

## PHASE 2 — Titles, meta descriptions et éléments essentiels

**Règle anti-cannibalisation :** seule la **home** cible « pompes funèbres Genève » en début de title. Les autres pages ciblent leur propre sujet et finissent par « | Murith ». Title ≤ 60 caractères et description de 140 à 155 caractères, avec un bénéfice concret et le téléphone ou « 24h/24 » quand c'est pertinent (pour améliorer le CTR, recommandation n° 3 du rapport SEO).

```
PHASE 2 — applique ces balises (FR). Vérifie la longueur exacte, ajuste si nécessaire
sans perdre le mot-clé principal, puis traduis-les dans les 4 autres langues en gardant le mot-clé local
(EN : funeral director / funeral home Geneva ; DE : Bestattungsinstitut Genf ; ES : funeraria Ginebra ;
PT : agência funerária Genebra). Consigne tout dans CHANGELOG-SEO.md.
```

| Page (nouvelle URL) | Mot-clé principal | Title proposé | Meta description proposée | H1 proposé |
|---|---|---|---|---|
| `/` | pompes funèbres Genève | Pompes funèbres Genève 24h/24 \| Maison Murith depuis 1888 | Pompes funèbres à Genève depuis 1888, face aux HUG. Obsèques, crémation, salons funéraires et rapatriements. Une famille à vos côtés 24h/24 : 022 809 56 00. | Pompes funèbres à Genève depuis 1888 *(sous-titre « Jacques, Philippe, Jean-Marc et Jimmy… » sorti du H1, en `<p>`)* |
| `/obseques` | obsèques Genève | Obsèques à Genève : enterrement et crémation \| Murith | Organiser des obsèques à Genève : inhumation, crémation, cérémonie laïque ou religieuse. Un conseiller dédié et un devis sous 24h. Joignable 24h/24. | Organiser des obsèques à Genève |
| `/formalites` | décès Genève / acte de décès Genève | Décès à Genève : démarches et acte de décès \| Murith | Un décès à Genève ? Déclaration, acte de décès, documents à préparer : téléchargez notre check-list gratuite. Nous nous chargeons des formalités. | Décès à Genève : les démarches à effectuer |
| `/prevoyance-funeraire` | prévoyance funéraire Genève | Prévoyance funéraire à Genève : préparer ses obsèques \| Murith | Préparez vos obsèques de votre vivant à Genève : volontés, cérémonie, financement. La Ville n'accepte plus de prévoyance depuis 2014 : nous vous guidons. | Prévoyance funéraire à Genève |
| `/transports` | rapatriement de corps | Rapatriement de corps depuis Genève \| Pompes funèbres Murith | Rapatriement funéraire depuis Genève vers la Suisse et l'étranger : formalités, consulats, transport aérien ou routier. Organisation rapide, 24h/24. | Rapatriement de corps et transports internationaux |
| `/salons` | salon funéraire Genève / chapelle de la Cluse | Salons funéraires à Genève – Chapelle de la Cluse \| Murith | Salons funéraires privés au centre de Genève, accessibles 24h/24 avec un code, et chapelle de la Cluse jusqu'à 60 personnes pour les cérémonies. | Nos salons funéraires et la chapelle de la Cluse |
| `/cercueils` | cercueil | Cercueils à Genève : modèles et essences de bois \| Murith | Choisissez un cercueil pour une inhumation ou une crémation : chêne, sapin, finitions et capitonnages. Modèles de fabrication européenne, conseil personnalisé. | Nos cercueils |
| `/fleurs` | fleurs enterrement | Fleurs pour enterrement à Genève : gerbes, couronnes \| Murith | Fleurs pour un enterrement à Genève : couronnes, gerbes, coussins et dessus de cercueil, livrés au lieu de la cérémonie. Composez votre arrangement. | Fleurs pour un enterrement à Genève |
| `/contact` | urgence décès Genève | Contact et urgence décès 24h/24 à Genève \| Murith | Un décès vient de survenir ? Appelez le 022 809 56 00, jour et nuit. Boulevard de la Cluse 89, 1205 Genève, face aux HUG. Rendez-vous à domicile possible. | Nous contacter, 24h/24 |
| `/devis` | devis obsèques Genève | Devis obsèques à Genève gratuit sous 24h \| Murith | Recevez gratuitement et sans engagement un devis détaillé pour des obsèques à Genève (crémation ou inhumation), sous 24h. | Demander un devis d'obsèques |
| `/notre-histoire` | Murith Genève (marque) | Notre histoire : la famille Murith à Genève depuis 1888 | Cinq générations de la famille Murith au service des familles genevoises depuis 1888. Découvrez l'histoire de notre maison, boulevard de la Cluse. | Notre histoire depuis 1888 |
| `/conseillers` | conseiller funéraire Genève | Nos conseillers funéraires à Genève \| Murith | Rencontrez les conseillers et maîtres de cérémonie de la Maison Murith, qui vous accompagnent avec écoute à chaque étape des obsèques. | Nos conseillers funéraires |
| `/remerciements` | cartes de remerciements deuil | Cartes de remerciements après un décès \| Murith Genève | Cartes de remerciements et faire-part de deuil personnalisés : modèles, textes et impression pour remercier vos proches après les obsèques. | Cartes de remerciements |
| `/murith-care` | assistance décès à l'étranger | Murith Care Everywhere : assistance décès à l'étranger \| Murith | [À CONFIRMER : décrire précisément le service] | Murith Care Everywhere |
| `/blog` | conseils obsèques Genève | Obsèques et deuil à Genève : guides pratiques \| Murith | Démarches après un décès, coût des obsèques, prévoyance, rapatriement : nos guides pratiques pour les familles genevoises. | Guides et conseils pour les familles |
| `/produits` | — | ⚠️ Page doublon de salons, cercueils et fleurs : fusionner dans une autre page ou passer en `noindex,follow`. | | |

**Autres éléments essentiels à vérifier sur chaque page :**
```
- Texte ALT descriptif sur chaque image (déjà présent : vérifie qu'il décrit l'image ; pas de liste de mots-clés).
- Noms de fichiers images explicites SANS accents : pompes-funebres-geneve-chapelle-cluse.webp, salon-funeraire-geneve.webp…
  (c'est aussi l'endroit naturel pour la variante sans accents « pompes funebres geneve »).
- Fil d'Ariane visible et cohérent avec BreadcrumbList.
- Chaque page interne a au moins 3 liens internes contextuels vers des pages proches (ancres descriptives, pas « en savoir plus »).
- Tel cliquable (tel:+41228095600) visible au-dessus de la ligne de flottaison sur mobile.
- Corrige les H1 des articles de blog : supprime « – Maison Murith » et « – Pompes funèbres Murith SA » du H1,
  utilise la casse normale (« Combien coûte un rapatriement de corps ? »).
```

---

## PHASE 3 — Page d'accueil : viser la 1re place sur « pompes funèbres Genève » (avec et sans accents)

**Réalité du marché :** le site de la Ville (geneve.ch, très forte autorité, obsèques gratuites sous conditions) et PFG (environ 1 500 mots sur la home, page presse, boutique, 5 langues, YouTube) sont les références. Pour les dépasser, il faut trois leviers en même temps : une **home plus complète et plus locale**, la **fiche Google Business Profile** (le « pack local » s'affiche au-dessus des résultats naturels) et des **liens locaux de qualité**. Personne ne peut garantir la 1re place ; l'objectif réaliste est le top 3 naturel et le top 3 du pack local en 3 à 6 mois.

**Variantes à couvrir naturellement :** pompes funèbres Genève · pompes funebres geneve · pompe funèbre Genève · pompes funèbres à Genève · entreprise de pompes funèbres Genève · pompes funèbres Ville de Genève · pompes funèbres canton de Genève · services funéraires Genève · Murith pompes funèbres Genève.
Google rapproche généralement les formes avec et sans accents, mais l'écart mesuré (position 5 contre 35) montre qu'il faut aussi des **signaux sans accents** : noms de fichiers, slugs, ancres des backlinks, description de la fiche Google, annuaires. Dans le texte visible, on garde un français correct (avec accents).

```
PHASE 3 — HOME (index.html FR, puis adaptation EN/DE/ES/PT). Tout ajout ou reformulation est en rouge (.seo-new).

1. HIÉRARCHIE
   H1 : « Pompes funèbres à Genève depuis 1888 » (seul).
   H2 dans cet ordre (reformule les H2 existants, ne supprime pas le contenu émotionnel) :
   - « Votre entreprise de pompes funèbres à Genève, face aux HUG »
   - « Un décès vient de survenir à Genève : que faire ? » (3 étapes courtes + téléphone)
   - « Nos services funéraires à Genève » (obsèques, crémation/inhumation, salons, rapatriement, prévoyance, fleurs)
   - « Pompes funèbres de la Ville de Genève ou entreprise privée : quelle différence ? » (NOUVEAU, voir point 3)
   - « Nous intervenons dans tout le canton de Genève » (NOUVEAU, voir point 4)
   - « Ils nous ont fait confiance » (avis)
   - « Questions fréquentes sur les pompes funèbres à Genève »

2. PREMIER PARAGRAPHE (dans les 100 premiers mots) : y placer « pompes funèbres à Genève », « 24h/24 »,
   « boulevard de la Cluse », « depuis 1888 ». Exemple à valider :
   « Entreprise familiale de pompes funèbres à Genève depuis 1888, la Maison Murith accompagne les familles
   24h/24 et 7j/7 depuis le boulevard de la Cluse, face aux Hôpitaux universitaires de Genève (HUG). »

3. NOUVELLE SECTION « Ville de Genève ou entreprise privée ? » (150-200 mots, factuelle, respectueuse, sans dénigrer) :
   - Le Service des pompes funèbres de la Ville de Genève (créé en 1866) assure gratuitement certaines prestations
     de base aux personnes domiciliées en Ville de Genève, s'il est mandaté directement.
   - Les familles restent libres de choisir l'entreprise de pompes funèbres qu'elles souhaitent.
   - La Ville n'accepte plus de nouvelles prévoyances funéraires depuis 2014.
   - Ce que Murith apporte : conseiller dédié, salons privés 24h/24, chapelle de la Cluse, personnalisation, rapatriement.
   → Lien vers /blog/pompes-funebres-ville-de-geneve-ou-privees (Phase 5).
   Cette section capte les recherches « pompes funèbres ville de genève », « spf genève » et « gratuité obsèques genève »
   SANS créer de page au nom d'un concurrent. Sources : geneve.ch (gratuité des funérailles, FAQ).

4. NOUVELLE SECTION « Tout le canton » : liste de communes en texte (et non en liens creux) :
   Genève (Plainpalais, Jonction, Eaux-Vives, Champel, Pâquis, Servette, Saint-Jean), Carouge, Lancy, Onex,
   Vernier, Meyrin, Thônex, Chêne-Bourg, Chêne-Bougeries, Plan-les-Ouates, Bernex, Versoix, Grand-Saconnex,
   Cologny, Veyrier. Mentionne les lieux réels où Murith intervient : HUG, EMS, centre funéraire de Saint-Georges,
   cimetière des Rois, crématoire de Saint-Georges, églises et temples [À CONFIRMER PAR MURITH].

5. CONFIANCE (E-E-A-T) : chiffres clés (1888, 5 générations, 24h/24), brevet fédéral d'entrepreneur de pompes funèbres
   [À CONFIRMER : qui le détient], autorisation cantonale, langues parlées par l'équipe [À CONFIRMER],
   avis Google (texte et lien, pas d'étoiles en schéma).

6. FAQ HOME (différente de /obseques) — 5 à 6 questions à forte intention, réponses de 40 à 60 mots :
   - Que faire en cas de décès à Genève, la nuit ou le week-end ?
   - Combien coûtent des obsèques à Genève ? (fourchette uniquement si Murith la valide → sinon lien vers le guide des coûts)
   - Peut-on choisir librement ses pompes funèbres à Genève ?
   - Où se recueillir auprès du défunt à Genève ?
   - Crémation ou inhumation à Genève : comment ça se passe ?
   - Le défunt est décédé aux HUG : quelles démarches ?
   Mets à jour le JSON-LD FAQPage en conséquence.

7. Longueur cible : 1 800 à 2 200 mots de texte utile (PFG ≈ 1 500). Les mots-clés doivent rester naturels :
   « pompes funèbres » + « Genève » 6 à 10 fois au maximum dans toute la page.

8. PIED DE PAGE « Sujets d'informations » : remplace les 20 ancres-mots-clés par 8 à 10 liens utiles vers des
   pages DIFFÉRENTES et réelles (obsèques, décès Genève, coût des obsèques, prévoyance, rapatriement, salons,
   avis de décès, crémation). Plus aucun lien du pied de page ne pointe vers la home.
```

---

## PHASE 4 — Stratégie de mots-clés pour toutes les pages

Basée sur votre fichier de priorités, sur les requêtes réelles de Search Console et sur les pages des concurrents.

### 4.1 Mapping « 1 mot-clé principal = 1 page »

| Page | Mot-clé principal (volume/mois) | Mots-clés secondaires | Concurrent à battre |
|---|---|---|---|
| `/` | pompes funèbres genève (390) + pompes funebres geneve (390) | pompe funèbre genève, entreprise pompes funèbres genève, pompes funèbres ville de genève, murith genève | geneve.ch SPF, PFG |
| `/formalites` | **décès genève (2 400)** | acte de décès genève (140), acte de décès (110), déclarer un décès genève, que faire en cas de décès, décès aux HUG | geneve.ch, everlife |
| `/avis-de-deces` *(nouvelle)* | **avis de décès genève (1 300 + 1 000 + 480)** | avis mortuaire genève (390), pompes funèbres murith avis de décès (18 100), avis de décès murith (590), nécrologie genève | hommages.ch, everlife, Tribune de Genève |
| `/obseques` | obsèques genève | enterrement genève, funérailles genève, organisation obsèques, inhumation genève, cérémonie laïque | PFG |
| `/cremation-geneve` *(nouvelle)* | crémation genève | crématoire genève (Saint-Georges), incinération genève, prix crémation suisse, urne funéraire | geneve.ch |
| `/prevoyance-funeraire` | **prévoyance funéraire (1 300)** + prévoyance funéraire genève | contrat obsèques suisse, préparer ses obsèques, dernières volontés | everlife, cassar.ch |
| `/salons` | salon funéraire genève | chapelle de la cluse, funérarium genève (140), centre funéraire (390), maison funéraire, chambre mortuaire | PFG (maison funéraire de Carouge) |
| `/cercueils` | **cercueil (590)** | prix cercueil suisse, cercueil crémation, cercueil en chêne, cercueil écologique | cassar.ch |
| `/fleurs` | fleurs enterrement (140, difficulté 4 ✅) | fleurs deuil, couronne mortuaire, gerbe funéraire, fleurs funérailles genève | fleuristes |
| `/transports` | rapatriement de corps | rapatriement funéraire, transport funéraire, rapatriement corps portugal/espagne/italie/kosovo [selon les pays réellement desservis] | PFG |
| `/blog/cout-obseques-geneve` *(migration)* | **prix enterrement suisse / coût obsèques genève** | prix crémation suisse, combien coûte un enterrement en suisse, prix d'un cercueil | — (aucun concurrent n'affiche de prix : opportunité) |
| `/blog/thanatopraxie` *(nouvelle)* | thanatopracteur suisse (170) | soins de conservation, toilette mortuaire | tdg.ch |
| `/notre-histoire` | murith (5 400), a murith sa (390), murith sa | famille murith, pompes funèbres murith genève | pfmurith.ch (Fribourg) |
| `/remerciements` | cartes de remerciements deuil | faire-part de décès, texte de remerciement condoléances | — |

### 4.2 Décisions par rapport au fichier de mots-clés

```
PHASE 4 — applique le mapping ci-dessus :
- Pour chaque page, intègre le mot-clé principal dans : title, H1, premier paragraphe, au moins un H2, ALT d'une image,
  et l'ancre d'au moins 2 liens internes venant d'autres pages. Ajoute les secondaires dans les H2/H3 et dans la FAQ.
- Enrichis les pages trop courtes (< 700 mots) : cercueils (613), fleurs (690), devis (541), conseillers (577),
  murith-care (662) → objectif 800 à 1 200 mots utiles chacune (tout ajout en rouge).
- NE CRÉE PAS de pages au nom des concurrents (/pfg-geneve, /pompes-funebres-generales-geneve-sa,
  /service-des-pompes-funebres-cimetieres-et-crematoire) : risque juridique (loi contre la concurrence déloyale),
  intention de recherche non correspondante et image dégradée. On capte ces recherches avec la section
  « Ville ou privé ? » (home) et l'article comparatif.
- NE CRÉE PAS une page par variante de mot-clé (/deces-murith, /avis-deces-murith, /murith-pompes-funebres…) :
  ce serait du contenu dupliqué (cannibalisation). Une page forte par sujet suffit.
- Slugs toujours SANS accents, en minuscules et avec des tirets ; aucune coquille (« Pommes » → « Pompes »).
- Liste dans QUESTIONS-MURITH.md tout ce qui doit être confirmé (pays de rapatriement, tarifs, langues, etc.).
```

### 4.3 Problème de marque : Murith Genève ≠ Murith Fribourg
Une grande partie des 18 100 recherches « pompes funèbres murith avis de décès » vient probablement de personnes qui cherchent Murith Fribourg (pfmurith.ch, Bulle et Fribourg). D'où :
```
- Ajoute sur /notre-histoire et /avis-de-deces une phrase claire : « Pompes funèbres A. Murith SA est une entreprise
  genevoise indépendante. Pour les avis de décès des pompes funèbres Murith de Fribourg, consultez pfmurith.ch. » [À CONFIRMER PAR MURITH]
  → l'internaute est orienté, Google comprend qu'il s'agit de deux entités distinctes, et les clics « genevois » vont chez vous.
- Mets « Genève » dans toutes les mentions de marque : « Murith Genève », « A. Murith SA – Genève ».
```

---

## PHASE 5 — Nouvelles pages et contenus à créer (texte en rouge)

```
PHASE 5 — crée ces pages avec le même gabarit que les pages existantes (header, footer, langues, schéma, breadcrumb).
Tout le texte est nouveau, donc entièrement en .seo-new. Commence par le FR, les traductions viendront après validation.

1. /blog/cout-obseques-geneve  ← MIGRATION PRIORITAIRE de l'article Wix
   « Comprendre le coût d'un enterrement à Genève : conseils et estimation des frais ».
   Reprends le texte d'origine depuis /_archive-wix/ (en NOIR, car inchangé), puis ajoute en rouge :
   tableau des postes de coût, inhumation vs crémation, gratuité Ville de Genève (conditions), aides possibles,
   FAQ (« combien coûte un enterrement en Suisse ? », « prix d'une crémation en Suisse ? »).
   Aucun prix inventé : [À CONFIRMER PAR MURITH] pour chaque montant.

2. /avis-de-deces  (avis de décès Genève)
   Option A (recommandée si Murith publie des avis avec l'accord des familles) : liste des avis récents + page par avis.
   Option B : guide « Où publier et consulter un avis de décès à Genève » (Tribune de Genève, hommages.ch),
   avec l'aide de Murith pour la rédaction + phrase de distinction avec Murith Fribourg.
   Demande-moi l'option avant de coder.

3. /cremation-geneve  — déroulement, crématoire de Saint-Georges, délais, urnes, dispersion des cendres
   (autorisée en Suisse hors propriété de tiers), coûts → lien vers le guide des coûts.

4. /blog/pompes-funebres-ville-de-geneve-ou-privees  — comparatif factuel et respectueux, sources geneve.ch.

5. /blog/que-faire-deces-hug  — « Décès aux HUG : les démarches » (Murith est situé en face des HUG :
   avantage de proximité unique). Source : hug.ch/renseignements-pratiques-lors-deces.

6. /blog/thanatopraxie-soins-de-conservation  (« thanatopracteur suisse »).

7. /politique-de-confidentialite  et  /mentions-legales  (nLPD suisse : responsable, finalités, cookies,
   droits, hébergeur Vercel/Infomaniak). Liens dans le pied de page de toutes les langues.

8. Versions PT et ES de /transports : contenu spécifique aux rapatriements vers le Portugal et l'Espagne
   (communautés importantes à Genève) [pays À CONFIRMER] — gros potentiel, aucun concurrent n'y répond bien.

Pour chaque nouvel article : auteur (nom + fonction), date, temps de lecture, sommaire, 3 liens internes
vers les pages services, schéma Article + FAQPage si une FAQ est présente.
```

---

## PHASE 6 — Ne pas perdre le SEO actuel : migration Wix → Vercel + Infomaniak

### 6.1 Table de redirections 301 (minimum connu, à compléter avec l'INVENTAIRE de la Phase 0)

| Ancienne URL (Wix) | Nouvelle URL | Note |
|---|---|---|
| `/` | `/` | identique ✅ (les 3 backlinks Linkuma pointent ici) |
| `/obseques`, `/salons`, `/fleurs`, `/formalites`, `/contact`, `/blog` | identiques | ✅ grâce à cleanUrls |
| `/notrehistoire` | `/notre-histoire` | 301 |
| `/cerceuils` | `/cercueils` | 301 |
| `/prevoyancefuneraire` | `/prevoyance-funeraire` | 301 |
| `/tranports` (avec la faute) | `/transports` | 301 |
| `/post/comprendre-le-cout-d-un-enterrement-a-geneve-conseils-et-estimation-des-frais` | `/blog/cout-obseques-geneve` | 301 — meilleur article |
| `/post/<slug prévoyance>` | `/blog/prevoyance-funeraire-geneve` (actuel post-prevoyance) | 301 |
| `/post/<slug 10 étapes>` | `/blog/deces-proche-suisse-10-etapes` (actuel post-etapes) | 301 |
| `/post/<slug rapatriement>` | `/blog/cout-rapatriement-corps` (actuel post-rapat) | 301 |
| `/politique-de-confidentialit%C3%A9` | `/politique-de-confidentialite` | 301 |
| `/en/cerceuils` | `/en/cercueils` *(ou mieux /en/coffins)* | 301 |
| `/en/<autres pages>` | `/en/…` équivalentes | 301 |
| `/blog/categories/*`, `/blog/page/*`, `/copy-of-*`, autres pages Wix | page la plus proche | 301, jamais vers la home par défaut |
| `*.html` (anciens liens du nouveau site) | version sans .html | automatique avec cleanUrls |

```
PHASE 6 — crée vercel.json à la racine :
{
  "cleanUrls": true,
  "trailingSlash": false,
  "redirects": [ ...une entrée par ligne de la table, "permanent": true... ],
  "headers": [
    { "source": "/(img|fonts)/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] },
    { "source": "/(.*)", "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" } ] }
  ]
}
- Ajoute une redirection murith.ch → www.murith.ch (réglage du domaine dans Vercel).
- Écris test-redirects.mjs qui teste CHAQUE ancienne URL de l'inventaire (code 301 + destination 200, sans chaîne de redirections).
- Vérifie que 404.html renvoie bien un statut 404 (et non 200).
- Renomme post-prevoyance / post-etapes / post-rapat en /blog/<slug-explicite> et mets à jour tous les liens.
```

### 6.2 Check-list de mise en ligne (à faire à la main, dans cet ordre)

**J-14 à J-7 — préparation**
- [ ] Vérifier que Google Search Console est configuré en **propriété de domaine** (vérification par TXT DNS chez Infomaniak) et **exporter** les performances des 16 derniers mois (pages et requêtes) : c'est la référence de comparaison.
- [ ] Exporter la liste des backlinks (Search Console › Liens) et y ajouter les 3 URLs Linkuma.
- [ ] Faire un crawl complet de l'ancien site (Screaming Frog, gratuit jusqu'à 500 URLs) et le garder.
- [ ] Chez Infomaniak, baisser le **TTL DNS** à 300 s pour les enregistrements A/CNAME du site.
- [ ] ⚠️ Noter tous les enregistrements **MX / SPF / DKIM** (e-mail murith@murith.ch) : ils ne doivent **pas** être modifiés.

**J-3 — préproduction sur Vercel**
- [ ] Déployer sur l'URL de prévisualisation Vercel (`*.vercel.app`) : elle doit rester en `noindex` (en-tête `X-Robots-Tag: noindex` sur les domaines `vercel.app` uniquement).
- [ ] Lancer `check-seo.mjs`, `test-redirects.mjs` et Lighthouse mobile.
- [ ] **Retirer le texte rouge** : valider tous les changements avec Murith, puis demander à Claude Code de « supprimer la classe seo-new et la règle CSS ».

**J0 — bascule (de préférence un mardi matin, jamais un vendredi)**
- [ ] Ajouter `www.murith.ch` et `murith.ch` dans Vercel › Domains.
- [ ] Chez Infomaniak : modifier **uniquement** les enregistrements du site (A de `@` → IP Vercel, CNAME `www` → valeur indiquée par Vercel ; utiliser les valeurs affichées par Vercel au moment de la bascule).
- [ ] Vérifier le HTTPS, l'absence de `noindex` en production, les redirections 301 et l'envoi du formulaire.
- [ ] Search Console : soumettre `sitemap.xml` et demander l'indexation de la home et des 10 pages principales.
- [ ] Mettre à jour le site web dans la fiche **Google Business Profile** (avec UTM `?utm_source=gbp&utm_medium=organic`), Bing Places, Apple Business Connect, local.ch, search.ch et bestatter.ch.
- [ ] Ne résilier l'abonnement Wix qu'**après** une sauvegarde complète, et garder les exports.

**J+1 à J+90 — suivi**
- [ ] Chaque jour pendant 2 semaines : Search Console › Pages (erreurs 404 et pages « Explorée, non indexée »). Ajouter une 301 pour chaque 404 venant de l'ancien site.
- [ ] Chaque semaine : comparer clics, impressions et positions avec l'export de référence (une baisse de 10-20 % pendant 2 à 4 semaines est normale ; au-delà, chercher la cause).
- [ ] Garder les redirections **au moins 1 an** (idéalement pour toujours).
- [ ] Suivre les positions de « pompes funèbres genève » / « pompes funebres geneve » / « pompe funèbre genève » chaque semaine (même tableau de bord que le rapport actuel).

---

## PHASE 7 — Ce à quoi vous n'aviez peut-être pas pensé (pour dépasser les concurrents)

1. **Google Business Profile = levier n° 1 pour « pompes funèbres Genève ».** Catégorie principale « Pompes funèbres », description avec « pompes funèbres à Genève depuis 1888 », horaires et mention 24h/24, 20 photos ou plus (chapelle de la Cluse, salons, équipe, façade), une publication par mois, réponse à chaque avis, questions-réponses préremplies.
2. **Campagne d'avis Google.** Vous avez 40 avis, PFG en a 42. Un e-mail ou une carte de remerciement avec QR code envoyé quelques semaines après les obsèques. Objectif : 80 avis en 12 mois. Les mots naturels des familles (« Genève », « obsèques », « cérémonie ») aident aussi le référencement local.
3. **Cohérence du NAP** (nom, adresse, téléphone identiques partout) : local.ch, search.ch, bestatter.ch, neho.ch (qui liste déjà Murith), Moneyhouse, Apple Plans, Bing.
4. **Liens locaux de qualité plutôt que des liens achetés.** Les 3 liens Linkuma ont tous la même ancre exacte sur des blogs français généralistes, ce que Google peut considérer comme un schéma de liens. Pour la suite :
   - varier les ancres (marque « Murith », URL nue, « Maison Murith Genève », et une seule fois sur cinq une ancre de type « pompes funebres geneve ») ;
   - privilégier les liens suisses et pertinents : paroisses et unités pastorales, EMS, Pro Senectute, associations de deuil, communes (pages « en cas de décès »), Tribune de Genève et GHI (article « 5 générations depuis 1888 »), partenaires fleuristes et marbriers, murithprevoyance.ch.
5. **Analyse de la concurrence :**
   - *Ville de Genève (SPF)* : autorité maximale et gratuité, mais page institutionnelle sans conseil ni émotion. Vous gagnez sur l'accompagnement, sans jamais dénigrer.
   - *PFG (Carouge)* : longue home rédigée (crématoire, cimetières, EMS, Tribune de Genève), presse, boutique, YouTube, 5 langues. → Votre home doit être au moins aussi riche et locale (Phase 3) ; ajoutez une page « Presse / Ils parlent de nous » si des articles existent.
   - *Other Ways (Carouge)* : positionnement cérémonies laïques et personnalisées. → Renforcer le contenu « cérémonie laïque » sur /obseques.
   - *Everlife* : plateforme nationale de prévoyance qui capte « avis de décès genève » et fait de la publicité Google. → Pages /avis-de-deces et /prevoyance-funeraire solides ; envisager une petite campagne Google Ads sur « pompes funèbres genève » pendant les 4 semaines de la migration pour amortir la baisse temporaire.
6. **Transparence des prix** : aucun concurrent n'affiche de fourchettes. Une page coûts honnête (« à partir de… », exemples types) répond aux requêtes « prix enterrement », qui génèrent déjà vos meilleurs clics de blog.
7. **Proximité HUG** : vous êtes le seul en face de l'hôpital cantonal. Page « Décès aux HUG » et mention dans la fiche Google.
8. **Mesure** : GA4 ou Plausible (plus simple pour la nLPD, sans bannière lourde) + événements de conversion (clic `tel:`, envoi du formulaire, demande de devis, téléchargement de la check-list PDF) + bannière de consentement si GA4.
9. **murithprevoyance.ch** : vérifier qu'il ne duplique pas les textes de /prevoyance-funeraire (contenu dupliqué entre deux domaines). Liens croisés clairs entre les deux sites.
10. **Multilingue** : les pages PT et ES sont une vraie opportunité (rapatriements, communautés portugaise et espagnole). Elles doivent être traduites par un humain ou relues, et non simplement traduites automatiquement.
11. **Rythme de contenu** : 1 article par mois (démarches, deuil, traditions religieuses à Genève, crémation, droits de succession, aides). Chaque article renvoie vers une page service.
12. **Accessibilité et seniors** : contraste, taille de texte ≥ 16 px, gros bouton « Appeler » sur mobile. Une bonne partie de votre public est âgée, et cela améliore aussi la conversion.

---

## PHASE 8 — Contrôle final avant lancement

```
PHASE 8 — exécute et montre-moi le rapport RAPPORT-FINAL-SEO.md :
- check-seo.mjs : 0 noindex en production, 1 H1/page, title ≤ 60, description 120-160, canonical absolu,
  hreflang réciproques, JSON-LD valide, aucun lien cassé, aucune image sans alt, aucune URL .html dans les liens.
- test-redirects.mjs : 100 % des anciennes URLs en 301 → 200.
- Lighthouse mobile des 5 pages principales.
- Liste des [À CONFIRMER PAR MURITH] restants.
- Puis, uniquement après ma validation écrite : supprime toutes les balises .seo-new (en gardant leur contenu)
  et la règle CSS, puis fais le commit « SEO — version de production ».
```

---

### Indicateurs de succès (à 3 et 6 mois)

| Indicateur | Aujourd'hui (mai 2026) | Objectif 3 mois | Objectif 6 mois |
|---|---|---|---|
| Position « pompes funèbres genève » | 5,3 | ≤ 3 | 1-2 |
| Position « pompes funebres geneve » | 35,5 | ≤ 10 | ≤ 3 |
| Position « pompe funebre geneve » | 38,3 | ≤ 10 | ≤ 5 |
| CTR de la home | 0,86 % | 2 % | 3 % + |
| Clics hebdomadaires sur tout le site | 101 | 150 | 250 |
| Avis Google | 40 (4,8) | 55 | 80 |
