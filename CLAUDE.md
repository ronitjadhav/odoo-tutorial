# Zero to Odoo Expert — agent guide

Interactive tutorial platform teaching Odoo 19 development, plus the companion code
readers build against. Live at https://ronitjadhav.github.io/odoo-tutorial/.

**Source of truth: `ODOO_TUTORIAL_MASTER_PLAN.md`.** Read it before non-trivial work:
§4 site/authoring conventions, §5.3 syllabus, §5.5 LibreFleet data blueprint, §5.6
challenge design, §6 milestones and standing rules. **Every decision or milestone
change must be logged in its §10 changelog**, so work can resume cold.

## Layout

- `web/` — Next.js 16 + Fumadocs + Tailwind 4, static export, basePath `/odoo-tutorial`.
  Chapters are MDX in `web/content/docs/<part>/<NN-slug>.mdx`; nav order in each
  folder's `meta.json`. Custom components in `web/components/` (Quiz, Mermaid,
  progress pill, mark-complete).
- `code/` — reader-facing: `docker-compose.yml` (odoo:19 + postgres:16), `odoo.conf`,
  `odoolings.py` (stdlib-only XML-RPC work checker), `addons/` (capstone module from
  ch8), `checkpoints/` (per-chapter snapshots).

## Commands

```bash
cd web && npm run dev        # local site
cd web && npm run build     # must pass before any push (validates all MDX)
cd code && docker compose up -d          # the tutorial's Odoo environment
python3 code/odoolings.py check chNN     # verify a chapter's hands-on state
```

## Non-negotiable authoring rules

1. **Never ship unexecuted code.** Every command and snippet in a chapter is run for
   real in the Docker env first; quoted output is real output.
2. **Style: natural, conversational prose. No em dashes (—).** Use commas, colons,
   parentheses, or a new sentence. En dashes in numeric ranges (`1–7`) are fine.
3. **Original prose only.** Never copy from Odoo docs/source/blogs. Link out
   generously, always version-pinned to `/documentation/19.0/`.
4. Chapters follow the §4.3 template exactly (incl. Quick check quiz and ⭐-graded
   exercises); hands-on chapters register odoolings checks; new jargon gets a
   glossary entry the same day.
5. Screenshots and "author does the tour" steps stay pending until the author
   personally re-executes them; do not fake or skip that loop.
6. To write a new chapter, use the `write-chapter` skill in `.claude/skills/`.

Content license CC BY-SA 4.0, code AGPL-3. Commit style: `M<N>: ...` for milestone
work on this repo; tutorial code examples teach OCA style (`[TAG] module: ...`).
