#!/usr/bin/env python3
"""Fetch + optimise the stimuli for the embedded angle-matching demo (24 trials).

Gauge arc: the response gauge spans 180 deg (surface orientation is
180-symmetric). Sampled at 5 deg: frame i (0..36) <-> orientation -90+5i deg
<-> source reference frame (270+5i) % 360.

Probe frames are restricted to multiples of 5 (so the folded true orientation
lands exactly on the gauge grid) and avoid the experiment's +-4 frame exclusion
zone around frames 30 and 90.

Source frames are 512x512 (gauge is RGBA with real transparency; probes are
already baked onto #272727). The demo shows them ~300 CSS px, so everything is
composited onto the experiment background, downscaled and re-encoded lossy.
"""
import io
import json
import urllib.request
from pathlib import Path

from PIL import Image

R2 = "https://pub-9b73eb88ce514ce48d5167e1c9702609.r2.dev"
SITE = Path("/Users/emil/Docs/Webpage/EmilStroecker.github.io")
OUT = SITE / "assets/img/ames_demo"
MANIFEST = Path("/Users/emil/Docs/RMCogNeuro/20252026/VIL Internship/Webpage/manifest.json")

SIZE = 360
QUALITY = 82
STEP = 5
BG = (39, 39, 39)          # experiment background #272727

GAUGE_VARIANT = "voronoi_flat"
# The study pairs a window probe with a circle gauge and circle/dots with a
# diamond gauge, so the gauge shape never matches the probe shape.
GAUGE_FOR = {"window": "circle", "circle": "diamond", "dots": "diamond"}
LABEL_FOR = {"window": "Window", "circle": "Ring", "dots": "Dots"}
PER_CATEGORY = 8


def fetch(url):
    # r2.dev 403s the default urllib User-Agent.
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def save_web(raw, dest):
    im = Image.open(io.BytesIO(raw))
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGBA", im.size, BG + (255,))
        im = Image.alpha_composite(bg, im.convert("RGBA"))
    im = im.convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=QUALITY, method=6)
    return dest.stat().st_size


def valid_frames():
    return [f for f in range(120)
            if f % 5 == 0 and not (abs(f - 30) <= 4 or abs(f - 90) <= 4)]


def select():
    conds = json.loads(MANIFEST.read_text())["conditions"]
    chosen = []
    for cat in ("window", "circle", "dots"):
        cc = sorted((c for c in conds if c["category"] == cat),
                    key=lambda c: c["stimulus_params"]["depth_slant_deg"])
        idxs = [round(i * (len(cc) - 1) / (PER_CATEGORY - 1)) for i in range(PER_CATEGORY)]
        chosen.extend(cc[i] for i in idxs)

    frames = valid_frames()
    trials = []
    for k, c in enumerate(chosen):
        f = frames[(k * 7) % len(frames)]
        truth = (f * 3) % 180
        if truth > 90:
            truth -= 180
        cat = c["category"]
        trials.append({
            "slug": f"{cat}{k:02d}",
            "render_path": c["render_path"],
            "frame": f,
            "truth": truth,
            "gauge": GAUGE_FOR[cat],
            "label": LABEL_FOR[cat],
            "slant": c["stimulus_params"]["depth_slant_deg"],
        })
    return trials


def main():
    total = 0
    n_arc = 180 // STEP + 1

    for shape in sorted(set(GAUGE_FOR.values())):
        key = f"{shape}_{GAUGE_VARIANT}"
        for i in range(n_arc):
            src = (270 + STEP * i) % 360
            total += save_web(fetch(f"{R2}/stimuli/reference/{key}/{src + 1:04d}.webp"),
                              OUT / "gauge" / shape / f"{i:02d}.webp")
        print(f"gauge/{shape}: {n_arc} frames")

    trials = select()
    for t in trials:
        url = f"{R2}/{t['render_path']}/{t['frame'] + 1:04d}.webp"
        total += save_web(fetch(url), OUT / "probe" / f"{t['slug']}.webp")
    print(f"probes: {len(trials)}")

    # Compact client-side trial list (no absolute paths, no study internals).
    compact = [[t["slug"], t["gauge"], t["truth"], t["label"]] for t in trials]
    (OUT / "trials.json").write_text(json.dumps(compact, separators=(",", ":")))
    total += (OUT / "trials.json").stat().st_size

    print(f"\ntotal {total/1024:.0f} KB in {OUT}")
    print("truths:", sorted(t["truth"] for t in trials))


if __name__ == "__main__":
    main()
