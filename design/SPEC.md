# Hello Construction Group — build spec

Build a static marketing site for a Chicago general contractor and licensed
electrical contractor, with a control that switches between three approved
design directions so the client can pick one by eye.

Its readers are other general contractors, architects and engineers who
already know the owner and are checking that the company is real, licensed
and does commercial work. Not homeowners shopping for a remodeler. The job
is credibility in ten seconds: the name, the licences, the kind of work, a
few real projects, one way to get in touch.

## Stack and ground rules

Plain HTML, CSS and a small amount of vanilla JS. **No build step, no
package manager, no framework, no dependencies.** It must run by opening
`index.html` in a browser, and by `python3 -m http.server` for relative
links.

- **Mobile first.** Phone styles are the base; everything else is a
  `min-width` media query. Never write a `max-width` query.
- **`styles/tokens.css` is generated and authoritative. Do not edit it and
  do not hard-code a colour, font size, radius or spacing value anywhere
  else.** Every value in the design is already a custom property or a
  `.t-*` type class. If something seems to need a value that is not in
  there, that is a bug in the design, not a licence to invent one — stop
  and say so.
- Semantic HTML. Real `<button>`, `<a href>`, `<input>` with a matching
  `<label>`, `<nav>`, `<header>`, `<main>`, `<footer>`. Never a `role` or
  a click handler on a `div` or `span`.
- No images except the supplied logotype. No stock photography and no
  generated imagery, ever — see **Photo placeholders**.

## Files to produce

```
index.html              Home
services.html           Services overview
commercial.html         Commercial
residential.html        Residential       (same template as commercial)
electrical.html         Electrical        (same template as commercial)
projects.html           Projects index
project.html            Project detail (one worked example)
about.html              About
contact.html            Contact
styles/tokens.css       SUPPLIED — do not edit
styles/site.css         everything else you write
scripts/theme.js        the theme switch
scripts/nav.js          the mobile menu and the Services drop-down
assets/hellocg-wordmark.png
assets/hellocg-wordmark-transparent.png
```

`residential.html` and `electrical.html` reuse the `commercial.html`
template with their own copy from CONTENT.md. The brief only wrote copy
for Commercial in full; the other two get their H1, lead and the shared
licence block, with the body sections marked as gaps.

## The theme switch

Three positions, in this order:

| value | name shown | what it is |
|---|---|---|
| `a-orange` | Direction A · Orange | the default |
| `a-blue` | Direction A · Deep blue | same design, accent only |
| `b` | Direction B · Quiet | a different design |

Behaviour:

- Sets `data-theme` on `<html>`. Nothing else. All three themes are already
  defined in `tokens.css`.
- Persists in `localStorage` under `hellocg-theme`, so the selection
  survives navigation between pages and a reload.
- **Applied before first paint.** Put a tiny inline `<script>` in `<head>`
  of every page, before the stylesheet link, that reads localStorage and
  sets the attribute. Without this the page flashes Direction A on every
  navigation. Wrap the read in try/catch — it throws in some privacy modes.
- The control itself is a `fieldset` of three `<input type="radio">` with
  labels, fixed to the bottom-right on desktop and across the bottom on
  phone, in a small neutral panel. It is scaffolding for the client review
  and gets deleted before launch, so keep it in one file and one block of
  CSS, clearly commented, and do not let it leak into the site's own
  styles.
- Give the control `aria-label="Design direction"` and make sure it is
  reachable by keyboard.

```html
<!-- in <head>, before the stylesheet -->
<script>
  try {
    var t = localStorage.getItem('hellocg-theme');
    if (t) document.documentElement.setAttribute('data-theme', t);
  } catch (e) {}
</script>
```

## Breakpoints

Three, from the brief. They are already wired into `tokens.css`; match them
in `site.css`.

| range | what changes |
|---|---|
| base, up to 750px | one column. Hamburger nav. Phone type scale, 24px page margin. |
| `min-width: 751px` | desktop type scale and section padding arrive automatically from tokens.css. Three-up card rows become two-up. |
| `min-width: 1001px` | full 12-column grids: three-up cards, four-up Why Hello. Full horizontal nav with the Services drop-down. |

