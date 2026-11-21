# Side B Labs: the website

The hub for Side B Labs, Peter Logarn's independent software studio: one page that lists every project as a track on side B of a tape, and the websites of two of them, The Last Herald and ThreadMix Auto DJ, in folders of their own.

**https://sideblabs.com**

It's plain HTML, CSS and a little JavaScript, served as it is by GitHub Pages from the `main` branch: no build step. The hub's page loads nothing from other sites until you ask it to (the font, Pixelify Sans, is in `fonts/`, under the SIL Open Font License in `fonts/OFL.txt`), and has no cookies or analytics. Two things do reach another site, each when you press it: a film plays from YouTube (its no-cookie player) in a window on the page, and the contact form is sent through Web3Forms. (The two project sites each load one thing: The Last Herald loads itch.io's player when its play button is pressed, and ThreadMix asks GitHub for the number of its newest version.) The one thing it keeps in the browser is the tape type you chose (Normal or Chrome: the light or the dark colours), in `localStorage`.

- `index.html`: the page. Each project is an `<article class="track">`.
- `css/site.css`: the look. The colours of both tape types are at the top.
- `js/site.js`: the tape type switch, the deck at the bottom that says which track is playing, the tape that winds from one reel to the other as you scroll, the window films play in, sending the contact form, and Gremlin's moods. The page works without it: the films are then ordinary links to YouTube.
- `assets/tracks/`: the tracks' pictures.
- `404.html`: the page for an address that isn't there.
- `last-herald/`: The Last Herald's website, with its privacy policy (`last-herald/privacy/`) and the watch faces' (`last-herald/watchfaces/privacy/`). See [Two sites in folders](#two-sites-in-folders).
- `threadmix/`: ThreadMix Auto DJ's website.
- `robin-coco/`: Robin & Coco's website, with its privacy policy (`robin-coco/privacy/`). See [Robin & Coco](#robin--coco).
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

To add a project: copy a track, give it the next number, and change the "nine tracks" in the hero, the "9 tracks" under Tracklist and on the cassette's label (`independent software · 9 tracks`, in the `<svg>` in `index.html` and in `tools/make_images.py`).

**When something comes out:** Robin & Coco and Ensemble Reader say "Coming to Google Play", and have no links yet. When they're live, change the status to `<span class="status live">Released</span>` and add, after the tags:

```html
<p class="links">
  <a class="btn" href="https://play.google.com/store/apps/details?id=...">Google Play</a>
</p>
```

Where the pictures come from:

| Track | Picture | From |
|---|---|---|
| The Last Herald | `last-herald.png` | the game's store screenshots (`last-herald/assets/screens/1-title.png`), at half the size |
| The Last Herald 2 | `last-herald-2.webp` | `last-herald-2/shots/title.png` |
| Armada Zero: Firestorm | `armada-zero.png` | a capture of the hangar screen (`spaceshooter/test_output/m4_art`) |
| Robin & Coco | `robin-coco.png` | the Play feature graphic (`watchfaces/store/roomie`) |
| ThreadMix Auto DJ | `threadmix.webp` | the turntable visualizer (`threadmix/assets/shots`) |
| ESP32 projects | `gremlin-moods.png` | Gremlin's 15 moods in a row, 32 x 24 each, from `esp32/tools/sprite_preview.py`. `js/site.js` has the list of moods it shows, and which frame each is |
| The Last Herald on the Amiga | `amiga.png` | the Amiga's own display (`last-herald/assets/amiga/square.png`) |
| D&D character sheet | none | drawn in the page (the `<svg class="arcane">`). Replace it with a screenshot when there's one to show |
| Ensemble Reader | `ensemble-*.webp` | the Play screenshots (`bookreader/store/graphics`) |

## Films

Any link on the hub to a film on YouTube (`https://www.youtube.com/watch?v=...`) plays in a window on the page instead of leaving it: nothing else is needed than the link. A picture that is such a link (the Amiga's) gets a play button drawn over it. With Ctrl or a middle click the link opens on YouTube as usual.

## The contact form

There's no email address on the page, or anywhere in these files, so that address collectors don't find one. "Write in" is a form, sent by [Web3Forms](https://web3forms.com), which passes each message on by email to the address its access key belongs to.

The key is in `index.html`, in the form: `<input type="hidden" name="access_key" value="...">`. It's meant to be public: all it can do is send a message to that address. For the messages to go somewhere else, enter the new address on web3forms.com and put the key they mail you there instead.

The form has a hidden box named `botcheck` that people don't see and robots tick, which Web3Forms uses to drop their messages. Should spam get through all the same, Web3Forms can add a captcha to the form (their documentation says how).

The Last Herald's footer and the two privacy policies link to the form too, instead of giving an address.

## Two sites in folders

`last-herald/` and `threadmix/` are the websites of those two projects, copied from their own repositories (`logge/last-herald` and `logge/threadmix`) so that everything is under one domain: `sideblabs.com/last-herald/` and `sideblabs.com/threadmix/`. Each has a README of its own with how it works. What was changed in the copies: the addresses for link previews (`og:image`, `og:url`) and a `canonical` link, which name sideblabs.com, and the way back to Side B Labs: a link at the top of every page (over the corner of The Last Herald's title picture and in its privacy pages' bar; first in ThreadMix's bar) and one in each footer.

The two old repositories are still there and still published, because things point at them:

- Google Play has The Last Herald's privacy policy as `https://logge.github.io/last-herald/privacy/`, and the watch faces' as `https://logge.github.io/last-herald/watchfaces/privacy/`. The same pages are now at `https://sideblabs.com/last-herald/privacy/` and `https://sideblabs.com/last-herald/watchfaces/privacy/`; once the domain is up, the Play Console can be given those instead.
- ThreadMix's installers are the `threadmix` repository's releases, and the Amiga version of The Last Herald is a release of the `last-herald` repository. The download buttons point there, and that doesn't need to change.

For as long as both copies of a site are up, a change to one has to be made in the other too. Once the domain is up, the old ones could be replaced by a page that sends visitors on to the new address.

## Robin & Coco

`robin-coco/` is Robin & Coco's own small site, **https://sideblabs.com/robin-coco/**, made here (it has no repository of its own). It looks like the app: its sunset bands, its sand, the cream and ink of Robin's speech bubbles, and its own pixel font (`robin-coco/fonts/roomie_pixel.ttf`, from the watch face's `roomie/src/main/res/font`). The page runs through a day on the island: blue sky at the top, the sand, dusk in bands, and night at the foot.

- `index.html`: the page. The bar at the top, on every page, has the way back to Side B Labs; the foot has it again.
- `privacy/`: its privacy policy, **https://sideblabs.com/robin-coco/privacy/**. It's the watch faces' policy (`watchfaces/store/privacy-policy.md`) told for Robin & Coco alone: the same facts, with nothing of Sunward or Walkies. It gives no email address: its Contact links to the hub's form. If the app's policy changes, change both.
- `css/site.css`: the look. The island at the top is laid out in pixels of the art (`--u`, three screen pixels to one on a wide screen, two on a narrow one), so every sprite is drawn sharp.
- `js/site.js`: the sky of the visitor's own hour over the island (day, dusk from 17, night from 21 to 6), what Robin says, poking her (her six snaps, from the watch face's `tools/roomie/robin.py`), and the window the films play in (a link with `data-film`).
- `assets/sprites/`: the app's own art, from the watch face's `tools/roomie/pixellab`, each cut to its edges: the island's things, and Robin standing, shaking her fist and dancing, each a strip of frames with her feet on its bottom edge (`robin-idle.png` 4 frames of 96, `robin-huff.png` and `robin-dance.png` 9 of 132).
- `assets/watch/` and `assets/phone/`: the Play screenshots (`watchfaces/store/roomie`), the watch's at half their size. `assets/film.png` is the promo film's thumbnail, `assets/og.png` the Play feature graphic.

**When it's out on Google Play:** in `index.html`, under "Get Robin & Coco", there's a comment with the link to put in place of "Coming soon to Google Play". On the hub, change the track's status to `<span class="status live">Released</span>`.

Google Play has the watch faces' privacy policy as `https://logge.github.io/last-herald/watchfaces/privacy/` (the copy here is at `/last-herald/watchfaces/privacy/`). Robin & Coco's listing can be given `https://sideblabs.com/robin-coco/privacy/` instead.

## Publishing

On GitHub: **Settings > Pages > Build and deployment > Deploy from a branch**, `main`, `/ (root)`. Every push to `main` is live a minute later.

## The domain

The site is at **https://sideblabs.com**. The `CNAME` file in this repository is what tells GitHub Pages so (GitHub wrote it, from **Settings > Pages > Custom domain**); the old address, `logge.github.io/sideblabs.com`, sends visitors on to the domain. Everything on the pages uses relative addresses; only the link-preview pictures' addresses and the 404 page's link home name the domain.

The DNS records at the domain's registrar, should they ever need to be set again:

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

**Enforce HTTPS**, under the custom domain in Settings > Pages, sends anyone who arrives by `http://` on to `https://`.
