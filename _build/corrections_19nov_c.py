#!/usr/bin/env python3 -I
"""Corrections client du 2026-11-19, partie 3 (6 langues, idempotent) :
 accueil mobile : « Demander un devis » placé sous « Un décès vient de survenir »."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
L = ['', 'en/', 'de/', 'it/', 'es/', 'pt/']
changed = set(); problems = []
def rw(path, fn):
    p = root / path
    if not p.exists(): problems.append(f'absent {path}'); return
    s = p.read_text(encoding='utf8'); n = fn(s)
    if n != s: p.write_text(n, encoding='utf8'); changed.add(path)

# ---- 1) devis sous « Un décès vient de survenir »
def hero(s, l):
    if 'class="ph-devis"' in s: return s
    m = re.search(r'<a class="btn btn-ghost btn-devis" href="([^"]*)">([^<]*)</a>', s)
    if not m: problems.append(l + 'index.html :: lien devis introuvable'); return s
    link = f'<a class="ph-devis" href="{m.group(1)}">{m.group(2)}</a>'
    s = s[:m.start()] + s[m.end():]
    j = s.find('class="ph urgent"'); k = s.find('</a>', j) + 4
    if j < 0: problems.append(l + 'index.html :: lien urgent introuvable'); return s
    return s[:k] + link + s[k:]
for l in L: rw(l + 'index.html', lambda s, l=l: hero(s, l))

if __name__ == '__main__':
    print('modifiés :', len(changed)); print('problèmes :', len(problems))
    for p in problems: print('  !', p)
