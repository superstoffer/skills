# Perception and behavior laws

Read this when deciding how many options to show, how large and where to
put a control, how fast to respond, or what a user will remember. Each
law below states what it actually established and where it is misapplied.

## Gestalt grouping

The basis for spacing. Elements are read as belonging together by
**proximity** (close together), **similarity** (same shape/color),
**common region** (inside the same border or surface), **closure** and
**continuity**. Proximity beats similarity: two related items 8px apart
with 24px to the next group read as a group regardless of color.

Rule: gaps *inside* a group are smaller than gaps *between* groups, at
every level. The most common rhythm bug is a label the same distance from
its field as from the previous field.

## Weber's law

The just-noticeable difference is proportional to the stimulus. A 2px
difference in padding is invisible at 32px and glaring at 4px; a 10%
change in type size is barely a step. This is why scales use ratios rather
than fixed increments, and why a step under ~15% does not read as a level.

## Fitts's law

Time to acquire a target ≈ a + b · log₂(D/W + 1). Larger and nearer is
faster; the effect is logarithmic, so doubling a tiny target helps far more
than doubling a large one. Screen edges and corners have effectively
infinite width (the cursor stops there).

Applied: hit areas larger than the visible control (44 × 44 minimum on
touch, 24 × 24 legal floor); the primary action nearest where attention
ends (bottom of a form, bottom of a card); full-width buttons in narrow
containers; destructive actions *farther* away and smaller, deliberately.

## Hick's law

Decision time grows with log₂(n + 1) for n equally likely, unfamiliar
options. It does not apply to ordered or well-learned sets: an alphabetical
list of 50 countries is faster than a menu of 6 novel categories. Reduce
choices when they are novel and unordered; sort and group when they are
not. Conflict with progressive disclosure is resolved in SKILL.md.

## Miller's "7 ± 2"

Miller (1956) measured immediate recall of one-dimensional stimuli such as
digits and tones. It says nothing about menu length, navigation items, or
how many cards fit on a page — those are recognition tasks, not recall.
The transferable finding is **chunking**: recall improves when items are
grouped into meaningful units. Phone numbers in 3-3-4, card numbers in
4-4-4-4, a 12-item nav in three labeled groups of four.

## Tesler's law (conservation of complexity)

Every process has an irreducible core of complexity; design decides who
carries it, the user or the system. A date picker that accepts "next
tuesday" moved complexity into the parser. Smart defaults, remembered
choices and inferred fields are all transfers. The failure mode is
transferring complexity *to* the user and calling it flexibility.

## Jakob's law

Users spend most of their time on other sites; they arrive expecting yours
to work the same way. Logo top-left goes home, cart top-right, search is a
magnifier, primary button is filled and on the right of a dialog.
Deviation costs attention; spend it only where the deviation buys
something users will notice.

## The Doherty threshold

Productivity rises sharply when system response drops below ~400ms.
Perceptual budgets: under 100ms feels instantaneous (no indicator);
100–400ms needs an immediate state change on the control; over 1s needs
a progress indicator or skeleton; over 10s needs a way out. Optimistic
UI (show the result, reconcile later) keeps interactions under the
threshold when the network cannot.

## Von Restorff (isolation) effect

The item that differs from its group is the one remembered. This only
works if *one* item differs: emphasize the recommended tier, the primary
action, the unread item — and nothing else in that view. Two isolated
items cancel. This is the psychological basis for "accent color on one
element per view".

## Serial position effect

First and last items in a sequence are recalled best (primacy, recency);
the middle is lost. Put the most important nav items at the ends; the
default or recommended choice in a list of three gets attention from the
rule of odds, not from memory. In long lists, the middle needs visual
grouping to survive.

## Peak–end rule

Experiences are judged by their most intense moment and their end, not
their average. Invest in the success state, the completion screen, the
error recovery path, and the empty state; a smooth middle does not
compensate for a confusing end. Also: onboarding's last step is what the
whole onboarding will be remembered as.

## Aesthetic–usability effect

Users rate attractive interfaces as easier to use and forgive minor
problems in them. Two consequences: polish has real functional value, and
polish *masks* usability problems in testing — users of a beautiful
prototype under-report friction. Test ugly wireframes for flow, then
polish. See the conflict with Rams in SKILL.md.

## Quick reference

| Law | Use it for | Do not use it for |
|---|---|---|
| Fitts | target size, placement, edge targets | justifying huge everything |
| Hick | novel, unordered choices | sorted lists, expert menus |
| Miller | chunking long inputs and lists | capping nav at 7 |
| Tesler | deciding who carries complexity | claiming complexity can vanish |
| Jakob | defaults and conventions | never innovating |
| Doherty | response-time budgets | — |
| Von Restorff | one emphasis per view | multiple highlights |
| Serial position | ordering nav and lists | — |
| Peak–end | prioritizing polish effort | — |
| Aesthetic–usability | why polish matters | skipping usability testing |
