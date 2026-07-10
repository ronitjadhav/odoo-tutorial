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
| D1 | Odoo version to teach | **Odoo 18.0 Community** as the baseline, with "What changed in 19" callout boxes | The author's team shared the 18.0 docs; 18 is in the middle of the 3-version support window (17/18/19 as of mid-2026); most client projects at integrators run n-1 or n-2. Odoo 20 arrives ~Oct 2026 — plan a version-bump pass afterwards, don't chase it now. |
| D2 | Edition | **Community (open source)** | Enterprise source is not freely redistributable; Community is what OCA targets; everything learned transfers. Mention Enterprise-only features in info boxes. |
| D3 | Site generator | **MkDocs + Material for MkDocs theme** | Python-native (fits the Odoo world), Markdown-based, excellent search, code annotations, tabs, admonitions, dark mode, trivial GitHub Pages deploy via Actions. (Alternative considered: Docusaurus — heavier, React-based, no advantage here.) |
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
  version-pinned URLs (18.0), never `/master/`.

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

### 4.1 Monorepo structure

```
odoo-tutorial/                      # public GitHub repo
├── mkdocs.yml                      # site config (Material theme)
├── docs/                           # all tutorial content (Markdown)
│   ├── index.md                    # landing page: what/why/how to use
│   ├── 00-orientation/             # Part 0
│   ├── 01-environment/             # Part 1  (one folder per part, one .md per chapter)
│   ├── 02-first-module/
│   ├── ...
│   ├── assets/                     # screenshots, diagrams (original only)
│   └── glossary.md                 # Odoo jargon: addon, manifest, recordset, sudo, ...
├── code/
│   ├── addons/
│   │   └── <capstone_module>/      # final state of the capstone module(s)
│   ├── checkpoints/
│   │   ├── ch03/ ch04/ ...         # snapshot of the addon after each chapter
│   ├── docker-compose.yml          # the exact dev env the tutorial uses
│   ├── .pre-commit-config.yaml     # OCA-style hooks, used from Part 6 onward
│   └── requirements-dev.txt
├── .github/workflows/
│   ├── deploy-pages.yml            # mkdocs gh-deploy on push to main
│   └── ci.yml                      # lint + run Odoo tests for code/addons (later milestone)
├── LICENSE-content (CC BY-SA 4.0), LICENSE-code (AGPL-3)
├── CONTRIBUTING.md                 # how readers can file issues/PRs
└── README.md
```

### 4.2 Site features to configure (Material for MkDocs)
- Navigation: parts as top-level sections, chapters as pages; "prev/next" footer nav.
- Code blocks with copy button, line highlights, and **annotations** for explaining
  specific lines.
- Admonition boxes with consistent semantics used throughout:
  - `!!! note "Official docs"` → link to the canonical doc page for the topic
  - `!!! warning "Gotcha"` → real-world pitfalls
  - `!!! tip "In the field"` → integrator/OCA practice notes
  - `!!! info "Odoo 19 changed this"` → version deltas
  - `!!! example "Exercise"` → hands-on tasks with a link to the checkpoint solution
- Per-chapter footer template: *Prerequisites · What you built · Official reading ·
  OCA modules worth studying for this topic · Exercise checklist.*
- Search (built-in), dark mode, mermaid diagrams enabled for architecture drawings.

### 4.3 Chapter template (every chapter MUST follow this skeleton)

```markdown
# NN. Chapter Title
**Goal:** one sentence. **Time:** ~X h. **Checkpoint:** code/checkpoints/chNN

## Why this matters            <- motivation, real-world framing
## Concepts                    <- original explanation, diagrams, links to official docs
## Hands-on                    <- numbered steps on the capstone project
## Verify                      <- how to prove it works (UI steps, shell commands, tests)
## Gotchas                     <- pitfalls collected while writing/testing the chapter
## Exercises                   <- 2–4 tasks WITHOUT step-by-step solutions inline
## Further reading             <- official docs + OCA examples + (optional) videos
```

**Authoring rule for the agent:** every "Hands-on" section must be *executed and
verified* in the Docker environment before the chapter is marked done. No untested
code ships. Screenshots are taken from the author's own running instance.

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
5. Dev setup with Docker Compose: Odoo 18 + Postgres 16, volumes for addons and
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
37. Migrations: why yearly releases force them, migrating a module 17→18 (manifest,
    views, API changes), OCA migration process & preserving git history, OpenUpgrade
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

