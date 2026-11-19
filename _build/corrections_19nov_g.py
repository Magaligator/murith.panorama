#!/usr/bin/env python3 -I
"""Corrections client du 2026-11-19, partie 7 (6 langues, idempotent) :
page « Transports internationaux » : la photo de la Mercedes dans la forêt d'automne (celle du mobile)
devient aussi la photo d'en-tête sur ordinateur."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
L = ['', 'en/', 'de/', 'it/', 'es/', 'pt/']
ALT = {
 '': "Corbillard Mercedes de la Maison Murith dans une allée d'automne",
 'en/': "Maison Murith Mercedes hearse on an autumn forest road",
 'de/': "Mercedes-Leichenwagen der Maison Murith auf einem herbstlichen Waldweg",
 'it/': "Carro funebre Mercedes della Maison Murith su un sentiero autunnale",
 'es/': "Coche fúnebre Mercedes de la Maison Murith en un camino de otoño",
 'pt/': "Carro funerário Mercedes da Maison Murith num caminho de outono",
}
changed = []; problems = []
for l in L:
    p = root / f'{l}transports-funeraires.html'
    s = p.read_text(encoding='utf8')
    if '<picture><source media="(max-width:700px)" srcset="/img/transport-mercedes-foret-mobile' not in s:
        if 'src="/img/transport-mercedes-foret-mobile-900.webp"' in s: continue
        problems.append(f'{l}transports-funeraires.html :: bloc photo introuvable'); continue
    img = ('<img alt="%s" class="pan-ph-img" decoding="async" fetchpriority="high" height="1208" '
           'sizes="100vw" src="/img/transport-mercedes-foret-mobile-900.webp" '
           'srcset="/img/transport-mercedes-foret-mobile-480.webp 480w, /img/transport-mercedes-foret-mobile-900.webp 900w, /img/transport-mercedes-foret-mobile-1500.webp 1500w" width="1500"/>' % ALT[l])
    n = re.sub(r'<picture><source media="\(max-width:700px\)".*?</picture>', lambda m: img, s, count=1, flags=re.S)
    if n == s: problems.append(f'{l}transports-funeraires.html :: remplacement'); continue
    p.write_text(n, encoding='utf8'); changed.append(f'{l}transports-funeraires.html')
if __name__ == '__main__':
    print('modifiés :', len(changed), changed); print('problèmes :', len(problems))
    for x in problems: print('  !', x)
