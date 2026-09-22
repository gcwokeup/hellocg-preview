# Copy, page by page

Use this text as written. It is the client's approved copy.

Bracketed `[RON: …]` and `[…]` text is a **gap the client will fill**.
Render it as visible placeholder text in a distinct style — monospace,
`#6b4bc4`, inside a 1px dashed outline of the same colour. Never invent
content for one.

Titles and meta descriptions are for the build, not the page. They are here
so headline hierarchy matches.

---

## Site-wide

**Header CTA:** Start a project

**Nav, exactly and in this order:**
Home · Services ▾ (Commercial · Residential · Electrical) · Projects · About · Contact

**Footer, three columns.**

Legal — reproduce character for character:

> Hello Construction Group, a DBA of Hello Home Construction Co.
> City of Chicago General Contractor License TGC133426 · Electrical Contractor License ECC96203
> EPA Lead-Safe Certified Firm

Contact:

> 4311 N. Ravenswood Ave., Suite 100
> Chicago, IL 60613
> info@hellocg.com

Links: Services · Projects · About · Contact

Footer bottom line:

> © 2026 Hello Home Construction Co. · Serving Chicago `[RON: and the suburbs? which?]`

**There is no phone number on this site.** Not in the header, not in the
footer, not on the contact page.

---

## Home — `index.html`

### Hero
- **H1:** Commercial, residential and electrical. Built right, in Chicago.
- **Sub:** Licensed general contractor and electrical contractor. We self-perform the electrical and the finish work, so the schedule is ours to keep.
- **Buttons:** See our work (primary) · Start a project (secondary)
- **Photo:** `[RON: one strong commercial interior]`

### What we do — three cards, commercial first
- **Eyebrow:** What we do
- **H2:** What we do

**Commercial.** Tenant build-outs, industrial and plant work. One licensed contractor for the general trades and the electrical.

**Residential.** Kitchens, baths and high-end renovations, with the same crew and the same standards.

**Electrical.** Licensed electrical contractor. Service upgrades, new circuits, build-out power and lighting.

### Why Hello — four short items, on a banded section
- **H2:** Why contractors, architects and engineers bring us in

**Licensed on both sides.** General contractor and electrical contractor under one roof, so there is one contract and one point of accountability.

**We self-perform.** Electrical, finish carpentry, tile, flooring and paint are our own crews, not a chain of subs.

**Certified for the work.** EPA Lead-Safe Certified Firm for renovation in older buildings.

**Founded by an engineer.** `[RON: one line from your bio]`

### Recent projects
- **H2:** Recent projects
- Three project cards, each: `[neighbourhood]` · `[one-line scope]`
- Link: All projects

### What clients say — Direction A only
- **H2:** What clients say
- Four Google review cards, placeholder text `Google review, 5 stars`, with the Google mark.
- No written review text. These are not testimonials.

### Closing
- **H2:** Every good beginning starts with hello.
- **Body:** Tell us what you are building and when it needs to be done.
- **Button:** Start a project

---

## Services overview — `services.html`

- **H1:** What we do
- **Intro:** Hello Construction Group is a licensed general contractor and licensed electrical contractor in Chicago. We self-perform electrical, finish carpentry, tile, flooring and interior painting, and we run the general trades on the projects we lead.

Three blocks, each an H2, two lines and a link:

**Commercial.** Tenant build-outs, industrial and plant work. One licensed contractor for the general trades and the electrical. → Commercial

**Residential.** Kitchens, baths and high-end renovations, with the same crew and the same standards. → Residential

**Electrical.** Licensed electrical contractor. Service upgrades, new circuits, build-out power and lighting. → Electrical

- **Button:** Start a project

---

## Commercial — `commercial.html`

- **H1:** Commercial construction and tenant build-outs
- **Lead:** The work we do most now, and the reason for the new name. We take commercial projects from an architect's set or an owner's sketch through permit, build and closeout, with our own electrical crew on site.

**H2: What we take on**
- Tenant build-outs: office, retail, healthcare and light-industrial interiors
- Industrial and plant work: `[RON: two or three examples you can name]`
- Renovation of occupied commercial space, phased around the tenant's hours

**H2: How we work with general contractors, architects and engineers**
- As the licensed GC of record, or as the electrical subcontractor on your project
- Drawings and submittals handled in-house
- One licensed contractor for general and electrical means one schedule and one contract

