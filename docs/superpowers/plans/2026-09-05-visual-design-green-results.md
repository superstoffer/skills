# GREEN results — `visual-design`

Run 2026-09-05 with the skill present. The same two scenarios as RED,
with the agent told to read `SKILL.md` first, plus a triggering test
against the description alone.

## Scoring — before and after

| ID | Rule | RED build | GREEN build | RED critique | GREEN critique |
|---|---|---|---|---|---|
| C1 | Sizes from a scale, integer px | PASS | PASS | PASS | PASS |
| C2 | Spacing from one unit | PASS | PASS (two off-unit values, both declared: badge cap-height padding, 1px borders) | PASS | PASS |
| C3 | Measure 45–75ch | PASS | PASS (`45ch`) | PASS | PASS (`50ch`) |
| C4 | Line height inverse with size | PASS | PASS | PASS | PASS |
| C5 | Tracking inverse with size | PASS | PASS | PASS | PASS |
| **C6** | **Perceptual color model** | FAIL | **PASS** — OKLCH throughout, hue carried into neutrals, script run on 25 pairs, a clipped hover color caught by the gamut flag | FAIL | **PASS** — item 10 names HSL as root cause with computed L 0.57 / 0.85 / 0.83 |
| C7 | Contrast checked | PASS | PASS (WCAG + APCA; muted dark text raised twice to clear Lc 60) | PASS | PASS (every fix re-measured) |
| C8 | Dark mode by remap; surface lightens | PASS | PASS (semantic tier only; +0.04 L; alpha borders) | n/a | n/a |
| **C9** | **Accent once per view** | PARTIAL | **PASS** — filled Pro button only; badge and check icons neutral | PASS | PASS (item 3) |
| C10 | Shadow ladder | PASS | PASS (two levels used, tinted, buttons flat) | PASS | PASS (item 22) |
| **C11** | **Nested radii** | PARTIAL | **PASS** — rule applied, found to bottom out at padding ≥ radius, overridden with a stated reason | FAIL | **PASS** — item 21 states inner = outer − padding |
| **C12** | **Gradient space** | n/e | n/e (no gradient) | FAIL | **PASS** — item 23 measures midpoint chroma 0.11 vs 0.22/0.24 |
| **C13** | **Optical adjustments** | PARTIAL | **PASS** — cap-height badge centering, icon on the cap band, stroke matched to stem, weight-compensated 12px text | FAIL | **PASS** — item 25 |
| C14 | Three-tier tokens | PARTIAL | PASS | n/a | n/a |
| C15 | Golden ratio not cited | PASS | PASS | PASS | PASS |
| C16 | One dominant element | PASS | PASS | PASS | PASS (item 15) |
| **C17** | **Emphasis by one device** | FAIL | **PASS** — *"One device: the Pro card has the only filled accent button … no ring, no lift, no tinted glow"* | FAIL | **PASS** — item 2 prescribes keeping exactly one |

**GREEN build: 16 PASS, 1 not exercised. GREEN critique: 15 PASS, 2 n/a.**
Every RED failure is closed. The critique run ordered its 26 findings by
the leverage ranking (hierarchy → contrast → type → rhythm → optical) and
opened with the five-second test.

## Before / after on the pricing card

| Decision | Without the skill | With the skill |
|---|---|---|
| Palette | HSL, "OKLCH would need a conversion step to verify contrast" | OKLCH, hue 290 carried into neutrals at C 0.005–0.02; contrast checked on 25 pairs with the script |
| Recommended tier | Border + ring + badge + filled button + tinted shadow + 8px lift: "five cooperating signals" | Filled button only; badge neutral; identical surface, border and shadow across cards |
| Accent | Six carriers, including check icons on every card | One element |
| Dark accent | Lightened, white text kept | Lightened two steps with chroma −0.05; on-accent text flipped dark; first attempt flagged out of gamut by the script and corrected |
| Radii | "Controls 8px (half the card)" | Rule applied; override documented because padding ≥ radius |
| Optical | One 1px icon nudge | Cap-height centering in the pill, icon on the cap band, stroke weight matched, 12px text weight-compensated |
| References | — | Read 4 of 7, skipped 3 with reasons; progressive disclosure held |

## Triggering test

Twenty requests judged from the description alone. All twelve clear
positives and negatives were correct. Hesitation on four:

| Request | Cause | Change made |
|---|---|---|
| "Clean up this component, it's gotten messy" | visual vs code cleanup not distinguished | "(when the mess is visual)" |
| "Add a hover state to the card" | interaction states not named | "hover/focus/active states" |
| "Increase the padding on the modal" | no floor for trivial changes | "when a spacing or size value must land on the system" |
| 1–3 vs `frontend-design` | relation between the skills unstated | A "complements frontend-design" sentence was added, then moved out of the description after review (it carried no trigger vocabulary and the two skills conflict on hex vs OKLCH); hard rule 1 now states the precedence |

## Refactor after GREEN

- SKILL.md's optical-pass line "padding ≥ radius → 0–2" was too
  prescriptive; the build run rightly chose 8px for a 44px control.
  Reworded to: when padding ≥ radius the inner radius is not derived —
  choose it for the element itself and keep it clearly smaller than the
  outer.
- Description tightened as above (872 characters).

## Post-review changes

An eight-angle code review of the branch produced fixes applied before
merge: the script now scores contrast on the 8-bit hex it prints (float
verdicts flipped at the 4.5:1 boundary), accepts the full CSS hex and
`oklch()` grammar including alpha (composited) and `none`, takes several
pairs per call, reports out-of-gamut input with the largest in-gamut
chroma instead of scoring a color no browser paints, and validates
arguments. Documentation fixes: the script path is anchored to the skill
directory; the shadow ladder lives in one file; optical-center, measure,
line-height, radius and dark-mode ladder numbers agree across files; the
accent token is the 600 step; the `#f97316` conflict example is
qualified with APCA; the description no longer carries the
frontend-design sentence, whose content moved into hard rule 1.

## Not verified

- No run rendered the page in a browser; both critiques were by
  inspection. I rendered both builds afterwards with headless Chrome; the
  PNGs are in `.context/shots/`, excluded from git by the workspace's
  local exclude file and now also by `.gitignore`.
- The perception and heuristic references have no rule to violate and
  were not scenario-tested; the GREEN build skipped them as
  non-trivial-only reading, which is the intended behavior.
