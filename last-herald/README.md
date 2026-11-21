# The Last Herald: the website

> **This is the copy in the [sideblabs.com](https://github.com/logge/sideblabs.com) repository, published at https://sideblabs.com/last-herald/.** It was copied from the `last-herald` repository, which is still published at https://logge.github.io/last-herald/: the addresses below are that one's. Google Play has its privacy policy address, and the Amiga version is a release of that repository, so it stays. Change the site here, and there too for as long as both are up.

The promotional website for **The Last Herald**, a free point-and-click adventure: three kids from a Swedish sawmill town find a starship under a hill in October 1987.

**https://logge.github.io/last-herald/**

- `index.html`: the game: the story, the kids, pictures, what's in it, and where to get it.
- `privacy/`: the privacy policy, **https://logge.github.io/last-herald/privacy/**, the address to give Google Play (and later the App Store).
- `watchfaces/privacy/`: the privacy policy of the watch faces Sunward, Walkies and Roomie (from the [watchfaces](https://github.com/logge/watchfaces) repository's `store/privacy-policy.md`), **https://logge.github.io/last-herald/watchfaces/privacy/**, for their Google Play listings. Nothing on the site links to it.

It's plain HTML and CSS, served as it is by GitHub Pages from the `main` branch: no build step. It loads nothing from other sites (the font, Pixelify Sans, is in `fonts/`, under the SIL Open Font License in `fonts/OFL.txt`), and has no cookies or analytics. The one exception is the game itself: the "Play it here" section is a picture and a button, and only when the button is pressed does it load itch.io's player (`https://itch.io/embed-upload/20450633`, the browser build's upload on itch.io; a new upload gets a new number, so change it in `index.html` when the build is replaced). The privacy policy says so.

## The stores

The buttons at the top go live once they have an address, at the top of `js/site.js`; until then a button says "Coming soon". Google Play, itch.io and the Amiga are live; the App Store is still to come:

```js
const STORES = {
  play: 'https://play.google.com/store/apps/details?id=io.github.logge.lastherald',
  itch: 'https://plogarn.itch.io/the-last-herald',
  apple: '',
  amiga: 'https://github.com/logge/last-herald/releases/download/amiga-1.0/TheLastHerald-Amiga-1.0.zip',
};
```

## On the Amiga

The Amiga 1200 version (from the game's port, its `release.sh`) is a release of this repository on GitHub, `amiga-1.0`, its zip there: the game's drawer and icons, the configurations for WinUAE and FS-UAE, and a ReadMe. The "Amiga 1200" buttons (at the top, and in the "On the Amiga" section) download it; a new version is a new release, its address in `js/site.js`. The section's picture, `assets/amiga/square.png`, is the Amiga's own display (320 x 256, from its demo film), shown large, its pixels sharp; it and the film button link to the demo film (https://www.youtube.com/watch?v=VHJVSludNbY). In this copy, on sideblabs.com, a plain click plays the film in a window on the page (the links' `data-film`, and the end of `js/site.js`), from YouTube's youtube-nocookie.com player. Both are links: nothing loads from GitHub or YouTube until they're pressed.

## Playing it here

Under the story, the game can be played on the page, in itch.io's player for the browser build: `data-src` on the `.player` in `index.html`, `https://itch.io/embed-upload/20450633`. That number is the upload's on itch.io, so it changes if the zip there is deleted and a new one uploaded: then put the new one in (it's in the address of the game's frame on the itch.io page, `html-classic.itch.zone/html/<number>/`). Pushing new builds with itch.io's `butler` keeps the same upload, and the same number.

## The picture at the top, alive

In this copy, on sideblabs.com, the picture at the top moves as the game's title screen does: clouds drifting over the sky and the moon, smoke from the chimneys, the glow in the hill breathing with motes of light rising from it, the lake shimmering, a glint across the name every eight seconds, and the kids breathing. It isn't a film: `js/title.js` is the game's own code for its title screen (`art/title.ts`, lit by `engine/lighting.ts`, the kids by `engine/actor.ts`), drawing on a canvas laid exactly over the still picture, with the date under the name as text over it, as in the game. The still picture, `assets/screens/1-title.png`, is what's there before the script has loaded, without scripts, and for anyone who has asked their device for less movement. It draws at most 30 times a second, and only while the picture is on the screen.

`js/title.js` is built from `tools/title.ts`, which says how at its top: it needs the game's repository checked out beside this one. Build it again if the game's title screen changes.

## The pictures

The screenshots, the icon and the feature graphic are the store pictures from the game's repository (`store/`), and the kids in `assets/kids/` are drawn by the game's own character rig (`rigFrame` in its `src/art/rig.ts`, in the side view, facing right), moving as they do in the game when they stand about (its `engine/actor.ts`: a blink, a breath in every three seconds, the fidget each has): Sofia stands and then checks her compass (`compass`), Danny holds his boombox over his head, its speakers pumping (`hoist` and `hoist2`), Benjamin puts his headphones on and nods along (`music`). Each is `<kid>-frames.png`: six seconds as 48 frames of an eighth of a second, side by side, at the game's own size, every frame cut to the same box with the feet in the same place. The page shows a frame at a time, six times its size (the `.sprite` in `css/site.css`, which takes a frame's size in the game's pixels from `--wide` and `--tall` on the element). With reduced motion asked for, they stand still, in the frame `--still`. In this copy, on sideblabs.com, they're from the side; the original site has them from the front.
