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


def _librefleet_module(env):
    mods = env.call("ir.module.module", "search_read",
                    [("name", "=", "librefleet")],
                    fields=["state", "latest_version", "application"])
    assert mods, "no module named 'librefleet' known to this database"
    return mods[0]


def librefleet_installed(env):
    state = _librefleet_module(env)["state"]
    assert state == "installed", "module state is %r, not 'installed'" % state


def librefleet_version_ok(env):
    v = _librefleet_module(env)["latest_version"] or ""
    assert v.startswith("19.0."), "installed version is %r, expected 19.0.x.y.z" % v


def librefleet_is_app(env):
    assert _librefleet_module(env)["application"], "'application' is not True in the manifest"


def vehicle_model_exists(env):
    ids = env.call("ir.model", "search", [("model", "=", "librefleet.vehicle")])
    assert ids, "no model 'librefleet.vehicle' registered in this database"


def _vehicle_fields(env):
    return {f["name"]: f for f in env.call(
        "ir.model.fields", "search_read",
        [("model", "=", "librefleet.vehicle")],
        fields=["name", "ttype", "required"])}


def vehicle_fields_typed(env):
    expected = {"license_plate": "char", "vin": "char", "model_name": "char",
                "year": "integer", "mileage_km": "float", "notes": "text",
                "active": "boolean"}
    actual = _vehicle_fields(env)
    for name, ttype in expected.items():
        assert name in actual, "field %r is missing on librefleet.vehicle" % name
        assert actual[name]["ttype"] == ttype, (
            "field %r is %r, expected %r" % (name, actual[name]["ttype"], ttype))


def vehicle_plate_required(env):
    f = _vehicle_fields(env).get("license_plate")
    assert f and f["required"], "license_plate is not required=True"


def workshop_groups_exist(env):
    for xmlid in ("librefleet.group_librefleet_user", "librefleet.group_librefleet_manager"):
        res = env.call("ir.model.data", "check_object_reference",
                       xmlid.split(".")[0], xmlid.split(".")[1])
        assert res and res[0] == "res.groups", "%s does not resolve to a res.groups record" % xmlid


def vehicle_acls_exist(env):
    acls = env.call("ir.model.access", "search_count",
                    [("model_id.model", "=", "librefleet.vehicle")])
    assert acls >= 2, ("found %d access rules for librefleet.vehicle, expected one "
                       "per group (user + manager)" % acls)


def admin_reads_vehicles(env):
    ids = env.call("librefleet.vehicle", "search", [])
    assert ids, "admin got an empty vehicle list; are the ch09 vehicles still there?"


def service_type_fields_typed(env):
    fields = {f["name"]: f for f in env.call(
        "ir.model.fields", "search_read",
        [("model", "=", "librefleet.service.type")],
        fields=["name", "ttype", "required"])}
    assert fields, "no model 'librefleet.service.type' registered in this database"
    for name, ttype in {"name": "char", "flat_fee": "float", "default_duration_h": "float"}.items():
        assert name in fields, "field %r is missing on librefleet.service.type" % name
        assert fields[name]["ttype"] == ttype, (
            "field %r is %r, expected %r" % (name, fields[name]["ttype"], ttype))
    assert fields["name"]["required"], "service type 'name' is not required=True"


def service_type_acls_exist(env):
    acls = env.call("ir.model.access", "search_count",
                    [("model_id.model", "=", "librefleet.service.type")])
    assert acls >= 2, ("found %d access rules for librefleet.service.type, "
                       "expected one per group" % acls)


def vehicle_action_exists(env):
    res = env.call("ir.model.data", "check_object_reference",
                   "librefleet", "action_librefleet_vehicle")
    assert res[0] == "ir.actions.act_window", "librefleet.action_librefleet_vehicle is not a window action"
    act = env.call("ir.actions.act_window", "read", [res[1]], ["res_model", "view_mode"])[0]
    assert act["res_model"] == "librefleet.vehicle", "the action's res_model is %r" % act["res_model"]
    assert act["view_mode"] == "list,form", "view_mode is %r, expected 'list,form'" % act["view_mode"]


def root_menu_exists(env):
    res = env.call("ir.model.data", "check_object_reference",
                   "librefleet", "menu_librefleet_root")
    assert res[0] == "ir.ui.menu", "librefleet.menu_librefleet_root is not a menu"


def vehicle_views_exist(env):
    views = env.call("ir.ui.view", "search_read",
                     [("model", "=", "librefleet.vehicle")], fields=["type"])
    types = {v["type"] for v in views}
    assert "list" in types, "no list view defined for librefleet.vehicle (remember: <list>, not <tree>)"
    assert "form" in types, "no form view defined for librefleet.vehicle"


def config_menu_manager_only(env):
    res = env.call("ir.model.data", "check_object_reference",
                   "librefleet", "menu_librefleet_config")
    menu = env.call("ir.ui.menu", "read", [res[1]], ["group_ids"])[0]
    mgr = env.call("ir.model.data", "check_object_reference",
                   "librefleet", "group_librefleet_manager")[1]
    assert mgr in menu["group_ids"], "the Configuration menu is not restricted to Workshop / Manager"


