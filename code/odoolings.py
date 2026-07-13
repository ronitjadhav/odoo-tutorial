#!/usr/bin/env python3
"""odoolings — auto-check your tutorial work against each chapter's goals.

Inspired by rustlings: after finishing a chapter's Hands-on section, run

    python odoolings.py check ch05

and it inspects your *actually running* Odoo over XML-RPC. Green means your
work matches the chapter checkpoint; red comes with a hint.

Stdlib only — nothing to install. Defaults match the tutorial's Docker env
(http://localhost:8069, database "tutorial", admin/admin).
"""
import argparse
import sys
import xmlrpc.client


class Env:
    """Tiny XML-RPC wrapper. Checks call env.call(model, method, *args)."""

    def __init__(self, url, db, user, password):
        self.url, self.db, self.user, self.password = url, db, user, password
        self.common = xmlrpc.client.ServerProxy(url + "/xmlrpc/2/common")
        self.uid = None

    def login(self):
        self.uid = self.common.authenticate(self.db, self.user, self.password, {})
        assert self.uid, "authentication failed for %r on database %r" % (self.user, self.db)
        self.models = xmlrpc.client.ServerProxy(self.url + "/xmlrpc/2/object")

    def call(self, model, method, *args, **kw):
        if self.uid is None:
            self.login()
        return self.models.execute_kw(self.db, self.uid, self.password, model, method, list(args), kw)


# ---------------------------------------------------------------- checks --
# One function per check; raise AssertionError (or anything) to fail.

def server_up(env):
    env.version_info = env.common.version()


def server_is_19(env):
    v = env.common.version()["server_version"]
    assert v.startswith("19"), "server reports version %s, tutorial targets 19.x" % v


def can_login(env):
    env.login()


def shell_partner_exists(env):
    ids = env.call("res.partner", "search", [("name", "=", "Ada Lovelace")])
    assert ids, "no res.partner named 'Ada Lovelace' in the database"


# Each chapter: list of (description, check_fn, hint shown on failure).
CHAPTERS = {
    "ch05": [
        ("Odoo server is reachable", server_up,
         "Is the dev environment running? From code/: docker compose up"),
        ("server version is 19.x", server_is_19,
         "The tutorial targets Odoo 19. Check the image tag in docker-compose.yml (image: odoo:19)."),
        ("can log in as admin", can_login,
         "Create a database (default name: tutorial) at http://localhost:8069 with admin/admin, "
         "or pass --db/--user/--password for yours."),
    ],
    "ch06": [
        ("can log in as admin", can_login,
         "Is the dev environment running with the tutorial database? See ch05."),
        ("the partner created from odoo shell exists", shell_partner_exists,
         "In the ch06 hands-on you create a contact named 'Ada Lovelace' from "
         "odoo shell. Did you run env.cr.commit() before quitting? Without it, "
         "shell writes are rolled back."),
    ],
    # Chapters 8+ add checks as they are written, e.g. "model librefleet.vehicle
    # exists", "field mileage is Float" — via env.call('ir.model', ...) and
    # fields_get().
}


def cmd_check(env, chapter):
    checks = CHAPTERS.get(chapter)
    if checks is None:
        print("Unknown chapter %r. Chapters with checks: %s" % (chapter, ", ".join(sorted(CHAPTERS))))
        return 2
    for desc, fn, hint in checks:
        try:
            fn(env)
        except Exception as e:
            # server Faults carry a full traceback; the last line is the point
            msg = e.faultString.strip().splitlines()[-1] if isinstance(e, xmlrpc.client.Fault) else e
            print("✘ %s" % desc)
            print("    %s" % msg)
            print("    hint: %s" % hint)
            return 1
        print("✔ %s" % desc)
    print("\n%s complete! On to the next chapter 🔧" % chapter)
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="odoolings", description=__doc__.split("\n")[0])
    p.add_argument("command", choices=["check", "list"])
    p.add_argument("chapter", nargs="?", help="e.g. ch05")
    p.add_argument("--url", default="http://localhost:8069")
    p.add_argument("--db", default="tutorial")
    p.add_argument("--user", default="admin")
    p.add_argument("--password", default="admin")
    a = p.parse_args(argv)

    if a.command == "list":
        for ch in sorted(CHAPTERS):
            print("%s  (%d checks)" % (ch, len(CHAPTERS[ch])))
        return 0
    if not a.chapter:
        p.error("check needs a chapter, e.g.: odoolings.py check ch05")
    return cmd_check(Env(a.url, a.db, a.user, a.password), a.chapter)


if __name__ == "__main__":
    sys.exit(main())
