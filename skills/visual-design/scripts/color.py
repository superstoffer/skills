#!/usr/bin/env python3
"""Dependency-free color math for the visual-design skill.

  color.py oklch L C H                 -> hex the browser paints, or a gamut warning
  color.py hex COLOR                   -> oklch(L C H) of any color
  color.py contrast FG BG [FG BG ...]  -> WCAG 2 ratio and APCA Lc per pair (fg on bg)
  color.py palette L C H [H ...]       -> one hex per hue at fixed L and C
  color.py ramp H C L [L ...]          -> one hex per lightness at fixed hue

COLOR is CSS: '#rgb', '#rrggbb', '#rrggbbaa', or 'oklch(L C H [/ A])' with %,
deg/grad/rad/turn and 'none' accepted. Numeric CLI arguments take the same
units (65%, 250deg).

Contrast is computed on the 8-bit sRGB value that ships, so the ratio always
describes the hex printed beside it. A translucent foreground is composited
over the background first; the background must be opaque.

Out-of-gamut OKLCH is reported, not blessed: browsers currently paint the
per-channel clip, CSS Color 4 specifies chroma reduction, and the two differ.
The script prints the clipped hex the browser paints plus the largest chroma
that stays in gamut at that L and H, and marks any verdict on such a pair.

OKLab math from Bjorn Ottosson; APCA constants from APCA-W3 0.1.9 (0.0.98G-4g).
"""
import math
import os
import re
import sys

NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"


# ---------------------------------------------------------------- transforms

