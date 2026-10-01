#!/usr/bin/env python3
"""Generate the Hello Construction Group static review site from the Claude Design package.
Outputs: site/ (spec-compliant full documents) and artifact/ (index.html as inner content for the
Artifact tool, plus the same supporting files)."""
import pathlib, shutil, re

ROOT = pathlib.Path(__file__).parent
PKG = ROOT / "hello-cg-build" / "hello-cg-build"
SITE = ROOT / "hcg-site"
ART = ROOT / "hcg-artifact"

FONTS = "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Inter:wght@400;600&family=Fraunces:opsz,wght@9..144,300&family=DM+Sans:wght@400;500&display=swap"

LEGAL = [
    "Hello Construction Group, a DBA of Hello Home Construction Co.",
    "City of Chicago General Contractor License TGC133426 · Electrical Contractor License ECC96203",
    "EPA Lead-Safe Certified Firm",
]

def gap(text):
    return f'<span class="gap">[{text}]</span>'

def ph(label, cls=""):
    return f'<div class="photo {cls}"><span class="photo-label">PHOTO: {label}</span></div>'

HEAD_SCRIPT = """<script>
  try {
    var t = localStorage.getItem('hellocg-theme');
    if (t) document.documentElement.setAttribute('data-theme', t);
  } catch (e) {}
</script>"""

