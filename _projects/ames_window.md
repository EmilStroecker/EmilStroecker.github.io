---
layout: page
title: Illusory Depth Estimation
description: Do depth estimation networks share humans' geometric biases?
img: /assets/img/Ames_preview.png
importance: 1
---

## Overview

The **Ames Window Illusion** is a striking perceptual phenomenon in which a trapezoidal silhouette of a window ---
designed to mimic the perspective projection of a rectangle --- is perceived by human observers as a full rectangular
window oscillating back and forth, rather than rotating continuously in depth. This illusion reveals a powerful
geometric prior in the human visual system: we strongly expect windows (and rectangular objects in general) to be
rectangular, and our depth perception is shaped accordingly.

This project asks: do modern neural networks trained for depth estimation exhibit the same geometric biases?

<div class="ames-gallery" id="amesGallery" tabindex="0" role="group" aria-roledescription="carousel" aria-label="Ames illusion stimuli">
  <div class="ames-frame">
    <div class="ames-viewport">
      <figure class="ames-slide is-active" data-name="Window" data-note="Six-pane window &mdash; the classic Ames construction">
        <video width="422" height="912" autoplay muted loop playsinline preload="auto"
               aria-label="Trapezoidal six-pane window rotating clockwise. Top panel, frontal view: the shape appears to oscillate back and forth. Bottom panel, raised viewpoint: the same object is seen to rotate continuously.">
          <source src="{{ '/assets/anim/ames_window_pair.webm' | relative_url }}" type="video/webm">
          <source src="{{ '/assets/anim/ames_window_pair.mp4' | relative_url }}" type="video/mp4">
        </video>
      </figure>

      <figure class="ames-slide" data-name="Ring" data-note="Closed contour &mdash; no corners, no rectangularity cue">
        <video width="422" height="912" muted loop playsinline preload="auto"
               aria-label="Tapered ring rotating clockwise, shown from a frontal viewpoint above and a raised viewpoint below.">
          <source src="{{ '/assets/anim/ames_circle_pair.webm' | relative_url }}" type="video/webm">
          <source src="{{ '/assets/anim/ames_circle_pair.mp4' | relative_url }}" type="video/mp4">
        </video>
      </figure>

      <figure class="ames-slide" data-name="Dots" data-note="Stochastic dot field &mdash; the taper carried by size gradient alone">
        <video width="422" height="912" muted loop playsinline preload="auto"
               aria-label="Field of stochastically placed dots rotating clockwise, shown from a frontal viewpoint above and a raised viewpoint below.">
          <source src="{{ '/assets/anim/ames_dots_pair.webm' | relative_url }}" type="video/webm">
          <source src="{{ '/assets/anim/ames_dots_pair.mp4' | relative_url }}" type="video/mp4">
        </video>
      </figure>
    </div>
  </div>

  <div class="ames-controls">
    <button type="button" class="ames-arrow ames-arrow--prev" aria-label="Previous stimulus">&#8249;</button>
    <div class="ames-dots-nav" role="tablist" aria-label="Choose stimulus"></div>
    <button type="button" class="ames-arrow ames-arrow--next" aria-label="Next stimulus">&#8250;</button>
  </div>

  <p class="ames-caption">
    <strong class="ames-caption__name">Window</strong>
    <span class="ames-caption__note">Six-pane window &mdash; the classic Ames construction</span>
  </p>
</div>

