# Tokens and systems

Read this when setting up design tokens, adding theming or dark mode,
naming components, or deciding how to structure a session's design work.

## Atomic design

Brad Frost's five levels: **atoms** (button, input, label, icon) →
**molecules** (search form = input + button) → **organisms** (header,
pricing card) → **templates** (page structure with placeholders) →
**pages** (real content). Tokens sit below atoms.

The useful discipline: an atom knows nothing about layout; a molecule owns
the spacing *between* its atoms; an organism owns the spacing between
molecules. When a component sets its own outer margin, it has broken the
level above it — spacing between siblings belongs to the parent (use `gap`).

## Three-tier tokens

The single structural decision that makes theming and dark mode tractable.

| Tier | Contains | Example | Changes when |
|---|---|---|---|
| **Primitive** | raw values, named by what they *are* | `--blue-600`, `--space-4`, `--radius-lg` | the palette or scale changes |
| **Semantic** | roles, named by what they are *for*, alias primitives | `--color-accent`, `--color-text-muted`, `--surface-raised` | theme, mode, or brand changes |
| **Component** | per-component slots, alias semantics | `--button-bg`, `--card-radius` | a component's design changes |

Rules:

- Component CSS references **semantic or component** tokens only. Never a
  primitive, never a literal. `background: var(--blue-600)` inside a button
  is the bug that makes dark mode a rewrite.
- Dark mode, high contrast and brand themes **remap the semantic tier
  only**. Primitives are constant across themes.
- A component tier exists so a component can be restyled without touching
  semantics; skip it until a second theme or variant needs it.

### Worked example — pricing card tokens

```css
/* ---- Primitive: what values exist ---- */
:root {
  /* OKLCH: hue 250, chroma tapered at the ends so every step is in gamut */
  --blue-50:  oklch(0.97 0.012 250);
  --blue-100: oklch(0.93 0.03 250);
  --blue-300: oklch(0.78 0.11 250);
  --blue-500: oklch(0.58 0.16 250);
  --blue-600: oklch(0.50 0.14 250);
  --blue-700: oklch(0.42 0.11 250);

  /* Neutrals carry a trace of the brand hue */
  --gray-50:  oklch(0.975 0.006 250);
  --gray-100: oklch(0.96 0.01 250);
  --gray-200: oklch(0.92 0.01 250);
  --gray-500: oklch(0.55 0.01 250);
  --gray-600: oklch(0.42 0.01 250);
  --gray-800: oklch(0.28 0.015 250);
  --gray-850: oklch(0.24 0.015 250);
  --gray-900: oklch(0.20 0.015 250);
  --gray-950: oklch(0.16 0.015 250);

  --space-1: 4px;  --space-2: 8px;  --space-3: 12px; --space-4: 16px;
  --space-6: 24px; --space-8: 32px; --space-12: 48px; --space-16: 64px;

  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 16px; --radius-full: 999px;

  /* The worked ladder from optical-correction.md; change it there first */
  --shadow-1: 0 1px 2px oklch(0.2 0.02 250 / 0.06), 0 1px 3px oklch(0.2 0.02 250 / 0.08);
  --shadow-2: 0 2px 4px oklch(0.2 0.02 250 / 0.06), 0 6px 16px oklch(0.2 0.02 250 / 0.10);
  --shadow-3: 0 4px 8px oklch(0.2 0.02 250 / 0.08), 0 16px 40px -8px oklch(0.2 0.02 250 / 0.16);
}

/* ---- Semantic: what values mean. Only this tier changes per theme. ---- */
:root {
  --color-bg:            var(--gray-100);
  --color-surface:       white;
  --color-surface-raised: white;
  --color-border:        var(--gray-200);
  --color-text:          var(--gray-900);
  --color-text-muted:    var(--gray-600);
  --color-accent:        var(--blue-600);   /* 500 is 4.28:1 with white; 600 is 6.02:1 */
  --color-accent-hover:  var(--blue-700);
  --color-on-accent:     white;
  --elevation-card:      var(--shadow-1);
  --elevation-card-hover: var(--shadow-2);
  --elevation-featured:  var(--shadow-3);
  --space-inset-surface: var(--space-8);
  --radius-surface:      var(--radius-lg);
  --radius-control:      var(--radius-md);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg:            var(--gray-950);
    --color-surface:       var(--gray-900);
    --color-surface-raised: var(--gray-850);   /* lighter = higher */
    --color-border:        oklch(1 0 0 / 0.10); /* alpha borders survive any surface */
    --color-text:          var(--gray-100);
    --color-text-muted:    oklch(0.93 0.01 250); /* Lc −91 on raised surface at 14px/400 */
    --color-accent:        var(--blue-300);     /* lighter accent keeps contrast */
    --color-accent-hover:  var(--blue-100);
    --color-on-accent:     var(--gray-950);
    --elevation-card:      0 1px 2px oklch(0 0 0 / 0.4);
    --elevation-card-hover: 0 4px 12px oklch(0 0 0 / 0.5);
    --elevation-featured:  0 8px 24px -6px oklch(0 0 0 / 0.6);
  }
}

/* ---- Component tokens: per-component slots alias semantics ---- */
:root {
  --card-padding:    var(--space-inset-surface);
  --card-radius:     var(--radius-surface);
  --card-cta-radius: var(--radius-control);
}

/* ---- Component CSS: consumes semantic and component tokens only ---- */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--card-radius);
  padding: var(--card-padding);
  box-shadow: var(--elevation-card);
}
.card__cta {
  background: var(--color-accent);
  color: var(--color-on-accent);
  border-radius: var(--card-cta-radius); /* see optical-correction.md */
}
```

