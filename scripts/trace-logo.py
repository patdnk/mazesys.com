#!/usr/bin/env python3
"""Traces design/mazesys-logo-source.jpg into src/assets/mazesys-logo.svg.

The logo is solid black with straight 45°/90° edges, so: threshold → marching squares
(boundary loops) → Douglas–Peucker simplification. Each loop becomes its own <path> so the
site can draw the maze wall by wall. Pure Python + Pillow; run with `python3 scripts/trace-logo.py`.
"""
from PIL import Image
import math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'design', 'mazesys-logo-source.jpg')
OUT = os.path.join(ROOT, 'src', 'assets', 'mazesys-logo.svg')
SCALE = 2          # trace at 2x for smoother edges
EPSILON = 1.6      # simplification tolerance, in traced pixels

img = Image.open(SRC).convert('L')
w, h = img.size
img = img.crop((8, 8, w - 8, h - 8))   # drop the frame around the source image
img = img.resize((img.width * SCALE, img.height * SCALE), Image.LANCZOS)
W, H = img.size
px = img.load()
ink = [[px[x, y] < 128 for x in range(W)] for y in range(H)]

def filled(x, y):
    return 0 <= x < W and 0 <= y < H and ink[y][x]

# Boundary edges on the pixel-corner lattice, oriented consistently around each ink region:
# for every ink pixel, each side that faces empty space becomes one directed unit edge.
edges = {}
def add(p, q):
    edges.setdefault(p, []).append(q)
for y in range(H):
    row = ink[y]
    for x in range(W):
        if not row[x]:
            continue
        if not filled(x, y - 1): add((x + 1, y), (x, y))          # top, right→left
        if not filled(x - 1, y): add((x, y), (x, y + 1))          # left, top→bottom
        if not filled(x, y + 1): add((x, y + 1), (x + 1, y + 1))  # bottom, left→right
        if not filled(x + 1, y): add((x + 1, y + 1), (x + 1, y))  # right, bottom→top

loops = []
while edges:
    start = next(iter(edges))
    loop, cur = [start], start
    while True:
        nxt = edges[cur].pop()
        if not edges[cur]:
            del edges[cur]
        if nxt == start:
            break
        loop.append(nxt)
        cur = nxt
    if len(loop) > 12:
        loops.append(loop)

def rdp(points, eps):
    if len(points) < 3:
        return points
    (x1, y1), (x2, y2) = points[0], points[-1]
    dx, dy = x2 - x1, y2 - y1
    norm = math.hypot(dx, dy) or 1
    far, idx = 0, 0
    for i in range(1, len(points) - 1):
        x0, y0 = points[i]
        dist = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / norm
        if dist > far:
            far, idx = dist, i
    if far > eps:
        return rdp(points[: idx + 1], eps)[:-1] + rdp(points[idx:], eps)
    return [points[0], points[-1]]

def simplify_closed(loop):
    # Split the ring at its farthest-apart points so RDP has stable anchors.
    i0 = min(range(len(loop)), key=lambda i: (loop[i][0], loop[i][1]))
    ring = loop[i0:] + loop[:i0]
    j = max(range(len(ring)), key=lambda i: (ring[i][0] - ring[0][0]) ** 2 + (ring[i][1] - ring[0][1]) ** 2)
    a = rdp(ring[: j + 1], EPSILON)
    b = rdp(ring[j:] + [ring[0]], EPSILON)
    return a[:-1] + b[:-1]

shapes = []
for loop in loops:
    pts = simplify_closed(loop)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    area = 0.5 * sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    shapes.append({'pts': pts, 'box': (min(xs), min(ys), max(xs), max(ys)), 'area': area})

minx = min(s['box'][0] for s in shapes); miny = min(s['box'][1] for s in shapes)
maxx = max(s['box'][2] for s in shapes); maxy = max(s['box'][3] for s in shapes)
pad = 4

def fmt(v):
    return f"{v / SCALE:.1f}".rstrip('0').rstrip('.')

# The wordmark letters sit in a band below the mark's left and right feet; everything taller is the maze.
mark_height = maxy - miny
def is_letter(s):
    x0, y0, x1, y1 = s['box']
    return (y1 - y0) < mark_height * 0.12 and y0 > miny + mark_height * 0.75

walls = sorted([s for s in shapes if not is_letter(s)], key=lambda s: (s['box'][0], s['box'][1]))
letters = sorted([s for s in shapes if is_letter(s)], key=lambda s: s['box'][0])

def path(s):
    p = s['pts']
    return 'M' + ' L'.join(f"{fmt(x - minx + pad)} {fmt(y - miny + pad)}" for x, y in p) + 'Z'

vw, vh = fmt(maxx - minx + 2 * pad), fmt(maxy - miny + 2 * pad)
lines = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw} {vh}" role="img" aria-label="Mazesys">',
         '  <g class="maze" fill-rule="evenodd">']
lines += [f'    <path class="wall" style="--i:{i}" pathLength="1" d="{path(s)}"/>' for i, s in enumerate(walls)]
lines += ['  </g>', '  <g class="wordmark" fill-rule="evenodd">']
lines += [f'    <path d="{path(s)}"/>' for s in letters]
lines += ['  </g>', '</svg>']
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w').write('\n'.join(lines) + '\n')
print(f"{len(walls)} wall paths, {len(letters)} letter paths, "
      f"{sum(len(s['pts']) for s in shapes)} points, viewBox {vw}x{vh} → {os.path.relpath(OUT, ROOT)}")
