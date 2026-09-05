# Optical correction

Read this for the last pass on any surface, after everything measures
correctly. The eye is not a ruler: equal measurements look unequal, and
the corrections below make things *look* equal. This is Rams's "thorough
down to the last detail" and it is where amateur and professional work
diverge most visibly.

## Overshoot

Round and pointed forms look smaller than flat ones at the same measured
height because less of their mass touches the boundary. Type designers
draw the O and the A past the baseline and cap height by ~1.5–3%. In UI:

- **Icon keylines** (Material): in a 24px box, a square is drawn at 18,
  a circle at 20, a vertical rectangle at 16 × 20, a horizontal at 20 × 16.
  Same box, different fills, equal apparent size.
- A circular avatar beside a square thumbnail: make the circle 4–6%
  larger.
- A triangular play glyph inside a circle: nudge it right by ~6–8% of
  the glyph width, toward its point, and enlarge it slightly.

## Optical center

The visual center sits **~5% of the height above** the geometric center.
Anything centered by measurement looks like it is sagging.

| Element | Correction |
|---|---|
| Modal, dialog, empty state | center it at ~45% of container height (≈5% up), not 50% |
| Icon in a circular button | shift up ~1px at 40px, ~2px at 64px |
| Text in a pill or badge | center the **cap height**, not the line box: `padding-top` 1px less than `padding-bottom`, or `line-height: 1` plus a 1px `padding-bottom` |
| Text beside an icon | align icon to cap height / x-height, not to the line box center |
| Logo in a header | 1–2px above center |
| Left-edge alignment | text with round glyphs starts ~1px left of the container edge; icons and images sit exactly on it |

The same fact underlies the Tschichold page canon: the bottom margin is
the largest so the text block sits high.

## Nested (concentric) radii

Two rounded rectangles sharing a center look concentric only when
`inner radius = outer radius − padding`. Same radius inside and outside
makes the inner corner look fatter and the gap uneven around the corner.

| Outer | Padding | Inner |
|---|---|---|
| 16 | 12 | 4 |
| 16 | 8 | 8 |
| 24 | 8 | 16 |
| 12 | 4 | 8 |
| 16 | 24 | not derived — pick for the element, clearly under 16 |

Going the other way — a card containing a 12px-radius image with 8px
padding — the card gets 20. When padding ≥ outer radius the inner element
sits clear of the corner curve, so its radius is not derived: choose it
for the element itself (4–8 is typical for a control) and keep it clearly
smaller than the outer, never the outer value.

Where this bites: images inside cards, buttons in card footers, a badge
tucked in a card corner, list rows inside a bordered panel, an input
inside a search container. In the baseline pricing card the 16px button
inside a 16px card looked "off" and was diagnosed as "half-pill" — the
actual defect was the uncompensated nesting.

## Continuous curvature (superellipse)

A plain circular corner has a curvature discontinuity where the arc meets
the straight edge; the eye sees a faint kink. Apple's icons and large
cards use a superellipse (squircle) where curvature ramps continuously.

- CSS `corner-shape: squircle` (Chromium 139+, 2025); falls back to the
  circular radius elsewhere, which is acceptable.
- Matters above ~12px radius on large surfaces (cards, sheets, app icons,
  device frames). Below 8px nobody sees it.
- Do not mix squircles and circular corners on sibling elements.

## Shadows

One light source, from the top. Every shadow in a product has `x = 0`
(or a consistent small positive value) and `y > 0`. Mixed directions read
as multiple lights and look wrong before anyone can say why.

A shadow has three parameters that move together with elevation:
**y-offset** grows, **blur** grows faster (≈ 2–3× y), **opacity per
layer** falls. Two layers, a tight *contact* shadow (what the object
touches) and a soft *ambient* one (what it blocks), read as physical;
one layer reads as a drop-shadow filter.

### Worked ladder (light mode; tinted with the surface hue)

```css
/* 1 — resting card, input */
--shadow-1: 0 1px 2px oklch(0.2 0.02 250 / 0.06),
            0 1px 3px oklch(0.2 0.02 250 / 0.08);
/* 2 — hover, dropdown, popover */
--shadow-2: 0 2px 4px oklch(0.2 0.02 250 / 0.06),
            0 6px 16px oklch(0.2 0.02 250 / 0.10);
/* 3 — modal, featured, drag */
--shadow-3: 0 4px 8px oklch(0.2 0.02 250 / 0.08),
            0 16px 40px -8px oklch(0.2 0.02 250 / 0.16);
```

Negative spread on the largest layer keeps the glow under the element
rather than around it. Tinting the shadow with the surface hue (not
black) avoids a muddy gray; a *colored* glow (accent-tinted) is an
emphasis device and counts as one.

**Dark mode**: shadows are nearly invisible on dark surfaces. Carry
elevation by lightening the surface (`color.md`) and keep a single
contact shadow at higher alpha (0.4–0.6) so edges stay crisp.

**Never**: the same shadow on card, button and badge (the baseline
critique's item 2). A button at rest is at elevation 0 or 1; a badge is
flat.

## Gamma-correct gradient interpolation

sRGB is gamma-encoded; interpolating its channel values is not
interpolating light. Between distant hues the midpoint sags in lightness
and chroma:

| Gradient | sRGB midpoint | Endpoints | Midpoint |
|---|---|---|---|
| `#ff0000` → `#0000ff` | `#800080` | L 0.63 / 0.45 | **L 0.421** — a dark band |
| `#0d7dd4` → `#1c882d` (blue → green) | `#148280` | C 0.16 / 0.16 | **C 0.09** — a gray band |
| `#0d7dd4` → `#eab308` (blue → yellow) | `#7b986e` | C 0.16 / 0.16 | **C 0.07 at hue 136** — a dull green nobody chose |

Fixes:

- `linear-gradient(in oklch, A, B)` — perceptual lightness *and* hue
  travel; for near-complementary pairs this goes around the hue circle
  (specify `longer hue` or `shorter hue`) and keeps chroma.
- `in oklab` for same-hue or tint gradients (blue → light blue): straight
  line, no hue travel, no sag.
- Where the midpoint hue is outside sRGB (blue → green passes through
  cyan, a narrow hue), add an explicit gamut-safe middle stop.
- **Banding**: an 8-bit gradient over a large area shows steps when the
  lightness delta per pixel is small. Reduce the span (fewer than ~40
  lightness units over 1000px), add a subtle noise layer, or use more
  hue movement than lightness movement.

## Visual weight and thin things

- Thin or small text looks lighter than its color. Muted text at 12–13px
  needs a darker token than the same role at 16px, or weight 500.
- Light-on-dark text looks bolder than dark-on-light at the same weight
  (irradiation); drop one weight step or reduce size 1px in dark mode for
  body text if the family has the step.
- 1px borders look brighter on dark surfaces than on light; use alpha
  (`oklch(1 0 0 / 0.1)`) instead of a fixed gray.
- Icons beside text: stroke weight should match the text's stem weight.
  A 1.5px icon beside 600-weight text looks anemic; use the 2px cut.
- Buttons with a leading icon: reduce padding on the icon side by 4px
  so the visual mass is centered.

## Checklist for the pass

The mandatory list is "The optical pass" in `SKILL.md`; this file supplies
the numbers behind each item.