Dark mode is twelve semantic lines. Nothing in `.card` changed.

### Naming

`--{category}-{role}-{variant?}-{state?}`: `--color-text-muted`,
`--color-accent-hover`, `--space-inset-card`. Numeric ramps for
primitives (`50`–`950`, lightness descending). Do not name semantics by
appearance (`--color-blue-button` is a primitive in disguise).

### Spacing and type tokens

Spacing tokens are the 8-point set. Type tokens pair size with line
height so they cannot drift: `--text-md: 1rem / 1.5`, `--text-2xl: 2.5rem
/ 1`. A composite token per role (`--type-price`, `--type-body`) beats
loose size tokens once a second theme exists.

### The DTCG format

The W3C Design Tokens Community Group JSON format is what tooling
(Style Dictionary, Tokens Studio) exchanges:

```json
{
  "color": { "blue": { "600": {
    "$type": "color",
    "$value": {
      "colorSpace": "oklch",
      "components": [0.50, 0.14, 250],
      "alpha": 1,
      "hex": "#0465af"
    }
  } } },
  "semantic": { "accent": {
    "$type": "color",
    "$value": "{color.blue.600}"
  } }
}
```

Aliases (`{color.blue.600}`) are the three tiers in JSON.

## When to add a token

On the **third** use of a value. First use: a literal is fine. Second: a
coincidence. Third: a rule, and it gets a name. Conversely, a token with
one consumer is a literal with extra steps — inline it or generalize it.

Lint for raw values in component CSS (`px` colors, hex codes, magic
numbers) once tokens exist; the anti-pattern list in SKILL.md is the
lint rule set.

## Double diamond in a coding session

Discover → Define → Develop → Deliver, diverging then converging twice.
Compressed for a single component:

1. **Discover** (2 minutes): who sees this, on what device, coming from
   where, to do what. What exists nearby that it must match.
2. **Define** (1 sentence): "This surface exists so that ___ can ___; the
   one thing they must notice is ___." That sentence decides hierarchy
   and the single emphasis device.
3. **Develop**: try two emphasis mechanisms, not five stacked. Pick one.
   Build with tokens.
4. **Deliver**: the optical pass, then the critique checklist, then ship.

Skipping Define is how a pricing card ends up with a badge, a border, a
lift, a glow and a filled button all saying "this one".