Body copy never scales — 18px in Direction A and 17px in Direction B at
every width. Only headlines scale, and that happens at 751px.

## Layout primitives

Build these three and use nothing else for page structure.

```css
.section  { padding-block: var(--section-y); padding-inline: var(--page-margin); }
.container{ max-width: var(--content); margin-inline: auto; }
.band     { background: var(--surface-sunken); }   /* on .section, for an alternating section */
```

The visual page margin at 1440px (120px in A, 160px in B) is the result of
`max-width` plus `padding-inline` centring itself. **Do not hard-code it.**
Nothing in the design may depend on a pixel position.

Every section is a grid or a stack. This site gets rebuilt by hand in Wix
Studio afterward and anything absolutely positioned will not survive the
translation. The one exception is the Direction A hero scrim, below.

## Components

Use the `.t-*` classes from tokens.css for all type. Where a state is
listed, build it.

### Button
Two kinds, plus one variant that only exists over a photo.

- **Primary** — `background: var(--primary)`, `border: 1px solid
  var(--primary-border)`, `color: var(--on-primary)`, `border-radius:
  var(--radius)`, padding `var(--space-3) var(--space-4)`, label in
  `.t-label`.
  Hover swaps to `--primary-hover` / `--on-primary-hover`.
- **Secondary** — transparent fill, `1px solid var(--border-input)`,
  `color: var(--ink)`. On hover the border goes to `--ink` and the fill to
  `--surface`.
- **On-photo secondary** — border and label both `var(--ink-inverse)`.
  Only over the Direction A hero scrim. Never on `--ground` or `--surface`.
- **Disabled** — `--disabled-bg` fill and border, `--disabled-ink` label,
  `cursor: not-allowed`.
- **Focus**, for every button and link:
  ```css
  box-shadow: 0 0 0 2px var(--ground), 0 0 0 4px var(--focus);
  ```
  The ring sits *outside* the control with a gap in the page's own ground
  colour, so it never has to contrast against the control's fill. That is
  why one ring colour works on a black button and an orange one. Use
  `--focus-inverse` inside the footer. Do not replace this with `outline`
  unless you keep the offset.

Labels are written in sentence case in the HTML and rendered in capitals by
`.t-label`. Do not type them in capitals.

**Why the orange button looks the way it does:** white on `#e8590c` is
3.58:1 and fails WCAG AA. The label is therefore near-black at 5.15:1, and
the ink keyline holds the button's edge so the fill can lighten on hover
without the shape dissolving into the page. Do not "fix" this by making the
label white.

### Header
Logotype left, nav right, one button — **Start a project**. Nav is exactly:
Home · Services ▾ (Commercial · Residential · Electrical) · Projects ·
About · Contact.

The band is `var(--surface)` in every theme, including Direction A where
the page ground is warm. This is not a style choice: the logotype PNG has
an opaque white background and shows a visible white rectangle on anything
that is not white.

Logotype 140px wide on phone, 180px at `min-width: 1001px`. Use
`assets/hellocg-wordmark.png`.

- Below 1001px: hamburger, and a panel that opens with the nav stacked.
  Services expands inline — the three service links indented behind a 2px
  `--accent` rule, in `--ink-muted` at `.t-small` — rather than opening a
  second screen. **Start a project** sits full-width at the foot of the
  panel.
- At 1001px and up: the horizontal nav. The Services drop-down is the only
  element in the system with elevation: `--surface` fill, `--rule` border,
  `--radius-md`, `var(--shadow-menu)`. It must open on keyboard focus of
  the Services item as well as on hover — hover alone is not reachable.
- The current page's nav item takes a 2px `--accent` underline.

### Footer
Three columns at `min-width: 1001px`, stacked below that in the order
Legal, Contact, Links. Then a rule and the copyright line.

