"""Builds fonts/armada-pixel.ttf from the game's own 5x7 pixel font.

    python armada-zero/tools/make_font.py [path/to/ui/pixel_font.gd]

The glyphs are the bitmaps in the game's ui/pixel_font.gd. Each lit pixel becomes a
100-unit square in an 800-unit em (7 rows of glyph and one of spacing), so the type is
sharp at any font-size that is a multiple of 8px. Lowercase letters use the capitals,
as in the game. Needs nothing but Python.
"""
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', '..', 'spaceshooter', 'ui', 'pixel_font.gd')
OUT = os.path.join(HERE, '..', 'fonts', 'armada-pixel.ttf')

U = 100                 # font units per glyph pixel
ROWS, COLS = 7, 5
ADVANCE = 6 * U
EM = 8 * U
ASCENT, DESCENT = ROWS * U, U
NAME = 'Armada Pixel'

# Characters the pages use that the game's font doesn't have, drawn as one it has.
ALIASES = {0x00A0: ' ', 0x2019: "'", 0x2018: "'", 0x201C: '"', 0x201D: '"', 0x2013: '-', 0x2014: '-', 0x00B7: '.'}


def read_glyphs(path):
    text = open(path, encoding='utf-8').read()
    glyphs = {}
    for m in re.finditer(r'^\t"(\\.|[^"\\])":\s*"([01/]+)"', text, re.M):
        key = m.group(1)
        if key.startswith('\\'):
            key = key[1]
        rows = m.group(2).split('/')
        if len(rows) != ROWS or any(len(r) != COLS for r in rows):
            raise SystemExit('unexpected glyph size for %r' % key)
        glyphs[key] = rows
    if 'A' not in glyphs:
        raise SystemExit('no glyphs found in ' + path)
    return glyphs


def rectangles(rows):
    """The lit pixels as rectangles (x0, y0, x1, y1) in font units: runs along a row,
    joined with the same run in the row below."""
    done, open_runs = [], {}
    for r, bits in enumerate(rows):
        runs, x = set(), 0
        while x < COLS:
            if bits[x] == '1':
                x0 = x
                while x < COLS and bits[x] == '1':
                    x += 1
                runs.add((x0, x))
            else:
                x += 1
        for run in list(open_runs):
            if run not in runs:
                done.append(open_runs.pop(run))
        top, bottom = (ROWS - r) * U, (ROWS - r - 1) * U
        for run in runs:
            if run in open_runs:
                open_runs[run][1] = bottom
            else:
                open_runs[run] = [run[0] * U, bottom, run[1] * U, top]
    done.extend(open_runs.values())
    return [tuple(d) for d in done]


def glyph_data(contours):
    """A simple TrueType glyph from closed contours, each a list of (x, y) points."""
    if not contours:
        return b''
    points, ends = [], []
    for c in contours:
        points.extend(c)
        ends.append(len(points) - 1)
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    data = struct.pack('>hhhhh', len(contours), min(xs), min(ys), max(xs), max(ys))
    data += b''.join(struct.pack('>H', e) for e in ends)
    data += struct.pack('>H', 0)                    # no instructions
    data += bytes([1]) * len(points)                # every point on the curve, 16-bit deltas
    last = 0
    for x in xs:
        data += struct.pack('>h', x - last)
        last = x
    last = 0
    for y in ys:
        data += struct.pack('>h', y - last)
        last = y
    return data + b'\0' * (-len(data) % 4)


def box(x0, y0, x1, y1, clockwise=True):
    pts = [(x0, y0), (x0, y1), (x1, y1), (x1, y0)]
    return pts if clockwise else pts[::-1]