<style>
  .ames-gallery {
    margin: 2rem auto;
    max-width: 30rem;
    outline: none;
  }
  .ames-frame {
    display: flex;
    justify-content: center;
  }
  .ames-viewport {
    position: relative;
    flex: 0 1 20rem;
    min-width: 0;
    border-radius: 10px;
    overflow: hidden;
    background: #050505;
  }
  .ames-slide {
    display: none;
    margin: 0;
  }
  .ames-slide.is-active {
    display: block;
  }
  .ames-slide video {
    display: block;
    width: 100%;
    height: auto;
  }
  .ames-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-top: 0.75rem;
  }
  .ames-arrow {
    flex: 0 0 auto;
    width: 2.25rem;
    height: 2.25rem;
    line-height: 1;
    font-size: 1.5rem;
    border: 1px solid currentColor;
    border-radius: 50%;
    background: transparent;
    color: var(--global-theme-color);
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
  }
  .ames-arrow:hover,
  .ames-arrow:focus-visible {
    background: var(--global-theme-color);
    color: #fff;
  }
  .ames-caption {
    margin: 0.6rem 0 0;
    text-align: center;
    font-size: 0.9rem;
    line-height: 1.45;
  }
  .ames-caption__name {
    display: block;
    color: var(--global-theme-color);
  }
  .ames-caption__note {
    color: var(--global-text-color-light, inherit);
  }
  .ames-dots-nav {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
  }
  .ames-dot {
    width: 0.55rem;
    height: 0.55rem;
    padding: 0;
    border: 1px solid var(--global-theme-color);
    border-radius: 50%;
    background: transparent;
    cursor: pointer;
  }
  .ames-dot[aria-selected="true"] {
    background: var(--global-theme-color);
  }
  @media (max-width: 576px) {
    .ames-controls {
      gap: 0.75rem;
    }
    .ames-arrow {
      width: 1.9rem;
      height: 1.9rem;
      font-size: 1.2rem;
    }
  }
</style>

<script>
  (function () {
    var gallery = document.getElementById('amesGallery');
    if (!gallery) return;

    var slides = Array.prototype.slice.call(gallery.querySelectorAll('.ames-slide'));
    var dotsNav = gallery.querySelector('.ames-dots-nav');
    var nameEl = gallery.querySelector('.ames-caption__name');
    var noteEl = gallery.querySelector('.ames-caption__note');
    var index = 0;

    var dots = slides.map(function (slide, i) {
      var dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'ames-dot';
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-label', slide.dataset.name);
      dot.addEventListener('click', function () { show(i); });
      dotsNav.appendChild(dot);
      return dot;
    });

    slides.forEach(function (slide) {
      var video = slide.querySelector('video');
      if (!video) return;
      // A refusal is often transient, so the controls offered as a fallback
      // are removed again as soon as the clip does start.
      video.addEventListener('playing', function () { video.controls = false; });
      // The first play() can land before the element has any data.
      video.addEventListener('canplay', function () {
        if (slide.classList.contains('is-active')) playActive();
      });
    });

    function playActive() {
      var video = slides[index].querySelector('video');
      if (!video) return;
      var playing = video.play();
      // If autoplay is refused for good (iOS Low Power Mode, strict autoplay
      // settings) expose native controls rather than leave a frozen frame.
      if (playing && playing.catch) {
        playing.catch(function () { video.controls = true; });
      }
    }

    function show(i) {
      index = (i + slides.length) % slides.length;
      slides.forEach(function (slide, j) {
        var active = j === index;
        slide.classList.toggle('is-active', active);
        // Only the visible clip should be decoding: a paused, hidden video
        // costs nothing, whereas three simultaneously animating clips would
        // all compete for decode.
        var video = slide.querySelector('video');
        if (video && !active) {
          video.pause();
          // Safari has historically thrown on a seek before metadata exists,
          // and this must not abort the rest of show().
          try { video.currentTime = 0; } catch (e) {}
        }
      });
      playActive();
      dots.forEach(function (dot, j) {
        dot.setAttribute('aria-selected', j === index ? 'true' : 'false');
      });
      nameEl.textContent = slides[index].dataset.name;
      noteEl.innerHTML = slides[index].dataset.note;
    }

    gallery.querySelector('.ames-arrow--prev').addEventListener('click', function () { show(index - 1); });
    gallery.querySelector('.ames-arrow--next').addEventListener('click', function () { show(index + 1); });

    gallery.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowLeft') { show(index - 1); event.preventDefault(); }
      if (event.key === 'ArrowRight') { show(index + 1); event.preventDefault(); }
    });

    var touchStartX = null;
    var viewport = gallery.querySelector('.ames-viewport');
    viewport.addEventListener('touchstart', function (event) {
      touchStartX = event.changedTouches[0].clientX;
    }, { passive: true });
    viewport.addEventListener('touchend', function (event) {
      if (touchStartX === null) return;
      var dx = event.changedTouches[0].clientX - touchStartX;
      if (Math.abs(dx) > 40) show(index + (dx < 0 ? 1 : -1));
      touchStartX = null;
    }, { passive: true });

    show(0);

    // The gallery sits below the fold, so on load the clip is off screen and
    // browsers decline to start a muted clip that nobody can see. Start it
    // when it actually scrolls into view. Without this the visitor waits on a
    // still frame until they happen to press an arrow, whose click counts as
    // the user gesture that unconditionally permits playback.
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) playActive();
        });
      }, { threshold: 0.15 }).observe(gallery);
    }

    // A page opened in a background tab has playback suspended, and the one
    // play() above resolves without ever starting; retry when it is actually
    // on screen so the visitor never lands on a frozen frame.
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) playActive();
    });
  })();
