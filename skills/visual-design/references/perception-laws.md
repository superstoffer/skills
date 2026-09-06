# Perception and behavior laws

Read this when deciding how many options to show, how large and where to
put a control, how fast to respond, or what a user will remember. Each
law below states what it actually established and where it is misapplied.

## Law of Prägnanz (good figure)

The eye resolves an ambiguous or complex form into the simplest, most
stable interpretation available. This is the umbrella the other Gestalt
laws sit under: grouping happens at all because a grouped reading is
simpler than an ungrouped one.

Applied to the whole composition, not the parts: at a squint, the page
should reduce to a few clean rectangles. Icons built from circles,
rectangles and one stroke weight read faster than accurate outlines.
When a screen feels busy but every element is justified, the failure is
usually Prägnanz — the *shape of the whole* has no simple reading.

Not "make everything minimal". Prägnanz is about perceptual simplicity
of form, not quantity of content: a dense table on a clean rectangular
grid has good Prägnanz; three sparse cards at odd angles do not.

## Gestalt grouping

The basis for spacing. Elements are read as belonging together by:

- **Proximity** — close together. The default grouping tool and the one
  to reach for first, because it costs no ink.
- **Similarity** — same shape, color, size or orientation, even far
  apart. This is what makes small multiples work, and what makes the
  fifth card styled slightly differently read as a different *kind* of
  thing rather than a card with a typo. One treatment per role.
- **Common region** — inside the same border or surface. A container can
  overcome spacing or similarity, which makes it a strong grouping tool.
  Nest three deep and hierarchy dies: everything is inside something,
  so nothing is grouped.
- **Connectedness** — a connected region with uniform color, texture or
  motion tends to read first as one unit. A line or bar that physically
  joins already-distinct elements is the related cue of *element
  connectedness*. Use explicit connectors for steppers, diagrams and
  leader lines. An enclosing shape is common region, not connectedness.
- **Closure and continuity** — the eye completes interrupted shapes and
  follows the smoothest path. A card cropped by the viewport edge still
  reads as a whole card, which is what makes horizontal scrollers
  legible as scrollers.

Rule: gaps *inside* a group are smaller than gaps *between* groups, at
every level. The most common rhythm bug is a label the same distance
from its field as from the previous field.

These are tendencies, not a universal precedence ladder. Connectedness
and common region can each overcome proximity or similarity in controlled
displays, but the result depends on the strength and combination of cues;
strong proximity can be as efficient as connectedness. Make the intended
cues reinforce one another and test conflicts. A divider that spans a
container can partition it into regions and weaken grouping across that
boundary, so do not put one between a heading and body that should read
together.

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

Applied to width: hit areas larger than the visible control (44 × 44
minimum on touch, 24 × 24 legal floor); full-width buttons in narrow
containers; destructive actions *farther* away and smaller, deliberately.

Applied to distance: D is measured from where the pointer already is,
which is where attention last ended — not from the centre of the screen.
So put the action against its object. Row actions inline in the row
rather than in a top toolbar; submit directly under the last field, not
above the form; menus opening at the cursor; a primary action at the
bottom of the card it belongs to. Distance and width trade off, and
shortening travel is usually cheaper than growing the target, because
growing it costs density.

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

## Postel's law (robustness principle)

"Be conservative in what you send, be liberal in what you accept."
Originally about TCP implementations (RFC 761, RFC 1122). The interface
reading: accept input in any form a user might reasonably produce, and
render output in one consistent form.

Applied: a card or phone field that strips spaces, dashes and parentheses
instead of rejecting them; a date field that takes `2026-09-06`, `6/9/26`
and "next tuesday"; paste that survives Word formatting; search that
tolerates a typo. Validate on blur or submit rather than per keystroke,
and phrase the failure as what *would* be accepted, not what was wrong.

Not silent coercion. Liberal parsing must show what it decided — "next
tuesday" resolves to a visible `Tue 8 Sep 2026` the user can correct.
Quietly guessing an ambiguous date is worse than rejecting it — and that
condition is load-bearing, because protocol designers have since walked
Postel's law back (RFC 9413) on the grounds that tolerant parsers let
malformed input become the de facto spec. Interfaces escape that only by
showing the interpretation to a human who can correct it. This is
Tesler's law with a direction, kept honest by Norman's feedback.

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

## Parkinson's law