def technician_exists_in_group(env):
    users = env.call("res.users", "search_read",
                     [("login", "=", "tina")], fields=["group_ids"])
    assert users, "no user with login 'tina'"
    gid = env.call("ir.model.data", "check_object_reference", "librefleet", "group_librefleet_user")[1]
    assert gid in users[0]["group_ids"], "'tina' is not in the Workshop / User group"


def _model_fields(env, model):
    fields = {f["name"]: f for f in env.call(
        "ir.model.fields", "search_read", [("model", "=", model)],
        fields=["name", "ttype", "required", "relation", "relation_field"])}
    assert fields, "no model %r registered in this database" % model
    return fields


def _expect_field(fields, model, name, ttype, relation=None, required=None):
    assert name in fields, "field %r is missing on %s" % (name, model)
    f = fields[name]
    assert f["ttype"] == ttype, "%s.%s is %r, expected %r" % (model, name, f["ttype"], ttype)
    if relation:
        assert f["relation"] == relation, (
            "%s.%s points at %r, expected %r" % (model, name, f["relation"], relation))
    if required is not None:
        assert f["required"] == required, (
            "%s.%s required is %r, expected %r" % (model, name, f["required"], required))


def vehicle_relations(env):
    f = _model_fields(env, "librefleet.vehicle")
    _expect_field(f, "librefleet.vehicle", "owner_id", "many2one", "res.partner")
    _expect_field(f, "librefleet.vehicle", "service_order_ids", "one2many", "librefleet.service.order")
    assert f["service_order_ids"]["relation_field"] == "vehicle_id", (
        "service_order_ids must be the inverse of librefleet.service.order.vehicle_id")


def order_model_shape(env):
    m = "librefleet.service.order"
    f = _model_fields(env, m)
    _expect_field(f, m, "vehicle_id", "many2one", "librefleet.vehicle", required=True)
    _expect_field(f, m, "service_type_id", "many2one", "librefleet.service.type")
    _expect_field(f, m, "technician_ids", "many2many", "res.users")
    _expect_field(f, m, "line_ids", "one2many", "librefleet.service.order.line")
    _expect_field(f, m, "stage", "selection")
    _expect_field(f, m, "scheduled_start", "datetime")
    _expect_field(f, m, "scheduled_end", "datetime")


def part_and_line_shape(env):
    f = _model_fields(env, "librefleet.part")
    for name, ttype in [("name", "char"), ("code", "char"),
                        ("standard_cost", "float"), ("list_price", "float")]:
        _expect_field(f, "librefleet.part", name, ttype)
    m = "librefleet.service.order.line"
    f = _model_fields(env, m)
    _expect_field(f, m, "order_id", "many2one", "librefleet.service.order", required=True)
    _expect_field(f, m, "part_id", "many2one", "librefleet.part")
    _expect_field(f, m, "qty", "float")
    _expect_field(f, m, "price_unit", "float")


def new_models_have_acls(env):
    for model in ("librefleet.service.order", "librefleet.service.order.line", "librefleet.part"):
        n = env.call("ir.model.access", "search_count", [("model_id.model", "=", model)])
        assert n >= 2, "found %d access rules for %s, expected one per group" % (n, model)


def order_record_rules(env):
    rules = env.call("ir.rule", "search_count",
                     [("model_id.model", "=", "librefleet.service.order")])
    assert rules >= 2, ("found %d record rules on service orders, expected the "
                        "technician rule AND the manager all-access rule" % rules)


