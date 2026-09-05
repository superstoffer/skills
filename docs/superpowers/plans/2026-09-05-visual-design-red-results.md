# RED baseline results — `visual-design`

Run 2026-09-05 with the skill absent from disk. Two runs, scored against
`2026-09-05-visual-design-red-checklist.md`.

## Runs

| Run | Prompt | Outcome |
|---|---|---|
| RED-BUILD | "Build a pricing card component for a SaaS product and make it look professional and polished." Three tiers, light + dark, single HTML file, then a design-decisions document. | 471-line file plus a decisions document. Responsive, `:focus-visible`, `prefers-reduced-motion`, WCAG ratios computed for every pair. |
| RED-CRITIQUE | A pricing card with fifteen planted defects. "Tell me what to fix so it looks more professional. Be specific." | 21 ranked findings, each with line, cause and fix. Also caught four unplanted defects (badge shifting card alignment, no responsive wrap, missing focus states, button not inheriting font). |

## Scoring

| ID | Rule | BUILD | CRITIQUE | Evidence |
|---|---|---|---|---|
| C1 | Sizes from a scale, integer px | PASS | PASS | 12/14/16/20/32/40 "roughly 1.25, rounded to whole pixels"; critique item 6 flags `41.89px`, `25.89px` |
| C2 | Spacing from one unit | PASS | PASS | "strict 4px grid … nothing is off-grid"; critique item 21 lists the orphan values and snaps to 8 |
| C3 | Measure 45–75ch | PASS | PASS | lede `max-width: 36rem` (~70 characters); critique item 5 → `max-width: 60ch` |
| C4 | Line height inverse with size | PASS | PASS | 1.5 / 1.2 / 1; critique item 7 |
| C5 | Tracking inverse with size | PASS | PASS | −0.01 / −0.02 / −0.03em; critique item 10 |
| **C6** | **Perceptual color model** | **FAIL** | **FAIL** | Build, verbatim: *"OKLCH: more perceptually even, but I'd have needed a conversion step to verify contrast; HSL let me verify directly."* Critique gives every color fix in HSL and never names a model |
| C7 | Contrast checked | PASS | PASS | WCAG script over every pair, 5.6:1 muted; critique items 3 and 12 give ratios |
| C8 | Dark mode by remapping; surface lightens | PASS | n/a | "surface sits 4L above bg in dark mode"; accent lightened, on-accent flipped to near-black |
| C9 | Accent once per view | PARTIAL | PASS | Build puts accent on featured border, ring, badge, tinted shadow, primary button *and* the check icons on all three cards; critique item 8 catches "brand blue used for five different things" |
| C10 | Shadow ladder, one light source | PASS | PASS | two-layer contact + ambient, hover and featured levels; critique item 2 |
| **C11** | **Nested radii compensated** | PARTIAL | **FAIL** | Build: "controls 8px (half the card)" — a halving habit, not the concentric rule; no visible defect only because 32px padding keeps controls off the corner. Critique item 15 sees one radius everywhere but reasons "half-pill", "full pill by accident"; the inner = outer − padding relation is never named |
| **C12** | **Gradient in a perceptual space** | NOT-EXERCISED | **FAIL** | Critique item 4 removes the hero as "content-free"; the gray band of sRGB blue→green interpolation goes unmentioned |
| **C13** | **Optical adjustments** | PARTIAL | **FAIL** | Build has one `margin-top: 0.0625rem /* optical alignment */` on the check icon and nothing else; critique says nothing optical anywhere |
| C14 | Three-tier tokens | PARTIAL | n/a | semantic names (`surface`, `muted`, `accent-ink`) but a single tier with values inline; no primitive ramp |
| C15 | Golden ratio not cited | PASS | PASS | never mentioned |
| C16 | One dominant element | PASS | PASS | price 40 over name 20; critique item 8 pulls `h2` out of brand color |
| **C17** | **Emphasis by one device** | **FAIL** | **FAIL** | Build, verbatim: *"Pro is distinguished by five cooperating signals, none of which alone would be loud"* — border, ring, badge, filled button, tinted shadow, plus an 8px lift. Critique item 1 *adds* `translateY(-8px)` + deeper shadow or tinted background + outlined siblings on top of the retained border |

**BUILD: 10 PASS, 2 FAIL, 4 PARTIAL, 1 NOT-EXERCISED. CRITIQUE: 10 PASS, 5 FAIL, 2 n/a.**

## Conclusion

The mechanical layer does not need teaching. Unaided, Claude builds a
rounded 1.25 scale, keeps a 4px grid, computes WCAG ratios for every
pair, tightens leading and tracking as size grows, and remaps semantic
colors for dark mode with the surface lightening on elevation. Restating
any of that in `SKILL.md` costs context on every invocation and changes
nothing.

Failures cluster in three places:

1. **Color model, with a rationalization.** HSL is chosen both times. The
   build run's stated reason — that OKLCH would need a conversion step to
   verify contrast — is the loophole the skill must close. Contrast is
   checked on the rendered sRGB value either way; OKLCH changes how the
   palette is *chosen*, not how it is *checked*.
2. **Emphasis restraint.** Both runs stack four to six devices on the
   recommended tier and describe that as a virtue ("cooperating signals").
   The accent is also spread onto icons on every card.
3. **The optical layer.** Concentric radii, gradient interpolation space
   and optical centering are neither applied nor recognised. This is the
   layer that separates "measures correctly" from "looks correct", and it
   is exactly where the baseline is silent.

## Rules that ship in `SKILL.md`

- **C6** — specify palettes in OKLCH; convert with the shipped script;
  check contrast on the converted hex.
- **C17 + C9** — one emphasis device per recommended element; accent on
  one element per view.
- **C11, C12, C13** — a mandatory optical pass: concentric radii, gradient
  interpolation space, optical centering, shadow ladder.

C1–C5, C7, C8, C10, C14, C16 are demoted to reference files as the
worked examples the brief requires. C15 ships as an anti-pattern line
only.
