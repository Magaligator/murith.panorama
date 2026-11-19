#!/usr/bin/env python3 -I
"""Corrections client du 2026-11-19, partie 3 (6 langues, idempotent) :
 - accueil mobile : « Demander un devis » placé sous « Un décès vient de survenir » ;
 - raccourci « Prévoyance funéraire » (bandeau) sous l'en-tête de chaque page."""
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

# ---- 2) bandeau « Prévoyance funéraire »
T = {  # (titre, sous-titre, lien)
 '': ("Prévoyance funéraire", "Organisez et financez vos obsèques à l'avance", "Préparer ma prévoyance"),
 'en/': ("Funeral pre-planning", "Organise and pay for your funeral in advance", "Prepare my pre-planning"),
 'de/': ("Bestattungsvorsorge", "Organisieren und finanzieren Sie Ihre Bestattung im Voraus", "Meine Vorsorge vorbereiten"),
 'it/': ("Previdenza funeraria", "Organizzate e finanziate in anticipo le vostre esequie", "Preparare la mia previdenza"),
 'es/': ("Previsión funeraria", "Organice y financie sus exequias por adelantado", "Preparar mi previsión"),
 'pt/': ("Previdência funerária", "Organize e financie os seus funerais com antecedência", "Preparar a minha previdência"),
}
ICON = '<svg aria-hidden="true" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24"><path d="M12 3l7 3v5c0 4.500-3 8-7 10-4-2-7-5.500-7-10V6l7-3Z"/><path d="m9 12 2 2 4-4"/></svg>'
ARR = '<svg aria-hidden="true" class="arr" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24"><path d="M4 12h15m-6-6 6 6-6 6"></path></svg>'
PAGES = ['index', 'obseques', 'formalites', 'salons', 'cercueils', 'fleurs', 'conseillers', 'notre-histoire', 'transports-funeraires',
         'murith-care-everywhere', 'remerciements', 'contact']
def strip(s, l):
    if 'class="pv-strip' in s:
        return re.sub(r'<span class="pv-s-go">(?!<span class="pv-s-lbl">)([^<]*)<svg', r'<span class="pv-s-go"><span class="pv-s-lbl">\1</span><svg', s)
    t, sub, go = T[l]
    html = (f'<section class="pv-strip-sec"><div class="container"><a class="pv-strip reveal" href="/{l}prevoyance-funeraire">'
            f'<span class="pv-s-ic">{ICON}</span><span class="pv-s-t"><b>{t}</b><small>{sub}</small></span>'
            f'<span class="pv-s-go"><span class="pv-s-lbl">{go}</span>{ARR}</span></a></div></section>')
    i = s.find('</section>')
    if i < 0: problems.append('pas de section'); return s
    return s[:i + 10] + html + s[i + 10:]
for l in L:
    for p in PAGES: rw(f'{l}{p}.html', lambda s, l=l: strip(s, l))

if __name__ == '__main__':
    print('modifiés :', len(changed)); print('problèmes :', len(problems))
    for p in problems: print('  !', p)