def header(current):
    def item(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    svc_cur = ' aria-current="page"' if current in ("services", "commercial", "residential", "electrical") else ""
    return f"""<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="index.html"><img src="assets/hellocg-wordmark.png" alt="Hello Construction Group" width="982" height="172"></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu"><span class="menu-bars" aria-hidden="true"><i></i><i></i><i></i></span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul class="nav-list">
        {item("index.html", "Home", "home")}
        <li class="has-sub">
          <a href="services.html"{svc_cur}>Services</a><button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub-services" aria-label="Services menu"><span aria-hidden="true">▾</span></button>
          <ul id="sub-services" class="sub-list">
            {item("commercial.html", "Commercial", "commercial")}
            {item("residential.html", "Residential", "residential")}
            {item("electrical.html", "Electrical", "electrical")}
          </ul>
        </li>
        {item("projects.html", "Projects", "projects")}
        {item("about.html", "About", "about")}
        {item("contact.html", "Contact", "contact")}
      </ul>
      <a class="btn btn-primary nav-cta" href="contact.html"><span class="t-label">Start a project</span></a>
    </nav>
  </div>
</header>"""

FOOTER = f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col">
      <p class="t-label footer-heading">Hello Construction Group</p>
      <p class="t-small footer-muted">{LEGAL[0]}</p>
      <p class="t-small footer-muted">{LEGAL[1]}</p>
      <p class="t-small footer-muted">{LEGAL[2]}</p>
    </div>
    <div class="footer-col">
      <p class="t-label footer-heading">Contact</p>
      <p class="t-small">4311 N. Ravenswood Ave., Suite 100<br>Chicago, IL 60613</p>
      <p class="t-small"><a href="mailto:info@hellocg.com">info@hellocg.com</a></p>
    </div>
    <div class="footer-col">
      <p class="t-label footer-heading">Links</p>
      <ul class="footer-links t-small">
        <li><a href="services.html">Services</a></li>
        <li><a href="projects.html">Projects</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p class="t-small footer-muted">© 2026 Hello Home Construction Co. · Serving Chicago {gap("RON: and the suburbs? which?")}</p>
  </div>
</footer>"""

THEME_CONTROL = """<!-- Review scaffolding: delete before launch -->
<fieldset class="theme-control" aria-label="Design direction">
  <legend class="t-label">Direction</legend>
  <label><input type="radio" name="theme" value="a-orange" id="theme-a-orange"> A · Orange</label>
  <label><input type="radio" name="theme" value="a-blue" id="theme-a-blue"> A · Deep blue</label>
  <label><input type="radio" name="theme" value="a-red" id="theme-a-red"> A · Redmond</label>
  <label><input type="radio" name="theme" value="b" id="theme-b"> B · Quiet</label>
</fieldset>"""

def btn(href, label, kind="primary", extra=""):
    return f'<a class="btn btn-{kind} {extra}" href="{href}"><span class="t-label">{label}</span></a>'

def service_cards(as_links=False):
    items = [
        ("commercial.html", "Commercial.", "Tenant build-outs, industrial and plant work. One licensed contractor for the general trades and the electrical."),
        ("residential.html", "Residential.", "Kitchens, baths and high-end renovations, with the same crew and the same standards."),
        ("electrical.html", "Electrical.", "Licensed electrical contractor. Service upgrades, new circuits, build-out power and lighting."),
    ]
    out = []
    for href, title, body in items:
        out.append(f'<a class="service-card" href="{href}"><span class="tick" aria-hidden="true"></span><h3 class="t-h3">{title}</h3><p class="t-body muted">{body}</p></a>')
    return '<div class="grid-3 service-grid">' + "".join(out) + "</div>"

PROJECTS = [
    ("Commercial tenant build-out", "Commercial", "commercial interior, from Ron"),
    ("Industrial plant work", "Commercial", "plant floor, from Ron"),
    ("Kitchen and bath renovation", "Residential", "kitchen, from Ron"),
    ("Electrical service upgrade", "Electrical", "electrical panel, from Ron"),
]

def project_card(title, typ, photo):
    return f"""<a class="project-card" href="project.html">
  {ph(photo)}
  <div class="project-card-body">
    <p class="t-label muted">{typ}</p>
    <h3 class="t-h3">{title}</h3>
    <p class="t-small">{gap("neighborhood")} · {gap("one-line scope")}</p>
  </div>
</a>"""

# ---------------- pages ----------------
PAGES = {}

PAGES["index"] = ("Hello Construction Group | Commercial, Residential & Electrical Contractor, Chicago",
"Licensed Chicago general contractor and electrical contractor. Commercial tenant build-outs, industrial and plant work, high-end residential renovation. Hello Construction Group.",
"home", f"""
<section class="hero">
  <figure class="hero-media">{ph("one strong commercial interior, from Ron", "photo-hero")}</figure>
  <div class="hero-copy">
    <h1 class="t-display">Commercial, residential and electrical. Built right, in Chicago.</h1>
    <p class="t-lead">Licensed general contractor and electrical contractor. We self-perform the electrical and the finish work, so the schedule is ours to keep.</p>
    <div class="hero-actions">{btn("projects.html", "See our work")}{btn("contact.html", "Start a project", "secondary", "btn-on-photo")}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="t-label eyebrow"><span class="eyebrow-rule" aria-hidden="true"></span>What we do</p>
    <h2 class="t-h2">What we do</h2>
    {service_cards()}
  </div>
</section>

<section class="section band">
  <div class="container">
    <h2 class="t-h2 narrow">Why contractors, architects and engineers bring us in</h2>
    <div class="grid-4 why-grid">
      <div class="why-item"><span class="tick" aria-hidden="true"></span><h3 class="t-h3">Licensed on both sides.</h3><p class="t-body muted">General contractor and electrical contractor under one roof, so there is one contract and one point of accountability.</p></div>
      <div class="why-item"><span class="tick" aria-hidden="true"></span><h3 class="t-h3">We self-perform.</h3><p class="t-body muted">Electrical, finish carpentry, tile, flooring and paint are our own crews, not a chain of subs.</p></div>
      <div class="why-item"><span class="tick" aria-hidden="true"></span><h3 class="t-h3">Certified for the work.</h3><p class="t-body muted">EPA Lead-Safe Certified Firm for renovation in older buildings.</p></div>
      <div class="why-item"><span class="tick" aria-hidden="true"></span><h3 class="t-h3">Founded by an engineer.</h3><p class="t-body muted">{gap("RON: one line from your bio")}</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="t-h2">Recent projects</h2>
    <div class="grid-3 project-grid">
      {"".join(project_card(t, ty, p) for t, ty, p in PROJECTS[:3])}
    </div>
    <p class="section-link"><a class="t-label link-accent" href="projects.html">All projects</a></p>
  </div>
</section>

<section class="section reviews">
  <div class="container">
    <h2 class="t-h2">What clients say</h2>
    <div class="grid-4 review-grid">
      {"".join(f'<div class="review-card"><p class="stars" aria-label="Five stars">★★★★★</p><p class="t-small">{gap("Google review, 5 stars")}</p><p class="t-small google-mark"><span class="mark-placeholder" aria-hidden="true">G</span> Google</p></div>' for _ in range(4))}
    </div>
  </div>
</section>

<section class="section closing">
  <div class="container">
    <h2 class="t-h2 narrow">Every good beginning starts with hello.</h2>
    <p class="t-body narrow">Tell us what you are building and when it needs to be done.</p>
    <p class="section-link">{btn("contact.html", "Start a project")}</p>
  </div>
</section>
""")

PAGES["services"] = ("Services | Commercial, Residential & Electrical | Hello Construction Group",
"General contracting and electrical contracting for commercial build-outs, industrial work and high-end residential renovation in Chicago.",
"services", f"""
<section class="section page-head">
  <div class="container">
    <h1 class="t-h1">What we do</h1>
    <p class="t-lead narrow">Hello Construction Group is a licensed general contractor and licensed electrical contractor in Chicago. We self-perform electrical, finish carpentry, tile, flooring and interior painting, and we run the general trades on the projects we lead.</p>
  </div>
</section>
<section class="section band">
  <div class="container">
    <div class="stack-lg">
      <article class="service-block"><span class="tick" aria-hidden="true"></span><h2 class="t-h2">Commercial.</h2><p class="t-body muted narrow">Tenant build-outs, industrial and plant work. One licensed contractor for the general trades and the electrical.</p><p><a class="t-label link-accent" href="commercial.html">Commercial</a></p></article>
      <article class="service-block"><span class="tick" aria-hidden="true"></span><h2 class="t-h2">Residential.</h2><p class="t-body muted narrow">Kitchens, baths and high-end renovations, with the same crew and the same standards.</p><p><a class="t-label link-accent" href="residential.html">Residential</a></p></article>
      <article class="service-block"><span class="tick" aria-hidden="true"></span><h2 class="t-h2">Electrical.</h2><p class="t-body muted narrow">Licensed electrical contractor. Service upgrades, new circuits, build-out power and lighting.</p><p><a class="t-label link-accent" href="electrical.html">Electrical</a></p></article>
    </div>
  </div>
</section>
<section class="section">
  <div class="container"><p>{btn("contact.html", "Start a project")}</p></div>
</section>
""")

LICENSED = '<h2 class="t-h2">Licensed and insured</h2><p class="t-body narrow">City of Chicago General Contractor License TGC133426 (Class D) and Electrical Contractor License ECC96203. Certificate of insurance on request.</p>'

def service_page(key, title, meta, h1, lead, sections, photos, photo_label):
    body = f"""
<section class="section page-head">
  <div class="container">
    <p class="t-label eyebrow"><span class="eyebrow-rule" aria-hidden="true"></span>Services</p>
    <h1 class="t-h1">{h1}</h1>
    <p class="t-lead narrow">{lead}</p>
  </div>
</section>
<section class="section band">
  <div class="container stack-lg">
    {sections}
    {LICENSED}
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid-2 photo-grid">{ph(photo_label)}{ph(photo_label)}</div>
    <p class="t-small muted photo-note">{gap(photos)}</p>
    <p class="section-link">{btn("contact.html", "Talk to us about your project")}</p>
  </div>
</section>
"""
    PAGES[key] = (title, meta, key, body)

service_page("commercial",
    "Commercial Construction & Tenant Build-Outs in Chicago | Hello Construction Group",
    "Commercial general contractor for tenant build-outs, industrial and plant work in Chicago. Licensed GC and electrical contractor on one contract.",
    "Commercial construction and tenant build-outs",
    "The work we do most now, and the reason for the new name. We take commercial projects from an architect's set or an owner's sketch through permit, build and closeout, with our own electrical crew on site.",
    f"""<div><h2 class="t-h2">What we take on</h2><ul class="t-body list narrow"><li>Tenant build-outs: office, retail, healthcare and light-industrial interiors</li><li>Industrial and plant work: {gap("RON: two or three examples you can name")}</li><li>Renovation of occupied commercial space, phased around the tenant's hours</li></ul></div>
    <div><h2 class="t-h2">How we work with general contractors, architects and engineers</h2><ul class="t-body list narrow"><li>As the licensed GC of record, or as the electrical subcontractor on your project</li><li>Drawings and submittals handled in-house</li><li>One licensed contractor for general and electrical means one schedule and one contract</li></ul></div>""",
    "RON: two to four commercial interiors", "commercial interior, from Ron")

service_page("residential",
    "High-End Residential Renovation, Kitchens & Baths, Chicago | Hello Construction Group",
    "Kitchens, baths and whole-home renovation in Chicago by a licensed general contractor and electrical contractor with EPA Lead-Safe certified crews.",
    "Residential renovation in Chicago",
    "Kitchens, baths and high-end renovations, with the same crew and the same standards we bring to commercial work.",
    f"""<div><h2 class="t-h2">What we take on</h2><p class="t-body narrow">{gap("RON: the residential scope you want listed")}</p></div>""",
    "RON: two to four residential interiors", "residential interior, from Ron")

service_page("electrical",
    "Licensed Electrical Contractor, Chicago | Hello Construction Group",
    "Licensed Chicago electrical contractor for commercial build-outs, service upgrades, new circuits and lighting. License ECC96203.",
    "Licensed electrical contractor",
    "Service upgrades, new circuits, build-out power and lighting — as your electrical subcontractor, or as part of a project we lead.",
    f"""<div><h2 class="t-h2">What we take on</h2><p class="t-body narrow">{gap("RON: the electrical scope you want listed")}</p></div>""",
    "RON: two to four electrical photos", "electrical work, from Ron")

PAGES["projects"] = ("Projects | Commercial & Residential Work in Chicago | Hello Construction Group",
"Selected commercial build-outs, industrial work and residential renovations by Hello Construction Group, a licensed Chicago general and electrical contractor.",
"projects", f"""
<section class="section page-head">
  <div class="container">
    <h1 class="t-h1">Projects</h1>
    <p class="t-lead narrow">A selection of recent work. Some of our projects are under agreements with the architects and owners and are not shown.</p>
    <div class="filter-row" role="group" aria-label="Filter projects">
      <a class="btn btn-secondary is-active" href="projects.html" aria-current="true"><span class="t-label">All</span></a>
      <a class="btn btn-secondary" href="projects.html"><span class="t-label">Commercial</span></a>
      <a class="btn btn-secondary" href="projects.html"><span class="t-label">Residential</span></a>
      <a class="btn btn-secondary" href="projects.html"><span class="t-label">Electrical</span></a>
    </div>
  </div>
</section>
<section class="section band">
  <div class="container">
    <div class="grid-3 project-grid">{"".join(project_card(t, ty, p) for t, ty, p in PROJECTS)}</div>
  </div>
</section>
""")

PAGES["project"] = ("[Project name] | Commercial in [Neighborhood] | Hello Construction Group",
"A commercial project by Hello Construction Group, licensed Chicago general and electrical contractor.",
"projects", f"""
<section class="section page-head">
  <div class="container">
    <p class="t-label eyebrow"><span class="eyebrow-rule" aria-hidden="true"></span>Projects</p>
    <h1 class="t-h1">{gap("Project name")}</h1>
  </div>
</section>
<section class="section-tight">
  <div class="container">
    <dl class="facts-row">
      <div><dt class="t-label muted">Neighborhood</dt><dd class="t-h3">{gap("neighborhood")}</dd></div>
      <div><dt class="t-label muted">Type</dt><dd class="t-h3">Commercial</dd></div>
      <div><dt class="t-label muted">Scope</dt><dd class="t-h3">{gap("scope")}</dd></div>
      <div><dt class="t-label muted">Role</dt><dd class="t-h3">GC of record</dd></div>
      <div><dt class="t-label muted">Year</dt><dd class="t-h3">{gap("year")}</dd></div>
    </dl>
  </div>
</section>
<section class="section">
  <div class="container">
    <p class="t-body narrow">{gap("RON: three to five sentences: what was asked, what was done, what was hard")}</p>
    <div class="grid-2 photo-grid gallery">
      <figure>{ph("before, from Ron")}<figcaption class="t-label muted">Before</figcaption></figure>
      <figure>{ph("after, from Ron")}<figcaption class="t-label muted">After</figcaption></figure>
    </div>
    <nav class="project-nav" aria-label="Project navigation">
      <a class="t-label link-accent" href="project.html">Previous project</a>
      <a class="t-label link-accent" href="projects.html">All projects</a>
      <a class="t-label link-accent" href="project.html">Next project</a>
    </nav>
  </div>
</section>
""")

PAGES["about"] = ("About Hello Construction Group | Licensed GC & Electrical Contractor, Chicago",
"Hello Construction Group is the new name of Hello Home Construction Co., a licensed Chicago general and electrical contractor founded by an engineer and US Army officer.",
"about", f"""
<section class="section page-head">
  <div class="container"><h1 class="t-h1">About Hello Construction Group</h1></div>
</section>
<section class="section band">
  <div class="container stack-lg">
    <div><h2 class="t-h2">Why the new name</h2><p class="t-body narrow">Hello Home Construction became Hello Construction Group because the work changed. More of what we build now is commercial: tenant build-outs, industrial and plant work. The company, the licenses and the crews are the same; the name now says what we do.</p></div>
    <div><h2 class="t-h2">Licensed general contractor and electrical contractor</h2><p class="t-body narrow">City of Chicago General Contractor License TGC133426 (Class D) and Electrical Contractor License ECC96203. EPA Lead-Safe Certified Firm. Veteran-founded.</p></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid-2 bio-grid">
      <div><h2 class="t-h2">Ron Domingo, President and Founder</h2><p class="t-body">{gap("RON: very short bio in your words, focused on your time as a US Army officer")}</p><p class="section-link">{btn("contact.html", "Start a project")}</p></div>
      {ph("a photo of you, on site if you have one", "photo-portrait")}
    </div>
  </div>
</section>
""")

PAGES["contact"] = ("Contact Hello Construction Group | Chicago",
"Tell us about your commercial, residential or electrical project. Hello Construction Group, 4311 N. Ravenswood Ave., Chicago. Email info@hellocg.com or use the form.",
"contact", f"""
<section class="section page-head">
  <div class="container">
    <h1 class="t-h1">Start a project</h1>
    <p class="t-lead narrow">Tell us what you are building, where, and when it needs to be done.</p>
  </div>
</section>
<section class="section band">
  <div class="container grid-contact">
    <form class="contact-form" id="contact-form" novalidate>
      <div class="field"><label class="t-label" for="f-name">Name</label><input class="t-body" type="text" id="f-name" name="name" autocomplete="name" required></div>
      <div class="field"><label class="t-label" for="f-company">Company <span class="muted">(optional)</span></label><input class="t-body" type="text" id="f-company" name="company" autocomplete="organization"></div>
      <div class="field"><label class="t-label" for="f-email">Email</label><input class="t-body" type="email" id="f-email" name="email" autocomplete="email" required aria-describedby="f-email-error"><p class="t-small field-error" id="f-email-error" hidden>Enter an email address we can reply to, for example name@company.com.</p></div>
      <div class="field"><label class="t-label" for="f-type">Project type</label><select class="t-body" id="f-type" name="type"><option>Commercial</option><option>Residential</option><option>Electrical</option><option>Not sure</option></select></div>
      <div class="field"><label class="t-label" for="f-message">Message</label><textarea class="t-body" id="f-message" name="message" rows="6" placeholder="Tell us what you are building, where, and when it needs to be done."></textarea></div>
      <button class="btn btn-primary" type="submit" id="f-send"><span class="t-label">Send</span></button>
      <!-- A real handler goes here: post to the Wix form / info@hellocg.com notification. -->
    </form>
    <p class="t-body form-success" id="contact-success" hidden><strong class="success-word">Sent.</strong> Thank you — we have your message and will come back to you at the email address you gave.</p>
    <aside class="contact-side">
      <p class="t-label muted">Office</p>
      <p class="t-body">4311 N. Ravenswood Ave., Suite 100<br>Chicago, IL 60613</p>
      <p class="t-body"><a href="mailto:info@hellocg.com">info@hellocg.com</a></p>
    </aside>
  </div>
</section>
""")

# ---------------- CSS ----------------
SITE_CSS = r"""/* Hello Construction Group — site styles. All values come from tokens.css. */
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--ground); color: var(--ink); font-family: var(--font-body); }
img { max-width: 100%; height: auto; display: block; }
a { color: inherit; }
ul { margin: 0; padding: 0; list-style: none; }
p, h1, h2, h3, dl, dd, figure { margin: 0; }
h1, h2, h3 { text-wrap: balance; }
.muted { color: var(--ink-muted); }
.narrow { max-width: 38em; }

