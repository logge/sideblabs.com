// The picture at the top of the page, alive as it is on the game's title screen: the game's own
// code for it (its art/title.ts, lit by its engine/lighting.ts, the kids standing on it by its
// engine/actor.ts), drawn on a canvas laid over the still picture.
//
// This is the source of ../js/title.js. It needs the game's repository (the-last-herald) checked
// out beside this one, as `adventure`; from this repository's folder:
//   ../adventure/node_modules/.bin/rolldown last-herald/tools/title.ts --file last-herald/js/title.js --format iife --minify
import { paintTitle, animateTitle, titleLighting, glowMask, KIDS } from '../../../adventure/src/art/title';
import { shade } from '../../../adventure/src/engine/lighting';
import { Surface } from '../../../adventure/src/engine/surface';
import { Actor } from '../../../adventure/src/engine/actor';
import { SOFIA, DANNY, BENJAMIN } from '../../../adventure/src/art/cast';
import type { RigDef } from '../../../adventure/src/art/rig';

const W = 320, H = 180;
/** Frames a second, at most: everything moves by the clock, so fewer frames is only fewer steps. */
const FPS = 30;

function start(art: HTMLElement) {
  const back = paintTitle(), frame = new Surface(W, H);
  const rigs: Record<string, RigDef> = { sofia: SOFIA, danny: DANNY, benjamin: BENJAMIN };
  const kids = KIDS.map(([id, x, y]) => {
    const k = new Actor({ id, name: id, color: '#fff', x, y, rig: rigs[id] });
    k.setPose('stand', 0, 1e9); // just standing and looking, as on the title screen
    return k;
  });

  // The game's picture, 320 x 180, is drawn small and then laid on the canvas a whole number of
  // times its size, at least as large as it's shown, so every one of its pixels is as wide as the next
  const live = document.createElement('div'), canvas = document.createElement('canvas'), date = document.createElement('p');
  live.className = 'title-live';
  live.setAttribute('aria-hidden', 'true'); // the still picture under it has the words for it
  date.textContent = 'Granvik, 21 October 1987'; // on the title screen it's text over the picture, too
  live.append(canvas, date);
  const small = document.createElement('canvas');
  small.width = W; small.height = H;
  const sctx = small.getContext('2d'), ctx = canvas.getContext('2d'), img = new ImageData(W, H);
  if (!sctx || !ctx) return;
  const fit = () => {
    const k = Math.max(1, Math.min(9, Math.ceil(((live.clientWidth || art.clientWidth) * (window.devicePixelRatio || 1)) / W)));
    if (canvas.width !== W * k) { canvas.width = W * k; canvas.height = H * k; }
    ctx.imageSmoothingEnabled = false;
  };

  const paint = (t: number) => {
    frame.copyFrom(back);
    animateTitle(frame, t);
    for (const k of kids) {
      k.view = 'back'; // looking out over the valley, away from us
      k.draw(frame, t);
    }
    shade(frame.buf, W, H, img.data, titleLighting(t), 0, { z: glowMask, w: W });
    sctx.putImageData(img, 0, 0);
    fit();
    ctx.drawImage(small, 0, 0, canvas.width, canvas.height);
  };

  // Only while the picture is on the screen (and the tab's showing: the browser sees to that)
  let seen = true, last = -Infinity;
  if ('IntersectionObserver' in window) new IntersectionObserver((e) => { seen = e[e.length - 1].isIntersecting; }).observe(art);
  const t0 = performance.now();
  const loop = (now: number) => {
    requestAnimationFrame(loop);
    if (!seen || now - last < 1000 / FPS - 3) return;
    last = now;
    paint((now - t0) / 1000);
  };
  art.append(live);
  paint(0);
  requestAnimationFrame(() => { live.classList.add('on'); requestAnimationFrame(loop); });
}

const art = document.querySelector<HTMLElement>('.hero-art');
// Not for someone who has asked for less movement: the still picture stays
if (art && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  try { start(art); } catch { art.querySelector('.title-live')?.remove(); }
}
