---
layout: page
title: RetinoType
description: A population-receptive-field fMRI brain–computer interface for spelling with imagined letters
img: /assets/img/imspell_preview.webp
importance: 1
---

## Overview

When you *imagine* a letter, early visual cortex lights up in almost the same
retinotopically-organised pattern as when you actually *see* it. Using
ultra-high-field (7&nbsp;T) fMRI,
[Senden et&nbsp;al. (2019)](https://doi.org/10.1007/s00429-019-01828-6) showed
that an imagined letter can be reconstructed from the very same
[population-receptive-field (pRF)](https://doi.org/10.1016/j.neuroimage.2007.09.034)
mapping of the visual field that describes perception.

**RetinoType** asks whether that correspondence can be turned into a *content-based*
brain–computer interface: a speller in which you simply picture the letter you
want, and it is read directly out of visual cortex — rather than mapping
arbitrary, effortful mental tasks onto letters, as earlier fMRI spellers do.

<div style="text-align:center; margin: 1.5rem 0;">
  <img src="/assets/img/imspell_pipeline.png" alt="RetinoType pipeline: pRF encoding, alphabet simulation, perception-to-imagery transfer, decoding, and language-model correction" style="max-width:100%; border-radius:8px;">
</div>

## How it works

1. **Extract each subject's pRF map** — the receptive-field location and size of
   every unit in early visual cortex (V1–V3).

2. **Simulate the whole alphabet.** The original experiment only presented four
   letters (H, T, S, C). But a subject's pRF map lets us *predict* the cortical
   response to any letter that was never shown — encoding each of the 26 letters
   into a simulated brain response, then reconstructing the visual field back
   out of it (below).

3. **Transfer perception → imagery.** Imagined letters are far weaker and noisier
   than perceived ones. We estimate the signal-degradation profile that separates
   seeing a letter from imagining it — calibrated on the letters that *were*
   imagined in the scanner (H, T, S, C) — and extrapolate it to the remaining 22,
   producing as-authentic-as-possible simulated imagery responses.

4. **Decode in conversational context.** Because imagery signals are blurry and
   letters are easily confused, we don't decode letters in isolation. We fold in
   a large language model that integrates conversational context and each
   subject's letter-confusion matrix, collapsing the space of possibilities onto
   the most likely intended message.

5. **Evaluate on conversations, not characters.** The paradigm is scored not on
   isolated per-letter accuracy but on how reliably whole simulated questions and
   answers — spanning common and uncommon phrasings — are recovered.

## Simulating cortical responses to every letter

Each letter is rendered as a stimulus, encoded through the subject's pRF model
into a simulated early-visual-cortex response, and then reconstructed back into a
visual-field image. Reconstruction requires a cortical-magnification correction —
the fovea is vastly over-represented in cortex, so a naive read-out is
geometrically distorted until that sampling bias is undone.

<div style="text-align:center; margin: 1.5rem 0;">
  <img src="/assets/img/imspell_alphabet_sim.png" alt="Per-letter simulation: stimulus, naive back-projection, and distortion-corrected reconstruction for A–Z" style="max-width:100%; border-radius:8px;">
</div>

The preview image for this project is made the same way — *RETINO&nbsp;/&nbsp;TYPE*
spelled out entirely in reconstructed, brain-decoded letters.

## Why it matters

Conventional BCI spellers make you spell *indirectly*. Rather than reading out the
letter you intend, they map arbitrary or effortful mental tasks onto letters
([Sorger et&nbsp;al., 2012](https://doi.org/10.1016/j.cub.2012.05.022)) and narrow
the alphabet down over several trials, each ruling out a fraction of the
candidates. If every trial keeps, say, a third of the options, isolating one letter
out of 26 takes

$$
26 \cdot 3^{-n} = 1 \quad\Longrightarrow\quad n = \log_3 26 \approx 3
$$

three trials — and each trial is slow: Sorger et&nbsp;al.'s fMRI speller needed at
least **50&nbsp;seconds to encode a single letter**. Between memorising a code and
the trials-per-letter overhead, spelling this way is both effortful and slow.

A pRF-based, *content-based* approach instead aims to produce a uniquely
identifiable signal for the intended letter in a *single* trial — decoding the
*shape* you actually picture. Paired with a language model that exploits
conversational context, this promises communication that is both more intuitive
and more time-efficient, for healthy and clinical populations alike.

## Toward a portable device

fMRI is powerful but immobile and costly. Encouragingly, the same protocol
transfers directly to portable optical imaging. Functional near-infrared
spectroscopy (fNIRS) — in particular High-Density Diffuse Optical Tomography
(HD-DOT; Frijia et&nbsp;al., 2020) and Time-Domain fNIRS (TD-fNIRS; Torricelli
et&nbsp;al., 2013) — can now reach deeper cortex at comparatively high spatial
resolution (Oveisi et&nbsp;al., 2024). Conceptually, an HD-DOT / TD-fNIRS variant
runs the very same encode → reconstruct → decode pipeline. If it holds up, a
content-based imagery speller could give people with locked-in syndrome or similar
conditions a far more convenient and cost-effective way to communicate.

## Data & methods

The work builds a fully-reproducible pipeline on two independent 7&nbsp;T datasets.
The [Senden&nbsp;et&nbsp;al. (2019)](https://doi.org/10.1007/s00429-019-01828-6)
data provides, for each of six subjects, retinotopy, letter-*perception* (letters
shown on screen) and letter-*imagery* (letters pictured from memory) trials —
although only four letters (**H, T, S, C**) were ever presented. To this we add the
[LAION-fMRI](https://laion-fmri.hebartlab.com/) retinotopy dataset, converging on a
shared surface-based pRF analysis (DICOM → BIDS conversion, anatomy typing,
per-trial event decoding).

Two limitations of the scanner data motivate the simulation-first design: only four
of the 26 letters were collected, and imagined letters are intrinsically hard to
decode — a noisy-channel problem that has cast doubt on their fitness for a BCI.
Simulating the full alphabet from each subject's pRF map, and decoding in
conversational context, are precisely the moves that work around those two limits.

This work is conducted at the
[Kriegeskorte Visual Inference Lab](https://kriegeskortelab.zuckermaninstitute.columbia.edu/),
Columbia University, Zuckerman Institute.