/* layout primitives */
.section { padding-block: var(--section-y); padding-inline: var(--page-margin); }
.section-tight { padding-block: var(--space-5); padding-inline: var(--page-margin); }
.container { max-width: var(--content); margin-inline: auto; }
.band { background: var(--surface-sunken); }
.stack-lg { display: grid; gap: var(--space-6); }
.grid-2, .grid-3, .grid-4 { display: grid; gap: var(--gutter); }
.section > .container > .t-h2, .section > .container > .t-h1 { margin-bottom: var(--space-5); }
.page-head .t-h1 { margin-bottom: var(--space-4); }
.section-link { margin-top: var(--space-5); }
.eyebrow { display: flex; align-items: center; gap: var(--space-3); color: var(--ink-muted); margin-bottom: var(--space-3); }
.eyebrow-rule { display: inline-block; width: var(--space-5); height: 2px; background: var(--accent); }
[data-theme="b"] .eyebrow-rule { background: var(--ink); }

/* focus */
a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible {
  outline: none; box-shadow: 0 0 0 2px var(--ground), 0 0 0 4px var(--focus);
}
.site-footer a:focus-visible { box-shadow: 0 0 0 2px var(--footer-bg), 0 0 0 4px var(--focus-inverse); }

/* buttons */
.btn { display: inline-flex; align-items: center; justify-content: center; gap: var(--space-2);
  padding: var(--space-3) var(--space-4); border-radius: var(--radius); text-decoration: none;
  border: 1px solid transparent; cursor: pointer; font: inherit; background: none; min-height: 48px; }
