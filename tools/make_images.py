"""Draws the site's icons and its link-preview picture (assets/og.png).

    python tools/make_images.py

Needs Pillow. The lettering is Segoe UI Black (on Windows) and the site's own
Pixelify Sans; with neither to hand it falls back to Pillow's built-in font.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

PAPER, INK = "#efe6d3", "#1a1714"
STRIPES = ["#e8452c", "#f08a1c", "#f2c230", "#2a9d8f", "#2b4a8c"]
LABEL, SHELL, SHELL_2, DARK = "#f6efdf", "#211e1a", "#2e2a25", "#0e0d0b"


def font(names, size):
    for name in names:
        try:
            return ImageFont.truetype(str(name), size)
        except OSError:
            pass
    return ImageFont.load_default(size)


def heavy(size):
    return font(["seguibl.ttf", "C:/Windows/Fonts/seguibl.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], size)


def pixel(size):
    return font([ROOT / "fonts" / "pixelify-sans-latin-600-normal.woff2", "consolab.ttf", "DejaVuSansMono-Bold.ttf"], size)


def icon(size):
    s = 8  # drawn large, then scaled down, for smooth edges
    n = 64 * s
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, n - 1, n - 1), radius=12 * s, fill=INK)
    for i, c in enumerate(STRIPES):
        d.rectangle((0, (44 + 4 * i) * s, n, (48 + 4 * i) * s), fill=c)
    mask = Image.new("L", (n, n), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, n - 1, n - 1), radius=12 * s, fill=255)
    im.putalpha(mask)
    d = ImageDraw.Draw(im)
    d.text((n / 2, 23 * s), "B", font=heavy(46 * s), fill=PAPER, anchor="mm")
    return im.resize((size, size), Image.LANCZOS)


def cassette(scale):
    """The hero's cassette, 600 x 384 before scaling."""
    k = scale
    im = Image.new("RGBA", (600 * k, 384 * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def box(x, y, w, h, r, **kw):
        d.rounded_rectangle((x * k, y * k, (x + w) * k, (y + h) * k), radius=r * k, **kw)

    def dot(x, y, r, **kw):
        d.ellipse(((x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k), **kw)

    box(3, 3, 594, 378, 20, fill=SHELL)
    box(30, 26, 540, 248, 10, fill=LABEL)
    for i, c in enumerate(STRIPES):
        d.rectangle((30 * k, (140 + 15 * i) * k, 570 * k, (155 + 15 * i) * k), fill=c)
    dot(74, 76, 25, fill=INK)
    d.text((74 * k, 75 * k), "B", font=heavy(36 * k), fill=LABEL, anchor="mm")
    d.text((116 * k, 71 * k), "SIDE B LABS", font=heavy(33 * k), fill=INK, anchor="ls")
    d.line((116 * k, 84 * k, 546 * k, 84 * k), fill="#a59f92", width=k)
    d.text((116 * k, 108 * k), "hobby software · 9 tracks", font=pixel(19 * k), fill=INK, anchor="ls")
    d.line((116 * k, 118 * k, 546 * k, 118 * k), fill="#a59f92", width=k)
    d.text((546 * k, 252 * k), "MADE AFTER HOURS", font=pixel(13 * k), fill=INK, anchor="rs")
    box(150, 128, 300, 100, 12, fill=DARK, outline=INK, width=3 * k)
    for x, r in ((212, 40), (388, 30)):
        dot(x, 178, r, fill="#3b2a1e", outline="#5a4433", width=2 * k)
        dot(x, 178, 19, fill=LABEL)
        dot(x, 178, 7, fill=DARK)
    d.polygon([(118 * k, 381 * k), (144 * k, 294 * k), (456 * k, 294 * k), (482 * k, 381 * k)], fill=SHELL_2)
    for x in (226, 374):
        dot(x, 340, 11, fill=DARK)
    for x, y in ((22, 22), (578, 22), (22, 362), (578, 362)):
        dot(x, y, 6, fill=SHELL_2)
    return im


def og():
    s = 2
    w, h = 1200 * s, 630 * s
    im = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(im)
    for i, c in enumerate(STRIPES):
        d.rectangle((0, (540 + 18 * i) * s, w, (558 + 18 * i) * s), fill=c)
    d.rectangle((70 * s, 118 * s, 86 * s, 134 * s), fill=STRIPES[0])
    d.text((100 * s, 127 * s), "HOBBY SOFTWARE LABEL", font=pixel(28 * s), fill="#51483e", anchor="lm")
    d.text((66 * s, 250 * s), "FLIP THE", font=heavy(124 * s), fill=INK, anchor="ls")
    d.text((66 * s, 362 * s), "TAPE.", font=heavy(124 * s), fill=INK, anchor="ls")
    d.text((70 * s, 440 * s), "sideblabs.com", font=pixel(40 * s), fill=INK, anchor="ls")

    tape = cassette(2).rotate(5, resample=Image.BICUBIC, expand=True)
    shadow = Image.new("RGBA", tape.size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 40), mask=tape.getchannel("A"))
    x, y = 640 * s, 96 * s
    tape_w = 500 * s
    tape = tape.resize((tape_w, round(tape.height * tape_w / tape.width)), Image.LANCZOS)
    shadow = shadow.resize(tape.size, Image.LANCZOS)
    im.paste(shadow, (x + 14 * s, y + 16 * s), shadow)
    im.paste(tape, (x, y), tape)
    return im.resize((1200, 630), Image.LANCZOS)


if __name__ == "__main__":
    icon(64).save(ASSETS / "favicon-64.png", optimize=True)
    icon(180).save(ASSETS / "icon-180.png", optimize=True)
    icon(512).save(ASSETS / "icon-512.png", optimize=True)
    og().save(ASSETS / "og.png", optimize=True)
    print("wrote favicon-64.png, icon-180.png, icon-512.png and og.png in", ASSETS)
