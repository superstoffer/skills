# Typography

Read this when setting text sizes, line heights, tracking, measure, or
pairing typefaces. Four facts do most of the work: measure at 45–75
characters, line height inverse to size, tracking inverse to size, and
x-height, not point size, governs apparent size.

## Measure

45–75 characters per line for continuous text, 66 as the target
(Bringhurst). Under 45 the eye returns too often; over 75 it loses the
next line on the return sweep. Multi-column text tolerates 40–50.

**CSS `ch` overstates.** `1ch` is the advance width of the digit `0`,
wider than the average glyph in a proportional face. `max-width: 60ch`
yields roughly 66–72 characters of English prose; `65ch` yields ~72–78.
Use `60ch` for body columns and `45ch` for captions and sidebars. Never
express measure in px — it stops tracking the font size.

| Context | `max-width` | ≈ characters |
|---|---|---|
| Body column | 60ch | 66–72 |
| Lead / intro paragraph | 50ch | 55–60 |
| Card body, sidebar | 40–45ch | 45–50 |
| Headline | 20–25ch, plus `text-wrap: balance` | — |

## Line height

Scales inversely with size and directly with measure. Long lines need more
leading so the return sweep finds the next line; large type needs less
because the glyphs already carry the spacing.

| Size | Line height | Notes |
|---|---|---|
| 12–14px | 1.5–1.6 | small text needs air |
| 16–18px | 1.5 | 1.6 at a full 75ch measure, 1.4 inside cards |
| 20–24px | 1.3–1.4 | |
| 32–40px | 1.1–1.2 | |
| 48px+ | 1.0–1.1 | display; check descender collisions |
| Price / single-line numerals | 1.0 | no wrapping, so no leading needed |

Express as unitless multipliers so it scales, then verify each product lands
on the spacing grid: 16 × 1.5 = 24 ✓, 20 × 1.4 = 28 ✓, 32 × 1.2 = 38.4 ✗ →
use 1.25 = 40.

## Tracking (letter-spacing)

Inverse to size. Small text is spaced out; display text is pulled in
because the counters and sidebearings were drawn for text sizes.

| Size | letter-spacing |
|---|---|
| 11–12px | +0.01 to +0.02em |
| 14–18px | 0 |
| 24px | −0.01em |
| 32px | −0.02em |
| 48px+ | −0.03 to −0.04em |
| ALL CAPS, any size | +0.05 to +0.10em |

Never track lowercase out at body size — it destroys word shapes. Numbers
that must align (prices, tables): `font-variant-numeric: tabular-nums`.

## Typographic color and the squint test

Typographic color is the evenness of gray a block of text produces. Squint,
or apply `filter: blur(4px)` in devtools: the page should reduce to a few
gray masses at clearly different darknesses. If everything blurs to the same
gray, hierarchy is missing; if it blurs to more than three darknesses,
hierarchy is noisy. Rivers (white channels through justified text), a
heading that disappears, or a block darker than the heading are all found
this way and not by measurement.

Three levels of prominence per view is the ceiling: primary (the one
thing), secondary, tertiary. A fourth level is invisible.

## Pairing faces — x-height governs apparent size

Two faces at the same `font-size` do not look the same size; the one with
the larger x-height looks larger and darker. Georgia at 15px matches Times
at 16px. When pairing:

1. Match x-heights, not point sizes. CSS `font-size-adjust` sets size by
   x-height ratio: `font-size-adjust: 0.5` makes any face render its
   x-height at half the font-size, so fallbacks and pairs agree.
2. Contrast in structure (serif with sans, humanist with geometric), never
   near-misses (two similar grotesques).
3. Two families maximum. A third is for code.

## Optical sizing and variable axes

Type designed for 9pt has sturdier strokes, larger x-height and looser
spacing than the same family drawn for 72pt. Variable fonts expose this as
the `opsz` axis; `font-optical-sizing: auto` (the default) lets the browser
select it from the rendered size. If a family has no `opsz`, use its Text
and Display cuts explicitly — display cuts at body size look spindly, text
cuts at display size look clumsy.

Other axes worth touching: `wght` for fine hierarchy (450 vs 400 for a
lead paragraph instead of a size change), `wdth` for fitting numerals or
labels in tight cells rather than shrinking them.

## Worked example — a pricing card

Body 16px, unit 4/8, scale 1.25 snapped (every line box a multiple of 4):

| Element | Size / line-height | Weight | Tracking | Extra |
|---|---|---|---|---|
| Price | 40 / 40 | 700 | −0.03em | `tabular-nums` |
| "/month" | 14 / 20 | 400 | 0 | muted; not bold, not tracked |
| Tier name | 20 / 28 | 600 | −0.01em | |
| Tagline | 14 / 20 | 400 | 0 | muted |
| Feature list | 16 / 24 | 400 | 0 | 8 between rows |
| Button | 16 / 24 | 600 | 0 | `font: inherit` on `<button>` |
| Badge | 12 / 16 | 600 | +0.04em | uppercase |

Two weights (400, 600) plus one 700 for the price. One face.

## Details that read as care

- `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs.
- Hang punctuation and bullets outside the text edge (`hanging-punctuation`
  where supported; otherwise negative `text-indent` on the marker).
- Real quotes, apostrophes, en dashes for ranges, a thin or no-break space
  before units and after currency symbols.
- Oldstyle numerals in prose, lining in tables and UI.
- Do not fake small caps or bold; load the real cut or do without.
- `<button>` and `<input>` do not inherit font by default — `font: inherit`.