.btn-primary { background: var(--primary); border-color: var(--primary-border); color: var(--on-primary); }
.btn-primary:hover { background: var(--primary-hover); color: var(--on-primary-hover); }
.btn-secondary { background: transparent; border-color: var(--border-input); color: var(--ink); }
.btn-secondary:hover, .btn-secondary.is-active { border-color: var(--ink); background: var(--surface); }
.btn[disabled], .btn:disabled { background: var(--disabled-bg); border-color: var(--disabled-bg); color: var(--disabled-ink); cursor: not-allowed; }
.link-accent { color: var(--accent-ink); text-decoration: none; border-bottom: 2px solid var(--accent); padding-bottom: 2px; }
.link-accent:hover { color: var(--ink); border-color: var(--ink); }
[data-theme="b"] .link-accent { color: var(--ink); border-color: var(--ink); }

/* gaps for the client — delete this rule before launch */
.gap { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; color: #6b4bc4; outline: 1px dashed #6b4bc4; outline-offset: 2px; padding-inline: var(--space-1); }

/* header */
.site-header { background: var(--surface); border-bottom: 1px solid var(--rule); position: relative; z-index: 10; }
.header-inner { max-width: var(--content); margin-inline: auto; padding-inline: var(--page-margin); min-height: var(--header-h);
  display: flex; align-items: center; justify-content: space-between; gap: var(--space-4); }
.logo img { width: 140px; }
.menu-toggle { display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; background: none; border: 1px solid transparent; border-radius: var(--radius); cursor: pointer; color: var(--ink); }
.menu-bars { display: grid; gap: 5px; width: 22px; }
.menu-bars i { display: block; height: 2px; background: currentColor; }
.site-nav { display: none; position: absolute; left: 0; right: 0; top: 100%; background: var(--surface); border-bottom: 1px solid var(--rule);
  padding: var(--space-3) var(--page-margin) var(--space-4); box-shadow: var(--shadow-menu); }
.site-nav.is-open { display: block; }
.nav-list { display: grid; }
.nav-list > li { border-bottom: 1px solid var(--rule); }
.nav-list a { display: block; padding: var(--space-3) 0; text-decoration: none; font-family: var(--font-body); }
.nav-list a[aria-current="page"] { box-shadow: inset 0 -2px 0 var(--accent); }
.has-sub { display: grid; grid-template-columns: 1fr auto; align-items: center; }
.sub-toggle { background: none; border: 0; width: 48px; height: 48px; color: var(--ink); cursor: pointer; border-radius: var(--radius); }
.sub-list { grid-column: 1 / -1; display: none; padding-left: var(--space-3); border-left: 2px solid var(--accent); margin-bottom: var(--space-3); }
.sub-list.is-open { display: block; }
.sub-list a { color: var(--ink-muted); padding: var(--space-2) var(--space-3); }
.sub-list a[aria-current="page"] { color: var(--ink); box-shadow: none; }
.nav-cta { width: 100%; margin-top: var(--space-4); }

/* hero: base is stacked in every theme */
.hero { display: grid; }
.hero-media { display: block; }
.photo { background: var(--surface-sunken); border: 1px solid var(--rule); display: grid; place-items: center; aspect-ratio: 4 / 3; width: 100%; }
.photo-hero { aspect-ratio: 16 / 10; }
.photo-portrait { aspect-ratio: 3 / 4; }
.photo-label { font-family: var(--font-body); text-transform: uppercase; letter-spacing: 0.1em; color: var(--ink-muted); padding: var(--space-3); text-align: center; }
.hero-copy { padding: var(--space-6) var(--page-margin); display: grid; gap: var(--space-4); }
.hero-actions { display: grid; gap: var(--space-3); }

/* cards */
.tick { display: block; width: 32px; height: 3px; background: var(--accent); margin-bottom: var(--space-3); }
.service-card { display: block; text-decoration: none; background: var(--surface); border: 1px solid var(--rule); border-radius: var(--radius); padding: var(--space-4); }
.service-card .t-h3 { margin-bottom: var(--space-2); }
.service-card:hover { border-color: var(--ink); }
[data-theme="b"] .service-card { background: transparent; border: 0; padding: var(--space-5); }
[data-theme="b"] .tick { width: 24px; height: 1px; background: var(--ink); }
.why-item .t-h3 { margin-bottom: var(--space-2); }
.service-block .t-h2 { margin-bottom: var(--space-2); }
.service-block p + p { margin-top: var(--space-3); }

.project-card { display: block; text-decoration: none; background: var(--surface); border: 1px solid var(--rule); border-radius: var(--radius); overflow: hidden; }
.project-card .photo { border: 0; border-bottom: 1px solid var(--rule); }
.project-card-body { padding: var(--space-4); display: grid; gap: var(--space-2); }
.project-card:hover { border-color: var(--ink); }
[data-theme="b"] .project-card { background: transparent; border: 0; border-radius: 0; }
[data-theme="b"] .project-card .photo { border: 1px solid var(--rule); }
[data-theme="b"] .project-card-body { padding: var(--space-3) 0 0; }

.facts-row { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--space-4); background: var(--surface-sunken); border: 1px solid var(--rule); padding: var(--space-4); }
.facts-row dt { margin-bottom: var(--space-1); }
[data-theme="b"] .facts-row { background: transparent; border: 0; border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); padding-inline: 0; }

