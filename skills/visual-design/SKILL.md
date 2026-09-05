---
name: visual-design
description: >-
  Apply professional visual design judgment when building or refining
  anything with a visual surface — a UI, component, page, landing page,
  email, slide, chart, or design-token setup. Use when the request involves
  layout, spacing, typography, color, contrast, dark mode, shadows, radii,
  hierarchy, hover/focus/active states, or a critique of an existing screen,
  and for requests like "make this look better", "polish this", "clean up
  this component" (when the mess is visual), "build a landing page", or
  "what looks off here" even when the word design never appears. Also use
  when choosing a type scale, grid, palette, or token structure, or when a
  spacing or size value must land on the system. NOT for logic, backend,
  data, or CLI work with no visual output.
---

# Visual Design

Consistency does the work. A scale, a unit, one accent, one light source —
applied without exception — beats any individual clever choice. Then an
optical pass fixes what measures right but looks wrong.

## What this skill does not do

It does not teach the mechanics Claude already gets right unaided — type
scales, spacing grids, WCAG arithmetic, leading and tracking, dark-mode
remapping. Those live in the references as worked examples. The hard rules
below cover only what the baseline runs got wrong: color chosen in HSL,
emphasis stacked on one element, and the optical layer skipped. The
baseline evidence is in the README.

## Hard rules

1. **Palettes are specified in OKLCH.** Equal HSL lightness is not equal
   perceived lightness: `hsl(60 100% 50%)` is OKLCH L 0.97, `hsl(240 100%
   50%)` is L 0.45. Contrast is checked on the 8-bit sRGB value that ships
   either way — `color.py contrast` takes hex or `oklch()` pairs and prints
   WCAG 2 and APCA — so "HSL lets me verify directly" is not a reason. If
   another skill or the brand supplies hex, that is the direction: convert
   it with `color.py hex`, adjust in OKLCH, check. Out-of-gamut colors are
   reported with the largest in-gamut chroma; reduce chroma, never ship
   the flag. The script lives beside this file: run
   `python3 <directory of this SKILL.md>/scripts/color.py`, never a bare
   relative path from the project.
2. **One emphasis device per emphasized element; accent color on one
   element per view.** Isolation only works when one thing is isolated. A
   recommended tier gets a filled button *or* an accent border *or* a lift
   — decide with the five-second test, then remove the others.
3. **The optical pass is mandatory** before reporting done: nested radii,
   gradient interpolation space, optical centering, shadow ladder. See
   below.
4. **Use a scale; never defend a ratio.** Override any step that fails in
   context and say that you did.

## Decision procedure

Top-down. Read a reference only when that step is non-trivial in the task.

| Step | Establish | Read |
|---|---|---|
| 0 | The job, one sentence: "this surface exists so ___ can ___; the one thing to notice is ___." This fixes hierarchy and the single emphasis device. | — |
| 1 | Spacing unit (4/8) and type scale (base, ratio, snapped to integer px). Every later value comes from these two sets. | `references/proportion-and-layout.md` for scales, grids, margins, column math |
| 2 | Palette in OKLCH: neutrals with a trace of brand hue, one accent, status colors at matched L and C. Check every text pair; WCAG 2 is the floor, APCA the tuning. Dark mode remaps the semantic tier only. | `references/color.md` |
| 3 | Type: measure ≤ 60ch, line height and tracking inverse to size, ≤ 3 prominence levels, ≤ 2 families. | `references/typography.md` |
| 4 | Rhythm and structure: inner gaps smaller than outer gaps at every level; parents own sibling spacing; tokens in three tiers. | `references/tokens-and-systems.md`; `references/perception-laws.md` for target size, choice count, response timing |
| 5 | Optical pass. | `references/optical-correction.md` |
| 6 | Critique pass with the checklist below; findings ordered by leverage. | `references/heuristics-and-critique.md` |

## The optical pass

- **Nested radii:** inner = outer − padding. Card 16 with padding 12 → 4.
  When padding ≥ radius the inner value is not derived: choose it for the
  element itself, clearly smaller than the outer. Same radius inside and
  out looks fatter at the inner corner.
- **Gradients:** declare `in oklch` (or `in oklab` for same-hue). sRGB
  interpolation sags mid-way: red → blue through `#800080` is L 0.421
  between endpoints at 0.63 and 0.45; blue → green drops chroma from 0.16
  to 0.09 at the midpoint.
- **Optical center:** ~5% of height above geometric center for modals,
  empty states, icon-in-circle, text in pills. Arrows and triangles nudge
  toward their point.
- **Shadow ladder:** one light source, 2–3 levels, blur ≈ 2–3× y-offset,
  opacity falling as blur grows, contact + ambient layers. Dark mode:
  surfaces lighten with elevation; shadows barely read. Worked ladder in
  `references/optical-correction.md`.
- **Overshoot:** circles and points in an icon set drawn larger than
  squares in the same box (Material keylines: square 18, circle 20, in 24).
- **Weight:** thin or small text looks lighter than its color — darken or
  embolden; 1px borders in dark mode on alpha, not gray.

## Worked numbers

- **1.25 from 16, snapped:** `12 14 16 20 24 32 40 48 64`. Raw 25 → 24,
  39 → 40, 61 → 64 so line boxes land on the grid.
