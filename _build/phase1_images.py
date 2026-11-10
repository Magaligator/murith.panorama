# Phase 1-F (suite) : les pages pointent vers les WebP (srcset 480/960/1600) au lieu des JPG
import re, json, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
M = json.load(open('_build/images-manifest.json'))
def base(u):
    b = re.sub(r'-m\.jpg$', '.jpg', u)
    return b if b in M else (u if u in M else None)
def pick(b, maxw=960):
    v = [x for x in M[b]['variants'] if x['w'] <= maxw] or M[b]['variants'][:1]
    return v[-1]['file']
def big(b): return M[b]['variants'][-1]['file']
def srcset(b): return ', '.join(f"{x['file']} {x['w']}w" for x in M[b]['variants'])
n = 0
for f in glob.glob('**/*.html', recursive=True):
    if f.startswith('_'): continue
    s = open(f, encoding='utf-8').read(); o = s
    def img(m):
        t = m.group(0)
        sm = re.search(r'\ssrc="(/img/[^"]+\.jpe?g)"', t)
        if not sm: return t
        b = base(sm.group(1))
        if not b: return t
        t = t.replace(sm.group(0), f' src="{pick(b)}"')
        if re.search(r'\ssrcset="', t): t = re.sub(r'\ssrcset="[^"]*"', f' srcset="{srcset(b)}"', t)
        return t
    s = re.sub(r'<img\b[^>]*>', img, s)
    s = re.sub(r'\bposter="(/img/[^"]+\.jpe?g)"', lambda m: f'poster="{pick(base(m.group(1)))}"' if base(m.group(1)) else m.group(0), s)
    s = re.sub(r'\bdata-src="(/img/[^"]+\.jpe?g)"', lambda m: f'data-src="{big(base(m.group(1)))}"' if base(m.group(1)) else m.group(0), s)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print(n, 'pages mises à jour')
# images encore référencées après réécriture
used = set()
for f in glob.glob('**/*', recursive=True):
    if f.startswith(('_', 'img/', 'fonts/', 'node_modules')) or not os.path.isfile(f) or not f.endswith(('.html', '.css', '.js', '.xml', '.json', '.webmanifest')): continue
    t = open(f, encoding='utf-8', errors='ignore').read()
    used |= set(re.findall(r'/img/[A-Za-z0-9_\-/\.%~]+', t))
json.dump(sorted(used), open('_build/images-used.json', 'w'))
orphans = [u for u in M if u not in used]
print('JPG convertis et plus référencés :', len(orphans))