.photo-grid figure { display: grid; gap: var(--space-2); }
.photo-note { margin-top: var(--space-3); }
.gallery { margin-top: var(--space-6); }
.project-nav { display: flex; flex-wrap: wrap; gap: var(--space-4); margin-top: var(--space-6); }
.filter-row { display: flex; flex-wrap: wrap; gap: var(--space-2); margin-top: var(--space-4); }
.list { padding-left: 1.2em; list-style: disc; }
.list li + li { margin-top: var(--space-2); }
.bio-grid > div > .t-h2 { margin-bottom: var(--space-3); }

/* reviews (Direction A only; tokens.css hides in B) */
.review-card { background: var(--surface); border: 1px solid var(--rule); border-radius: var(--radius); padding: var(--space-4); display: grid; gap: var(--space-3); }
.stars { color: var(--accent-ink); letter-spacing: 0.1em; }
.mark-placeholder { display: inline-grid; place-items: center; width: 20px; height: 20px; border: 1px dashed var(--border-input); color: var(--ink-muted); }

/* form */
.grid-contact { display: grid; gap: var(--space-6); }
.contact-form { display: grid; gap: var(--space-4); }
.field { display: grid; gap: var(--space-2); }
.field input, .field select, .field textarea { width: 100%; padding: var(--space-3); background: var(--surface); border: 1px solid var(--border-input); border-radius: var(--radius); color: var(--ink); font: inherit; font-family: var(--font-body); }
.field input:focus, .field select:focus, .field textarea:focus { border-color: var(--ink); }
.field.has-error input { background: var(--error-bg); border-color: var(--error); }
.field-error { color: var(--error); }
.success-word { color: var(--success); }
.contact-side { display: grid; gap: var(--space-3); align-content: start; }

