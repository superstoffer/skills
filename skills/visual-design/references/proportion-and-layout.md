# Proportion and layout

Read this when choosing a type scale, a spacing unit, page margins, column
grids, or aspect ratios. The governing fact: **a scale works because it is a
small consistent set of values, not because of which ratio generated it.**
Pick one, snap it to integers, and override any step that fails in context.

## Modular scales

`size(n) = base × ratio^n`. Named ratios, all in common use:

| Name | Ratio | Character |
|---|---|---|
| Minor second | 1.067 | Almost flat; needs many steps to show hierarchy |
| Major second | 1.125 | Dense UIs, data tables, dashboards |
| Minor third | 1.200 | Product UI default; steps are distinct but close |
| Major third | 1.250 | Marketing and product; the usual safe choice |
| Perfect fourth | 1.333 | Editorial; headings pull clearly away from body |
| √2 ("silver", A-series paper) | 1.414 | Every step doubles area; pairs with A-paper layouts |
| Perfect fifth | 1.500 | Display-heavy landing pages, few steps |
| Golden | 1.618 | Very few usable steps between 12 and 64px |

The musical names are mnemonics from Bringhurst. They carry no perceptual
meaning; the ear has nothing to do with the eye. A ratio is a generator,
not a justification (see SKILL.md, "What the evidence says").

### Worked example — 1.25 from a 16px base

| n | Raw | Rounded | Snapped to 4/8 | Use |
|---|---|---|---|---|
| −2 | 10.24 | 10 | 12 | caption (12 is the floor for legibility) |
| −1 | 12.80 | 13 | 14 | meta, labels |
| 0 | 16.00 | 16 | 16 | body |
| 1 | 20.00 | 20 | 20 | lead, h4 |
| 2 | 25.00 | 25 | 24 | h3 |
| 3 | 31.25 | 31 | 32 | h2 |
| 4 | 39.06 | 39 | 40 | h1 / price |
| 5 | 48.83 | 49 | 48 | display |
| 6 | 61.04 | 61 | 64 | hero |

Ship the last column. Fractional pixels blur on 1× screens and buy nothing.
Snapping 25→24 and 39→40 keeps line-heights on the spacing grid.

### Multi-stranded scales

One strand rarely gives both the body size you need and the display size you
want. Run two bases through the same ratio and interleave:

Strands 16 and 20, ratio 1.5: `16, 20, 24, 30, 36, 45, 54, 67.5` →
snapped `16, 20, 24, 32, 36, 44, 56, 68`. Use the second strand for a
distinct role (numbers, captions, a secondary face) rather than sprinkling
both everywhere.

### Weber's law and step size

A step must differ by roughly 15–20% to read as a different level rather
than a rendering error. Below 1.15 the scale needs weight or color to carry
hierarchy; above 1.5 you get three usable sizes between 14 and 64px.

## The 8-point grid

Spacing and sizing values are multiples of 8, with 4 as a half-step for
tight pairs (icon-to-label, label-to-input) and 2 only for hairlines.

```
4  8  12  16  24  32  48  64  96
```

Note it is not every multiple of 8 — 40 and 56 are omitted from the
*spacing* set on purpose so it stays small. Add a value back only when a
third use appears. Component *heights* are a separate set (below) and do
use 40 and 56.

**When it beats a ratio scale:** for spacing, component heights, icon boxes
and layout. Spacing must *add up* (padding + gap + padding must land on the
grid) and must align across unrelated components, which a geometric series
cannot do. Ratio scales are for type; additive grids are for space. Both
land on integer device pixels at 1×, 1.5× and 2×.

**Component heights on the grid:** control 32 / 40 / 48, list row 40 / 48
/ 56, top bar 56 / 64. Touch targets: 44 minimum (Apple), 48 (Material),
24 legal floor (WCAG 2.2 SC 2.5.8).

## Baseline grids and vertical rhythm

A true baseline grid puts every baseline on a multiple of one unit. On the
web the baseline sits inside the line box, not on its edge, so strict
baseline grids fight the rendering model. Use **rhythm** instead:

