# PHASE 2 (suite) — H1 des articles, intro de /formalites, H1 de l'accueil = mot-clé (phrase animée sortie du H1)
import re, os, html, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = ROOT + '/panorama/'
R = lambda t: f'<span class="seo-new">{t}</span>'
LANG = {'fr': '', 'en': 'en/', 'de': 'de/', 'es': 'es/', 'pt': 'pt/'}
LOG = []

# ---- 1. H1 des articles de blog : sans « – Maison Murith », casse normale, sans bourrage ----
POSTS = {
 'post-prevoyance.html': {'fr': "Prévoyance funéraire à Genève : le guide", 'en': "Funeral pre-planning in Geneva: the guide", 'de': "Bestattungsvorsorge in Genf: der Ratgeber", 'es': "Previsión funeraria en Ginebra: la guía", 'pt': "Previdência funerária em Genebra: o guia"},
 'post-rapat.html': {'fr': "Combien coûte un rapatriement de corps ?", 'en': "How much does repatriating a body cost?", 'de': "Was kostet die Rückführung eines Verstorbenen?", 'es': "¿Cuánto cuesta una repatriación de cuerpo?", 'pt': "Quanto custa um repatriamento de corpo?"},
 'post-etapes.html': {'fr': "Décès d'un proche en Suisse : les 10 étapes à suivre", 'en': "Death of a loved one in Switzerland: the 10 steps to follow", 'de': "Todesfall in der Schweiz: die 10 Schritte, die zu befolgen sind", 'es': "Fallecimiento de un familiar en Suiza: los 10 pasos a seguir", 'pt': "Falecimento de um familiar na Suíça: os 10 passos a seguir"},
}
for f, d in POSTS.items():
    for lg, new in d.items():
        p = P + LANG[lg] + f; s = open(p, encoding='utf-8').read()
        m = re.search(r'(<h1[^>]*>)(.*?)(</h1>)', s, re.S)
        old = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', m.group(2))).split())
        if 'seo-new' in m.group(2): continue
        s = s[:m.start()] + m.group(1) + R(html.escape(new, quote=False)) + m.group(3) + s[m.end():]
        s = s.replace(old, new) if old in s else s   # JSON-LD headline, etc.
        open(p, 'w', encoding='utf-8').write(s); LOG.append((f, lg, 'H1', old, new))

# ---- 2. /formalites : l'ancien H1 devient le chapô ----
for lg in LANG:
    p = P + LANG[lg] + 'formalites.html'; s = open(p, encoding='utf-8').read()
    if 'data-v76="lead"' in s: continue
    log = [x for x in json.load(open(ROOT + '/_build/phase2.log.json')) if x[0] == 'formalites.html' and x[1] == lg and x[2] == 'H1']
    if not log: continue
    old = log[0][3]
    m = re.search(r'(<h1[^>]*>.*?</h1>)(?!\s*<p class="lead)', s, re.S)
    if m:
        s = s[:m.end()] + f'<p class="lead" data-v76="lead">{html.escape(old, quote=False)}</p>' + s[m.end():]
        open(p, 'w', encoding='utf-8').write(s); LOG.append(('formalites.html', lg, 'chapô', '—', old))

# ---- 3. Accueil : H1 = mot-clé ; phrase d'accueil animée → <p class="hero-main"> ----
for lg in LANG:
    p = P + LANG[lg] + 'index.html'; s = open(p, encoding='utf-8').read()
    if 'class="hero-main"' in s: continue
    m = re.search(r'<h1><span class="eyebrow">(.*?)</span>(.*?)</h1>', s, re.S)
    if not m: print('!! h1 accueil', lg); continue
    s = s[:m.start()] + f'<h1><span class="eyebrow">{m.group(1)}</span></h1><p class="hero-main">{m.group(2)}</p>' + s[m.end():]
    open(p, 'w', encoding='utf-8').write(s); LOG.append(('index.html', lg, 'H1', 'phrase d\'accueil dans le H1', m.group(1)))

# JS : l'animation cible le <p class="hero-main"> (au lieu de créer un <span> dans le H1)
p = P + 'app.js'; s = open(p, encoding='utf-8').read()
old = "var main = d.createElement('span'); main.className = 'h1-main'; main.setAttribute('aria-live', 'polite');\n  while (eb.nextSibling) main.appendChild(eb.nextSibling); h1.appendChild(main);"
new = "var main = hero.querySelector('.hero-main');\n  if (!main) { main = d.createElement('span'); while (eb.nextSibling) main.appendChild(eb.nextSibling); h1.appendChild(main); }\n  main.classList.add('h1-main'); main.setAttribute('aria-live', 'polite');"
if old in s: open(p, 'w', encoding='utf-8').write(s.replace(old, new)); print('JS ok')
elif 'hero.querySelector(\'.hero-main\')' in s: print('JS déjà fait')
else: print('!! JS introuvable')

css = '''

/* ===== PHASE 2 — accueil : le H1 est le mot-clé ; la phrase d'accueil (animée) est un paragraphe ===== */
html[data-theme="panorama"][data-theme][lang] .hero-pan h1{font-size:var(--fs-xs);line-height:1.4;margin:0;text-shadow:none;letter-spacing:.24em}
html[data-theme="panorama"][data-theme][lang] .hero-pan .hero-main{display:block;margin:0;font-family:var(--font-display);font-weight:var(--display-weight);letter-spacing:var(--display-tracking);text-wrap:balance;color:#fff;font-size:var(--fs-h1);line-height:1.15;max-width:none;text-shadow:0 2px 30px rgba(10,16,40,.35);transition:opacity .38s ease,transform .5s var(--ease)}
html[data-theme="panorama"][data-theme][lang] .hero-pan .hero-main.out{opacity:0;transform:translateY(12px)}
html[data-theme="panorama"][data-theme][lang] .hero-pan .hero-main em{display:block;margin-top:.7em;font-size:var(--fs-h3);line-height:1.5;color:#E2E9F8;font-weight:400;letter-spacing:.005em;white-space:nowrap;max-width:none}
@media(max-width:700px){
  html[data-theme="panorama"][data-theme][lang] .hero-pan .hero-main{font-size:1.5rem;line-height:1.22;margin:0 0 .25em;letter-spacing:0}
  html[data-theme="panorama"][data-theme][lang] .hero-pan .hero-main em{margin-top:.6em;font-size:.88rem;line-height:1.5;white-space:normal;opacity:.88}
}
'''
p = P + 'style.css'; s = open(p, encoding='utf-8').read()
if 'PHASE 2 — accueil' not in s: open(p, 'w', encoding='utf-8').write(s + css); print('CSS ok')
old_log = json.load(open(ROOT + '/_build/phase2.log.json'))
json.dump(old_log + LOG, open(ROOT + '/_build/phase2.log.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(LOG))