/* footer */
.site-footer { background: var(--footer-bg); color: var(--footer-ink); padding-block: var(--space-7) var(--space-5); padding-inline: var(--page-margin); border-top: 1px solid var(--footer-rule); }
.footer-grid { display: grid; gap: var(--space-6); }
.footer-col { display: grid; gap: var(--space-2); align-content: start; }
.footer-heading { margin-bottom: var(--space-2); }
.footer-muted { color: var(--footer-muted); }
.footer-links { display: grid; gap: var(--space-2); }
.site-footer a { color: var(--footer-ink); }
.footer-bottom { margin-top: var(--space-6); padding-top: var(--space-4); border-top: 1px solid var(--footer-rule); }

/* review scaffolding: theme control. Delete before launch. */
.theme-control { position: fixed; bottom: 0; left: 0; right: 0; z-index: 20; margin: 0; display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-3);
  padding: var(--space-2) var(--space-3); background: var(--surface); border: 1px solid var(--rule); border-radius: 0; box-shadow: var(--shadow-menu); color: var(--ink); }
.theme-control legend { float: left; margin-right: var(--space-2); color: var(--ink-muted); }
.theme-control label { display: inline-flex; align-items: center; gap: var(--space-1); font-family: var(--font-body); cursor: pointer; }
body { padding-bottom: var(--space-7); }

