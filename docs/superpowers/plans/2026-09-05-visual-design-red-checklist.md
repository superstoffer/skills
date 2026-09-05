# RED checklist — `visual-design` candidate rules

Scored against two baseline runs with the skill absent from disk:

- **RED-BUILD** — "Build a pricing card component, make it look professional
  and polished." Three tiers, light + dark mode, single HTML file, followed
  by a design-decisions document.
- **RED-CRITIQUE** — a pricing card with fifteen planted defects; "tell me
  what to fix so it looks more professional, be specific."

A rule ships in `SKILL.md` only if it has an OBSERVED-FAIL in at least one
run. Rules that PASS unaided are cut from `SKILL.md` and, where they carry
real leverage, demoted to a reference file so they cost nothing per
invocation.

| ID | Rule | Run | FAIL signature | PASS signature |
|---|---|---|---|---|
| C1 | Type sizes come from a scale and render at integer px | both | sizes with fractional px, or sizes not derivable from one ratio/base | integer px from a stated scale |
| C2 | Spacing values come from one grid unit | both | orphan values (22, 26, 18, 7, 30, 14, 9) | multiples of 4 or 8, or a named step |
| C3 | Body measure held to 45–75ch | both | a paragraph allowed past ~90ch; `max-width` in px with no ch check | `max-width` in ch, or ≤ ~70ch |
| C4 | Line height scales inversely with size | both | heading line-height equal to body (1.5–1.6) | headings ≤ 1.2–1.3, body 1.5–1.6 |
| C5 | Tracking scales inversely with size | both | positive letter-spacing on display text | negative or zero at display size |
| C6 | Palette specified in a perceptual model (OKLCH/OKLab) | both | HSL/hex with equal HSL lightness across hues | OKLCH, or hex derived from OKLCH |
| C7 | Text contrast checked and passing | both | muted or white-on-yellow text below threshold, no check mentioned | ratio computed or stated; muted text ≥ 4.5:1 |
| C8 | Dark mode derived by remapping semantic tokens; elevated surfaces lighter | build | colors inverted, or same shadow/ramp reused; card darker than page | tokens remapped; surface lightens with elevation |
| C9 | Accent color used once per view | both | accent on headings, icon tiles, badges *and* the CTA | accent on one element (the recommended CTA) |
| C10 | Shadows form a ladder tied to elevation, one light source | both | one shadow value on card, button and badge | 2–3 levels with blur/spread growing with elevation |
| C11 | Nested radii compensated (inner = outer − padding) | both | inner element carries the same radius as its container | inner radius reduced by the padding |
| C12 | Gradients interpolated in a perceptual space | critique | sRGB hue-to-hue gradient (blue→green gray zone) not flagged | `in oklch`/`in oklab`, or gradient flagged |
| C13 | Optical adjustments applied or flagged | both | icons/glyphs placed at geometric center only, nothing said | optical centering, cap-height alignment, or overshoot mentioned |
| C14 | Tokens layered primitive → semantic → component | build | one flat `--brand`, `--text` layer, or hex literals in components | semantic aliases over primitives |
| C15 | Golden ratio not cited as justification | both | "golden ratio" or 1.618 cited as a reason | any other reason, or none |
| C16 | One dominant element per card | both | price and heading at the same size; heading in accent color | price clearly largest; heading neutral |
| C17 | Emphasis by one mechanism, not stacked | both | featured tier gets border + badge + shadow + color + scale together | one or two devices |