def _srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def oklch_to_rgb(L, C, H):
    """Linear sRGB floats; may fall outside 0..1 when out of gamut."""
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def rgb_to_oklch(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def in_gamut(rgb, tol=1e-6):
    return all(-tol <= c <= 1 + tol for c in rgb)


def clip(rgb):
    return tuple(min(1.0, max(0.0, c)) for c in rgb)


def max_chroma(L, H, tol=1e-4):
    """Largest chroma at this L and H that stays inside sRGB."""
    if L <= 0 or L >= 1:
        return 0.0
    lo, hi = 0.0, 0.5
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if in_gamut(oklch_to_rgb(L, mid, H)):
            lo = mid
        else:
            hi = mid
    return lo


def quantize(rgb):
    """Round linear floats to the 8-bit sRGB the browser rasterizes."""
    return tuple(_srgb_to_linear(round(_linear_to_srgb(c) * 255) / 255) for c in clip(rgb))


def to_hex(rgb):
    return "#" + "".join(f"{round(_linear_to_srgb(c) * 255):02x}" for c in clip(rgb))


# ------------------------------------------------------------------- parsing

class Color:
    """8-bit-quantized linear rgb, alpha, and gamut diagnostics."""

    def __init__(self, rgb, alpha=1.0, oog=None):
        self.rgb = quantize(rgb)
        self.alpha = alpha
        self.oog = oog  # None, or (L, H, requested C, max in-gamut C)

    @property
    def hex(self):
        return to_hex(self.rgb)

    def note(self):
        if not self.oog:
            return ""
        L, H, C, cmax = self.oog
        return f"  [out of sRGB gamut: painted as clipped {self.hex}; max chroma at L {L:.2f} H {H:.0f} is {cmax:.3f}, requested {C:.3f}]"


def parse_number(text, kind):
    """Parse a CSS number with an optional unit for L, C or H."""
    m = re.fullmatch(rf"({NUMBER})(%|deg|grad|rad|turn)?", text.strip(), re.IGNORECASE)
    if text.strip().lower() == "none":
        return 0.0
    if not m:
        raise ValueError(f"not a number: {text!r}")
    value, unit = float(m.group(1)), (m.group(2) or "").lower()
    if kind == "L":
        if unit == "%":
            value /= 100
        elif unit:
            raise ValueError(f"lightness cannot take unit {unit!r}")
        return min(1.0, max(0.0, value))  # CSS clamps L to 0..1
    if kind == "C":
        if unit == "%":
            value *= 0.004
        elif unit:
            raise ValueError(f"chroma cannot take unit {unit!r}")
        return max(0.0, value)  # CSS clamps negative chroma to 0
    if kind == "H":
        return {"": value, "deg": value, "grad": value * 0.9,
                "rad": math.degrees(value), "turn": value * 360}[unit] % 360
    if kind == "A":
        return min(1.0, max(0.0, value / 100 if unit == "%" else value))
    raise ValueError(kind)


def from_oklch(L, C, H, alpha=1.0):
    rgb = oklch_to_rgb(L, C, H)
    oog = None if in_gamut(rgb) else (L, H, C, max_chroma(L, H))
    return Color(rgb, alpha, oog)


def parse(text):
    text = text.strip()
    m = re.fullmatch(r"#?([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})", text)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        rgb = tuple(_srgb_to_linear(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))
        alpha = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return Color(rgb, alpha)
    m = re.fullmatch(r"oklch\(\s*([^\s,/]+)[\s,]+([^\s,/]+)[\s,]+([^\s,/]+)\s*(?:/\s*([^\s)]+))?\s*\)", text, re.IGNORECASE)
    if m:
        L, C, H = (parse_number(v, k) for v, k in zip(m.groups()[:3], "LCH"))
        alpha = parse_number(m.group(4), "A") if m.group(4) else 1.0
        return from_oklch(L, C, H, alpha)
    raise ValueError(f"cannot parse color: {text!r}")


# ------------------------------------------------------------------ contrast

def composite(fg, bg):
    if bg.alpha < 1:
        raise ValueError("background must be opaque; composite it over the page color first")
    if fg.alpha >= 1:
        return fg
    a = fg.alpha
    return Color(tuple(a * f + (1 - a) * b for f, b in zip(fg.rgb, bg.rgb)), 1.0, fg.oog)


def wcag(fg, bg):
    def lum(c):
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    l1, l2 = sorted((lum(fg.rgb), lum(bg.rgb)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def apca(fg, bg):
    """APCA Lc for text (fg) on background (bg). Positive = dark on light."""
    def y(c):
        srgb = [_linear_to_srgb(v) for v in c.rgb]  # APCA uses a plain 2.4 curve
        return 0.2126729 * srgb[0] ** 2.4 + 0.7151522 * srgb[1] ** 2.4 + 0.0721750 * srgb[2] ** 2.4

    def soft_clamp(v):
        return v if v >= 0.022 else v + (0.022 - v) ** 1.414

    ytxt, ybg = soft_clamp(y(fg)), soft_clamp(y(bg))
    if abs(ybg - ytxt) < 0.0005:
        return 0.0
    if ybg > ytxt:
        sapc = (ybg ** 0.56 - ytxt ** 0.57) * 1.14
        return 0.0 if sapc < 0.1 else (sapc - 0.027) * 100
    sapc = (ybg ** 0.65 - ytxt ** 0.62) * 1.14
    return 0.0 if sapc > -0.1 else (sapc + 0.027) * 100


def contrast_line(fg, bg):
    fg_c = composite(fg, bg)
    alpha_note = f"  (fg alpha {fg.alpha:.2f} composited over bg)" if fg.alpha < 1 else ""
    verdict = "" if not (fg.oog or bg.oog) else "  VERDICT UNRELIABLE: out-of-gamut input"
    return (f"WCAG 2  {wcag(fg_c, bg):.2f}:1   APCA Lc {apca(fg_c, bg):+.1f}   "
            f"({fg_c.hex} on {bg.hex}){alpha_note}{verdict}{fg.note()}{bg.note()}")


# ----------------------------------------------------------------------- cli

def _need(args, n, usage):
    if len(args) < n:
        raise ValueError(f"usage: color.py {usage}")


def run(argv):
    if not argv:
        raise ValueError(__doc__)
    cmd, args = argv[0], argv[1:]
    if cmd == "oklch":
        _need(args, 3, "oklch L C H")
        c = from_oklch(*(parse_number(v, k) for v, k in zip(args[:3], "LCH")))
        return [c.hex + c.note()]
    if cmd == "hex":
        _need(args, 1, "hex COLOR")
        c = parse(args[0])
        L, C, H = rgb_to_oklch(*c.rgb)
        return [f"oklch({L:.3f} {C:.3f} {H:.1f})" + c.note()]
    if cmd == "contrast":
        _need(args, 2, "contrast FG BG [FG BG ...]")
        if len(args) % 2:
            raise ValueError("contrast takes pairs: FG BG [FG BG ...]")
        return [contrast_line(parse(args[i]), parse(args[i + 1])) for i in range(0, len(args), 2)]
    if cmd in ("palette", "ramp"):
        _need(args, 3, f"{cmd} {'L C H [H ...]' if cmd == 'palette' else 'H C L [L ...]'}")
        if cmd == "palette":
            L, C = parse_number(args[0], "L"), parse_number(args[1], "C")
            triples = [(L, C, parse_number(h, "H")) for h in args[2:]]
        else:
            H, C = parse_number(args[0], "H"), parse_number(args[1], "C")
            triples = [(parse_number(l, "L"), C, H) for l in args[2:]]
        out = []
        for L, C, H in triples:
            c = from_oklch(L, C, H)
            out.append(f"oklch({L:.3f} {C:.3f} {H:>5.1f})  {c.hex}" + c.note())
        return out
    raise ValueError(__doc__)


def main(argv):
    try:
        for line in run(argv[1:]):
            print(line)
    except ValueError as e:
        sys.exit(f"{e}\n" if str(e).startswith("usage") or str(e).startswith("Dependency") else f"error: {e}")


if __name__ == "__main__":
    main(sys.argv)
