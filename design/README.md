# Hello Construction Group — build package

Everything needed to build the site, with a toggle that switches between
the three approved design directions.

## What's here

| file | what it is |
|---|---|
| `CLAUDE.md` | the short version — hard rules and what to build. Claude Code reads this automatically. |
| `SPEC.md` | the full build spec: stack, file layout, theme switch, breakpoints, every component and its states, accessibility floors, acceptance checks. |
| `CONTENT.md` | all copy for all nine pages, verbatim, with the client's gaps marked. |
| `styles/tokens.css` | the three themes as CSS custom properties, mobile-first. Generated from the design system — do not hand-edit. |
| `assets/` | the logotype, cropped to the header lockup, plus a transparent-background variant. |
| `reference/` | what the home page should look like in both directions, desktop and phone. |

## To use it

Unzip somewhere, then from inside the folder:

```
claude
```

and tell it: **"Read CLAUDE.md and build the site."**

It will pick up `CLAUDE.md` on its own, which points at the spec and the
content. When it finishes, open `index.html` — the theme control is in the
bottom-right corner.

## The three directions

- **Direction A · Orange** — Site and steel. Warm off-white ground, heavy
  condensed headlines, one construction-orange accent, full-bleed hero with
  a dark scrim, framed cards, near-black footer. The default.
- **Direction A · Deep blue** — the same design with a different accent.
  Seven custom properties differ and nothing else.
- **Direction B · Quiet** — Quiet and architectural. White, light serif
  headlines, no accent colour, photos framed with white space and never
  overlaid, white footer. Drops the Google reviews block.

## Two things worth knowing before you read the spec

**The orange button has a near-black label on purpose.** White on `#e8590c`
is 3.58:1 and fails WCAG AA. Ink on it is 5.15:1. The 1px ink keyline holds
the button's edge so the fill can lighten on hover. Do not "fix" this.

**The hero scrim has four stops on purpose.** It is graded against where
the text actually lands. A two-stop gradient ending at the hero's midpoint
leaves the first line of the headline on bare photograph.

## After the direction is chosen

The site gets rebuilt by hand in Wix Studio. That is why nothing here
depends on a pixel position, why every section is a grid or a stack, and
why every value lives in `tokens.css` — the Wix theme panel gets set
straight from that file. Once the client picks, delete the two themes he
didn't pick, delete the theme control, and the remaining CSS is the spec
for the Wix build.