Direction A closes on a near-black `--footer-bg` slab; Direction B stays
white and is separated by a `--footer-rule` hairline. Both come from the
tokens — the markup is identical.

Legal lines and the copyright line are `--footer-muted`; headings, the
address and the email link are `--footer-ink`.

### Service card
Short rule, a title of the form `Commercial.` (sentence case, full stop),
two lines of scope in `--ink-muted`. Commercial is always first.

Direction A frames it: `--surface` fill, `--rule` border, `--radius`,
`var(--space-4)` padding, and a 32×3px `--accent` tick above the title.
Direction B drops the fill and border, pads to `var(--space-5)`, and uses a
24×1px `--ink` rule instead of the tick. Do this with
`[data-theme="b"] .service-card { … }` in `site.css`.

One column on phone, two at 751px, three at 1001px.

### Project card
Photo placeholder, type label (`.t-label`, `--ink-muted`, reads Commercial
/ Residential / Electrical), title, then the neighbourhood and one-line
scope. Direction A frames it in a card with the photo flush to the top
edge; Direction B removes the card, gives the image a `--rule` border, and
sets the text on `--ground` beneath it.

### Facts row
Neighbourhood · Type · Scope · Role · Year, at the head of a project
detail page. Role is always spelled out — **GC of record** or **Electrical
subcontractor**. Labels `.t-label` in `--ink-muted`, values `.t-h3` in
`--ink`. Direction A bands it in `--surface-sunken` with a `--rule` border;
Direction B uses a hairline above and below and no fill. Two columns on
phone, three at 751px, five at 1001px. Never drop a fact to make it fit.

### Form
Name · Company (optional) · Email · Project type (Commercial / Residential
/ Electrical / Not sure) · Message · **Send**. Nothing else — no phone
field, no budget field, no map.

Labels sit above their field and are always visible. Never use a
placeholder as a label.

- Default: `--surface` fill, `1px solid var(--border-input)`.
- Focus: border to `--ink`, plus the standard outside ring.
- Error: `--error-bg` fill, `--error` border, and a message below in
  `--error`. Write it as an instruction with an example, not a diagnosis:
  *Enter an email address we can reply to, for example name@company.com.*
- Success: the form is replaced by a line that leads with the word
  **Sent.** in `--success` followed by plain confirmation in `--ink`.

Colour is never the only signal for either state — the words carry it.

The form does not submit anywhere. Wire the Send button to show the success
line client-side so the state is demonstrable, and leave a comment saying
where a real handler goes.

### Google reviews (Direction A only)
Four cards, each a five-star row in `--accent-ink`, the placeholder text
`Google review, 5 stars`, and the Google mark. `tokens.css` already hides
the whole block in Direction B via `[data-theme="b"] .reviews { display:
none; }` — give the section `class="reviews"` and do not add your own
logic.

**No Google asset ships with this package and a trademark must not be
redrawn from memory.** Render a labelled dashed placeholder where the mark
goes. Drop in the official mark from Google's own brand resources at build
time, or cut the block — it is optional and the client has not decided.

These carry **no invented review text**. The brief rules out testimonials.

## Photo placeholders

No project photography exists. The client's images are under
non-disclosure and have not arrived.

Every photo slot is a flat `--surface-sunken` block with a `--rule` border
and a label in `--ink-muted` naming exactly what belongs there —
`PHOTO: commercial interior, from Ron`. Label style: `.t-small`, uppercase,
`letter-spacing: 0.1em`.

Use no stock photography and no generated imagery. On a contractor's site
an image that reads as the company's own work and is not is a plain
misrepresentation.

## The hero — the one place the two directions differ structurally

Write one piece of markup and let CSS do the rest:

```html
<section class="hero">
  <figure class="hero-media"><!-- photo placeholder --></figure>
  <div class="hero-copy">
    <h1 class="t-display">…</h1>
    <p class="t-lead">…</p>
    <div class="hero-actions">…</div>
  </div>
</section>
```

- **Base (phone, all themes)** — stacked. Media above, copy below on
  `--ground` in `--ink`. Buttons full width, primary then secondary.