def technician_rule_enforced(env):
    tina_env = Env(env.url, env.db, "tina", "technician")
    tina_env.login()
    uid = tina_env.uid
    mine = tina_env.call("librefleet.service.order", "search",
                         [("technician_ids", "in", [uid])])
    others = tina_env.call("librefleet.service.order", "search",
                           [("technician_ids", "not in", [uid])])
    assert mine, "no service order assigned to tina; create the ch12 demo orders"
    assert others, "no service order WITHOUT tina; create the ch12 demo orders"
    tina_env.call("librefleet.service.order", "write", mine[:1], {"stage": "confirmed"})
    tina_env.call("librefleet.service.order", "write", mine[:1], {"stage": "draft"})
    try:
        tina_env.call("librefleet.service.order", "write", others[:1], {"stage": "confirmed"})
    except xmlrpc.client.Fault:
        return
    raise AssertionError("tina could write a service order she is not assigned to; "
                         "is the technician record rule active?")


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
    "ch08": [
        ("module librefleet is installed", librefleet_installed,
         "Is code/addons/librefleet in place with __manifest__.py and __init__.py? "
         "Install it: docker compose exec odoo odoo -c /etc/odoo/odoo.conf "
         "-d tutorial -i librefleet --stop-after-init"),
        ("manifest version is 19.0.x.y.z", librefleet_version_ok,
         "Set \"version\": \"19.0.1.0.0\" in __manifest__.py (Odoo major first, "
         "then your module's own version), then upgrade with -u librefleet."),
        ("LibreFleet is an app", librefleet_is_app,
         "Set \"application\": True in __manifest__.py and upgrade, so LibreFleet "
         "appears on the Apps home screen."),
    ],
    "ch09": [
        ("model librefleet.vehicle is registered", vehicle_model_exists,
         "Did you create models/vehicle.py with _name = 'librefleet.vehicle', "
         "import it from models/__init__.py AND the top-level __init__.py, then "
         "upgrade? New Python code needs -u librefleet --stop-after-init."),
        ("vehicle fields have the right types", vehicle_fields_typed,
         "Compare your field definitions with the chapter: license_plate/vin/"
         "model_name are Char, year is Integer, mileage_km is Float, notes is "
         "Text, active is Boolean. Upgrade after every change."),
        ("license_plate is required", vehicle_plate_required,
         "Add required=True to the license_plate field and upgrade."),
    ],
    "ch10": [
        ("Workshop User and Manager groups exist", workshop_groups_exist,
         "Define both res.groups records in security/librefleet_security.xml with "
         "ids group_librefleet_user and group_librefleet_manager, list the file in "
         "the manifest's data, and upgrade."),
        ("librefleet.vehicle has access rules", vehicle_acls_exist,
         "Add security/ir.model.access.csv with one line per group and list it in "
         "the manifest AFTER the security XML (the CSV references the groups)."),
        ("admin can read vehicles over XML-RPC", admin_reads_vehicles,
         "This failed in ch09 by design. It passes once the ACLs exist and admin "
         "is in the Workshop / Manager group (the users field on the group record)."),
        ("technician user 'tina' exists in Workshop / User", technician_exists_in_group,
         "Create the user from odoo shell as in the hands-on (login 'tina', "
         "group_ids includes librefleet.group_librefleet_user) and env.cr.commit()."),
    ],
    "ch11": [
        ("librefleet.service.type model with the right fields", service_type_fields_typed,
         "Create models/service_type.py (name Char required, flat_fee Float, "
         "default_duration_h Float), import it in models/__init__.py, upgrade."),
        ("service types have access rules", service_type_acls_exist,
         "Every new model needs its own lines in security/ir.model.access.csv "
         "(user read-only, manager full), or it stays invisible like ch09's vehicle."),
        ("vehicle window action exists with view_mode list,form", vehicle_action_exists,
         "Define ir.actions.act_window with id action_librefleet_vehicle, "
         "res_model librefleet.vehicle and view_mode list,form in views/vehicle_views.xml."),
        ("LibreFleet root menu exists", root_menu_exists,
         "Add <menuitem id=\"menu_librefleet_root\" .../> in views/librefleet_menus.xml "
         "and list the file in the manifest (after the views it references)."),
        ("vehicle list and form views defined", vehicle_views_exist,
         "Add both <list> and <form> views for librefleet.vehicle in "
         "views/vehicle_views.xml. On Odoo 19 the list tag is <list>, not <tree>."),
        ("Configuration menu is manager-only", config_menu_manager_only,
         "Put groups=\"group_librefleet_manager\" on the Configuration <menuitem> "
         "(id menu_librefleet_config) so technicians don't see it."),
    ],
    "ch12": [
        ("vehicle has owner_id and service_order_ids", vehicle_relations,
         "owner_id is Many2one('res.partner'); service_order_ids is "
         "One2many('librefleet.service.order', 'vehicle_id'), the inverse of the "
         "order's vehicle_id."),
        ("service order model has the right shape", order_model_shape,
         "Check models/service_order.py against the chapter: vehicle_id required "
         "Many2one, service_type_id Many2one, technician_ids Many2many to "
         "res.users, line_ids One2many, stage Selection, scheduled_start/end "
         "Datetime. Upgrade after each change."),
        ("part and order line models have the right shape", part_and_line_shape,
         "librefleet.part: name/code Char, standard_cost/list_price Float. "
         "Order line: order_id required Many2one, part_id Many2one, qty and "
         "price_unit Float."),
        ("the three new models have access rules", new_models_have_acls,
         "Every model needs its lines in security/ir.model.access.csv, one per "
         "group, or it is invisible (chapter 9 taught you how that looks)."),
        ("service orders have record rules", order_record_rules,
         "Two ir.rule records in security/librefleet_security.xml: the technician "
         "write-own-orders rule for Workshop / User AND the [(1,'=',1)] rule for "
         "Workshop / Manager (without it, managers get caught by the user rule)."),
        ("technicians can only write their own orders", technician_rule_enforced,
         "Log tina's work: she must be in technician_ids of at least one demo "
         "order and absent from another. Writing hers succeeds, writing the other "
         "must raise AccessError. Check the rule's domain and perm_write."),
    ],
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
