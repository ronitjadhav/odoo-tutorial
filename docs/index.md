# Zero to Odoo Expert

A free, hands-on tutorial that takes a competent Python developer with **zero Odoo
knowledge** to the point of contributing OCA-quality modules.

It is not a rewrite of the [official Odoo docs](https://www.odoo.com/documentation/18.0/).
It links to them generously and adds what they leave out: sequencing, the *why*, the
pitfalls, and the practices real Odoo integrators use every day.

## How it works

You build one project — **LibreFleet**, a vehicle-workshop and service-booking app —
across 40 chapters. Every chapter ends with a checkpoint in
[`code/checkpoints/`](https://github.com/ronitjadhav/odoo-tutorial/tree/main/code/checkpoints)
so you can diff your work against a known-good state whenever you get stuck.

Everything targets **Odoo 18.0 Community**, running in Docker. Chapters flag where
Odoo 19 differs.

This is not a read-only site — it's built for practice:

- **Quizzes** in each chapter give instant feedback (try one in
  [chapter 1](00-orientation/01-what-odoo-is.md#quick-check)).
- **`odoolings`**, a rustlings-style checker, inspects your *actually running* Odoo
  after each Hands-on section and tells you exactly what's missing:

    ```console
    $ python odoolings.py check ch09
    ✔ model libre.vehicle exists
    ✘ field mileage is Float
        hint: fields.Float, not fields.Integer — odometers have decimals.
    ```

- **Progress and streaks** are tracked in the header (stored only in your browser —
  no account, no tracking).

## The path

| Tier | Parts | You can... |
|---|---|---|
| Foundations | 0–3 | build and ship a clean custom module |
| Professional | 4–5 | extend core apps safely, test, build UI, debug anything |
| Expert | 6–7 | work the OCA way, migrate modules, tune performance, reason about deploys |

Start with [What Odoo Is](00-orientation/01-what-odoo-is.md).

## Status

Early. See the [roadmap](roadmap.md) for what's written and what isn't.

---

Content is [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); code is AGPL-3.0.
Issues and PRs welcome at
[ronitjadhav/odoo-tutorial](https://github.com/ronitjadhav/odoo-tutorial).
