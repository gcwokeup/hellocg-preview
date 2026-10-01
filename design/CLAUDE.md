# Hello Construction Group — website build

Read `SPEC.md` first, then `CONTENT.md`. Build the static site they
describe. `reference/` shows what the result should look like.

## The rules that break the build if you miss them

- **`styles/tokens.css` is generated. Do not edit it, and do not write a
  color, font size, radius or spacing value anywhere else.** Everything is
  already a `var(--…)` or a `.t-*` class. If you think you need a value
  that is not there, stop and say so — it is a design bug, not a license to
  invent one.
- **Mobile first.** Phone styles are the base. `min-width` queries only.
  Never a `max-width` query.
- **No build step, no dependencies.** Plain HTML, CSS and vanilla JS. It
  must run by opening `index.html`.
- **No phone number anywhere on the site**, including `tel:` links.
- **The three legal lines are fixed text.** Character for character, in the
  footer of every page.
- **No stock photography and no generated imagery.** Every photo slot is a
  labeled placeholder block. The only image on the site is the supplied
  logotype.
- **Bracketed `[RON: …]` text is a gap for the client, not copy.** Render
  it visibly distinct. Never invent content for one.
- Semantic HTML throughout. Real `<button>`, `<a href>`, `<input>` +
  `<label>`. Never a click handler on a `div`.

## What you are building

Nine page types plus shared header and footer, with a control that switches
between three approved design directions (`a-orange`, `a-blue`, `b`) by
setting `data-theme` on `<html>`. All three themes already exist in
`tokens.css`; the switch sets one attribute and persists the choice.

The client picks a direction by clicking through the result, so all three
have to look finished.

## When you are done

Run the acceptance checks at the end of `SPEC.md` and report what each one
returned.