---

## 6. Execution Roadmap for the Building Agent

Work in milestones; each ends in a deployable state. The author reviews each milestone
before the next starts. **Cadence assumption:** the author studies/writes ~1–2 h on
weekdays; agent prepares scaffolding, drafts, and verification scripts; the author
executes every hands-on section personally (that's the learning).

### M0 — Bootstrap (½ day)
- [ ] Create GitHub repo `odoo-tutorial` with structure from §4.1.
- [ ] MkDocs Material configured: theme, nav skeleton (all 40 chapters as stubs),
      admonitions, mermaid, code annotations.
- [ ] GitHub Actions: deploy to Pages on push. Verify live URL.
- [ ] `code/docker-compose.yml` for Odoo 18 + Postgres 16, tested end-to-end
      (fresh clone → `docker compose up` → login → install an app).
- **Acceptance:** live site with skeleton; `docker compose up` works on a clean machine.

### M1 — Part 0 + Part 1 (week 1)
- [ ] Write chapters 1–7 following the §4.3 template.
- [ ] Original diagrams (mermaid) for architecture & request lifecycle.
- [ ] Glossary started (every jargon term used gets an entry the day it appears).
- **Acceptance:** a Python dev with no Odoo background gets a running dev env and
  understands the ecosystem map, verified by the author actually doing it.

### M2 — Part 2 (weeks 2–3) — the heart of the tutorial
- [ ] Chapters 8–15 with checkpoints `ch08`–`ch15` committed and installable.
- [ ] Every chapter's Verify section includes at least one `odoo-bin shell` or psql
      inspection so readers see what the ORM does under the hood.
- **Acceptance:** LibreFleet core installs from any checkpoint; author can rebuild it
  from memory (self-test at end of part).

### M3 — Parts 3 & 4 (weeks 4–6)
- [ ] Chapters 16–28 + checkpoints; test suite grows with ch28 and CI (`ci.yml`)
      starts running module tests on every push.
- **Acceptance:** CI green; PDF report renders; portal page works logged-in and
  logged-out; ≥ 15 meaningful tests.

### M4 — Part 5 (weeks 7–8)
- [ ] Chapters 29–32; OWL dashboard functional.
- **Acceptance:** custom widget + client action work with `--dev=all` hot reload.

### M5 — Parts 6 & 7 (weeks 9–11)
- [ ] Chapters 33–40; pre-commit adopted repo-wide; the extracted OCA-style module
      passes `pre-commit run -a` and has readme fragments.
- [ ] Author makes one real (small) OCA contribution as the ch35 exercise.
- **Acceptance:** the extracted module would plausibly survive an OCA review;
  migration exercise completed against a real 17.0 module.

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
2. **Verify version-sensitive facts** against the 18.0 docs before writing; add an
   "Odoo 19 changed this" box when the 19.0 docs differ.
3. **Original prose and images only** (see §1.4). Link, don't copy.
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

- Official docs (18.0): developer home, Server framework 101, ORM reference, view
  reference, OWL tutorials, testing, QWeb reports, controllers —
  `https://www.odoo.com/documentation/18.0/developer.html`
- Official docs (19.0) for delta boxes: `https://www.odoo.com/documentation/19.0/`
- Odoo source: `https://github.com/odoo/odoo` (branch `18.0`)
- OCA: `https://github.com/OCA` · contribute guide:
  `https://www.odoo-community.org/get-involved/contribute` · guidelines repo:
  `OCA/odoo-community.org` · `OCA/maintainer-tools` · `OCA/OpenUpgrade` ·
  Runboat: `https://runboat.odoo-community.org`
- OWL: `https://github.com/odoo/owl`
- YouTube: @Odoo (official) and @OdooCommunity (OCA Days talks)
- pre-commit / pylint-odoo: `OCA/pylint-odoo`, OCA addons repo template

## 9. Open Questions for the Author (answer before M1)
1. Monorepo OK, and repo name? (default: `odoo-tutorial`)
2. Capstone domain sign-off: LibreFleet, or a domain you personally enjoy more?
3. Will your team confirm the Odoo version your projects run? If most client work is
   on 16/17, add a short "working on older versions" appendix.
4. Public from day 1, or private until M3 quality bar is met? (Recommend: public
   early — it creates accountability.)
