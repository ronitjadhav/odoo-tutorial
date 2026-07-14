# Master Plan: "Zero to Odoo Expert" — A Hands-On Odoo Development Tutorial Site

> **Purpose of this document:** A complete, self-contained execution plan for building an
> Odoo development tutorial website. It is written so that (a) the author (a developer
> joining an Odoo team at Camptocamp, new to Odoo) can follow it as their own learning
> path, and (b) an AI agent (e.g. Claude Sonnet/Opus) can pick it up cold and start
> producing the site and content with no additional context.
>
> **Last researched:** July 2026.

---

## 1. Project Overview

### 1.1 What we are building
A free, open-source, hands-on tutorial website — working title **"Zero to Odoo Expert"** —
published on **GitHub Pages**, teaching Odoo development from absolute basics to
professional/OCA-level expertise. The site is paired with a **companion code repository**
containing every module built in the tutorial, one folder per chapter, so readers can
diff their work against a known-good state at any point.

### 1.2 Why (dual goal)
1. **Primary:** The author learns Odoo development deeply. Writing a tutorial forces
   understanding (the Feynman technique) — you cannot explain `_inherit` vs `_inherits`
   vs `_name` until you truly get it.
2. **Secondary:** The result becomes a public resource others can use, and a visible
   portfolio artifact (useful inside Camptocamp too — the company is one of the largest
   OCA contributors, so OCA-style quality will be noticed).

### 1.3 Target audience of the tutorial
- Developers with intermediate Python, basic SQL/HTML/JS, and Git experience,
  but **zero Odoo knowledge** (i.e., the author on day 1).
- Secondary audience: junior devs onboarding at Odoo integrator companies.

### 1.4 What this tutorial is NOT
- Not a copy/rewrite of the official docs — it **links to** official docs and OCA
  resources and adds the connective tissue: sequencing, explanations of *why*,
  real-world integrator practices, pitfalls, and exercises.
- Not a functional/end-user Odoo course (no "how to configure CRM stages" content
  except where needed to understand the code behind it).
- **Copyright rule for all content authors (human or AI): never copy text, images, or
  code verbatim from the Odoo documentation, Odoo source (LGPL — code snippets you
  write while following patterns are fine, wholesale copying is not), books, or blog
  posts. All prose must be original. Link out generously instead.**

---

## 2. Key Decisions (already made — do not re-litigate, but flag if outdated)

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| D1 | Odoo version to teach | ~~Odoo 18.0~~ → **Odoo 19.0 Community** as the baseline, with "On Odoo 18 this differs" callout boxes (revised 2026-07-10, see changelog) | Author's call after reviewing the 18→19 delta: core framework (modules, ORM, views, security, OWL) unchanged; 19 is supported until Oct 2028 vs Oct 2027 for 18, giving the content a longer shelf life. Teaching 19 idioms (`t-out`, `display_name`, `_read_group`) from day one means readers never learn deprecated forms — and those exact deprecations become ch37's 18→19 migration exercise. Version-bump pass after each October release stays planned. |
| D2 | Edition | **Community (open source)** | Enterprise source is not freely redistributable; Community is what OCA targets; everything learned transfers. Mention Enterprise-only features in info boxes. |
| D3 | Site generator | ~~MkDocs + Material~~ → **Next.js + Fumadocs + Tailwind (shadcn aesthetic)**, static-exported (revised 2026-07-10, see changelog) | The author wants an interactive, product-feel learning platform, not a docs site. Fumadocs provides docs plumbing (search, sidebar, MDX, dark mode) out of the box; custom React components add quizzes, progress/streaks, and the landing page. Static export keeps GitHub Pages hosting free. |
| D4 | Hosting | **GitHub Pages** via GitHub Actions on push to `main` | Free, zero-ops, requested by the author. |
| D5 | Repo layout | **Two repos**: `odoo-tutorial` (site) and `odoo-tutorial-code` (chapter-by-chapter module code) — or one monorepo with `/docs` and `/code`; monorepo preferred for simplicity | Keeps site deploys clean while letting readers clone runnable code. Start monorepo; split later only if needed. |
| D6 | Dev environment taught | **Docker Compose first** (Odoo + PostgreSQL), with a "native install" appendix | Reproducible on Linux/macOS/Windows; mirrors how integrators (incl. Camptocamp, which is Docker-heavy in its platform tooling) actually run projects. |
| D7 | Pedagogy | One continuous **capstone project** built across all chapters + small isolated exercises per chapter + a solutions folder | Mirrors the official tutorial's proven approach but with an original project (see §5.2) to avoid duplicating the official "Real Estate" module. |
| D8 | Language | English | Widest reach; author's working language. |
| D9 | License | Content: CC BY-SA 4.0; Code: AGPL-3 (matches OCA convention) | OCA modules are AGPL/LGPL; using AGPL for tutorial modules teaches the norm. |

---

## 3. Research Summary — Ecosystem Facts the Executing Agent Must Know

These were verified against live sources in July 2026. Re-verify anything
version-sensitive before writing the corresponding chapter.

### 3.1 Odoo versions & cadence
- Odoo ships **one major version per year, around October**, announced at Odoo
  Experience in Brussels. Current: **Odoo 19 (Oct 2025)**. Expected: **Odoo 20
  (~Oct 2026)**, with an agentic-AI focus per the public roadmap.
- Only the **3 most recent majors are supported** (17/18/19 as of mid-2026; when 20
  ships, 17 drops off). This is why integrators live and breathe **migrations** —
  a whole chapter of the tutorial is dedicated to this.
- Docs live at `https://www.odoo.com/documentation/<version>/` — always link
  version-pinned URLs (19.0, the tutorial baseline), never `/master/`.

### 3.2 Architecture fundamentals (chapter source material)
- Three-tier: presentation (HTML5/JS/CSS + the **OWL** framework), logic (Python),
  data (**PostgreSQL only**).
- Everything is a **module** (a.k.a. addon): a directory with `__manifest__.py` +
  `__init__.py`, found via `--addons-path`. Modules declare `depends`; install/uninstall
  cascades follow the dependency graph.
