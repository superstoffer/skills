# Color

Read this when building or reviewing a palette, choosing text colors,
checking contrast, deriving dark mode, or explaining why a color "looks
wrong" in context. Compute, don't recall: `scripts/color.py` converts
OKLCH ⇄ hex and prints WCAG 2 and APCA contrast with no dependencies.

## Why OKLCH, with the numbers

HSL's L is a coordinate of the RGB cube, not a measure of perceived
lightness. Two colors at `hsl(h 100% 50%)`:

| HSL | Hex | OKLCH L |
|---|---|---|
| `hsl(60 100% 50%)` yellow | `#ffff00` | **0.97** |
| `hsl(240 100% 50%)` blue | `#0000ff` | **0.45** |

Same HSL lightness, one is nearly white and the other nearly as dark as
mid-gray. Any palette derived by "same S and L, different H" — status
colors, chart series, tag colors — therefore has wildly uneven weight,
and the yellow/green members fail contrast that the blue members pass.

OKLCH (a polar form of OKLab, Ottosson 2020) has a lightness axis that
tracks perception, a chroma axis that is roughly uniform across hues, and
a hue axis that stays constant when lightness changes (HSL's hue drifts:
darken a blue in HSL and it turns purple). Supported in every current
browser since 2023; `scripts/color.py` gives hex fallbacks.

### Worked example — lightness held constant across hues

`oklch(0.65 0.15 H)`:

| H | Hex | Role |
|---|---|---|
| 25 | `#dc655f` | red |
| 145 | `#4aa651` | green |
| 250 | `#3a93e6` | blue |
| 320 | `#b76ec7` | magenta |

Squint at all four: same gray. Their HSL lightness values range from 51%
to 62% and their perceived weight would differ far more if picked in HSL.
Note hue 85 (yellow) at this chroma is *outside sRGB*: yellow only reaches
high chroma at high lightness. That is a fact about the gamut, not a bug;
lower C or raise L for yellows and cyans.

### Worked example — status colors that weigh the same

`oklch(0.60 0.14 H)`: danger 25 `#c65954`, success 145 `#419547`,
info 250 `#3284d0`, warning 60 `#bb6802`. All four are in gamut and
carry equal weight, so a row of status pills does not have one shouting
member.

### Worked example — a brand ramp, chroma tapered at the ends

Chroma must fall toward white and black or the ramp leaves sRGB.

| Step | OKLCH | Hex |
|---|---|---|
| 50 | `oklch(0.97 0.012 250)` | `#eff6fd` |
| 100 | `oklch(0.93 0.03 250)` | `#d9eafc` |
| 200 | `oklch(0.87 0.06 250)` | `#b7d8fb` |
| 300 | `oklch(0.78 0.11 250)` | `#80bdfb` |
| 400 | `oklch(0.68 0.15 250)` | `#449df0` |
| 500 | `oklch(0.58 0.16 250)` | `#0d7dd4` |
| 600 | `oklch(0.50 0.14 250)` | `#0465af` |
| 700 | `oklch(0.42 0.11 250)` | `#0e4f86` |
| 800 | `oklch(0.34 0.09 250)` | `#073964` |
| 900 | `oklch(0.26 0.07 250)` | `#022544` |

White on 500 is 4.28:1 and 500 on white is 4.28:1 — both short of AA.
Both the button fill and the text accent therefore use 600 (6.02:1 with
white, APCA Lc −85); 500 is the hover and decorative step, 700 the hover
for 600. Chosen by measurement, not by which step "looks like the brand".

### Worked example — neutrals with a trace of hue

Pure grays look dead next to a chromatic accent. `oklch(L 0.01 250)`:
`0.96 → #edf2f8`, `0.92 → #e0e5eb`, `0.72 → #a0a5ab`, `0.55 → #6d7277`,
`0.42 → #494e52`, `0.22 → #171b1f`. Chroma 0.01–0.02 is enough; more and
the neutrals become a second color.

## Albers — color is relative

**Simultaneous contrast**: a color is perceived relative to what
surrounds it. One gray on white and on navy are two different grays; a
muted text color that reads fine on a white card looks heavier on a
tinted page. Consequence: judge colors *in context* and *in pairs*, never
as swatches; test `--color-text-muted` on every surface it will sit on.
Above, `#6d7277` is 4.86:1 on white but 4.32:1 on `#edf2f8` — a token
that passes on one surface fails on the next.

**Bezold effect**: thin lines and patterns shift the perceived color of
the area they cross. A hairline border, a subtle stripe, or a grid changes
how a surface reads. This is why "add a border to separate it" often
changes the surface's apparent color more than its separation.

## Helmholtz–Kohlrausch effect

