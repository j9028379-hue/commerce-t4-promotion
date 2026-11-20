"""Comparer chaque image à la livraison identifiée par son empreinte dans la décision du propriétaire."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import cv2
import numpy as np

original, rendered, silent = map(Path, sys.argv[1:])
validation = json.loads(Path('approvals/validation.json').read_text())
assert hashlib.sha256(original.read_bytes()).hexdigest() == validation['mix_final_sha256']
def digest(path, *args):
    return subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0', *args, '-f', 'hash', '-hash', 'sha256', '-'], text=True).strip()
assert digest(original, '-pix_fmt', 'yuv420p') == 'SHA256=' + validation['images_decodees_sha256']
assert digest(rendered, '-c:v', 'copy') == digest(silent, '-c:v', 'copy'), 'Le mix a modifié le flux vidéo'
if digest(rendered, '-pix_fmt', 'yuv420p') == 'SHA256=' + validation['images_decodees_sha256']:
    print('900 images identiques bit pour bit à la livraison approuvée')
else:
    a, b = (cv2.VideoCapture(str(p)) for p in (original, rendered))
    worst = local = 0.
    for i in range(900):
        ok, x = a.read(); other, y = b.read()
        assert ok and other and x.shape == y.shape == (1280, 720, 3), i
        err = cv2.absdiff(x, y)
        mean = float(err.mean()); tile = float(cv2.resize(err.astype('float32'), (18, 32), interpolation=cv2.INTER_AREA).max())
        assert mean <= 1.5 and tile <= 8., (i, mean, tile)
        worst = max(worst, mean); local = max(local, tile)
    assert not a.read()[0] and not b.read()[0]
    print(f'900 images plein cadre conformes ; pire moyenne {worst:.3f}/255, pire zone 40x40 par canal {local:.3f}/255')