</script>

<p style="text-align:center; font-size:0.85rem; margin-top:-0.25rem;">
  All three stimuli share the same &minus;45&deg; depth slant and left/right taper, so they are directly comparable.
  Each is the perspective projection of a slanted object onto a flat, rigidly rotating plate.
</p>

## Research Questions

- When presented with the Ames Window stimulus, do state-of-the-art monocular depth networks (Metric3D, DSINE, MoGe)
  produce depth estimates consistent with the illusory percept?
- How do network responses compare quantitatively to psychophysical measurements of depth inversion in human observers?
- What do these comparisons reveal about the extent to which contemporary vision models capture human-like shape
  and depth priors?

## Methods

We run a psychophysics experiment (PsychoPy/PsychoJS) measuring depth inversion responses to the rotating Ames
Window in human participants. We compare these behavioural signatures against the outputs of three
state-of-the-art monocular depth estimation networks on the same stimuli.

Participants see a single static frame of a tapered object and report the 3D orientation they perceive by rotating
a probe gauge until it matches. Because a surface and its 180&deg; rotation project identically, responses are
scored modulo 180&deg;. The stimuli are sampled from a Sobol sequence over the generating parameters (taper, depth
slant, thickness, focal length, texture), so the space of shapes is covered quasi-uniformly rather than on a grid.

### Try the task

<div class="amx" id="amxDemo" data-base="{{ '/assets/img/ames_demo' | relative_url }}">
  <div class="amx__stage">
    <figure class="amx__panel">
      <div class="amx__imgwrap">
        <img class="amx__img" id="amxProbe" alt="Stimulus whose 3D orientation you judge" draggable="false">
      </div>
      <figcaption class="amx__cap">Stimulus</figcaption>
    </figure>

    <figure class="amx__panel">
      <div class="amx__imgwrap amx__imgwrap--gauge" id="amxGaugeWrap"
           role="slider" tabindex="0" aria-valuemin="-90" aria-valuemax="90" aria-valuenow="0"
           aria-label="Probe gauge orientation in degrees. Drag horizontally or use the left and right arrow keys.">
        <img class="amx__img" id="amxGauge" alt="Probe gauge you rotate to match the stimulus" draggable="false">
      </div>
      <figcaption class="amx__cap" id="amxGaugeCap">Probe gauge &mdash; drag to rotate</figcaption>
    </figure>
  </div>

  <div class="amx__bar" id="amxBar" hidden><span class="amx__barfill" id="amxBarFill"></span></div>

  <p class="amx__status" id="amxStatus" role="status" aria-live="polite">Loading&hellip;</p>

  <div class="amx__controls">
    <button type="button" class="amx__btn amx__btn--primary" id="amxAction">Start</button>
    <span class="amx__progress" id="amxProgress"></span>
  </div>

  <noscript>
    <p class="amx__note">This interactive demo needs JavaScript.</p>
  </noscript>
</div>

<p class="amx__note">
  A short, untimed excerpt of the task &mdash; 24 stimuli, no tutorial, and nothing recorded. The real study runs on
  Prolific with fullscreen enforcement, a 2&nbsp;s stimulus preview, a 5&nbsp;s response window, and several hundred
  trials per participant.