- **Spacing:** `4 8 12 16 24 32 48 64 96`. Not every multiple of 8.
- Palettes, ramps and contrast pairs with computed values:
  `references/color.md`.

## Leverage ranking

1. Hierarchy and a single emphasis (five-second test)
2. Contrast and legibility: text pairs, size floors, measure
3. Spacing from one unit; rhythm and alignment
4. Optical correction: radii, gradients, centering, shadows
5. Perceptual color model for palette construction
6. Grid system choice
7. Which ratio generates the scale — near zero

## What the evidence says

- There is no solid empirical evidence that the golden ratio produces
  better-looking layouts. Fechner's rectangle-preference results replicate
  poorly, and most golden-ratio-in-the-Parthenon claims are retrofitted.
- Musical-interval type scales have no perceptual connection to hearing.
  The names are mnemonics.
- What ratio systems provide is a small, consistent set of values.
  Consistency is what does the work. A 1.25 scale and a 1.618 scale both
  beat choosing sizes by eye.
- Therefore: use a scale, don't defend a specific ratio, and override any
  step that fails in context.

## Where principles conflict

| Conflict | Resolution |
|---|---|
| 8pt grid vs modular-scale rounding | Snap each type step to an integer, and to the 4/8 grid when that is within 1px (25 → 24, 39 → 40; 13 stays 13). The *line box* must land on the grid regardless (13/20, 20/28, 32/40). |
| WCAG contrast vs brand color | Keep hue and chroma; move lightness until the pair passes. `#f97316` (L 0.70) → `#c2410c` (L 0.55, same hue) gives 5.2:1 with white text. Dark text on the original orange passes WCAG (6.2:1) but sits at APCA Lc 49, so use it only for large bold labels. Never ship the failing pair; never fix by desaturating to gray. |
| Hick's law vs progressive disclosure | Hick applies to novel, unordered options. First layer: the complete common case, sorted. Disclose the rest on request. Never hide the common case to lower a count. |
| Aesthetic–usability vs Rams's "as little design as possible" | Polish is functional (it buys tolerance) but masks usability defects. Test the flow unpolished, polish last, then remove devices until the one thing is the only thing. |
| Fitts (bigger targets) vs density | Enlarge the hit area to 44, keep the visible control on the grid. |
| Von Restorff vs serial position | Emphasis by *difference*, placement by *order*: the recommended item sits in the middle of three (rule of odds) and is the only different one. |

## Anti-patterns

- HSL-derived palettes: `hsl(h 90% 55%)` across hues gives wildly different perceived lightness
- One shadow value on every element regardless of elevation
- Ratio-scale font sizes rendered at fractional pixels (`41.89px`)
- Decorative spacing values that exist nowhere in the scale (22, 26, 18, 7)
- Same radius inside and outside a padded container
- Gradients between distant hues with no interpolation space declared
- Accent color on more than one element per view; emphasis by stacking
- Pure `#000` backgrounds or `#fff` text in dark mode
- Citing the golden ratio as justification for a decision

## Critique checklist — observable failures

- The intended one thing is not the first thing noticed (five-second test)
- Accent color used on more than one element per view
- Recommended item carries more than one emphasis device
- Body measure over 75 characters, or `max-width` set in px
- Line-height ≥ 1.4 on 32px+ text; display text tracked out (positive spacing)
- Font sizes with fractional px, or not derivable from one scale
- Spacing values off the unit; a label equidistant from its own field and the previous one
- Muted text below 4.5:1; white text on saturated yellow, orange or green
- Concentric radii not compensated
- Gradient banding, or a gray or dark band from sRGB interpolation
- Uniform shadows at every elevation, or shadows from mixed directions
- Dark mode by inversion: card darker than page, accent unchanged, pure black
- Icons at inconsistent optical sizes; glyphs at geometric rather than optical center
- More than three levels of type prominence, or more than two families
- Blur test shows one flat gray, or six

## Reference files

- `references/proportion-and-layout.md` — full 1.25 table, multi-strand
  scales, 8pt grid, rhythm, Van de Graaf/Tschichold, root rectangles,
  Modulor, thirds/odds, Swiss grid column math
- `references/typography.md` — measure, leading and tracking tables, squint
  test, x-height and `font-size-adjust`, optical sizing, a full card spec
- `references/optical-correction.md` — overshoot, optical center, nested
  radii table, superellipse, shadow ladders, gradient interpolation with
  measured midpoints
- `references/color.md` — OKLCH with numbers, ramps, Albers, Bezold,
  Helmholtz–Kohlrausch, WCAG 2 vs APCA table, 60-30-10, dark mode
- `references/perception-laws.md` — Gestalt, Weber, Fitts, Hick, Miller,
  Tesler, Jakob, Doherty, Von Restorff, serial position, peak–end,
  aesthetic–usability, each with what it does *not* apply to
- `references/heuristics-and-critique.md` — Rams, Nielsen, Shneiderman,
  Norman, Tufte, CRAP, progressive disclosure, least astonishment, ma,
  notan; the critique procedure and extended failure list
- `references/tokens-and-systems.md` — atomic design, three-tier tokens
  with a full light/dark example, DTCG format, double diamond
- `scripts/color.py` — `oklch`, `hex`, `contrast` (WCAG 2 + APCA),
  `palette`, `ramp`; no dependencies