- Choose a vertical unit, normally the body line-height: 16px × 1.5 = 24.
- Every line-height, margin and block height is a multiple of 24, or of
  its half (12) or third (8). A 32px heading gets line-height 40 (not 38.4),
  a 40px heading gets 48.
- Margins between blocks come from the same set: 8 inside a group, 24
  between groups, 48 between sections.

The squint test shows whether rhythm holds: text should form even gray bars
with even gaps.

## Page margins — Van de Graaf and Tschichold

The medieval canon, reconstructed by Van de Graaf and codified by
Tschichold, applies to a 2:3 page: text block is also 2:3, its height equals
the page width, margins run inner : top : outer : bottom = 2 : 3 : 4 : 6,
which is inner 1/9 of page width, outer 2/9, top 1/9 of height, bottom 2/9.

Worked: a 600 × 900 page → text block 400 × 600, margins inner 67, top 100,
outer 133, bottom 200. The asymmetry (bottom heaviest) is what makes a
centered block look *low* — the same optical-center fact as
`optical-correction.md`.

**On screen:** the lesson is that margins should be unequal and the block
should sit high. A modal or empty state centered geometrically looks like
it is sliding down; shift it up ~5% of container height (numbers in
`optical-correction.md`, Optical center).

## Root rectangles and self-similarity

A √2 rectangle halved along its long side gives two √2 rectangles; the A
paper series is this. A golden rectangle minus a square is another golden
rectangle. The useful property is **self-similarity**: nested containers
that share a proportion look related without any other cue.

In practice this means picking **one family of aspect ratios** for a
product and sticking to it: 1:1 and 4:3 and 16:9, or 1:1 and 3:2 and 2:1.
Mixing 4:3 thumbnails with 16:9 cards and 3:2 heroes reads as accidental.

## The Modulor

Le Corbusier's Modulor derived two Fibonacci-like series from a 183 cm
figure (red: 113, 70, 43, 27…; blue: 226, 140, 86, 53…). Nobody uses the
numbers now. What transfers is **anthropometric anchoring**: some sizes are
fixed by the body, not by the scale. Touch targets, thumb reach on a phone,
reading distance (a 16px minimum at arm's length; larger on a TV), and the
~30° comfortable field of view that caps useful line length.

## Rule of thirds, rule of odds

Place focal points at the intersections of a 3 × 3 division rather than the
center; the eye enters, travels and rests. Groups of odd count (3 tiers,
5 features, 3 testimonials) resolve because there is a natural middle; four
items split into two pairs. The middle item of three receives emphasis
for free — it needs less added treatment, not more.

## Swiss / International Typographic Style grids

Müller-Brockmann's vocabulary: **columns** separated by **gutters**; rows
separated by the same gutter give **modules**; groups of modules form
**fields** that hold content. The grid is a constraint you break knowingly.

### Worked example — 12 columns

Container 1200px, gutter 24px:

```
column = (1200 − 11 × 24) / 12 = 78px
span 3  = 3 × 78 + 2 × 24 = 282px
span 4  = 4 × 78 + 3 × 24 = 384px
span 6  = 6 × 78 + 5 × 24 = 588px
span 8  = 8 × 78 + 7 × 24 = 792px
```

Three pricing cards = three span-4 fields. A sidebar layout = span 8 +
span 4. Content measure inside span 8 at 16px ≈ 792 / 8.5 ≈ 93 characters —
over the limit, so the text column inside it gets `max-width: 60ch`
regardless of the grid.

Fewer columns are better than more: 12 is conventional because it divides
by 2, 3, 4 and 6, not because layouts need twelve things across.

## Density

Density is a decision, not a default. Set it once per surface with the
spacing unit: 4-based for data-dense tools (tables, IDEs), 8-based for
product UI, 8-based with doubled margins for marketing. Mixing densities on
one screen is the most common reason a page "feels off" with nothing
measurably wrong.
