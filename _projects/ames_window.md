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
        <video width="422" height="912" muted loop playsinline preload="auto"
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

    // A refusal is often transient (a page opened in a background tab has
    // playback suspended), so the controls offered as a fallback are removed
    // again as soon as the clip does start.
    slides.forEach(function (slide) {
      var video = slide.querySelector('video');
      if (video) {
        video.addEventListener('playing', function () { video.controls = false; });
      }
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
          video.currentTime = 0;
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

This work is conducted as part of my MSc thesis at the
[Kriegeskorte Visual Inference Lab](https://kriegeskortelab.zuckermaninstitute.columbia.edu/),
Columbia University, Zuckerman Institute.

## Conference Abstract

Stroecker, E., Cheng, F., &amp; Kriegeskorte, N. (2026, August). *Measuring Depth Inversion in the Ames Window
Illusion* [Extended abstract, accepted]. 9th Annual Conference on Cognitive Computational Neuroscience, NYC, USA.
