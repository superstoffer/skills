# Heuristics and critique

Read this when reviewing an existing interface or when a design decision
needs a principle behind it. The heuristic lists overlap heavily; the
critique procedure at the end is the operational part.

## Rams — ten principles of good design

Good design is: innovative; makes a product useful; aesthetic;
makes a product understandable; unobtrusive; honest; long-lasting;
thorough down to the last detail; environmentally friendly; **as little
design as possible.**

Load-bearing for UI: *unobtrusive* (the interface is a tool, not an
ornament), *honest* (no false affordances, no dark patterns, no fake
urgency), *thorough to the last detail* (the optical pass is this
principle), and *as little design as possible* (every device you add to
the recommended tier is a claim on attention; remove until it breaks).

## Nielsen — ten usability heuristics

1. Visibility of system status
2. Match between system and the real world
3. User control and freedom (undo, exit)
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use (accelerators for experts)
8. Aesthetic and minimalist design
9. Help users recognize, diagnose and recover from errors
10. Help and documentation

Nielsen's "aesthetic and minimalist" and Rams's "as little as possible"
are the same rule from two fields: every extra unit of information
competes with the relevant units.

## Shneiderman — eight golden rules

Strive for consistency · seek universal usability · offer informative
feedback · design dialogs to yield closure · prevent errors · permit easy
reversal · keep users in control · reduce short-term memory load.

*Closure* is the one designers forget: multi-step flows need an explicit
end state (confirmation, summary) so the user knows the sequence is done.

## Norman — the vocabulary of interaction

| Term | Meaning | UI failure when missing |
|---|---|---|
| Affordance | What the object permits, relative to the agent | a link that cannot be clicked on mobile |
| Signifier | The perceivable cue that an affordance exists | flat text that is secretly a button |
| Mapping | Spatial/logical correspondence between control and effect | a slider that moves left to increase |
| Feedback | Immediate, informative response to an action | a button with no pressed or loading state |
| Constraints | Physical, cultural, semantic, logical limits on action | a form that lets you submit the impossible |
| Conceptual model | The user's mental model of how it works | "Sync" that sometimes means upload, sometimes merge |

The signifier is the designer's job: the affordance may exist, but if the
control does not *look* like what it does, it does not exist for the user.

## Tufte — data and ink

- **Data-ink ratio**: the share of ink that carries data. Erase non-data
  ink (borders, backgrounds, 3D); then erase redundant data-ink (a value
  shown by bar height *and* label *and* gridline).
- **Chartjunk**: moiré patterns, heavy grids, decorative 3D, mascots.
- **Small multiples**: the same design repeated with different data,
  aligned so the eye compares across them. Three pricing cards are small
  multiples; identical structure is what makes the differences legible.
- **Layering and separation**: use the *smallest effective difference* —
  the lightest gridline, the thinnest rule, the least contrast that still
  separates. Heavy separators fight the content.

## CRAP — Contrast, Repetition, Alignment, Proximity

Robin Williams's four:

- **Contrast**: if two things are not the same, make them clearly
  different. Near-misses (15px vs 16px, #333 vs #444) read as errors.
- **Repetition**: reuse the same treatment for the same role everywhere.
- **Alignment**: every element shares an edge or axis with another.
  Pick one alignment per composition; centered-everything is the beginner
  tell. Left-aligned text with a centered heading is a mixed alignment.
- **Proximity**: related things close, unrelated things apart. See
  Gestalt in `perception-laws.md`.

## Occam's razor

Among designs that satisfy the same requirements, prefer the one with the
fewest parts — fewest steps, fewest controls, fewest distinct treatments.
The operational form is subtractive, and it is a test rather than a
preference: build what works, then remove one element at a time until the
next removal breaks something. Whatever came out without loss was
decoration.

The clause that does the work is *satisfy the same requirements*. Dropping
a needed affordance is not parsimony, it is an unfinished design — so the
razor arbitrates between finished alternatives, it does not license
cutting scope. Rams's "as little design as possible" and Nielsen's
"aesthetic and minimalist" are the same idea stated as an aspiration; this
is the version you can actually run.

## Pareto principle

Roughly 80% of effects come from 20% of causes — Pareto's observation
about land ownership, generalised by Juran as "the vital few". Not a law,
and not literally 80/20. The usable claim is that impact is heavily
skewed and it pays to find out which few things carry it.

- A handful of screens carry most of the usage: take those to the last
  detail, accept a plainer treatment elsewhere.
- A handful of components (button, input, card, the type ramp) cover most
  of the surface, which is why a design system pays off there first.
- A handful of defects produce most of the cheapness. This is why a
  critique report is ordered by leverage rather than by file position;
  the leverage ranking in SKILL.md is this principle applied to the design
  principles themselves.

Not an excuse to abandon the tail. Error, empty and edge states are
low-traffic and high-stakes, and peak-end says they set the memory of the
whole product. The skew is in *effort allocation*, not in whether
something ships working.

## Progressive disclosure

Show the few things most people need; reveal the rest on request, in
stages. "Advanced settings", "Show 12 more", expandable feature
comparisons. The first layer must be complete for the common case, not a
teaser. Resolution against Hick's law is in SKILL.md.

## Principle of least astonishment

A component should do what it looks like it does and what its peers do.
A card that is entirely clickable must look clickable; a toggle that
saves immediately must not sit beside a Save button; a "Cancel" that
deletes the draft astonishes.

## *Ma* and *notan*

**Ma** (間): negative space as an active element, a pause with its own
duration. Whitespace is content: it groups, it paces, it signals value
(luxury goods sit in space; bargains are crowded). Do not fill it because
it is empty.

**Notan**: the balance of dark and light *masses* regardless of detail.
Squint until only masses remain. A good composition has a deliberate
distribution — often asymmetric — of dark mass against light. A page of
white cards on white with one dark button has a notan; a page with three
navy hero blocks and a black footer has none.

## Critique procedure

Run in this order; each pass catches what the next cannot.

1. **Five-second test.** Look, look away, name the one thing you
   remember. If it is not the intended one thing, hierarchy is wrong.
   Stop and fix that before anything else.
2. **Squint / blur test.** `filter: blur(4px)` or `grayscale(1)` in
   devtools. Check: three gray levels, not one and not six; masses
   balanced (notan); the accent appears once; rhythm even.
3. **Three distances.** At arm's length (structure), at reading distance
   (text), at nose distance (optical details: radii, alignment, shadows).
4. **Checklist pass.** Run the observable-failure list in SKILL.md, then
   the extended list below.
5. **Report.** Each finding: *observable symptom → cause (file:line or
   value) → one-line fix*, ordered by leverage: hierarchy and emphasis,
   then contrast and legibility, then rhythm and alignment, then optical
   detail. Never open with a line edit.

### Extended observable failures

Beyond the list in SKILL.md:

- Mixed alignments in one composition (centered heading over left text)
- Same visual weight on primary and secondary actions
- Disabled state indistinguishable from enabled, or from placeholder
- Placeholder text used as the label
- Hover state exists, focus-visible state does not
- Truncation with no affordance to see the full text
- Text over an image with no scrim or with a uniform scrim
- Border *and* shadow *and* background shift all separating the same card
- Empty state, loading state or error state missing
- Numbers that should align vertically set in proportional figures
- Animations with no `prefers-reduced-motion` guard
- Skeleton or spinner shown for responses under 100ms (flicker)
- A spanning divider that partitions content which should read as one group
- A long or interruptible multi-step flow with no preserved state, clear
  next action or explicit end state
- A field rejecting a format it could have parsed (spaces in a card
  number, parentheses in a phone number, a pasted value with formatting)
- A real deadline or expiring hold that is hidden or unclear, or an
  invented deadline that creates fake urgency