**H2: Licensed and insured**
- City of Chicago General Contractor License TGC133426 (Class D) and Electrical Contractor License ECC96203. Certificate of insurance on request.

- **Photos:** `[RON: two to four commercial interiors]`
- **Button:** Talk to us about your project

---

## Residential — `residential.html`

Same template as Commercial.

- **H1:** Residential renovation in Chicago
- **Lead:** Kitchens, baths and high-end renovations, with the same crew and the same standards we bring to commercial work.
- **H2: What we take on** — `[RON: the residential scope you want listed]`
- **H2: Licensed and insured** — same block as Commercial, verbatim.
- **Photos:** `[RON: two to four residential interiors]`
- **Button:** Talk to us about your project

The brief wrote Commercial in full and left these two shorter. Do not
invent body copy for the gaps.

---

## Electrical — `electrical.html`

Same template as Commercial.

- **H1:** Licensed electrical contractor
- **Lead:** Service upgrades, new circuits, build-out power and lighting — as your electrical subcontractor, or as part of a project we lead.
- **H2: What we take on** — `[RON: the electrical scope you want listed]`
- **H2: Licensed and insured** — same block as Commercial, verbatim.
- **Photos:** `[RON: two to four electrical photos]`
- **Button:** Talk to us about your project

---

## Projects index — `projects.html`

- **H1:** Projects
- **Intro:** A selection of recent work. Some of our projects are under agreements with the architects and owners and are not shown.
- **Filter row:** All · Commercial · Residential · Electrical (All selected; static is fine)

Four placeholder cards, each with a photo block, a title, a neighbourhood line and a one-line scope:

| Title | Type | Neighbourhood | Scope |
|---|---|---|---|
| Commercial tenant build-out | Commercial | `[neighbourhood]` | `[one-line scope]` |
| Industrial plant work | Commercial | `[neighbourhood]` | `[one-line scope]` |
| Kitchen and bath renovation | Residential | `[neighbourhood]` | `[one-line scope]` |
| Electrical service upgrade | Electrical | `[neighbourhood]` | `[one-line scope]` |

---

## Project detail — `project.html`

A template, shown with one worked example.

- **H1:** `[Project name]`
- **Facts row:** Neighbourhood · Type · Scope · Role (GC of record, or Electrical subcontractor) · Year
  Fill Type with `Commercial` and Role with `GC of record`; the rest are gaps.
- **Body:** `[three to five sentences: what was asked, what was done, what was hard]`
- **Gallery:** before and after, two placeholder blocks, captioned Before and After
- **Footer links:** Previous project · All projects · Next project

---

## About — `about.html`

- **H1:** About Hello Construction Group

**H2: Why the new name**
Hello Home Construction became Hello Construction Group because the work changed. More of what we build now is commercial: tenant build-outs, industrial and plant work. The company, the licences and the crews are the same; the name now says what we do.

**H2: Licensed general contractor and electrical contractor**
City of Chicago General Contractor License TGC133426 (Class D) and Electrical Contractor License ECC96203. EPA Lead-Safe Certified Firm. Veteran-founded.

**H2: Ron Domingo, President and Founder**
`[RON: very short bio in your words, focused on your time as a US Army officer]`
Photo: `[RON: a photo of you, on site if you have one]`

- **Button:** Start a project

---

## Contact — `contact.html`

- **H1:** Start a project
- **Lead:** Tell us what you are building, where, and when it needs to be done.

**Form:** Name · Company (optional) · Email · Project type (Commercial / Residential / Electrical / Not sure) · Message · **Send**

**Message field placeholder:** Tell us what you are building, where, and when it needs to be done.

**Success line:** **Sent.** Thank you — we have your message and will come back to you at the email address you gave.

**Email error:** Enter an email address we can reply to, for example name@company.com.

**Side block:**
> 4311 N. Ravenswood Ave., Suite 100
> Chicago, IL 60613
> info@hellocg.com

Nothing else. No phone, no map.

---

## Voice

Write plainly and in the first person plural. *"We self-perform the
electrical and the finish work, so the schedule is ours to keep"* is the
register: a statement of fact with a consequence attached, no adjectives
doing the selling.

Service names are sentence case with a full stop — `Commercial.`
`Residential.` `Electrical.` — followed by two lines of scope.

No emoji anywhere. No exclamation marks except inside the closing line
*Every good beginning starts with hello.*

Eyebrow labels are the only text set in capitals, and they get there
through `.t-label`, not by being typed that way.