</p>

<style>
  .amx {
    margin: 1.5rem auto 0.5rem;
    max-width: 40rem;
  }
  .amx__stage {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    justify-content: center;
  }
  .amx__panel {
    flex: 1 1 14rem;
    min-width: 0;
    margin: 0;
  }
  .amx__imgwrap {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    background: #272727;
    aspect-ratio: 1 / 1;
  }
  /* aspect-ratio is well supported, but keep older engines from collapsing. */
  @supports not (aspect-ratio: 1 / 1) {
    .amx__imgwrap { height: 0; padding-bottom: 100%; }
    .amx__imgwrap .amx__img { position: absolute; inset: 0; }
  }
  .amx__imgwrap--gauge {
    cursor: ew-resize;
    touch-action: pan-y;
    outline: none;
  }
  .amx__imgwrap--gauge:focus-visible {
    box-shadow: 0 0 0 3px var(--global-theme-color);
  }
  .amx__img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: contain;
    user-select: none;
    -webkit-user-drag: none;
  }
  .amx__bar {
    height: 3px;
    margin-top: 0.75rem;
    border-radius: 2px;
    background: rgba(128, 128, 128, 0.25);
    overflow: hidden;
  }
  .amx__bar[hidden] { display: none; }
  .amx__barfill {
    display: block;
    height: 100%;
    width: 0;
    background: var(--global-theme-color);
    transition: width 0.2s ease;
  }
  .amx__results {
    margin: 0.5rem auto 0;
    border-collapse: collapse;
    font-size: 0.85rem;
  }
  .amx__results th,
  .amx__results td {
    padding: 0.2rem 0.75rem;
    text-align: right;
    border-bottom: 1px solid rgba(128, 128, 128, 0.2);
  }
  .amx__results th:first-child,
  .amx__results td:first-child { text-align: left; }
  .amx__cap {
    margin-top: 0.4rem;
    text-align: center;
    font-size: 0.82rem;
    color: var(--global-text-color-light, inherit);
  }
  .amx__status {
    margin: 0.9rem 0 0;
    text-align: center;
    font-size: 0.92rem;
    min-height: 2.8em;
  }
  .amx__status b { color: var(--global-theme-color); }
  .amx__controls {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-top: 0.5rem;
  }
  .amx__btn {
    padding: 0.4rem 1.1rem;
    font: inherit;
    font-size: 0.9rem;
    border: 1px solid var(--global-theme-color);
    border-radius: 6px;
    background: transparent;
    color: var(--global-theme-color);
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
  }
  .amx__btn:hover:not(:disabled),
  .amx__btn:focus-visible:not(:disabled) {
    background: var(--global-theme-color);
    color: #fff;
  }
  .amx__btn:disabled { opacity: 0.45; cursor: default; }
  .amx__progress {
    font-size: 0.82rem;
    color: var(--global-text-color-light, inherit);
  }
  .amx__note {
    max-width: 40rem;
    margin: 0.6rem auto 0;
    text-align: center;
    font-size: 0.8rem;
    line-height: 1.5;
    color: var(--global-text-color-light, inherit);
  }
</style>