@media (prefers-reduced-motion: no-preference) { .btn, .service-card, .project-card { transition: background-color 120ms, border-color 120ms, color 120ms; } }

/* ---------- 751px and up ---------- */
@media (min-width: 751px) {
  .grid-2 { grid-template-columns: repeat(2, 1fr); }
  .grid-3 { grid-template-columns: repeat(2, 1fr); }
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
  .facts-row { grid-template-columns: repeat(3, 1fr); }
  .hero-actions { display: flex; gap: var(--space-3); }
  .grid-contact { grid-template-columns: 2fr 1fr; }
  .footer-grid { grid-template-columns: repeat(3, 1fr); }
  .theme-control { left: auto; bottom: var(--space-4); right: var(--space-4); border-radius: var(--radius-md); }
  body { padding-bottom: 0; }

  /* Direction A: media fills the hero, scrim over it, copy bottom-aligned */
  :root:not([data-theme="b"]):not([data-theme="a-red"]) .hero { position: relative; min-height: 820px; grid-template-columns: 1fr; }
  :root:not([data-theme="b"]):not([data-theme="a-red"]) .hero-media { position: absolute; inset: 0; }
  :root:not([data-theme="b"]):not([data-theme="a-red"]) .hero-media .photo { position: absolute; inset: 0; aspect-ratio: auto; height: 100%; border: 0; place-items: start; }
  :root:not([data-theme="b"]):not([data-theme="a-red"]) .hero-media .photo-label { padding: var(--space-4) var(--page-margin); }
  :root:not([data-theme="b"]):not([data-theme="a-red"]) .hero-media::after { content: ""; position: absolute; inset: 0; background: var(--hero-scrim); pointer-events: none; }
  :root:not([data-theme="b"]):not([data-theme="a-red"]) .hero-copy { position: relative; z-index: 1; align-self: end; color: var(--ink-inverse); max-width: var(--content); width: 100%; margin-inline: auto; padding-block: var(--space-8); }
  :root:not([data-theme="b"]):not([data-theme="a-red"]) .hero-copy .t-display { max-width: 18ch; }
  :root:not([data-theme="b"]):not([data-theme="a-red"]) .hero-copy .t-lead { max-width: 34em; }
  :root:not([data-theme="b"]):not([data-theme="a-red"]) .btn-on-photo { border-color: var(--ink-inverse); color: var(--ink-inverse); }
  :root:not([data-theme="b"]):not([data-theme="a-red"]) .btn-on-photo:hover { background: var(--ink-inverse); color: var(--ink); }

  /* Direction A Redmond: photo first, headline below it, like the client's reference site */
  [data-theme="a-red"] .hero-media .photo { aspect-ratio: 21 / 9; border-inline: 0; border-top: 0; }
  [data-theme="a-red"] .hero-copy { max-width: var(--content); margin-inline: auto; padding-block: var(--space-7) var(--space-5); }
  [data-theme="a-red"] .hero-copy .t-display { max-width: 18ch; }
  [data-theme="a-red"] .hero-copy .t-lead { max-width: 34em; }

  /* Direction B: never overlays */
  [data-theme="b"] .hero { padding-inline: var(--page-margin); padding-block: var(--section-y); max-width: calc(var(--content) + 2 * var(--page-margin)); margin-inline: auto; gap: var(--space-6); }
  [data-theme="b"] .hero-copy { padding: 0; }
}

