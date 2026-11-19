#!/usr/bin/env python3 -I
"""Corrections client du 2026-11-19, partie 8 (idempotent) : retours WhatsApp de Tio Jean Marc.
 - majuscules à « Association Suisse des Services Funéraires » (descriptif du personnel et partout) ;
 - majuscule à « Hôpitaux Universitaires de Genève » (texte des salons / chapelle de la Cluse) ;
 - étape « Sans rencontre » : « si vous préférez une demande à distance sans rencontre »."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
changed = set(); problems = []
pages = [p for p in root.rglob('*.html') if not any(x in p.parts for x in ('_build', '_src', 'node_modules', '_archive-wix', '.git'))]
def lang(p):
    f = p.relative_to(root).parts[0]
    return f if f in ('en', 'de', 'it', 'es', 'pt') else 'fr'

SUBS = {
 'fr': [(r'Association [Ss]uisse des [Ss]ervices [Ff]unéraires', 'Association Suisse des Services Funéraires'),
        (r'Hôpitaux universitaires de Genève', 'Hôpitaux Universitaires de Genève'),
        (r'si vous préférez ne pas venir nous voir,', 'si vous préférez une demande à distance sans rencontre,')],
 'it': [(r'Associazione [Ss]vizzera dei [Ss]ervizi [Ff]unerari', 'Associazione Svizzera dei Servizi Funerari'),
        (r'Ospedali universitari di Ginevra', 'Ospedali Universitari di Ginevra'),
        (r'se preferite non incontrare un consulente,', 'se preferite una richiesta a distanza senza incontro,')],
 'en': [(r'if you would rather not meet an advisor,', 'if you would rather make a remote request without a meeting,')],
 'de': [(r'Wenn Sie lieber kein Gespräch führen möchten,', 'Wenn Sie lieber eine Anfrage aus der Ferne ohne Treffen stellen möchten,')],
 'es': [(r'si prefiere no reunirse con un asesor,', 'si prefiere una solicitud a distancia sin reunión,')],
 'pt': [(r'se preferir não se reunir com um conselheiro,', 'se preferir um pedido à distância sem reunião,')],
}
for p in pages:
    s = p.read_text(encoding='utf8'); n = s
    for a, b in SUBS.get(lang(p), []): n = re.sub(a, b, n)
    if n != s: p.write_text(n, encoding='utf8'); changed.add(str(p.relative_to(root)))
# gabarits des scripts précédents (pour qu'un rejeu ne ré-introduise pas l'ancien texte)
for f in ('corrections_19nov.py', 'corrections_19nov_b.py', 'corrections_19nov_d.py'):
    p = root / '_build' / f; s = p.read_text(encoding='utf8'); n = s
    # remplacements littéraux
    n = n.replace('si vous préférez ne pas venir nous voir,', 'si vous préférez une demande à distance sans rencontre,')
    n = n.replace('if you would rather not meet an advisor,', 'if you would rather make a remote request without a meeting,')
    n = n.replace('Wenn Sie lieber kein Gespräch führen möchten,', 'Wenn Sie lieber eine Anfrage aus der Ferne ohne Treffen stellen möchten,')
    n = n.replace('se preferite non incontrare un consulente,', 'se preferite una richiesta a distanza senza incontro,')
    n = n.replace('si prefiere no reunirse con un asesor,', 'si prefiere una solicitud a distancia sin reunión,')
    n = n.replace('se preferir não se reunir com um conselheiro,', 'se preferir um pedido à distância sem reunião,')
    n = n.replace("Association suisse des services funéraires", "Association Suisse des Services Funéraires")
    n = n.replace("Associazione Svizzera dei servizi funerari", "Associazione Svizzera dei Servizi Funerari")
    if n != s: p.write_text(n, encoding='utf8'); changed.add('_build/' + f)
if __name__ == '__main__':
    print('modifiés :', len(changed), sorted(changed)[:6]); print('problèmes :', len(problems))