Saturated colors look brighter than a gray of the same luminance.
`#e11d48` (red, C 0.22) and `#767676` (gray) have near-identical WCAG
ratios on white — 4.70:1 and 4.54:1 — yet the red reads as far lighter
and more vivid. Consequences: chromatic text on white feels lower-contrast
than its ratio says; light text on a saturated background feels *higher*
contrast than its ratio says (the "white on orange fails WCAG but looks
fine" argument). Design with the effect, comply with the ratio.

## WCAG 2 and APCA

**WCAG 2** contrast ratio, (L₁ + 0.05)/(L₂ + 0.05): 4.5:1 for text,
3:1 for large text (≥ 24px, or ≥ 18.66px bold) and for UI component
boundaries, 7:1 for AAA. It is symmetric (ignores which color is text),
ignores polarity (dark-on-light vs light-on-dark), and is a step
function. It is the legal baseline in most jurisdictions (ADA case law,
EN 301 549 / European Accessibility Act, Section 508). Ship nothing
below it without a documented reason.

**APCA** (Accessible Perceptual Contrast Algorithm, a candidate method for
future accessibility guidance) returns Lc, a signed lightness contrast,
polarity-aware and weight/size-aware. For a reference sans: Lc 90 supports
body text at 14px/400, Lc 75 at 18px/400, Lc 60 at 24px/400 or 16px/700,
and Lc 45 at 36px/400 or 24px/700. Lc 30 is for non-content text and solid
non-text elements; Lc 15 is the approximate invisibility point. Use the
full font lookup table when the exact size or weight matters.

Where they disagree, and what to do:

| Pair | WCAG 2 | APCA Lc | Read |
|---|---|---|---|
| `#777777` on white | 4.48 (fail by 0.02) | +71 | fails both for 16px body; `#767676` fixes WCAG only, while about `#4a4a4a` is needed to reach Lc 90 |
| `#ffffff` on `#f97316` | 2.80 (fail) | −58 | below even WCAG's 3:1 large-text floor; use dark text (6.2:1) or darken the orange |
| `#a1a1aa` on `#18181b` | 6.91 (pass) | −51 | WCAG overstates light-on-dark; muted text in dark mode needs to be lighter than the ratio suggests |
| `#25f36a` on `#fafafa` | 1.43 | +19 | invisible by both; neon green checkmarks |

Rule: WCAG 2 is the floor you must pass; APCA is how you tune within and
above it. When APCA says a passing pair is weak, make it stronger. Size and
weight can select a lower APCA target, but the pair must still meet the
applicable WCAG 2 ratio; otherwise change the color.

## Distribution — 60-30-10

60% dominant (page and surface neutrals), 30% secondary (text, borders,
secondary surfaces), 10% accent. In product UI the accent is usually under
5%: a button, a link color, a focus ring, a selected state. If the accent
appears on more than one *element* in a view, it has stopped being an
accent. Status colors are not accents; they are a separate 10% that
appears only when a status exists.

## Dark mode

Not an inversion. The semantic tier is remapped (`tokens-and-systems.md`):

- **Background** `oklch(0.16–0.20 0.015 H)`, not `#000`. Pure black makes
  every surface a hole and halates light text.
- **Surfaces lighten with elevation**: `--gray-950` (0.16) page →
  `--gray-900` (0.20) card → `--gray-850` (0.24) raised/menu, as in the
  token example in `tokens-and-systems.md`. Shadows barely read on dark;
  lightness carries elevation.
- **Text** `oklch(0.93–0.96)`, not `#fff`. At 14px/400 even muted text
  needs about `0.93` (APCA −91 on a `0.24` raised surface); larger or
  heavier copy can step down after checking the full APCA lookup table.
  Small dark-mode text cannot be dimmed much without losing legibility.
- **Accent lightens** two ramp steps (500 → 300) so it keeps contrast on
  dark surfaces; on-accent text flips to dark.
- **Large chromatic areas desaturate** slightly (drop C by ~0.03); small
  ones keep chroma.
- **Borders** as `oklch(1 0 0 / 0.10)` alpha so they read on any surface.
- **Images** dim slightly (`filter: brightness(0.9)`) so white photos do
  not glare.

## Gradients

See `optical-correction.md` for interpolation space. Short form:
`linear-gradient(in oklch, A, B)`; add a middle stop when the midpoint
hue leaves the gamut; keep the lightness delta across a gradient under
~0.15 if text sits on it.

## Checking

`S` is the skill directory (the folder holding `SKILL.md`).

```
python3 $S/scripts/color.py oklch 0.58 0.16 250          # → #0d7dd4
python3 $S/scripts/color.py hex '#f97316'                 # → oklch(0.705 0.187 47.6)
python3 $S/scripts/color.py contrast '#6d7277' '#fff' '#fff' '#0465af'   # one line per pair
python3 $S/scripts/color.py contrast 'oklch(1 0 0 / 0.10)' 'oklch(0.20 0.015 250)'  # alpha composited
python3 $S/scripts/color.py palette 0.60 0.14 25 145 250 60
python3 $S/scripts/color.py ramp 250 0.16 0.97 0.87 0.78 0.68 0.58
```

- `contrast` takes any number of FG BG pairs and any CSS hex or `oklch()`
  form, including `/ alpha` and `none`. A translucent foreground is
  composited over the background first; the background must be opaque.
- Ratios are computed on the 8-bit hex printed beside them — the value
  that ships — so a pass never flips when the color is later written as hex.
- Out-of-gamut input is never scored silently. The script prints the
  clipped hex browsers paint today, the largest chroma that stays in gamut
  at that L and H, and marks the verdict unreliable. Reduce chroma to the
  reported maximum and re-run; CSS Color 4 gamut mapping and per-channel
  clipping disagree, so no out-of-gamut token is safe in any browser.