/* ---------- 1001px and up ---------- */
@media (min-width: 1001px) {
  .logo img { width: 180px; }
  .menu-toggle { display: none; }
  .site-nav { display: flex; position: static; background: transparent; border: 0; padding: 0; box-shadow: none; align-items: center; gap: var(--space-5); }
  .nav-list { display: flex; align-items: center; gap: var(--space-4); }
  .nav-list > li { border: 0; }
  .nav-list a { padding: var(--space-2) 0; }
  .nav-list a[aria-current="page"] { box-shadow: inset 0 -2px 0 var(--accent); }
  .has-sub { position: relative; display: flex; align-items: center; }
  .sub-toggle { width: 24px; height: 24px; }
  .sub-list { display: none; position: absolute; top: 100%; left: 0; min-width: 200px; background: var(--surface); border: 1px solid var(--rule); border-radius: var(--radius-md); box-shadow: var(--shadow-menu); padding: var(--space-2); margin: 0; border-left: 1px solid var(--rule); }
  .has-sub:hover .sub-list, .has-sub:focus-within .sub-list, .sub-list.is-open { display: block; }
  .sub-list a { color: var(--ink); padding: var(--space-2) var(--space-3); border-radius: var(--radius); }
  .sub-list a:hover { background: var(--surface-sunken); }
  .nav-cta { width: auto; margin: 0; }
  .grid-3 { grid-template-columns: repeat(3, 1fr); }
  .grid-4 { grid-template-columns: repeat(4, 1fr); }
  .facts-row { grid-template-columns: repeat(5, 1fr); }
  .bio-grid { grid-template-columns: 3fr 2fr; }
  [data-theme="b"] .hero { grid-template-columns: 1fr 1fr; align-items: center; }
  [data-theme="b"] .hero-media { order: 2; }
}
"""

THEME_JS = r"""// Theme switch: sets data-theme on <html>, persists it, and holds it if the host stamps its own value.
(function () {
  var KEY = 'hellocg-theme', VALID = ['a-orange', 'a-blue', 'a-red', 'b'], root = document.documentElement;
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function apply(v) {
    if (VALID.indexOf(v) < 0) v = 'a-orange';
    root.setAttribute('data-theme', v);
    try { localStorage.setItem(KEY, v); } catch (e) {}
    var r = document.getElementById('theme-' + v); if (r) r.checked = true;
  }
  apply(stored() || 'a-orange');
  document.addEventListener('change', function (e) {
    if (e.target && e.target.name === 'theme') apply(e.target.value);
  });
  if (window.MutationObserver) {
    new MutationObserver(function () {
      var v = root.getAttribute('data-theme');
      if (VALID.indexOf(v) < 0) apply(stored() || 'a-orange');
    }).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
  }
})();
"""

NAV_JS = r"""// Mobile menu, the Services drop-down, and the contact form's demonstrable states.
(function () {
  var toggle = document.querySelector('.menu-toggle'), nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }
  var sub = document.querySelector('.sub-toggle'), list = document.getElementById('sub-services');
  if (sub && list) {
    sub.addEventListener('click', function () {
      var open = list.classList.toggle('is-open');
      sub.setAttribute('aria-expanded', String(open));
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (list) { list.classList.remove('is-open'); if (sub) sub.setAttribute('aria-expanded', 'false'); }
      if (nav) { nav.classList.remove('is-open'); if (toggle) toggle.setAttribute('aria-expanded', 'false'); }
    }
  });
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = document.getElementById('f-email'), err = document.getElementById('f-email-error'), field = email.closest('.field');
      var ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
      if (!ok) { field.classList.add('has-error'); err.hidden = false; email.setAttribute('aria-invalid', 'true'); email.focus(); return; }
      field.classList.remove('has-error'); err.hidden = true; email.removeAttribute('aria-invalid');
      // A real handler goes here.
      form.hidden = true;
      var s = document.getElementById('contact-success'); s.hidden = false; s.setAttribute('tabindex', '-1'); s.focus();
    });
  }
})();
"""

def head_inner(title, meta):
    return f"""<title>{title}</title>
<meta name="description" content="{meta}">
<meta name="robots" content="noindex, nofollow">
{HEAD_SCRIPT}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="styles/tokens.css">
<link rel="stylesheet" href="styles/site.css">"""

def body_inner(current, content):
    return f"""{header(current)}
<main id="main">{content}</main>
{FOOTER}
{THEME_CONTROL}
<script src="scripts/theme.js"></script>
<script src="scripts/nav.js"></script>"""

def full_doc(title, meta, current, content):
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="a-orange">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_inner(title, meta)}
</head>
<body>
{body_inner(current, content)}
</body>
</html>
"""

def write_tree(base, artifact=False):
    if base.exists(): shutil.rmtree(base)
    (base / "styles").mkdir(parents=True); (base / "scripts").mkdir(); (base / "assets").mkdir()
    shutil.copy(PKG / "styles" / "tokens.css", base / "styles" / "tokens.css")
    (base / "styles" / "site.css").write_text(SITE_CSS)
    (base / "scripts" / "theme.js").write_text(THEME_JS)
    (base / "scripts" / "nav.js").write_text(NAV_JS)
    (base / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    (base / ".nojekyll").write_text("")
    for png in (PKG / "assets").glob("*.png"): shutil.copy(png, base / "assets" / png.name)
    for key, (title, meta, current, content) in PAGES.items():
        if artifact and key == "index":
            doc = head_inner(title, meta) + "\n" + body_inner(current, content) + "\n"
        else:
            doc = full_doc(title, meta, current, content)
        (base / f"{key}.html").write_text(doc)

write_tree(SITE)
write_tree(ART, artifact=True)
print("written", SITE, ART, "pages:", len(PAGES))
