# Side B Labs: the website

The hub for Side B Labs, a hobby software label: one page that lists every project as a track on side B of a tape.

**https://sideblabs.com** (once the domain points here; see [The domain](#the-domain))

It's plain HTML, CSS and a little JavaScript, served as it is by GitHub Pages from the `main` branch: no build step. It loads nothing from other sites (the font, Pixelify Sans, is in `fonts/`, under the SIL Open Font License in `fonts/OFL.txt`), and has no cookies or analytics. The one thing it keeps in the browser is the tape type you chose (Normal or Chrome: the light or the dark colours), in `localStorage`.

- `index.html`: the page. Each project is an `<article class="track">`.
- `css/site.css`: the look. The colours of both tape types are at the top.
- `js/site.js`: the tape type switch, the deck at the bottom that says which track is playing, the tape that winds from one reel to the other as you scroll, and Gremlin's moods. The page works without it.
- `assets/tracks/`: the tracks' pictures.
- `404.html`: the page for an address that isn't there.
- `tools/make_images.py`: draws the icons and the link-preview picture (`assets/og.png`). Run it again if the look changes: `python tools/make_images.py` (it needs Pillow).

## To see it on your own computer

```
python -m http.server 4173
```

and open http://localhost:4173.

## The tracks

A track in `index.html` has:

- `id`: its address on the page (`sideblabs.com/#threadmix`).
- `data-n` and `data-title`: what the deck at the bottom shows while it's playing.
- a class from `a1` to `a5`: which of the five stripes is its colour.
- `<span class="status live">`, `wip` or `soon`: the colour of the square before its status (green, orange or blue). The words are whatever you write.
- an `.art` (a link, if the project has somewhere to go), the `.notes`, the `.tags`, and `.links` if there are any.

The first five are full width. The ones in `<div class="b-grid">` are the smaller ones, two to a row; add `small` to the track's classes there.

To add a project: copy a track, give it the next number, and change the "nine tracks" in the hero, the "9 tracks" under Tracklist and on the cassette's label (`hobby software · 9 tracks`, in the `<svg>` in `index.html` and in `tools/make_images.py`).

**When something comes out:** Robin & Coco and Ensemble Reader say "Coming to Google Play", and have no links yet. When they're live, change the status to `<span class="status live">Released</span>` and add, after the tags:

```html
<p class="links">
  <a class="btn" href="https://play.google.com/store/apps/details?id=...">Google Play</a>
</p>
```

Where the pictures come from:

| Track | Picture | From |
|---|---|---|
| The Last Herald | `last-herald.png` | the game's store screenshots (`last-herald/assets/screens/1-title.png`) |
| The Last Herald 2 | `last-herald-2.webp` | `last-herald-2/shots/title.png` |
| Armada Zero: Firestorm | `armada-zero.png` | a capture of the hangar screen (`spaceshooter/test_output/m4_art`) |
| Robin & Coco | `robin-coco.png` | the Play feature graphic (`watchfaces/store/roomie`) |
| ThreadMix Auto DJ | `threadmix.webp` | the turntable visualizer (`threadmix/assets/shots`) |
| ESP32 projects | `gremlin-moods.png` | Gremlin's 15 moods in a row, 32 x 24 each, from `esp32/tools/sprite_preview.py`. `js/site.js` has the list of moods it shows, and which frame each is |
| The Last Herald on the Amiga | `amiga.png` | the Amiga's own display (`last-herald/assets/amiga/square.png`) |
| D&D character sheet | none | drawn in the page (the `<svg class="arcane">`). Replace it with a screenshot when there's one to show |
| Ensemble Reader | `ensemble-*.webp` | the Play screenshots (`bookreader/store/graphics`) |

## Publishing

On GitHub: **Settings > Pages > Build and deployment > Deploy from a branch**, `main`, `/ (root)`. Every push to `main` is live a minute later.

## The domain

Until the domain is set up the site is at `https://logge.github.io/<repository name>/`. Everything on the page uses relative addresses, so it works there and on the domain alike. (The 404 page's link home and the link-preview picture's address assume the domain.)

To put it on sideblabs.com:

1. At the domain's registrar, in its DNS settings, add these records:

   | Type | Name | Value |
   |---|---|---|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | AAAA | `@` | `2606:50c0:8000::153` |
   | AAAA | `@` | `2606:50c0:8001::153` |
   | AAAA | `@` | `2606:50c0:8002::153` |
   | AAAA | `@` | `2606:50c0:8003::153` |
   | CNAME | `www` | `logge.github.io` |

2. On GitHub: **Settings > Pages > Custom domain**, enter `sideblabs.com` and save. GitHub adds a file named `CNAME` to the repository (pull it afterwards) and checks the DNS; that can take up to a day.
3. When the check has passed, tick **Enforce HTTPS**.

Don't add the `CNAME` file before the DNS is in place: with it, the `logge.github.io` address redirects to the domain, which leads nowhere until then.