def checksum(data):
    data += b'\0' * (-len(data) % 4)
    return sum(struct.unpack('>%dL' % (len(data) // 4), data)) & 0xFFFFFFFF


def build():
    source = read_glyphs(SRC)
    order = [' '] + sorted(k for k in source if k != ' ')

    # Glyph 0 is the box shown for a character the font doesn't have.
    glyphs = [glyph_data([box(0, 0, COLS * U, ROWS * U), box(U, U, (COLS - 1) * U, (ROWS - 1) * U, False)])]
    gid = {}
    for ch in order:
        gid[ch] = len(glyphs)
        glyphs.append(glyph_data([box(*r) for r in rectangles(source[ch])]))

    cmap_pairs = {ord(ch): g for ch, g in gid.items()}
    for ch, g in gid.items():
        if 'A' <= ch <= 'Z':
            cmap_pairs[ord(ch.lower())] = g
    for code, ch in ALIASES.items():
        if ch in gid:
            cmap_pairs[code] = gid[ch]

    # glyf and loca
    glyf, offsets = b'', [0]
    for g in glyphs:
        glyf += g
        offsets.append(len(glyf))
    loca = struct.pack('>%dL' % len(offsets), *offsets)

    n = len(glyphs)
    hmtx = b''.join(struct.pack('>Hh', ADVANCE, 0) for _ in range(n))
    max_points = max((len(g) and struct.unpack('>h', g[:2])[0] * 4) for g in glyphs)
    max_contours = max((len(g) and struct.unpack('>h', g[:2])[0]) for g in glyphs)

    head = struct.pack('>LLLLHHqqhhhhHHhhh', 0x00010000, 0x00010000, 0, 0x5F0F3CF5, 0x000B, EM,
                       3846700800, 3846700800, 0, 0, COLS * U, ROWS * U, 0, 8, 2, 1, 0)
    hhea = struct.pack('>LhhhHhhhhhhhhhhhH', 0x00010000, ASCENT, -DESCENT, 0, ADVANCE, 0, U, COLS * U,
                       1, 0, 0, 0, 0, 0, 0, 0, n)
    maxp = struct.pack('>LH13H', 0x00010000, n, max_points, max_contours, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0)
    os2 = struct.pack('>HhHHH10hh10s4L4sHHHhhhHH2LhhHHH', 3, ADVANCE, 400, 5, 0,
                      4 * U, 4 * U, 0, U, 4 * U, 4 * U, 0, 3 * U, U, 3 * U, 0,
                      bytes([2, 0, 0, 9, 0, 0, 0, 0, 0, 0]), 1, 0, 0, 0, b'SBL ', 0x0040,
                      min(cmap_pairs), min(max(cmap_pairs), 0xFFFF), ASCENT, -DESCENT, 0, ASCENT, DESCENT,
                      1, 0, ROWS * U, ROWS * U, 0, 32, 0)
    post = struct.pack('>LLhhLLLLL', 0x00030000, 0, -U, U, 1, 0, 0, 0, 0)

    # cmap, format 4: one segment per run of codes whose glyphs also run in order
    segments = []
    for code in sorted(cmap_pairs):
        g = cmap_pairs[code]
        if segments and segments[-1][1] + 1 == code and segments[-1][2] + (code - segments[-1][0]) == g:
            segments[-1][1] = code
        else:
            segments.append([code, code, g])
    segments.append([0xFFFF, 0xFFFF, 0])
    count = len(segments)
    search = 2 * (1 << (count.bit_length() - 1))
    sub = struct.pack('>HHHH', count * 2, search, count.bit_length() - 1, count * 2 - search)
    sub += b''.join(struct.pack('>H', s[1]) for s in segments) + struct.pack('>H', 0)
    sub += b''.join(struct.pack('>H', s[0]) for s in segments)
    sub += b''.join(struct.pack('>H', (s[2] - s[0]) & 0xFFFF) for s in segments[:-1]) + struct.pack('>H', 1)
    sub += struct.pack('>%dH' % count, *([0] * count))
    sub = struct.pack('>HHH', 4, len(sub) + 6, 0) + sub
    cmap = struct.pack('>HHHHL', 0, 1, 3, 1, 12) + sub

    # name
    strings = {1: NAME, 2: 'Regular', 3: NAME + ' 1.0', 4: NAME, 5: 'Version 1.0', 6: NAME.replace(' ', '')}
    records, blob = b'', b''
    for name_id in sorted(strings):
        s = strings[name_id].encode('utf-16-be')
        records += struct.pack('>HHHHHH', 3, 1, 0x409, name_id, len(s), len(blob))
        blob += s
    name = struct.pack('>HHH', 0, len(strings), 6 + len(records)) + records + blob

    tables = {'OS/2': os2, 'cmap': cmap, 'glyf': glyf, 'head': head, 'hhea': hhea, 'hmtx': hmtx,
              'loca': loca, 'maxp': maxp, 'name': name, 'post': post}
    tags = sorted(tables)
    count = len(tags)
    search = 16 * (1 << (count.bit_length() - 1))
    font = struct.pack('>LHHHH', 0x00010000, count, search, count.bit_length() - 1, count * 16 - search)
    offset = 12 + 16 * count
    body, head_at = b'', 0
    for tag in tags:
        data = tables[tag]
        if tag == 'head':
            head_at = offset
        font += struct.pack('>4sLLL', tag.encode(), checksum(data), offset, len(data))
        data += b'\0' * (-len(data) % 4)
        body += data
        offset += len(data)
    font += body
    adjust = (0xB1B0AFBA - checksum(font)) & 0xFFFFFFFF
    font = font[:head_at + 8] + struct.pack('>L', adjust) + font[head_at + 12:]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'wb') as f:
        f.write(font)
    print('%s: %d glyphs, %d bytes' % (os.path.relpath(OUT), n, len(font)))


if __name__ == '__main__':
    build()