"Work expands so as to fill the time available for its completion."
Parkinson introduced the aphorism satirically; later experiments found
bounded effects when people were given excess time or expected spare time.
They do not show that a descriptive estimate makes a task fill that time.

Keep four concepts separate: an **estimate** forecasts duration; an
**anchor** can bias a forecast; a **deadline** constrains completion; a
**time budget** allocates a resource. Keep truthful, measured estimates —
they help users decide whether to start and plan their time. Reduce the
work with autofill, saved payment and sensible defaults, not by hiding or
shortening the estimate.

Where a limit is real and consequential (session timeout, held seat,
booking window), communicate it clearly and show a countdown when it is
operationally useful. Never invent urgency. Distinct from Doherty, which
governs *system* response time; Parkinson concerns slack in *user* task
time.

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

## Zeigarnik and Ovsiankina effects

Zeigarnik (1927) reported better recall for interrupted tasks, but a 2025
meta-analysis found no general recall advantage: interrupted and completed
tasks were recalled at about the same rate. The same synthesis found a
general tendency to resume an interrupted task when given the opportunity
— the **Ovsiankina effect** — although its size depends on the task and
setting.

Applied: for genuinely long or interruptible work, preserve completed
state, show the remaining work accurately and make the next action
obvious. That supports orientation and resumption; do not justify a
progress indicator with a supposed memory boost. In web surveys, progress
indicators do not reliably reduce dropout and their effect depends on the
presentation, so test them when completion is the goal. Pairs with
Shneiderman's closure: make the open state clear, then end the sequence
explicitly.

**Endowed progress** is narrower evidence from reward programs. Nunes and
Drèze gave car-wash customers either 2 of 10 stamps or 0 of 8; both groups
still needed eight purchases. Redemption was 34% versus 19%. Treat this as
evidence that a credible head start can affect pursuit of a discrete,
extrinsic reward — not that any partly filled bar motivates. Do not pad a
goal, disguise a bonus as work the user completed or manufacture
incompleteness. A "your profile is 60% complete" meter for data the
product does not need is a dark pattern and fails Rams's *honest*.

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
| Prägnanz | simplifying the shape of the whole | arguing for less content |
| Proximity | grouping without ink | — |
| Similarity | one treatment per role | grouping across a stronger cue |
| Common region | strong grouping when spacing fails | nesting containers deeply |
| Connectedness | explicit connectors in steppers, diagrams, leader lines | treating every separator as a connector |
| Weber | why steps need to be ratios | — |
| Fitts | target size, travel distance, edge targets | justifying huge everything |
| Hick | novel, unordered choices | sorted lists, expert menus |
| Miller | chunking long inputs and lists | capping nav at 7 |
| Tesler | deciding who carries complexity | claiming complexity can vanish |
| Postel | tolerant input parsing, shown back | silent coercion of ambiguity |
| Jakob | defaults and conventions | never innovating |
| Doherty | system response-time budgets | user task duration |
| Parkinson | caution about real slack; honest estimates; real limits | suppressing estimates or inventing urgency |
| Von Restorff | one emphasis per view | multiple highlights |
| Serial position | ordering nav and lists | — |
| Zeigarnik / Ovsiankina | preserving state and a clear resume path | claiming a general recall boost |
| Endowed progress | credible head starts toward discrete rewards | padding goals or faking completion |
| Peak–end | prioritizing polish effort | — |
| Aesthetic–usability | why polish matters | skipping usability testing |

## Sources for the disputed effects

- Palmer, [common region (1992)](https://doi.org/10.1016/0010-0285(92)90014-S);
  Palmer and Rock, [uniform connectedness (1994)](https://doi.org/10.3758/BF03200760);
  Han, Humphreys and Chen, [connectedness versus proximity (1999)](https://doi.org/10.3758/BF03205537)
- Bryan and Locke, [time limits and work rate (1967)](https://doi.org/10.1016/0030-5073(67)90021-9);
  Brannon et al., [expected spare time (1999)](https://doi.org/10.3758/BF03210823);
  Goswami and Urminsky, [time limits and duration estimates (2020)](https://doi.org/10.1017/S1930297500008196)
- Ghibellini and Meier, [Zeigarnik and Ovsiankina meta-analysis (2025)](https://doi.org/10.1057/s41599-025-05000-w);
  Villar, Callegaro and Yang, [progress-indicator meta-analysis (2013)](https://doi.org/10.1177/0894439313497468);
  Nunes and Drèze, [endowed progress (2006)](https://doi.org/10.1086/500480)