- Business objects are Python classes mapped to tables by the **ORM**. Views are XML.
  Security = access rights CSV (`ir.model.access.csv`) + record rules + groups.
- The official beginner path is **"Server framework 101"** (builds a Real Estate
  module over ~16 chapters: models, fields, security, views, relations, compute/onchange,
  actions, constraints, inheritance, interacting with other modules, sprinkles/polish).
  Our curriculum tracks the same concept order (it's well-designed) but with an
  **original capstone project** and added integrator-world chapters the official
  tutorial lacks (OCA, Docker, migrations, code review, performance).
- Other official tutorials to link per-chapter: "Discover the web framework" (OWL),
  "Master the web framework", "Define module data", "Restrict access to data",
  "Safeguard your code with unit tests", "Build PDF reports", "Website themes".

### 3.3 OCA (Odoo Community Association) — critical for a Camptocamp dev
- Nonprofit (Swiss association) hosting hundreds of GitHub repos of community
  modules at `github.com/OCA`, organized by domain (server-tools, web, partner-contact,
  account-financial-tools, etc.), each governed by a **PSC** (Project Steering Committee).
- Contribution workflow (must become second nature): sign the **CLA** → fork repo →
  branch off the **version branch** (e.g. `18.0`, never `master`) → commit with
  **`[TAG] module_name: description`** convention (`[FIX]`, `[IMP]`, `[ADD]`, `[MIG]`,
  `[REF]`...) → run **pre-commit** locally (ruff/pylint-odoo/prettier hooks) → open PR
  targeting the version branch → CI (GitHub Actions) + **Runboat** (throwaway live test
  instances per PR, successor to the old runbot) → needs ~2–3 approving reviews incl.
  a PSC member → merged via the **OCA GitHub bot** (`/ocabot merge minor` etc.).
- Module **maturity levels** in `__manifest__.py` `development_status`: Alpha, Beta
  (default), Production/Stable, Mature — each with defined merge requirements.
- README files are generated from `readme/` RST fragments by OCA tooling — don't edit
  README.rst by hand in OCA modules.
- Translations go through **Weblate** — never edit `.po` files in PRs.
- **Module migration** between versions is a first-class OCA activity: each repo has a
  "Migration to version X" tracking issue; git history must be preserved (technique:
  `git format-patch` / the documented migration procedure); **OpenUpgrade** is the
  OCA project for Community-edition database migrations.
- OCA coding guidelines extend Odoo's own; key tools: `pre-commit`, `pylint-odoo`,
  `oca-maintainer-tools`, module template repo. Reviewing others' PRs is expected
  etiquette ("keep a good submitted/reviewed ratio").
- Camptocamp context: long-time major OCA contributor (staff have built core OCA
  infrastructure and tooling). Expect heavy use of OCA modules in client projects,
  Docker-based deployment, and strong code-review culture. The tutorial's "expert"
  tier should explicitly teach *working the OCA way*.

### 3.4 Frontend
- Odoo's JS framework is **OWL** (Odoo Web Library) — a small component framework with
  hooks and a QWeb-based XML template syntax (conceptually React-like but distinct).
- **QWeb** is also the server-side templating engine for reports and website pages.
- Website building blocks ("snippets"), portal pages, and the POS all ride on this stack.

### 3.5 Tooling landscape worth teaching
- `odoo-bin` CLI: `-d`, `-i`, `-u`, `--addons-path`, `--dev=all`, `--test-enable`,
  `--test-tags`, `shell` subcommand, `scaffold` subcommand.
- Debugging: `--dev=all` auto-reload, `pdb`/`debugpy`, browser devtools for OWL,
  developer mode (`?debug=1`) in the UI, `ir.logging`, PostgreSQL query logging.
- Quality: `pre-commit`, `ruff`, `pylint-odoo`, OCA CI.
- Data/ops: `click-odoo`, `odoo-shell` scripting; (mention, without depending on them,
  Camptocamp OSS like `marabunta`/`anthem` for migrations/seeding — verify current
  status when writing that chapter).

---
## 4. Website & Repository Design

### 4.1 Monorepo structure (as built — post-D3 revision)

```
odoo-tutorial/                      # public GitHub repo
├── ODOO_TUTORIAL_MASTER_PLAN.md    # this file — single source of truth + changelog
├── web/                            # Next.js 16 + Fumadocs + Tailwind 4, static export
│   ├── content/docs/               # all tutorial content (MDX)
│   │   ├── index.mdx               # docs landing: what/why/how to use
│   │   ├── roadmap.mdx             # milestone status table (keep in sync with §6)
│   │   ├── glossary.mdx            # Odoo jargon: addon, manifest, recordset, sudo, ...
│   │   ├── 00-orientation/         # one folder per part, one NN-slug.mdx per chapter,
│   │   ├── 01-environment/         #   nav order in each folder's meta.json
│   │   └── ...
│   ├── components/                 # quiz.tsx, mermaid.tsx, progress-pill.tsx,
│   │                               #   mark-complete.tsx, search.tsx (see §4.4)
│   └── app/, lib/, ...             # Fumadocs plumbing; basePath /odoo-tutorial
├── code/
│   ├── addons/
│   │   └── librefleet/             # final state of the capstone module(s)
│   ├── checkpoints/
│   │   └── ch08/ ch09/ ...         # snapshot of the addon after each chapter
│   ├── odoolings.py                # XML-RPC work checker (see §4.4), stdlib only
│   ├── docker-compose.yml          # odoo:19 + postgres:16 — the exact dev env taught
│   ├── odoo.conf
│   ├── .pre-commit-config.yaml     # OCA-style hooks, added in Part 6
│   └── requirements-dev.txt        # added when first needed, not before
├── .github/workflows/              # deploy Pages on push; ci.yml for module tests (M3)
├── LICENSE-content (CC BY-SA 4.0), LICENSE-code (AGPL-3)
├── CONTRIBUTING.md
└── README.md
```

### 4.2 Site conventions (Next.js + Fumadocs)
- Navigation: parts as sidebar sections, chapters as pages; prev/next footer nav,
  Orama static search, dark mode — all from Fumadocs.
- Code blocks with copy button and line highlights (Shiki via Fumadocs MDX).
- Callout boxes with consistent semantics used throughout (Fumadocs `<Callout>`):
  - `type="info"  title="Official docs"` → link to the canonical doc page for the topic
  - `type="warn"  title="Gotcha"` → real-world pitfalls
  - `type="info"  title="In the field"` → integrator/OCA/Camptocamp practice notes
  - `type="info"  title="On Odoo 18 this differs"` → version deltas for older projects
- Diagrams: the `<Mermaid>` client component (architecture, request lifecycle, ERDs).
- Per-chapter footer: *Prerequisites · What you built · Official reading ·
  OCA modules worth studying · Exercise checklist.*

### 4.3 Chapter template (every chapter MUST follow this skeleton)

```markdown
# NN. Chapter Title            <- frontmatter: title + description
**Goal:** one sentence. **Time:** ~X h. **Checkpoint:** code/checkpoints/chNN

## Why this matters            <- motivation, real-world framing
## Concepts                    <- original explanation, diagrams, links to official docs
## Hands-on                    <- numbered steps on the capstone project
## Verify                      <- prove it works: UI steps, odoo-bin shell/psql, and
                                  `python odoolings.py check chNN` where checks exist
## Gotchas                     <- pitfalls collected while writing/testing the chapter
## Quick check                 <- <Quiz> with 3–5 questions, each with a `why`
## Exercises                   <- graded ⭐/⭐⭐/⭐⭐⭐ tasks (see §5.6), no inline solutions
## Further reading             <- official docs + OCA examples + (optional) videos
```

**Authoring rules for the agent:**
1. Every "Hands-on" section must be *executed and verified* in the Docker environment
   before the chapter is marked done. No untested code ships. Screenshots are taken
   from the author's own running instance.
2. Every chapter that changes the capstone module must register odoolings checks for
   its end state, and its Verify section must reference them. Quizzes must test the
   chapter's *ideas* (predict behavior, choose the right approach), not recall of
   syntax that the reader can look up.

### 4.4 Interactive mechanics — inventory & roadmap

Built (keep polishing, don't rebuild):
- **`<Quiz>`** — per-chapter multiple choice, instant feedback with explanations.
- **`odoolings.py`** — rustlings-style CLI verifying the reader's *running* Odoo over
  XML-RPC, with hints on failure. Chapter checks (`ch05`…) plus, from Part 2 on,
  boss-challenge check sets (`boss2`…, see §5.6).
- **Progress + streaks** — localStorage pill; per-chapter "mark complete". No
  accounts/backend by design; revisit only if a real learner community shows up.
- **`<Mermaid>`** — diagrams as code.

Planned (build at the milestone that needs them, not before):
- **Sidebar completion checkmarks** driven by the same localStorage state (small; do
  during M1 wrap-up so Part 2 readers see their trail).
- **Quiz persistence + per-part mastery** — remember quiz results, show a "Part N
  mastery" bar; feeds the end-of-part review quiz (§5.6). M2.
- **`<Term>` glossary tooltips** — inline hover definitions linking to the glossary,
  so jargon is explained where it occurs. M2, then backfill.
- **Predict-the-output quizzes** — a `code` field on quiz questions rendering a
  snippet above the options ("what does this recordset expression return?"). Extends
  `<Quiz>`, not a new component. M2 (recordsets chapter is the natural debut).
- **ch37 interactive migration checklist** — trackable checkboxes for the OCA
  migration procedure. Build when writing ch37.

---

## 5. Curriculum — The Complete Syllabus

### 5.1 Shape of the journey
Seven parts, ~40 chapters, three proficiency tiers:

- **Tier 1 — Foundations (Parts 0–3):** can build and ship a clean custom module.
- **Tier 2 — Professional (Parts 4–5):** can extend core apps safely, write tests,
  build UI, debug anything.
- **Tier 3 — Expert/Integrator (Parts 6–7):** works the OCA way, migrates modules,
  tunes performance, reasons about deployments and upgrades.

### 5.2 The capstone project
An original, non-trivial domain that exercises every framework feature and does not
collide with the official Real Estate tutorial or common demo apps:

> **"LibreFleet" — a vehicle-workshop & service-booking management app.**
> Customers, vehicles, service orders with stages and a kanban, parts consumption,
> technician assignment (many2many), computed totals and margins, statbuttons,
> constraints (no overlapping bookings), an approval wizard, mail/chatter integration,
> a customer portal page to view service history, a QWeb PDF service report, a small
> OWL dashboard widget (jobs per technician), scheduled actions (maintenance
> reminders), and — in the expert tier — a refactor of one feature into an
> OCA-quality standalone module with tests, readme fragments and pre-commit passing.

(The agent may propose a different domain, but it must exercise the same feature
matrix; get the author's sign-off before writing Part 2.)

### 5.3 Chapter list

**Part 0 — Orientation (no code)**
1. What Odoo is: ERP concept, apps vs modules, Community vs Enterprise, editions,
   versioning & the October cadence, odoo.sh vs on-prem vs Odoo Online.
2. The ecosystem map: Odoo SA, integrators/partners, the OCA, where Camptocamp-style
   integrators fit; how the official docs, OCA repos, and YouTube channels relate.
3. Architecture overview: three tiers, request lifecycle, the ORM idea, modules and
   the addons path. (Mermaid diagrams.)
4. Guided tour as a *user*: install a demo DB, click through Sales/CRM/Inventory for
   30 minutes, enable developer mode — you must know the product to develop it.

**Part 1 — Environment**
5. Dev setup with Docker Compose: Odoo 19 + Postgres 16, volumes for addons and
   filestore, config file, first login. Appendix: native install from source.
6. Daily driver workflow: `odoo-bin` flags that matter, `--dev=all`, log reading,
   database create/drop/duplicate, `psql` basics, VS Code setup (Python + XML
   tooling), using `odoo-bin shell`.
7. Git for Odoo work: repo layouts integrators use, addons pinning, branch-per-version
   mindset (mirrors OCA/odoo branches like `18.0`).

**Part 2 — Your first module (ORM core)**
8. Scaffold LibreFleet: manifest anatomy, module install/upgrade cycle, app icon.
9. Models & fields: `models.Model`, field types & attributes, automatic fields,
   what the ORM creates in Postgres (inspect with psql!).
10. Security first: groups, `ir.model.access.csv`, why the module 404s without it.
11. Menus, actions, and your first views: window actions, menu items, list & form.
12. Relations: many2one, one2many, many2many — modeled on customers→vehicles→orders.
13. Computed fields, related fields, onchange; store vs non-store; dependencies.
14. Constraints: SQL vs Python (`@api.constrains`), default values, sequences
    (`ir.sequence`) for order references.
15. Recordsets deep-dive: search/browse/filtered/mapped/sorted, environment (`env`),
    `create`/`write`/`unlink`, `ensure_one`, context, `sudo` (and its dangers).

**Part 3 — Views & UX**
16. View architecture: `ir.ui.view`, inheritance with xpath, view priorities.
17. List & form mastery: widgets, decorations, statusbar, smart buttons, notebooks.
18. Search views, filters, group-by, default filters via context.
19. Kanban views (with the service-order pipeline) + calendar, pivot, graph views.
20. Wizards: `TransientModel`, an "approve & invoice" wizard for service orders.

**Part 4 — Business logic like a pro**
21. Model inheritance the three ways: classic `_inherit` extension, prototype
    (`_inherit` + new `_name`), delegation `_inherits` — and when to use each.
22. Extending core apps: add fields to `res.partner`, extend Sales flow; never
    modify core, always extend (the golden rule).
23. Mail & chatter: `mail.thread`, activities, followers, email templates,
    automated notifications.
24. Data files: XML vs CSV, `noupdate`, demo data vs master data, `ref()`/xml-ids
    across modules.
25. Scheduled actions (cron), server actions, automated actions.
26. QWeb reports: PDF service report with header/footer, paper formats.
27. Controllers & portal: HTTP routes, `type='http'` vs `'json'`, auth levels,
    building the customer portal page; a taste of the website builder.
28. Testing: `TransactionCase`, `HttpCase`/tours intro, `--test-tags`, demo-data
    pitfalls, writing tests for everything built so far.

**Part 5 — Frontend (OWL) & the web client**
29. OWL fundamentals: components, props, state, hooks, QWeb templates in JS,
    assets bundles (`web.assets_backend`).
30. Extending the web client: a custom field widget, patching existing components.
31. The LibreFleet dashboard: a client action with an OWL component pulling data
    via ORM RPC (`useService("orm")`).
32. (Survey chapter, lighter) Website themes & snippets, POS customization —
    what exists, where the docs are, when you'd go deeper.

**Part 6 — The OCA way (expert tier begins)**
33. OCA safari: how repos/PSCs are organized, finding modules (odoo-community.org,
    GitHub, Odoo Apps store), judging maturity levels, reading OCA module source
    as study material.
34. OCA tooling on your own module: pre-commit (ruff, pylint-odoo, prettier),
    readme fragments, manifest conventions, module naming rules.
35. Contributing: CLA, fork/branch/commit conventions (`[FIX] module: ...`), PR
    targeting version branches, Runboat, review etiquette, the ocabot; do a real
    first contribution (docs fix or small improvement).
36. Refactor a LibreFleet feature into a standalone OCA-quality module —
    the capstone-of-the-capstone.

**Part 7 — Integrator craft**
37. Migrations: why yearly releases force them, migrating a module 18→19 (manifest,
    views, API changes — the deprecation list from the D1 revision is the exercise
    material), OCA migration process & preserving git history, OpenUpgrade
    for database migrations, Enterprise upgrade service (concept level).
38. Performance: read the ORM's SQL, N+1 patterns, `read_group`, batch `create`,
    indexes, `prefetch`, profiling; when to drop to SQL (and the rules for doing so).
39. Deployments & ops (concept level): workers, longpolling/gevent, nginx, filestore,
    backups, staging/prod flows, odoo.sh vs Docker platforms; multi-company and
    localization awareness.
40. Career map: reading core source effectively, Odoo certification, OCA Days /
    Odoo Experience, keeping up with version releases; what changes in Odoo 19/20
    and how to re-learn efficiently each October.

### 5.4 Concept coverage checklist (agent: verify before calling the syllabus done)
ORM CRUD ▢ recordsets ▢ env/context ▢ compute/related/onchange ▢ constraints ▢
sequences ▢ all 3 inheritance types ▢ view inheritance/xpath ▢ all view types ▢
wizards ▢ security (groups/ACL/record rules/sudo) ▢ mail.thread ▢ cron ▢
server actions ▢ QWeb reports ▢ controllers ▢ portal ▢ OWL component ▢ widget ▢
assets ▢ tests (unit + tour) ▢ data files/noupdate ▢ i18n basics ▢ pre-commit/OCA
conventions ▢ migration exercise ▢ performance patterns ▢ deployment concepts ▢

### 5.5 LibreFleet blueprint (data model & feature map — added 2026-07-13)

The schema below is fixed *before* M2 so chapters build one coherent module instead of
inventing fields as they go. Module name **`librefleet`** — deliberately not `fleet`,
because core Odoo ships a `fleet` module (that collision is itself a ch8 teaching
point). Models use the `librefleet.` prefix. **Author sign-off on this blueprint is
the gate for starting M2** (like the capstone-domain sign-off was for Part 2 planning).

Models, with the chapter that introduces each piece:

- **`librefleet.vehicle`** (ch9) — the reader's first model. `license_plate` (Char,
  required), `vin` (Char), `model_name` (Char), `year` (Integer), `mileage_km`
  (Float), `notes` (Text), `active` (Boolean — archiving). ch12 adds `owner_id`
  (many2one → `res.partner`) and `service_order_ids` (one2many). ch13 adds
  `service_count` (computed, statbutton). ch14 adds a SQL unique constraint on
  `license_plate` and a Python constraint on `year`.
- **`librefleet.service.type`** (ch11) — deliberately tiny config model (`name`,
  `flat_fee`, `default_duration_h`) so the first menus/actions/views chapter works on
  something with no relations yet.
- **`librefleet.service.order`** (ch12) — the centerpiece. `reference` (Char, from
  `ir.sequence`, ch14), `vehicle_id` (many2one), `customer_id` (related to
  `vehicle_id.owner_id`, stored — ch13), `service_type_id` (many2one),
  `technician_ids` (many2many → `res.users`), `line_ids` (one2many), `stage`
  (Selection: draft → confirmed → in_progress → done/cancelled; statusbar ch17,
  kanban pipeline ch19), `scheduled_start`/`scheduled_end` (Datetime; the
  no-overlapping-bookings-per-vehicle constraint, ch14), `parts_total` / `labor_total`
  / `margin` (computed with `@api.depends`, ch13). Later: chatter (ch23), approve &
  invoice wizard (ch20), QWeb PDF report (ch26), portal view (ch27), maintenance-
  reminder cron (ch25), OWL jobs-per-technician dashboard (ch31).
- **`librefleet.part`** (ch12) — `name`, `code`, `standard_cost`, `list_price`.
  Self-contained on purpose: no dependency on `product`/`sale` in Tier 1. Bridging to
  real product/invoice flows is exactly what ch22 (extending core apps) then teaches.
- **`librefleet.service.order.line`** (ch12/13) — `order_id`, `part_id`, `qty`,
  `price_unit` (default from part), `subtotal` (computed).

Security (ch10): two groups — *Workshop / User* (technicians: read all, write orders
assigned to them via record rule) and *Workshop / Manager* (full CRUD + config
models). The record rule lands in ch10 and is *felt* throughout Part 2–3.

Part 6 extraction candidate (ch36): the maintenance-reminder feature becomes a
standalone OCA-quality `librefleet_maintenance_reminder` module.

### 5.6 Challenge design (added 2026-07-13 — makes the tutorial *hard* in the right places)

Three exercise grades, used in every chapter's Exercises section:
- **⭐ Apply** — same pattern, new target ("add a `color` field to vehicles and show
  it in the list"). Confidence reps.
- **⭐⭐ Transfer** — combine this chapter with earlier ones, no steps given ("managers
  see cancelled orders, technicians don't — no view duplication allowed").
- **⭐⭐⭐ Stretch** — requires reading official docs/OCA source beyond the chapter;
  flagged as optional so beginners don't stall.

**Boss challenges** close each part from Part 2 on — a one-page *spec* (no steps) for
a small feature or mini-module built from memory, verified by an odoolings check set:
- **Part 2 boss (`boss2`):** build a tiny "garage inventory" module (one model,
  security, menu, list+form, one computed field, one constraint) from a spec, without
  looking back at chapters. This replaces the vague "rebuild from memory" self-test
  with something *checkable*.
- **Part 3 boss (`boss3`):** full view suite (search defaults, kanban with grouping,
  a wizard) for a provided model spec.
- **Part 4 boss (`boss4`):** extend a core app per spec (field on `res.partner` +
  automated activity + a test that proves it).
- **Part 5 boss (`boss5`):** a small OWL component against a documented RPC shape.
Boss specs live on the site; solutions live in `code/checkpoints/bossN/`.

**Break-it labs** — one per chapter where instructive: deliberately cause the failure
the chapter protects against (delete the ACL line and upgrade; make two fields depend
on each other; drop a required field from a form view), read the actual
traceback/log, then fix it. Debugging literacy is the #1 skill gap of new Odoo devs
and no existing tutorial teaches it systematically — this is our differentiator.

**End-of-part review quizzes** — a cumulative `<Quiz>` on each part's index page
mixing questions from all its chapters (spaced repetition; pairs with the per-part
mastery bar from §4.4).

Work in milestones; each ends in a deployable state. The author reviews each milestone
before the next starts. **Cadence assumption:** the author studies/writes ~1–2 h on
weekdays; agent prepares scaffolding, drafts, and verification scripts; the author
executes every hands-on section personally (that's the learning).

### M0 — Bootstrap (½ day) — ✅ done 2026-07-10 (then rebuilt on the D3 stack, see changelog)
- [x] Create GitHub repo `odoo-tutorial` with structure from §4.1.
- [x] Site configured (Next.js + Fumadocs after the D3 pivot): nav skeleton (all 40
      chapters as stubs), callouts, mermaid, quizzes, progress, odoolings.
- [x] GitHub Actions: deploy to Pages on push. Verify live URL.
- [x] `code/docker-compose.yml` for Odoo 19 + Postgres 16, tested end-to-end
      (fresh clone → `docker compose up` → login → install an app).
- **Acceptance:** live site with skeleton; `docker compose up` works on a clean machine.

### M1 — Part 0 + Part 1 (week 1) — ✅ done 2026-07-13
- [x] Chapters 1–4 following the §4.3 template (quizzes included; ch4 hands-on
      executed for real on odoo:19).
- [x] Chapters 5–7 written 2026-07-13, hands-on executed for real (ch05/ch06
      odoolings checks green; OCA clone measurements in ch7 are live data).
- [x] Original diagrams (mermaid) for architecture & request lifecycle.
- [x] Glossary started (every jargon term used gets an entry the day it appears).
- [x] Sidebar completion checkmarks (§4.4) as M1 wrap-up (done 2026-07-13:
      `ChapterItem` sidebar override reading the existing localStorage progress).
- **Acceptance:** a Python dev with no Odoo background gets a running dev env and
  understands the ecosystem map, verified by the author actually doing it.

### M2 — Part 2 (weeks 2–3) — the heart of the tutorial
- [x] **Gate: author signs off on the §5.5 LibreFleet blueprint** (2026-07-13).
- [ ] Chapters 8–15 with checkpoints `ch08`–`ch15` committed and installable, each
      registering odoolings checks; exercises graded per §5.6; break-it labs where
      instructive.
- [ ] Every chapter's Verify section includes at least one `odoo-bin shell` or psql
      inspection so readers see what the ORM does under the hood.
- [ ] Quiz persistence + per-part mastery, `<Term>` tooltips, predict-the-output
      quiz variant (§4.4); Part 2 review quiz.
- [ ] `boss2` challenge: spec page + odoolings check set + solution checkpoint.
- **Acceptance:** LibreFleet core installs from any checkpoint; author completes
  `boss2` from the spec alone with odoolings green.

### M3 — Parts 3 & 4 (weeks 4–6)
- [ ] Chapters 16–28 + checkpoints; test suite grows with ch28 and CI (`ci.yml`)
      starts running module tests on every push.
- [ ] `boss3` + `boss4` challenges; Part 3/4 review quizzes.
- **Acceptance:** CI green; PDF report renders; portal page works logged-in and
  logged-out; ≥ 15 meaningful tests; author clears both bosses.

### M4 — Part 5 (weeks 7–8)
- [ ] Chapters 29–32; OWL dashboard functional; `boss5`; Part 5 review quiz.
- **Acceptance:** custom widget + client action work with `--dev=all` hot reload.

### M5 — Parts 6 & 7 (weeks 9–11)
- [ ] Chapters 33–40; pre-commit adopted repo-wide; the extracted OCA-style module
      passes `pre-commit run -a` and has readme fragments.
- [ ] Author makes one real (small) OCA contribution as the ch35 exercise.
- [ ] ch37 interactive migration checklist (§4.4).
- **Acceptance:** the extracted module would plausibly survive an OCA review;
  migration exercise completed against a real 18.0 module (18→19).

### M6 — Polish & launch (week 12)
- [ ] Full read-through edit; consistency pass on admonitions and footers.
- [ ] Landing page with learning-path graphic; "how to use this tutorial" guide.
- [ ] README, CONTRIBUTING, licenses; announce (LinkedIn, r/Odoo, OCA Discord —
      author's call).
- [ ] Post-launch backlog issue: "Odoo 19/20 delta pass" (schedule after Odoo 20
      ships ~Oct 2026).

### Standing rules for the agent
1. **Never ship unexecuted code.** Run every snippet in the Docker env; paste real
   output, not imagined output.
2. **Verify version-sensitive facts** against the 19.0 docs before writing; add an
   "On Odoo 18 this differs" box when the 18.0 docs differ (readers may be on older
   client projects).
3. **Original prose and images only** (see §1.4). Link, don't copy.
3b. **Style: natural, conversational prose; no em dashes** (author preference,
    2026-07-13). Use commas, colons, parentheses or a new sentence instead. En
    dashes in numeric ranges (`1–7`) are fine.
4. Small PRs per chapter; the author reviews and *manually re-executes* each Hands-on
   before merge — this is the learning loop, do not optimize it away.
5. Maintain `docs/glossary.md` and the §5.4 checklist continuously.
6. If the author's team reveals internal conventions (their Docker platform, CI,
   project template), prefer those in "In the field" boxes — ask, don't guess.

---

## 7. The Author's Parallel Learning Plan (how to use this while onboarding)

- **Before onboarding starts:** M0 + M1. Also watch, at 1.5×: the official Odoo
  YouTube "developer" playlists and 2–3 OCA Days technical talks (e.g. contribution
  workflow talks) — note anything worth linking from chapters.
- **Weeks 1–3 of the job:** M2. This aligns with typical integrator onboarding
  (first bugfixes on models/views). Bring questions from real tickets back into
  "Gotchas" sections — that is what will make this tutorial better than the docs.
- **Weeks 4–8:** M3–M4 while taking on real tasks.
- **Month 3:** M5 — and ask the team for a real OCA PR to make; Camptocamp
  colleagues review OCA PRs constantly and will gladly point you to a good first one.
- **Retention tactics:** end-of-part self-tests (rebuild from memory), teach-back
  (explain one concept per week to a colleague or in a blog-style chapter intro),
  spaced review of the glossary.

## 8. Canonical Link Index (seed list for chapter "Further reading" sections)

- Official docs (19.0): developer home, Server framework 101, ORM reference, view
  reference, OWL tutorials, testing, QWeb reports, controllers —
  `https://www.odoo.com/documentation/19.0/developer.html`
- Official docs (18.0) for "On Odoo 18 this differs" boxes:
  `https://www.odoo.com/documentation/18.0/`
- Odoo source: `https://github.com/odoo/odoo` (branch `19.0`)
- OCA: `https://github.com/OCA` · contribute guide:
  `https://www.odoo-community.org/get-involved/contribute` · guidelines repo:
  `OCA/odoo-community.org` · `OCA/maintainer-tools` · `OCA/OpenUpgrade` ·
  Runboat: `https://runboat.odoo-community.org`
- OWL: `https://github.com/odoo/owl`
- YouTube: @Odoo (official) and @OdooCommunity (OCA Days talks)
- pre-commit / pylint-odoo: `OCA/pylint-odoo`, OCA addons repo template

## 9. Open Questions for the Author (answer before M1)
1. ~~Monorepo OK, and repo name?~~ **Answered 2026-07-10: monorepo, `odoo-tutorial`.**
2. ~~Capstone domain sign-off~~ **Answered 2026-07-10: LibreFleet confirmed.**
3. Will your team confirm the Odoo version your projects run? If most client work is
   on 16/17, add a short "working on older versions" appendix.
4. ~~Public from day 1?~~ **Answered 2026-07-10: public from day 1.**
5. ~~Sign off on the §5.5 LibreFleet blueprint (models/fields/security)?~~
   **Answered 2026-07-13: approved as written. M2 unblocked.**

---

## 10. Changelog (running log — update whenever a decision or milestone changes)

### 2026-07-14 (later) — ch10 written (security first); record rule deferred to ch12
- **Ch10 written and fully executed**: Workshop privilege + User/Manager groups
  (`security/librefleet_security.xml`), vehicle ACLs (user 1,1,0,0 / manager
  1,1,1,1), admin added to Manager via `user_ids`, technician user `tina` created
  from shell, permissions felt via `with_user` (create denied with the
  group-naming AccessError, quoted live). Fresh-install discipline taught via the
  break-it lab: swapping the manifest data order upgrades FINE on the dev db but
  kills a fresh install ("No matching record found for external id"), demonstrated
  on a throwaway db. Checkpoint `ch10`; module version bumped to 19.0.1.2.0.
- **§5.5 deviation, decided:** the blueprint put the technicians-write-their-own-
  orders record rule in ch10, but `librefleet.service.order` only exists from ch12.
  Ch10 teaches the ACL-vs-record-rule concept and previews `ir.rule` in a ⭐⭐⭐
  exercise; the real rule lands in ch12 with the model. Blueprint §5.5 stays as the
  target state.
- **Odoo 19 facts verified in-container (differ from 18, called out in-chapter):**
  `res.groups` lost `category_id` and `users` (now `privilege_id` via new model
  `res.groups.privilege`, and `user_ids`); `res.users.groups_id` is now
  `group_ids`. Core idiom copied from `hr_security.xml` (privilege record, manager
  implies user, admin added on the manager group). Also verified: a long-running
  server does NOT pick up groups/ACLs loaded by a CLI upgrade process (restart
  required; taught as a gotcha), and the no-ACL RPC error is "Object ... doesn't
  exist" (ties back to the ch09 finding).
- odoolings `ch10` added (groups exist / ACLs exist / admin reads vehicles over RPC,
  which is ch09's failure inverted / tina in Workshop User), run red then green;
  ch05–ch09 still green. Glossary +6 (access rights, group, privilege, record rule,
  superuser, XML id). Roadmap: M2 ch 8–10.

### 2026-07-14 — ch09 written (models & fields), first real model shipped
- **Ch09 written and fully executed**: `librefleet.vehicle` added per the §5.5
  blueprint (`license_plate` required, `vin`, `model_name`, `year`, `mileage_km`,
  `notes`, `active` default True) plus `_rec_name = "license_plate"` (taught via
  observe-the-ugly-fallback-then-fix; `display_name` showed `"librefleet.vehicle,1"`
  live). Table inspected via `\d`, records created/committed from shell, archiving
  demoed (`active_test=False`). Break-it lab: commenting the model import and
  upgrading silently *deletes the model's metadata* (INFO-level only) while the
  table and rows survive; recovery verified.
- **Facts verified live, two corrected assumptions worth remembering:** (1) in 19,
  removing a *field* and upgrading DROPS its column (metadata prune cascades to
  `ALTER TABLE ... DROP COLUMN`), unlike removing a whole *model*, which keeps the
  table; ch09 exercise 1 teaches the real behavior. (2) A no-ACL model over XML-RPC
  answers "Object librefleet.vehicle doesn't exist" (no AccessError), so odoolings
  ch09 checks read `ir.model` / `ir.model.fields` instead of the model itself; the
  record-visibility check belongs to ch10.
- odoolings `ch09` added (model registered / field types / required flag), run red
  then green. Checkpoint `code/checkpoints/ch09/` committed; module version bumped
  to 19.0.1.1.0. Glossary +5 (archiving, automatic fields, display_name, model,
  registry). Roadmap: M2 ch 8–9.

### 2026-07-13 (evening, later) — blueprint signed off; M2 started with ch08
- **§5.5 LibreFleet blueprint approved by the author (§9 Q5 closed). M2 unblocked.**
- **Ch08 written and executed for real**: `code/addons/librefleet/` created
  (manifest, empty `__init__.py`, generated icon), installed and upgraded via CLI
  against the `tutorial` db, version bump observed in `ir_module_module`, break-it
  lab captured live (syntax-broken manifest → the cryptic "inconsistent states"
  error). Checkpoint `code/checkpoints/ch08/` committed. odoolings `ch08` checks
  added (installed / version format / application flag), verified red then green.
- Roadmap: M2 🚧. Glossary: +technical name.

### 2026-07-13 (evening) — M1 fully done: sidebar completion checkmarks shipped
- `web/components/chapter-item.tsx`: sidebar `Item` override (Fumadocs
  `sidebar.components` slot) showing a green check next to chapters marked
  complete, driven by the same localStorage progress store as the pill. Wired in
  `app/docs/layout.tsx`. Build + type check green. **M1 closed.**
- Next milestone is M2 (ch8–15); its gate remains author sign-off on the §5.5
  blueprint (§9 Q5).

### 2026-07-13 (later) — M1 chapters complete; content style pass
- **Chapters 5–7 written (Part 1 — Environment), M1 content done.** Every command
  executed for real: compose lifecycle, `odoo db init/duplicate/drop/dump` (19's
  filestore-aware db command), `odoo shell` (incl. the commit gotcha), OCA
  branch-per-version measured live (server-tools: 32 modules on 19.0 vs 73 on 16.0),
  real `[TAG]` commit messages quoted. `--dev=all` facts verified against the
  container (`all` = access,reload,qweb,xml on 19).
- **odoolings: ch06 checks added** (login + "Ada Lovelace partner created from shell
  exists" — fails with a commit-hint if the reader skips `env.cr.commit()`; verified
  both red and green paths). Success message reworded (no em dash).
- **Style rule added (standing rule 3b): natural prose, no em dashes** (author
  request). All existing content (ch1–4, index, glossary, roadmap, stubs) swept
  clean; exercises in ch1–4 retrofitted with §5.6 ⭐ grades; ch5–7 written with
  grades and one break-it lab each (ch5 `down -v`, ch6 stopped db container).
- Glossary +8 terms (filestore, master password, env, odoo shell, commit tags,
  pinning...). `librefleet.vehicle` naming aligned in odoolings sample/comment.
  `code/odoo.conf` comment made reader-facing. Roadmap page: M1 ✅.
- Still open before M2: author sign-off on §5.5 blueprint (§9 Q5); sidebar
  completion checkmarks (§4.4) remain the last M1 wrap-up item.

### 2026-07-13 — plan consistency pass + detail/challenge/interactivity upgrades
- **Body of the plan reconciled with the July-10 pivots.** The D1 (Odoo 19) and D3
  (Next.js/Fumadocs) revisions had only been logged here in the changelog; §4
  (repo tree, site conventions, chapter template), §5.3 (ch5, ch37), §6 (standing
  rule 2, milestone statuses), and §8 (link index) still described the MkDocs/18.0
  world. All rewritten to match reality, so a cold-start agent no longer follows
  stale instructions. M0 ticked done; M1 marked ch1–4 done.
- **New §5.5 — LibreFleet blueprint:** full data model (5 models, fields, relations,
  security groups) mapped to the chapters that introduce each piece, fixed before M2
  so the capstone grows coherently. **Author sign-off on it is the new M2 gate**
  (§9 Q5).
- **New §5.6 — challenge design** (author asked for "more challenging" 2026-07-13):
  graded exercises (⭐ apply / ⭐⭐ transfer / ⭐⭐⭐ stretch), **boss challenges**
  ending Parts 2–5 (spec-only mini-builds verified by odoolings `bossN` check sets,
  replacing the unverifiable "rebuild from memory" self-test), **break-it labs**
  (deliberately trigger and debug the failure each chapter protects against —
  traceback literacy as a first-class skill), and cumulative end-of-part review
  quizzes.
- **New §4.4 — interactive mechanics inventory & roadmap** (author asked for "more
  interactive"): documents what's built (Quiz, odoolings, progress pill, Mermaid) and
  schedules what's next — sidebar completion checkmarks (M1 wrap-up), quiz
  persistence + per-part mastery bar (M2), `<Term>` glossary tooltips (M2),
  predict-the-output quiz variant (M2, recordsets chapter), ch37 migration checklist
  (M5). Still no accounts/backend by design.
- Chapter template (§4.3) now formally includes the Quick check section and the
  odoolings authoring rule; quizzes must test ideas, not syntax recall.

### 2026-07-10 (later still) — LibreFleet signed off; chapters 1–4 written
- **Capstone confirmed: LibreFleet** (§9 Q2 closed). Part 2+ can be planned in detail.
- **M1 started: chapters 1–4 (Part 0 — Orientation) written** per the §4.3 template,
  each with a 3-question quiz. Added a `<Mermaid>` client component (mermaid npm dep)
  for the ch3 architecture + request-lifecycle diagrams. Glossary grew to 20 sorted
  terms. Ch4's hands-on was executed for real on odoo:19 (demo DB `tour`,
  crm+sale_management installed, 44 demo leads verified via psql; CLI default is
  --without-demo in 19 — documented as a gotcha).
- Screenshots for ch4 are deliberately absent until the author does the tour
  personally (standing rule 4: the author re-executes every hands-on).
- Next: chapters 5–7 (Part 1 — Environment) to complete M1.

### 2026-07-10 (later) — baseline bumped to Odoo 19
- **D1 revised: Odoo 19.0 Community is the baseline** (was 18.0). Verified before
  switching: 18→19 dev-facing changes are deprecations/idioms
  (`read_group`→`_read_group`/`formatted_read_group`, `display_name` over `name_get()`,
  `t-out` over `t-esc`, `odoo.osv` retired, Python 3.12 recommended) — the fundamentals
  the tutorial teaches are identical. Callout convention flips to
  `"On Odoo 18 this differs"` for readers on older client projects.
- Applied: `code/docker-compose.yml` → `odoo:19` (verified: compose up, DB init, app
  install, odoolings green), odoolings version check → 19.x, all site/README text,
  doc links → `/documentation/19.0/`.
- **ch37 (Migrations) gains an interactive migration-checklist component** (author's
  idea: trackable checkboxes for the migration procedure). Build it when writing ch37,
  not before. The 18→19 deprecation list above is ch37's exercise material.
- Standing policy confirmed by author: re-verify the baseline each October when a new
  major ships (Odoo 20 ~Oct 2026 → schedule the delta/bump pass then). Note: Odoo has
  no LTS — one major per year, last three supported.

### 2026-07-10 — M0 shipped, then rebuilt as an interactive platform
- **M0 done** on the original MkDocs stack: monorepo `ronitjadhav/odoo-tutorial`
  created, 40 chapter stubs, GitHub Pages deploy, Docker env verified end-to-end
  (DB create + app install checked via psql).
- **Pivot: the tutorial is an interactive learning platform, not a docs site**
  (author decision). Duolingo-inspired but practice-first. Three mechanics:
  1. **Quizzes** per chapter with instant feedback (`<Quiz>` MDX component).
  2. **`odoolings`** (`code/odoolings.py`) — rustlings-style stdlib-only CLI that
     verifies the reader's work against their *running* Odoo over XML-RPC, with
     hints. Each chapter registers checks as it is written. First checks: ch05.
  3. **Progress + streaks** — localStorage only (pill bottom-right, per-chapter
     "mark complete"). No accounts/backend by design; revisit only if a real
     learner community shows up.
- **D3 revised**: MkDocs → **Next.js 16 + Fumadocs (base-ui) + Tailwind 4**, in
  `web/`, static-exported with basePath `/odoo-tutorial`. Search is Orama static
  (`/api/search` index generated at build). Landing page is a custom React page.
  MkDocs files removed.
- **Authoring implications for future chapters (agent: follow these):**
  - Chapters are `.mdx` in `web/content/docs/<part>/<NN-slug>.mdx` with
    frontmatter `title`/`description`; part nav order lives in each folder's
    `meta.json`. Chapter template of §4.3 now includes a **Quick check** section
    (quiz) between Gotchas and Exercises.
  - Every chapter with hands-on work must also add `odoolings` checks —
    "Verify" sections reference `python odoolings.py check chNN`.
- **Still open:** capstone sign-off (LibreFleet?), team's Odoo version.
- **Deferred with known ceiling:** odoolings checks all live in one file (split
  per chapter when it outgrows ~300 lines); sidebar completion checkmarks;
  quiz state isn't persisted (retaking is a feature for now).
