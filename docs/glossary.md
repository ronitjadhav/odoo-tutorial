# Glossary

Every piece of Odoo jargon gets an entry here the day a chapter first uses it.

**addon** — see *module*. The two words are used interchangeably; `--addons-path` is
the directory list Odoo scans for them.

**addons path** — the ordered list of directories Odoo searches for modules.

**manifest** — `__manifest__.py`, the dict at a module's root declaring its name,
version, `depends`, data files, and license. Its presence is what makes a directory a
module.

**module** — a directory with `__manifest__.py` and `__init__.py` that adds models,
views, data, or code to an Odoo database. An *app* is just a module with
`'application': True`.

**OCA** — Odoo Community Association. A Swiss nonprofit hosting hundreds of
community-maintained module repositories at [github.com/OCA](https://github.com/OCA).

**ORM** — Odoo's object-relational mapper: the layer that turns Python model classes
into PostgreSQL tables and back.

**OWL** — Odoo Web Library, the in-house JavaScript component framework used by the web
client since Odoo 14.

**QWeb** — Odoo's XML templating engine, used both server-side (PDF reports, website
pages) and client-side (OWL component templates).

**recordset** — the value every ORM operation returns: an ordered collection of records
of one model, which may hold zero, one, or many. Methods called on it apply to all of
them.
