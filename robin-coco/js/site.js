// Robin & Coco. The page works without this: it adds the sky of the hour, what Robin says,
// poking her, and the window the films play in.

(function () {
  'use strict';

  var still = window.matchMedia('(prefers-reduced-motion: reduce)');

  // ---- The sky over the island is the sky of your own hour, as in the app ----

  var hero = document.querySelector('.hero');
  if (hero) {
    var hour = new Date().getHours();
    hero.dataset.sky = hour >= 21 || hour < 6 ? 'night' : hour >= 17 ? 'dusk' : 'day';
  }

  // ---- What Robin says, and what she says when she's poked ----
  // Her lines are the app's own: the everyday ones from its pictures, and her snaps (HUFFS in
  // the watch face's tools/roomie/robin.py).

  var LINES = [
    "Coco, you're a great listener.",
    'Measure once. Hammer twice.',
    'Not cool, crab.',
    'Too many coconuts!',
    'Ta-da!'
  ];
  var HUFFS = ['Hey!', "I'm surviving here!", 'Shoo, seagull!', 'Personal sandbar!', 'Ow! No-poke zone!', 'Hmph!'];

  var robin = document.querySelector('.robin');
  var say = document.querySelector('.say-text');
  if (robin && say) {
    var line = 0;
    var lastHuff = -1;
    var calm = null;

    var talk = setInterval(function () {
      if (robin.classList.contains('huff') || document.hidden) return;
      line = (line + 1) % LINES.length;
      say.textContent = LINES[line];
    }, 6000);

    robin.addEventListener('click', function () {
      var n;
      do { n = Math.floor(Math.random() * HUFFS.length); } while (n === lastHuff);
      lastHuff = n;
      say.textContent = HUFFS[n];
      // start her fist again from its first frame, even if she's mid-shake
      robin.classList.remove('huff');
      void robin.offsetWidth;
      robin.classList.add('huff');
      clearTimeout(calm);
      calm = setTimeout(function () {
        robin.classList.remove('huff');
        say.textContent = LINES[line];
      }, still.matches ? 2200 : 1900);
    });
  }

  // ---- Films play in a window on the page ----
  // A link with data-film is a link to the film on YouTube, and works as one. A plain click
  // plays it here instead. Nothing is loaded from YouTube until then.

  var box = null;

  function buildBox() {
    var d = document.createElement('dialog');
    d.className = 'video';
    d.setAttribute('aria-label', 'Film');
    d.innerHTML =
      '<div class="video-bar">' +
        '<span class="video-title"></span>' +
        '<a rel="noopener" target="_blank">Open on YouTube</a>' +
        '<button type="button" aria-label="Close">X</button>' +
      '</div>' +
      '<div class="video-frame"></div>';
    d.querySelector('button').addEventListener('click', function () { d.close(); });
    d.addEventListener('click', function (e) { if (e.target === d) d.close(); });
    d.addEventListener('close', function () { d.querySelector('.video-frame').textContent = ''; });
    document.body.appendChild(d);
    return d;
  }

  if (typeof HTMLDialogElement === 'function') {
    document.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
      var link = e.target.closest && e.target.closest('a[data-film]');
      if (!link) return;
      var id = new URL(link.href).searchParams.get('v');
      if (!id) return;
      e.preventDefault();
      if (!box) box = buildBox();
      box.querySelector('.video-title').textContent = link.dataset.film;
      box.querySelector('a').href = link.href;
      var frame = document.createElement('iframe');
      frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
      frame.title = link.dataset.film;
      frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin'; // YouTube won't play without knowing the site
      var holder = box.querySelector('.video-frame');
      holder.textContent = '';
      holder.appendChild(frame);
      box.showModal();
    });
  }
})();