<script>
  (function () {
    var root = document.getElementById('amxDemo');
    if (!root) return;

    var BASE  = root.dataset.base;
    var STEP  = 5;                        // degrees between gauge positions
    var N      = 180 / STEP + 1;          // 37 frames spanning the 180 deg arc
    // Frame i corresponds to orientation -90 + STEP*i degrees.
    var toDeg   = function (i) { return -90 + STEP * i; };
    var toFrame = function (deg) { return Math.round((deg + 90) / STEP); };

    // [slug, gaugeShape, trueOrientationDeg, label], loaded from trials.json.
    var TRIALS = [];

    var probeEl = document.getElementById('amxProbe');
    var gaugeEl = document.getElementById('amxGauge');
    var wrapEl  = document.getElementById('amxGaugeWrap');
    var capEl   = document.getElementById('amxGaugeCap');
    var statusEl= document.getElementById('amxStatus');
    var actionEl= document.getElementById('amxAction');
    var progEl  = document.getElementById('amxProgress');
    var barEl   = document.getElementById('amxBar');
    var barFill = document.getElementById('amxBarFill');

    var cache = {};      // gaugeShape -> array of preloaded Image objects
    var trial = 0;
    var frame = toFrame(0);
    var phase = 'idle';  // idle | loading | respond | done
    var results = [];    // { label, error }

    function gaugeSrc(shape, i) {
      return BASE + '/gauge/' + shape + '/' + (i < 10 ? '0' + i : i) + '.webp';
    }

    function preload(shape) {
      if (cache[shape]) return Promise.resolve(cache[shape]);
      var imgs = [];
      var jobs = [];
      for (var i = 0; i < N; i++) {
        (function (i) {
          jobs.push(new Promise(function (resolve) {
            var im = new Image();
            im.onload = im.onerror = function () { resolve(); };
            im.src = gaugeSrc(shape, i);
            imgs[i] = im;
          }));
        })(i);
      }
      return Promise.all(jobs).then(function () {
        cache[shape] = imgs;
        return imgs;
      });
    }

    function renderGauge() {
      gaugeEl.src = gaugeSrc(TRIALS[trial][1], frame);
      wrapEl.setAttribute('aria-valuenow', String(toDeg(frame)));
      if (phase === 'respond') {
        capEl.textContent = 'Probe gauge — ' + fmt(toDeg(frame));
      }
    }

    function fmt(d) {
      return (d > 0 ? '+' : '') + d + '°';
    }

    // Orientation is 180-symmetric, so the error wraps into (-90, 90].
    function foldedError(response, truth) {
      var d = ((response - truth) % 180 + 180) % 180;
      if (d > 90) d -= 180;
      return d;
    }

    function setFrame(next) {
      var clamped = Math.max(0, Math.min(N - 1, next));
      if (clamped === frame) return;
      frame = clamped;
      renderGauge();
    }

    // ---- interaction -------------------------------------------------
    var dragging = false;
    var lastX = 0;
    var accum = 0;
    var PX_PER_STEP = 9;

    wrapEl.addEventListener('pointerdown', function (e) {
      if (phase !== 'respond') return;
      dragging = true;
      lastX = e.clientX;
      accum = 0;
      wrapEl.setPointerCapture(e.pointerId);
      e.preventDefault();
    });

    wrapEl.addEventListener('pointermove', function (e) {
      if (!dragging || phase !== 'respond') return;
      accum += e.clientX - lastX;
      lastX = e.clientX;
      var steps = (accum / PX_PER_STEP) | 0;
      if (steps !== 0) {
        accum -= steps * PX_PER_STEP;
        setFrame(frame + steps);
      }
    });

    function endDrag(e) {
      if (!dragging) return;
      dragging = false;
      try { wrapEl.releasePointerCapture(e.pointerId); } catch (err) {}
    }
    wrapEl.addEventListener('pointerup', endDrag);
    wrapEl.addEventListener('pointercancel', endDrag);

    wrapEl.addEventListener('keydown', function (e) {
      if (phase !== 'respond') return;
      if (e.key === 'ArrowLeft')  { setFrame(frame - 1); e.preventDefault(); }
      if (e.key === 'ArrowRight') { setFrame(frame + 1); e.preventDefault(); }
      if (e.key === 'Enter' || e.key === ' ') { advance(); e.preventDefault(); }
    });

    // ---- flow --------------------------------------------------------
    function showTrial() {
      var t = TRIALS[trial];
      phase = 'respond';
      probeEl.src = BASE + '/probe/' + t[0] + '.webp';
      // A random start orientation keeps responses from anchoring on the
      // previous trial's setting, as the real experiment does.
      frame = Math.floor(Math.random() * N);
      renderGauge();
      progEl.textContent = 'Trial ' + (trial + 1) + ' of ' + TRIALS.length;
      barFill.style.width = (100 * trial / TRIALS.length) + '%';
      // Prefetch the next probe so the run never stalls between trials.
      if (trial + 1 < TRIALS.length) {
        new Image().src = BASE + '/probe/' + TRIALS[trial + 1][0] + '.webp';
      }
    }

    function begin() {
      phase = 'loading';
      actionEl.disabled = true;
      actionEl.textContent = 'Loading…';
      statusEl.textContent = 'Loading stimuli…';

      // Both gauge shapes are needed because the trial order is shuffled.
      Promise.all([preload('circle'), preload('diamond')]).then(function () {
        trial = 0;
        results = [];
        barEl.hidden = false;
        actionEl.disabled = false;
        actionEl.textContent = 'Confirm';
        statusEl.innerHTML = 'Rotate the gauge until it matches the <b>3D orientation</b> you see in the stimulus, then confirm.';
        showTrial();
      });
    }

    function record() {
      var t = TRIALS[trial];
      results.push({ label: t[3], error: Math.abs(foldedError(toDeg(frame), t[2])) });
    }

    function summarise() {
      phase = 'done';
      barEl.hidden = true;
      capEl.textContent = 'Probe gauge';
      progEl.textContent = '';
      actionEl.textContent = 'Run again';

      var byLabel = {};
      var order = [];
      results.forEach(function (r) {
        if (!byLabel[r.label]) { byLabel[r.label] = []; order.push(r.label); }
        byLabel[r.label].push(r.error);
      });
      var mean = function (a) {
        return a.reduce(function (x, y) { return x + y; }, 0) / a.length;
      };

      var rows = order.map(function (label) {
        return '<tr><td>' + label + '</td><td>' + byLabel[label].length +
               '</td><td>' + mean(byLabel[label]).toFixed(1) + '°</td></tr>';
      }).join('');

      statusEl.innerHTML =
        'Mean unsigned error across ' + results.length + ' trials: <b>' +
        mean(results.map(function (r) { return r.error; })).toFixed(1) + '°</b>' +
        '<table class="amx__results"><thead><tr><th>Stimulus</th><th>n</th><th>Mean error</th></tr></thead>' +
        '<tbody>' + rows + '</tbody></table>' +
        '<span class="amx__note">A perfect observer scores 0°; responding at random averages 45°. ' +
        'In the study, systematic departures from 0° &mdash; and how they differ across these shape ' +
        'families &mdash; are the signature we compare against the depth networks.</span>';
    }

    function advance() {
      if (phase === 'idle' || phase === 'done') { begin(); return; }
      if (phase !== 'respond') return;
      record();
      if (trial + 1 < TRIALS.length) { trial++; showTrial(); }
      else { summarise(); }
    }

    actionEl.addEventListener('click', advance);

    // ---- init --------------------------------------------------------
    function shuffle(a) {
      for (var i = a.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = a[i]; a[i] = a[j]; a[j] = tmp;
      }
      return a;
    }

    actionEl.disabled = true;
    fetch(BASE + '/trials.json')
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (list) {
        TRIALS = shuffle(list.slice());
        // Idle preview: first stimulus and a frontal gauge.
        probeEl.src = BASE + '/probe/' + TRIALS[0][0] + '.webp';
        gaugeEl.src = gaugeSrc(TRIALS[0][1], toFrame(0));
        statusEl.innerHTML = 'Judge the <b>3D orientation</b> of each stimulus by rotating the probe gauge to match it. Drag it, or use the arrow keys.';
        progEl.textContent = TRIALS.length + ' trials, about two minutes';
        actionEl.disabled = false;
      })
      .catch(function () {
        statusEl.textContent = 'The demo stimuli could not be loaded.';
        actionEl.hidden = true;
      });
  })();
</script>

This work is conducted as part of my MSc thesis at the
[Kriegeskorte Visual Inference Lab](https://kriegeskortelab.zuckermaninstitute.columbia.edu/),
Columbia University, Zuckerman Institute.

## Conference Abstract

Stroecker, E., Cheng, F., &amp; Kriegeskorte, N. (2026, August). *Measuring Depth Inversion in the Ames Window
Illusion* [Extended abstract, accepted]. 9th Annual Conference on Cognitive Computational Neuroscience, NYC, USA.
