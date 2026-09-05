# visual-design

A Claude Code skill for the judgment that separates UI that *measures* correctly from UI that *looks* correct. It fires on any task with a visual surface, including ones that never say "design" — "make this look better", "build a landing page", "clean up this component".

## What it does

A six-step decision procedure, top-down: establish the job and the one thing to notice; fix a spacing unit and a type scale; build the palette in OKLCH and check every text pair; set type measure, leading and tracking; set rhythm and tokens; then run an optical pass and a critique pass. Seven reference files carry the depth and are read only when a step needs them.

## What it deliberately does not do

It does not teach the mechanics Claude already gets right.

Before this skill was written, two baseline runs — build a pricing card, critique a pricing card with fifteen planted defects — recorded what Claude produces unaided. Of seventeen candidate rules, ten passed in both runs. Claude independently built a rounded 1.25 type scale, kept a 4px grid, computed WCAG ratios for every pair, tightened leading and tracking as size grew, remapped semantic colors for dark mode with surfaces lightening on elevation, and, in review, caught fractional font sizes, orphan spacing values, a 170-character measure and brand blue on five elements.

Shipping rules for any of that would cost context on every invocation and change nothing.

## Where Claude actually fails

Both runs failed in the same three places:

| Failure | Evidence |
| --- | --- |
| Color chosen in HSL | *"OKLCH: more perceptually even, but I'd have needed a conversion step to verify contrast; HSL let me verify directly."* Every fix in the critique run was given in HSL. |
| Emphasis stacked | The recommended tier got border + ring + badge + filled button + tinted shadow + lift, described as *"five cooperating signals"*. The critique run's top recommendation was to add more. |
| Optical layer skipped | Concentric radii, gradient interpolation space and optical centering were neither applied when building nor recognised when reviewing. The same-radius-everywhere defect was diagnosed as "half-pill". |

So the skill ships four hard rules — OKLCH palettes, one emphasis device and one accent element per view, a mandatory optical pass, and "use a scale, never defend a ratio" — plus a dependency-free script that closes the HSL rationalization: `scripts/color.py contrast` accepts `oklch()` directly and prints WCAG 2 and APCA.

## Intellectual honesty

The skill ranks principles by leverage and says plainly that the golden ratio has no solid empirical support, that musical-interval type scales have no perceptual link to hearing, and that a 1.25 scale and a 1.618 scale both beat choosing sizes by eye because *consistency* is what does the work. It documents where principles conflict — 8pt grid vs scale rounding, WCAG vs brand color, Hick vs progressive disclosure, aesthetic–usability vs Rams — and how to resolve each.

## Install

See the [repository README](../../README.md) for the plugin install.

To copy this skill directly instead:

```bash
# personal, all projects
mkdir -p ~/.claude/skills && cp -r skills/visual-design ~/.claude/skills/

# project-local, shared via git
mkdir -p .claude/skills && cp -r skills/visual-design .claude/skills/
```

Both are safe to re-run to update an existing copy.

## Usage

Describe the surface you want built, improved or reviewed. The skill fires on layout, spacing, typography, color, contrast, dark mode, shadows, radii, hierarchy and critique vocabulary, and on plain requests like "polish this".

The color script needs only Python 3. It lives inside the skill folder, so the path depends on where the skill is installed (plugin cache, `~/.claude/skills/visual-design`, or `.claude/skills/visual-design`):

```bash
S=~/.claude/skills/visual-design/scripts/color.py
python3 $S oklch 0.58 0.16 250                        # → #0d7dd4
python3 $S contrast '#6d7277' '#fff' '#fff' '#0465af'  # → 4.86:1 / +73.7, 6.02:1 / −84.7
python3 $S contrast 'oklch(0.58 0.3 250)' '#fff'       # → out of gamut: max chroma 0.164
```

Ratios are computed on the 8-bit hex that ships; out-of-gamut colors are flagged with the largest usable chroma rather than scored.

## Scope

Anything with a visual surface. Not logic, backend, data or CLI work with no visual output. For distinctive aesthetic direction on new UI, the `frontend-design` skill is complementary; this one is about getting the craft right on whatever direction was chosen.

## What is verified

The hard rules, the triggering description and the decision procedure were exercised against the same two pricing-card scenarios with the skill present; see [the GREEN results](../../docs/superpowers/plans/2026-09-05-visual-design-green-results.md) in the repository (not copied with the skill folder). Every number in the references was computed with the shipped script, not recalled. The perception and heuristic content is summarised from the primary sources and has not been tested against a scenario, because it has no rule to violate.
