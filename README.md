# Zero to Odoo Expert

A hands-on Odoo 18 development tutorial, taking a Python developer from zero Odoo
knowledge to OCA-quality contributions. Built in the open, chapter by chapter, while I
learn Odoo myself.

**📖 Read it: <https://ronitjadhav.github.io/odoo-tutorial/>**

## What's here

| Path | Contents |
|---|---|
| `web/` | The site — Next.js + Fumadocs, statically exported to GitHub Pages |
| `code/addons/` | LibreFleet, the capstone module, in its final state |
| `code/odoolings.py` | rustlings-style CLI that checks your work against each chapter's goals |
| `code/checkpoints/` | A snapshot of LibreFleet after each chapter |
| `code/docker-compose.yml` | The Odoo 18 + Postgres 16 dev environment used throughout |
| `ODOO_TUTORIAL_MASTER_PLAN.md` | The full curriculum and the reasoning behind it |

## Run the dev environment

```bash
cd code && docker compose up
```

Then open <http://localhost:8069> and create a database. Master password is `admin`.

## Preview the site locally

```bash
cd web && npm install && npm run dev
```

## Status

M0 complete: interactive platform (quizzes, progress, odoolings checker) and dev
environment. Chapters are stubs — see the roadmap on the site.

## License

Prose and images: [CC BY-SA 4.0](LICENSE-content). Code: [AGPL-3.0](LICENSE-code),
matching OCA convention.