- **Direction A at `min-width: 751px`** — the media fills the hero,
  `--hero-scrim` is laid over the whole image with a pseudo-element, and
  `.hero-copy` sits over it, bottom-aligned, with the headline and lead in
  `--ink-inverse` and the secondary button in its on-photo variant. Hero
  height 820px.
- **Direction B at any width** — never overlays. At `min-width: 1001px`
  the media and copy sit side by side in two columns. B never bleeds a
  photo and never puts text on an image.

The scrim is four stops on purpose. It is graded against where the text
actually lands: white clears 4.3:1 at the top of the headline, which needs
3:1 at that size, and 11.6:1 at the sub, which needs 4.5:1. A two-stop
scrim ending at the hero's midpoint leaves the first line of the headline
sitting on bare photograph. Do not simplify it.

On phone Direction A stacks rather than scrimming because at 375px the
headline runs six lines, and no scrim dark enough to carry white across all
six would leave the photograph visible at all.

## Non-negotiables

These are settled client decisions, not suggestions.

1. **No phone number anywhere.** Not in the header, not in the footer, not
   on the contact page, not in a `tel:` link. The only contact routes are
   the form and `info@hellocg.com`.
2. **The three legal lines are fixed text.** Reproduce them character for
   character, in the footer of every page. They are in CONTENT.md.
3. **The nav is exactly** Home · Services ▾ (Commercial · Residential ·
   Electrical) · Projects · About · Contact, in that order, with one
   button.
4. **"Veteran-founded."** Never "veteran-owned".
5. **No testimonials.** The Google reviews block is not a testimonial and
   carries no written review text.
6. **Commercial comes first** everywhere the three services appear.
   Residential and electrical sit under it. Nothing is dropped.
7. **Bracketed `[RON: …]` text is a gap for the client to fill, not copy.**
   Render it visibly distinct — monospace, in a dashed 1px outline. Never
   invent content for one. There is no token for this because it is not a
   site colour; use `#6b4bc4` and delete the rule before launch.

## Accessibility

Every pair below already holds in all three themes. Keep it that way.

- Body text 4.5:1 against its background; 3:1 for text at 24px and above,
  and for any border, focus ring or mark that carries meaning.
- `--ink-muted` is the only secondary text colour. Do not lighten it. The
  warm grey `#8a8580` is in the palette as `--border-input` precisely
  because it is too light for body text at 3.3:1 and fine for a control
  border at 3.65:1.
- Every interactive element is keyboard reachable and shows the focus ring.
- The Services drop-down opens on focus, not hover alone.
- Touch targets at least 44px. The button padding already gives 48px.
- One `<h1>` per page, and heading levels do not skip.
- The logotype `<img>` needs `alt="Hello Construction Group"`.
- The theme radios need a group label.

## Acceptance checks

Run these before you call it done and report the results.

1. `grep -rniE 'tel:|\([0-9]{3}\)[[:space:]]*[0-9]{3}|[0-9]{3}[-.][0-9]{3}[-.][0-9]{4}' --include='*.html' .` — must return nothing.
2. `grep -rni 'veteran-owned' --include='*.html' .` — must return nothing.
3. Every `.html` contains all three legal lines verbatim and `info@hellocg.com`.
4. No hex colour, `px` font-size, or raw spacing value in `site.css` that
   is not a `var(--…)`. `grep -nE '#[0-9a-fA-F]{3,8}\b' styles/site.css` —
   the only allowed hit is the `[RON: …]` placeholder colour `#6b4bc4`.
   `grep -nE 'font-size:[^v]' styles/site.css` must return nothing.
5. Switch through all three themes on every page: no unstyled flash, the
   selection survives navigation, and the reviews block is absent in
   Direction B.
6. At 375px, 768px and 1440px: no horizontal scrollbar on any page.
7. Tab through the home page and the contact page: every control takes a
   visible focus ring, and the Services drop-down opens on focus.
8. The only `<img>` on the site is the logotype.
