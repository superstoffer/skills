# Design: `visual-design` skill

**Date:** 2026-09-05
**Status:** Built. RED and GREEN recorded in `plans/2026-09-05-visual-design-red-results.md` and `plans/2026-09-05-visual-design-green-results.md`
**Repo:** `superstoffer/skills`

## Objective

A skill that encodes professional visual design judgment — the kind that
separates UI that measures correctly from UI that looks correct — and fires
on any task with a visual surface, including ones that never say "design".

## What it must do

1. **Trigger accurately.** Build or refine a UI, choose type/spacing/color,
   design a layout, critique an interface, set up tokens — including "make
   this look better", "build a landing page", "clean up this component".
   Not for logic, backend, or data work with no visual surface.
2. **Lead with a decision procedure**, not a reference dump: grid unit and
   type scale first, then color and contrast, then component rhythm, then
   optical passes last.
3. **Progressive disclosure.** `SKILL.md` under ~200 lines as the
   always-loaded index; depth in seven reference files loaded per problem.
4. **Intellectual honesty.** Rank principles by leverage. Say plainly that
   the golden ratio has no solid empirical support, that musical-interval
   scales have no perceptual link to hearing, and that consistency is what
   does the work.
5. **Observable critique checklist**, worked numeric examples, documented
   conflicts with resolutions, and explicit anti-patterns.

## Structure

```
skills/visual-design/
  SKILL.md                              index + decision procedure + checklist
  README.md
  references/
    proportion-and-layout.md
    typography.md
    optical-correction.md
    color.md
    perception-laws.md
    heuristics-and-critique.md
    tokens-and-systems.md
  scripts/
    color.py                            OKLCH ⇄ hex, WCAG 2 + APCA; no dependencies
    test_color.py
```

## Method

RED → GREEN → REFACTOR as in the `nest` skill. Two baseline runs (build a
pricing card; critique a pricing card with planted defects) score seventeen
candidate rules in `plans/2026-09-05-visual-design-red-checklist.md`. Only
observed failures earn a place in `SKILL.md`; the rest live in references or
are cut. Then the same two runs are repeated with the skill present, which
doubles as the deliverable's before/after demonstration on a pricing card.

## Resolution

RED showed broad PASS on the mechanical layer (10 of 17 rules in both
runs) and consistent failure in three clusters: color chosen in HSL with
a stated rationalization, emphasis stacked on the recommended tier, and
the optical layer skipped. `SKILL.md` ships four hard rules for those,
the decision procedure, the honesty section, conflicts, anti-patterns and
the critique checklist; the references carry the mechanics as worked
examples. A dependency-free `scripts/color.py` closes the "OKLCH needs a
conversion step" loophole. GREEN closed every RED failure.
