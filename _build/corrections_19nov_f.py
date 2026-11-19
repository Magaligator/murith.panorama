#!/usr/bin/env python3 -I
"""Corrections client du 2026-11-19, partie 6 (6 langues, idempotent) :
 « Permanence téléphonique 24h/24 7J/7 » ajoutée dans les horaires (accueil + contact)."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
L = ['', 'en/', 'de/', 'it/', 'es/', 'pt/']
T = {
 '': "Permanence téléphonique 24h/24 7J/7",
 'en/': "Telephone helpline 24 hours a day, 7 days a week",
 'de/': "Telefonische Rufbereitschaft rund um die Uhr, 7 Tage die Woche",
 'it/': "Permanenza telefonica 24 ore su 24, 7 giorni su 7",
 'es/': "Atención telefónica permanente 24 h/24, 7 días a la semana",
 'pt/': "Atendimento telefónico permanente 24h/24, 7 dias por semana",
}
changed = []; problems = []
HRS = r'(13:30 - 17:30)(?!<br/><b class="h24">)'
for l in L:
    for page in ('index.html', 'contact.html'):
        p = root / f'{l}{page}'
        s = p.read_text(encoding='utf8')
        n, k = re.subn(HRS, lambda m: f'{m.group(1)}<br/><b class="h24">{T[l]}</b>', s)
        if k != 1: problems.append(f'{l}{page} :: {k} occurrence(s)')
        if n != s: p.write_text(n, encoding='utf8'); changed.append(f'{l}{page}')
if __name__ == '__main__':
    print('modifiés :', len(changed)); print('problèmes :', len(problems))
    for x in problems: print('  !', x)
