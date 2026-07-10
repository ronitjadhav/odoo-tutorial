import Link from 'next/link';
import {
  ArrowRight,
  BookOpenCheck,
  Container,
  Flame,
  GitPullRequest,
  Terminal,
  Wrench,
} from 'lucide-react';

const TIERS = [
  {
    icon: Wrench,
    name: 'Foundations',
    parts: 'Parts 0–3 · ch 1–20',
    blurb: 'Environment, ORM, views, security — build and ship a clean custom module.',
  },
  {
    icon: BookOpenCheck,
    name: 'Professional',
    parts: 'Parts 4–5 · ch 21–32',
    blurb: 'Extend core apps safely, write tests, build OWL UI, debug anything.',
  },
  {
    icon: GitPullRequest,
    name: 'Expert / Integrator',
    parts: 'Parts 6–7 · ch 33–40',
    blurb: 'Work the OCA way: contributions, migrations, performance, deployments.',
  },
];

const FEATURES = [
  {
    icon: Terminal,
    title: 'Your code, checked',
    body: 'odoolings — a rustlings-style CLI — inspects your actually running Odoo after every hands-on section and tells you exactly what’s missing, with hints.',
  },
  {
    icon: Flame,
    title: 'Practice, not prose',
    body: 'Quizzes with instant feedback, per-chapter completion, streaks. All stored in your browser — no account, no tracking.',
  },
  {
    icon: Container,
    title: 'Real integrator workflow',
    body: 'Docker-first environment, checkpoint diffs after every chapter, and the same conventions used in OCA and professional Odoo teams.',
  },
];

export default function HomePage() {
  return (
    <div className="flex flex-1 flex-col">
      {/* hero */}
      <section className="relative overflow-hidden px-6 py-24 text-center">
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(ellipse_60%_50%_at_50%_-10%,var(--color-fd-primary),transparent_70%)] opacity-15"
        />
        <p className="mx-auto mb-6 w-fit rounded-full border px-3 py-1 text-xs font-medium text-fd-muted-foreground">
          Free & open source · Odoo 19 Community
        </p>
        <h1 className="mx-auto max-w-3xl text-4xl font-bold tracking-tight sm:text-6xl">
          Zero to{' '}
          <span className="bg-gradient-to-r from-fd-primary to-purple-500 bg-clip-text text-transparent">
            Odoo Expert
          </span>
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-fd-muted-foreground">
          A hands-on path from your first module to OCA-quality contributions. You build
          a real app — LibreFleet — chapter by chapter, and every step of your work is
          verified against your own running Odoo.
        </p>
        <div className="mt-10 flex items-center justify-center gap-4">
          <Link
            href="/docs"
            className="group flex items-center gap-2 rounded-full bg-fd-primary px-6 py-3 font-medium text-fd-primary-foreground transition-transform hover:scale-105"
          >
            Start learning
            <ArrowRight className="size-4 transition-transform group-hover:translate-x-0.5" />
          </Link>
          <a
            href="https://github.com/ronitjadhav/odoo-tutorial"
            className="rounded-full border px-6 py-3 font-medium transition-colors hover:bg-fd-accent"
          >
            GitHub
          </a>
        </div>

        {/* odoolings teaser */}
        <div className="mx-auto mt-16 max-w-lg rounded-xl border bg-fd-card p-4 text-start font-mono text-sm shadow-lg">
          <p className="text-fd-muted-foreground">$ python odoolings.py check ch09</p>
          <p className="text-green-500">✔ model libre.vehicle exists</p>
          <p className="text-green-500">✔ field mileage is Float</p>
          <p className="text-red-500">✘ smart button shows service count</p>
          <p className="pl-4 text-fd-muted-foreground">
            hint: a computed Integer + a button of type &quot;object&quot;…
          </p>
        </div>
      </section>

      {/* features */}
      <section className="mx-auto grid max-w-5xl gap-6 px-6 pb-24 sm:grid-cols-3">
        {FEATURES.map((f) => (
          <div
            key={f.title}
            className="rounded-xl border bg-fd-card p-6 transition-all hover:-translate-y-1 hover:shadow-lg"
          >
            <f.icon className="mb-4 size-6 text-fd-primary" />
            <h3 className="mb-2 font-semibold">{f.title}</h3>
            <p className="text-sm text-fd-muted-foreground">{f.body}</p>
          </div>
        ))}
      </section>

      {/* learning path */}
      <section className="border-t bg-fd-secondary/30 px-6 py-24">
        <h2 className="text-center text-3xl font-bold">One path, three tiers</h2>
        <p className="mx-auto mt-4 max-w-xl text-center text-fd-muted-foreground">
          40 chapters, one capstone project, and a checkpoint to diff against after every
          single one.
        </p>
        <div className="mx-auto mt-12 grid max-w-5xl gap-6 sm:grid-cols-3">
          {TIERS.map((t, i) => (
            <div key={t.name} className="relative rounded-xl border bg-fd-background p-6">
              <span className="absolute -top-3 left-6 rounded-full bg-fd-primary px-2.5 py-0.5 text-xs font-bold text-fd-primary-foreground">
                Tier {i + 1}
              </span>
              <t.icon className="mb-4 size-6 text-fd-primary" />
              <h3 className="font-semibold">{t.name}</h3>
              <p className="mt-1 text-xs font-medium text-fd-muted-foreground">{t.parts}</p>
              <p className="mt-3 text-sm text-fd-muted-foreground">{t.blurb}</p>
            </div>
          ))}
        </div>
        <div className="mt-12 text-center">
          <Link
            href="/docs/00-orientation/01-what-odoo-is"
            className="font-medium text-fd-primary underline-offset-4 hover:underline"
          >
            Begin with chapter 1 →
          </Link>
        </div>
      </section>
    </div>
  );
}
