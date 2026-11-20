// Side B Labs. The page works without this: it adds the tape type switch,
// the deck at the bottom, the tape that winds as you scroll, and Gremlin's moods.

(function () {
  'use strict';

  var root = document.documentElement;
  var still = window.matchMedia('(prefers-reduced-motion: reduce)');

  // ---- The tape type: Normal (light) or Chrome (dark) ----

  var darkQuery = window.matchMedia('(prefers-color-scheme: dark)');
  var typeButtons = document.querySelectorAll('[data-tape]');

  function currentTape() {
    return root.dataset.theme || (darkQuery.matches ? 'dark' : 'light');
  }
  function showTape() {
    var now = currentTape();
    typeButtons.forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.tape === now));
    });
  }
  typeButtons.forEach(function (b) {
    b.addEventListener('click', function () {
      root.dataset.theme = b.dataset.tape;
      try { localStorage.setItem('tape', b.dataset.tape); } catch (e) {}
      showTape();
    });
  });
  darkQuery.addEventListener('change', showTape);
  showTape();

  // ---- The deck, and the tape winding from one reel to the other ----

  var tracks = Array.prototype.slice.call(document.querySelectorAll('.track'));
  var deck = document.querySelector('.deck');
  var deckN = deck.querySelector('.deck-n');
  var deckTitle = deck.querySelector('.deck-title');
  var deckNow = deck.querySelector('.deck-now');
  var deckCount = deck.querySelector('.deck-count');
  var prev = deck.querySelector('[data-skip="-1"]');
  var next = deck.querySelector('[data-skip="1"]');
  var list = document.getElementById('tracklist');
  var playing = -1;
  var waiting = false;

  // The smaller tracks sit two to a row. A row counts as one stop of the tape:
  // the deck names its first track, and the buttons go from row to row.
  function topOf(i) { return tracks[i].getBoundingClientRect().top; }
  function rowStart(i) {
    var top = topOf(i);
    while (i > 0 && Math.abs(topOf(i - 1) - top) < 8) i--;
    return i;
  }
  function rowAfter(i) {
    var top = topOf(i);
    for (var j = i + 1; j < tracks.length; j++) if (topOf(j) > top + 8) return j;
    return -1;
  }
  function rowBefore(i) {
    return i > 0 ? rowStart(i - 1) : -1;
  }

  function show(i) {
    prev.disabled = rowBefore(i) < 0;
    next.disabled = rowAfter(i) < 0;
    if (i === playing) return;
    playing = i;
    var t = tracks[i];
    var style = getComputedStyle(t);
    deckN.textContent = t.dataset.n;
    deckTitle.textContent = t.dataset.title;
    deckNow.href = '#' + t.id;
    deck.style.setProperty('--deck-accent', style.getPropertyValue('--accent'));
    deck.style.setProperty('--deck-on', style.getPropertyValue('--on-accent'));
  }

  function read() {
    waiting = false;
    var max = root.scrollHeight - window.innerHeight;
    var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
    root.style.setProperty('--p', p.toFixed(4));
    deckCount.textContent = String(Math.round(p * 999)).padStart(3, '0');

    // the track playing is the last one whose top has passed the middle of the window
    var mid = window.innerHeight * 0.5;
    var at = 0;
    for (var i = 0; i < tracks.length; i++) {
      if (topOf(i) <= mid) at = i;
    }
    show(rowStart(at));

    var box = list.getBoundingClientRect();
    deck.hidden = !(box.top < window.innerHeight * 0.6 && box.bottom > window.innerHeight * 0.4);
  }
  function onScroll() {
    if (!waiting) { waiting = true; requestAnimationFrame(read); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  read();

  function skip(by) {
    var to = by > 0 ? rowAfter(playing) : rowBefore(playing);
    if (to < 0) return;
    tracks[to].scrollIntoView({ behavior: still.matches ? 'auto' : 'smooth', block: 'start' });
  }
  prev.addEventListener('click', function () { skip(-1); });
  next.addEventListener('click', function () { skip(1); });

  // ---- Tracks arrive as they come into view ----

  if ('IntersectionObserver' in window) {
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); seen.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -12% 0px' });
    tracks.forEach(function (t) { seen.observe(t); });
  } else {
    tracks.forEach(function (t) { t.classList.add('in'); });
  }

  // ---- Gremlin ----
  // The frames are the firmware's own moods, in the order tools/sprite_preview.py draws them:
  // 0 sleepy, 1 idle, 2 scheming, 3 working, 4 alarm, 5 happy, 6 sad, 7 hot, 8 lost, 9 dead,
  // 10 on air, 11 muted, 12 groove, 13 dance, 14 dance (jump).

  var MOODS = [
    { name: 'happy', why: 'tests passed', frames: [5] },
    { name: 'working', why: 'Claude Code is busy', frames: [3] },
    { name: 'alarm', why: 'waiting for your permission', frames: [4] },
    { name: 'idle', why: 'nothing to report', frames: [1, 1, 1, 2] },
    { name: 'sad', why: 'the build failed', frames: [6] },
    { name: 'groove', why: 'music is playing', frames: [12] },
    { name: 'dance', why: 'the auto-DJ is mixing', frames: [13, 14] },
    { name: 'hot', why: 'the processor is flat out', frames: [7] },
    { name: 'on air', why: 'you are in a meeting', frames: [10] },
    { name: 'dead', why: 'somebody ran git push --force', frames: [9] },
    { name: 'sleepy', why: 'nothing for 20 minutes', frames: [0] }
  ];

  var stage = document.querySelector('.gremlin-stage');
  if (stage) {
    var sprite = stage.querySelector('.gremlin');
    var moodText = stage.querySelector('.g-mood');
    var whyText = stage.querySelector('.g-why');
    var mood = 0;
    var tick = 0;
    var timer = null;

    function draw() {
      var m = MOODS[mood];
      sprite.style.setProperty('--f', m.frames[tick % m.frames.length]);
      moodText.textContent = m.name;
      whyText.textContent = m.why;
      stage.classList.toggle('alarm', m.name === 'alarm');
    }
    function step() {
      tick++;
      if (tick % 6 === 0) mood = (mood + 1) % MOODS.length; // a new mood every 2.4 s
      draw();
    }
    function run(on) {
      if (on && !timer && !still.matches) timer = setInterval(step, 400);
      if (!on && timer) { clearInterval(timer); timer = null; }
    }
    var inView = !('IntersectionObserver' in window);
    draw();
    if (!inView) {
      new IntersectionObserver(function (entries) {
        inView = entries[0].isIntersecting;
        run(inView && !document.hidden);
      }).observe(stage);
    } else {
      run(true);
    }
    document.addEventListener('visibilitychange', function () { run(inView && !document.hidden); });
  }
})();
