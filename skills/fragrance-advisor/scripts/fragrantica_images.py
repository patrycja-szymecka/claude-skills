#!/usr/bin/env python3
"""Fetch and prepare Fragrantica images for the fragrance report.

Subcommands
  notes   ID [ID ...]      download note photos and turn them into one-colour engravings (transparent PNG)
  bottles ID [ID ...]      download perfume bottle photos (JPEG, white background)
  botanical ID [ID ...]    botanical plate of a note: thin burgundy lines + soft colour wash on paper (JPEG)
  embed   IN.html -o OUT   replace {{IMG_<perfume id>}}, {{NOTE_<note id>}} and {{BOT_<note id>}} placeholders with
                           data: URIs, downloading and processing whatever is not cached yet

IDs
  perfume id: the number at the end of the perfume URL, e.g. .../Orange-Smoke-78408.html -> 78408
  note id:    the number in the note image URL on a perfume page, e.g. .../sastojci/t.16.jpg -> 16
              (on a perfume page: img[src*="sastojci"], its alt text is the note name)

Requires Pillow and numpy (pip install pillow numpy).
"""
import argparse
import base64
import io
import re
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

NOTE_URLS = ["https://fimgs.net/mdimg/sastojci/o.{id}.jpg", "https://fimgs.net/mdimg/sastojci/t.{id}.jpg"]
BOTTLE_URL = "https://fimgs.net/mdimg/perfume/375x500.{id}.jpg"
HEADERS = {"Referer": "https://www.fragrantica.com/", "User-Agent": "Mozilla/5.0"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def fetch_first(urls):
    last = None
    for u in urls:
        try:
            return fetch(u)
        except Exception as e:  # try the next size
            last = e
    raise RuntimeError(f"could not download any of {urls}: {last}")


def hex_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def engrave(img: Image.Image, size=220, colour="#632C35", line_gain=2.1, tone_max=0.45) -> Image.Image:
    """Photo on white -> single-colour engraving on transparency.

    Alpha = combination of Sobel edges (the 'lines') and inverted luminance (soft 'shading'),
    so white backgrounds vanish and white flowers still keep their contours.
    """
    grey = img.convert("L").resize((size, size), Image.LANCZOS).filter(ImageFilter.BoxBlur(1))
    b = np.asarray(grey, dtype=np.float64) / 255.0
    p = np.pad(b, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    edges = np.clip(np.hypot(gx, gy) * line_gain, 0, 1)
    tone = (1 - b) ** 1.3 * tone_max
    alpha = 1 - (1 - edges) * (1 - tone)
    alpha[0, :] = alpha[-1, :] = alpha[:, 0] = alpha[:, -1] = 0
    r, g, bl = hex_rgb(colour)
    out = np.zeros((size, size, 4), dtype=np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = r, g, bl
    out[..., 3] = np.round(alpha * 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def _smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def botanical(img: Image.Image, size=460, line_colour="#5A2630", paper="#F4EEE5",
              t0=0.045, gain=7.0, wash=0.75, paper_mix=0.25, fade=0.10) -> Image.Image:
    """Photo on white -> botanical plate: thin burgundy contour lines over a soft, desaturated colour wash,
    composited onto the paper colour (JPEG-friendly). Edges fade out so cropped subjects don't end in a hard line."""
    rgb = np.asarray(img.convert("RGB").resize((size, size), Image.LANCZOS), dtype=np.float64) / 255.0
    lum = rgb @ np.array([0.299, 0.587, 0.114])
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0)
    grey = Image.fromarray(np.round(lum * 255).astype(np.uint8), "L").filter(ImageFilter.BoxBlur(1)).filter(ImageFilter.BoxBlur(1))
    b = np.asarray(grey, dtype=np.float64) / 255.0
    p = np.pad(b, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    line = np.clip((np.hypot(gx, gy) - t0) * gain, 0, 1)
    ink = np.maximum(1 - _smooth(0.86, 0.97, b), _smooth(0.10, 0.25, sat))
    yy, xx = np.mgrid[0:size, 0:size]
    edge = np.minimum(np.minimum(xx, size - 1 - xx), np.minimum(yy, size - 1 - yy)) / size
    ef = _smooth(0, fade, edge)
    wa = (wash * ink * ef)[..., None]
    la = (line * 0.92 * ef)[..., None]
    paper_rgb = np.array(hex_rgb(paper)) / 255.0
    line_rgb = np.array(hex_rgb(line_colour)) / 255.0
    washed = lum[..., None] + (rgb - lum[..., None]) * 0.55          # half-desaturate
    washed = washed * (1 - paper_mix) + paper_rgb * paper_mix         # pull toward paper
    a = la + wa * (1 - la)
    colour = np.where(a > 0, (line_rgb * la + washed * wa * (1 - la)) / np.maximum(a, 1e-9), paper_rgb)
    out = colour * a + paper_rgb * (1 - a)
    return Image.fromarray(np.round(np.clip(out, 0, 1) * 255).astype(np.uint8), "RGB")


def note_botanical(note_id: str, cache: Path) -> Path:
    dst = cache / f"botanical-{note_id}.jpg"
    if not dst.exists():
        raw = fetch_first([u.format(id=note_id) for u in NOTE_URLS])
        botanical(Image.open(io.BytesIO(raw))).save(dst, quality=86)
    return dst


def note_png(note_id: str, cache: Path, **kw) -> Path:
    dst = cache / f"note-{note_id}.png"
    if not dst.exists():
        raw = fetch_first([u.format(id=note_id) for u in NOTE_URLS])
        engrave(Image.open(io.BytesIO(raw)), **kw).save(dst, optimize=True)
    return dst


def bottle_jpg(perfume_id: str, cache: Path) -> Path:
    dst = cache / f"bottle-{perfume_id}.jpg"
    if not dst.exists():
        dst.write_bytes(fetch(BOTTLE_URL.format(id=perfume_id)))
    return dst


def data_uri(path: Path) -> str:
    mime = "image/png" if path.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache", default="fragrantica-images", help="folder for downloaded and processed images")
    ap.add_argument("--colour", default="#632C35", help="engraving colour (hex)")
    ap.add_argument("--size", type=int, default=220, help="engraving size in px")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("notes"); n.add_argument("ids", nargs="+")
    b = sub.add_parser("bottles"); b.add_argument("ids", nargs="+")
    bt = sub.add_parser("botanical"); bt.add_argument("ids", nargs="+")
    e = sub.add_parser("embed"); e.add_argument("html"); e.add_argument("-o", "--out", required=True)
    a = ap.parse_args(argv)

    cache = Path(a.cache); cache.mkdir(parents=True, exist_ok=True)
    kw = dict(size=a.size, colour=a.colour)

    if a.cmd == "notes":
        for i in a.ids:
            print(note_png(i, cache, **kw))
    elif a.cmd == "bottles":
        for i in a.ids:
            print(bottle_jpg(i, cache))
    elif a.cmd == "botanical":
        for i in a.ids:
            print(note_botanical(i, cache))
    else:
        html = Path(a.html).read_text(encoding="utf-8")
        failed = []

        def sub_img(m):
            try:
                return data_uri(bottle_jpg(m.group(1), cache))
            except Exception as ex:
                failed.append(f"bottle {m.group(1)}: {ex}"); return ""

        def sub_note(m):
            try:
                return data_uri(note_png(m.group(1), cache, **kw))
            except Exception as ex:
                failed.append(f"note {m.group(1)}: {ex}"); return ""

        def sub_bot(m):
            try:
                return data_uri(note_botanical(m.group(1), cache))
            except Exception as ex:
                failed.append(f"botanical {m.group(1)}: {ex}"); return ""

        html = re.sub(r"\{\{IMG_(\d+)\}\}", sub_img, html)
        html = re.sub(r"\{\{NOTE_(\d+)\}\}", sub_note, html)
        html = re.sub(r"\{\{BOT_(\d+)\}\}", sub_bot, html)
        Path(a.out).write_text(html, encoding="utf-8")
        print(f"wrote {a.out} ({len(html) // 1024} KB)")
        if failed:
            print("missing images (left empty):\n  " + "\n  ".join(failed), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
