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

<div style="text-align:center; margin: 1.5rem 0;">
  <img src="/assets/img/Ames_demo.gif" alt="Rotating Ames Window stimulus" style="max-width:100%; border-radius:8px;">
</div>

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
