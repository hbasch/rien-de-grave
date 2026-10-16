#!/usr/bin/env python3
"""Build the itch.io package of « Rien de grave »: one ESM bundle (three.js included), self-hosted fonts,
sounds, props and textures, zipped. Usage: python3 tools/build_itch.py <build_dir_with_node_modules>"""
import os, re, shutil, subprocess, sys, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = sys.argv[1]; D = os.path.join(B, 'dist')
shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
html = open(os.path.join(ROOT, 'rien-de-grave.html'), encoding='utf-8').read()
a = html.index('<script type="module">'); b = html.index('</script>', a)
js = html[a + len('<script type="module">'):b].replace('.glb.wasm', '.glb')
open(os.path.join(B, 'src.js'), 'w', encoding='utf-8').write(js)
subprocess.run([os.path.join(B, 'node_modules/.bin/esbuild'), os.path.join(B, 'src.js'), '--bundle', '--format=esm', '--target=es2022', '--minify', '--outfile=' + os.path.join(D, 'game.js')], check=True)
body = html[:a] + '<script type="module" src="game.js"></script>' + html[b + len('</script>'):]
body = re.sub(r'<script type="importmap">.*?</script>', '', body, flags=re.S)
body = re.sub(r'<link rel="(preconnect|stylesheet)"[^>]*>\n?', '', body)
FONTS = [('Atkinson Hyperlegible', 400, 'atkinson-hyperlegible-latin-400-normal'), ('Atkinson Hyperlegible', 700, 'atkinson-hyperlegible-latin-700-normal'),
         ('Caveat', 500, 'caveat-latin-500-normal'), ('Caveat', 700, 'caveat-latin-700-normal'), ('Special Elite', 400, 'special-elite-latin-400-normal')]
os.makedirs(os.path.join(D, 'fonts'))
ff = []
for fam, w, f in FONTS:
    pkg = {'Atkinson Hyperlegible': 'atkinson-hyperlegible', 'Caveat': 'caveat', 'Special Elite': 'special-elite'}[fam]
    shutil.copy(os.path.join(B, 'node_modules/@fontsource', pkg, 'files', f + '.woff2'), os.path.join(D, 'fonts'))
    ff.append(f"@font-face {{ font-family: '{fam}'; font-style: normal; font-weight: {w}; font-display: swap; src: url('fonts/{f}.woff2') format('woff2'); }}")
body = body.replace('<style>', '<style>\n' + '\n'.join(ff) + '\n', 1)
head = '<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="description" content="Rien de grave : un jeu narratif court. Tu es Claire, factrice. Huit ans de tournée dans une petite rue française, après une élection.">\n'
body = re.sub(r'^\s*<title>', head + '<title>', body, count=1)
body = body.replace('</title>', '</title>\n</head>\n<body>', 1) + '\n</body>\n</html>\n'
def ascii_only(h):
    # itch.io peut servir index.html sans charset utf-8 : on rend le fichier 100 % ASCII
    # (entites HTML dans le texte, echappements CSS dans <style>) pour que les accents s'affichent partout.
    css = lambda m: m.group(1) + ''.join('\\%x ' % ord(c) if ord(c) > 127 else c for c in m.group(2)) + m.group(3)
    h = re.sub(r'(<style[^>]*>)(.*?)(</style>)', css, h, flags=re.S)
    return ''.join('&#%d;' % ord(c) if ord(c) > 127 else c for c in h)
body = ascii_only(body)
open(os.path.join(D, 'index.html'), 'w', encoding='utf-8').write(body)
for d in ['sons', 'tex', 'props']:
    os.makedirs(os.path.join(D, d))
    for f in os.listdir(os.path.join(ROOT, d)):
        if d == 'props' and f.startswith('modular'): continue
        if d == 'tex' and f.startswith(('patterned_', 'plastered_wall', 'rough_plaster', 'stone_tiles', 'stone_wall_diff', 'white_plaster_rough_01_diff', 'wood_planks_diff')): continue
        shutil.copy(os.path.join(ROOT, d, f), os.path.join(D, d, f.replace('.glb.wasm', '.glb')))
Z = os.path.join(B, 'rien-de-grave-itch.zip')
if os.path.exists(Z): os.remove(Z)
with zipfile.ZipFile(Z, 'w', zipfile.ZIP_DEFLATED) as z:
    for r, _, fs in os.walk(D):
        for f in fs: p = os.path.join(r, f); z.write(p, os.path.relpath(p, D))
print('ok', Z, os.path.getsize(Z) // 1024, 'KB')
