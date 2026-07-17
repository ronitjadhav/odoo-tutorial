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


def _close(a, b):
    return abs(a - b) < 0.005


def line_subtotal_computed(env):
    f = _model_fields(env, "librefleet.service.order.line")
    _expect_field(f, "librefleet.service.order.line", "subtotal", "float")
    lines = env.call("librefleet.service.order.line", "search_read", [],
                     fields=["qty", "price_unit", "subtotal"])
    assert lines, "no order lines in the database; keep the ch12 demo data around"
    for l in lines:
        assert _close(l["subtotal"], l["qty"] * l["price_unit"]), (
            "line %d: subtotal %s != qty %s * price_unit %s"
            % (l["id"], l["subtotal"], l["qty"], l["price_unit"]))


def order_totals_computed(env):
    orders = env.call("librefleet.service.order", "search_read", [],
                      fields=["parts_total", "labor_total", "margin",
                              "service_type_id", "line_ids"])
    assert orders, "no service orders in the database"
    for o in orders:
        lines = env.call("librefleet.service.order.line", "search_read",
                         [("order_id", "=", o["id"])],
                         fields=["subtotal", "qty", "part_id"])
        parts = sum(l["subtotal"] for l in lines)
        assert _close(o["parts_total"], parts), (
            "order %d: parts_total %s, expected %s (sum of line subtotals)"
            % (o["id"], o["parts_total"], parts))
        fee = 0.0
        if o["service_type_id"]:
            fee = env.call("librefleet.service.type", "read",
                           [o["service_type_id"][0]], ["flat_fee"])[0]["flat_fee"]
        assert _close(o["labor_total"], fee), (
            "order %d: labor_total %s, expected the service type's flat fee %s"
            % (o["id"], o["labor_total"], fee))
        cost = 0.0
        for l in lines:
            if l["part_id"]:
                std = env.call("librefleet.part", "read",
                               [l["part_id"][0]], ["standard_cost"])[0]["standard_cost"]
                cost += l["qty"] * std
        assert _close(o["margin"], parts + fee - cost), (
            "order %d: margin %s, expected parts+labor-cost = %s"
            % (o["id"], o["margin"], parts + fee - cost))


def customer_follows_owner(env):
    f = _model_fields(env, "librefleet.service.order")
    _expect_field(f, "librefleet.service.order", "customer_id", "many2one", "res.partner")
    stored = env.call("ir.model.fields", "search_read",
                      [("model", "=", "librefleet.service.order"), ("name", "=", "customer_id")],
                      fields=["store", "related"])[0]
    assert stored["related"] == "vehicle_id.owner_id", (
        "customer_id related is %r, expected 'vehicle_id.owner_id'" % stored["related"])
    assert stored["store"], "customer_id must be stored (store=True) per the blueprint"
    orders = env.call("librefleet.service.order", "search_read", [],
                      fields=["customer_id", "vehicle_id"])
    for o in orders:
        owner = env.call("librefleet.vehicle", "read",
                         [o["vehicle_id"][0]], ["owner_id"])[0]["owner_id"]
        assert (o["customer_id"] or False) == (owner or False) or \
               (o["customer_id"] and owner and o["customer_id"][0] == owner[0]), (
            "order %d: customer_id %s but the vehicle's owner is %s"
            % (o["id"], o["customer_id"], owner))


def totals_not_stored(env):
    rows = env.call("ir.model.fields", "search_read",
                    [("model", "=", "librefleet.service.order"),
                     ("name", "in", ["parts_total", "labor_total", "margin"])],
                    fields=["name", "store"])
    assert len(rows) == 3, "parts_total, labor_total and margin must all exist"
    for r in rows:
        assert not r["store"], ("%s is stored; the chapter keeps the order totals "
                                "non-stored (compare with line subtotal)" % r["name"])


def vehicle_service_count(env):
    vehicles = env.call("librefleet.vehicle", "search_read", [],
                        fields=["service_count"])
    assert vehicles, "no vehicles in the database"
    for v in vehicles:
        n = env.call("librefleet.service.order", "search_count",
                     [("vehicle_id", "=", v["id"])])
        assert v["service_count"] == n, (
            "vehicle %d: service_count is %s but it has %d orders"
            % (v["id"], v["service_count"], n))


def _expect_fault(fn, msg):
    """Assert that an RPC call is refused by the server (constraint fired)."""
    try:
        fn()
    except xmlrpc.client.Fault:
        return
    raise AssertionError(msg)


def vehicle_plate_unique(env):
    cons = env.call("ir.model.constraint", "search_read",
                    [("model.model", "=", "librefleet.vehicle"), ("type", "=", "u")],
                    fields=["definition"])
    assert any("license_plate" in (c.get("definition") or "") for c in cons), (
        "no UNIQUE database constraint covering license_plate on librefleet.vehicle")


def vehicle_year_constrained(env):
    _expect_fault(
        lambda: env.call("librefleet.vehicle", "create",
                         {"license_plate": "ODOOLINGS-YR", "year": 1850}),
        "a vehicle with model year 1850 was accepted; the @api.constrains on year is "
        "missing or too loose")


def order_reference_from_sequence(env):
    assert env.call("ir.sequence", "search_count",
                    [("code", "=", "librefleet.service.order")]), \
        "no ir.sequence with code 'librefleet.service.order' (check data/ir_sequence.xml)"
    orders = env.call("librefleet.service.order", "search_read", [],
                      fields=["reference"])
    assert orders, "no service orders in the database"
    for o in orders:
        ref = o["reference"]
        assert ref and ref != "New", (
            "order %d still has reference %r; backfill legacy orders from the sequence"
            % (o["id"], ref))


def order_no_overlap(env):
    booked = env.call("librefleet.service.order", "search_read",
                      [("scheduled_start", "!=", False),
                       ("scheduled_end", "!=", False),
                       ("stage", "!=", "cancelled")],
                      fields=["vehicle_id", "scheduled_start", "scheduled_end"],
                      limit=1)
    assert booked, "need one scheduled, non-cancelled order to test overlap; keep the demo data"
    b = booked[0]
    _expect_fault(
        lambda: env.call("librefleet.service.order", "create",
                         {"vehicle_id": b["vehicle_id"][0],
                          "scheduled_start": b["scheduled_start"],
                          "scheduled_end": b["scheduled_end"]}),
        "a booking overlapping an existing one on the same vehicle was accepted; "
        "the @api.constrains overlap check is missing")


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
    "ch13": [
        ("line subtotals are computed and stored", line_subtotal_computed,
         "subtotal = fields.Float(compute='_compute_subtotal', store=True) with "
         "@api.depends('qty', 'price_unit'). Did you upgrade after adding it?"),
        ("order totals add up (parts, labor, margin)", order_totals_computed,
         "parts_total sums line subtotals, labor_total mirrors the service type's "
         "flat_fee, margin = parts + labor - what the parts cost you. Check your "
         "@api.depends paths: dotted ones like 'line_ids.subtotal' are allowed "
         "and required."),
        ("order totals are NOT stored", totals_not_stored,
         "Leave store off the three order totals: they are cheap to compute and "
         "this chapter wants you to see the difference in psql."),
        ("customer_id is a stored related field that follows the owner",
         customer_follows_owner,
         "customer_id = fields.Many2one(related='vehicle_id.owner_id', "
         "store=True). Stored related fields update automatically when the "
         "source changes; if yours lags, check the related= path."),
        ("vehicle.service_count matches reality", vehicle_service_count,
         "service_count is a non-stored computed Integer: for each record, "
         "len(rec.service_order_ids). Remember to loop over self in the compute."),
    ],
    "ch14": [
        ("license_plate has a UNIQUE database constraint", vehicle_plate_unique,
         "Add _license_plate_unique = models.Constraint('unique(license_plate)', "
         "'...') on librefleet.vehicle (Odoo 19 replaced _sql_constraints with "
         "models.Constraint). Upgrade after adding it."),
        ("vehicle rejects an out-of-range model year", vehicle_year_constrained,
         "Add an @api.constrains('year') method that raises ValidationError when "
         "year is outside a sane range (e.g. 1900..next year). Constrains run in "
         "Python on create/write, so they fire over RPC too."),
        ("service orders get a reference from the sequence", order_reference_from_sequence,
         "Define the ir.sequence (data/ir_sequence.xml, code "
         "'librefleet.service.order') and give reference a default that calls "
         "next_by_code. Backfill any legacy orders still reading 'New'."),
        ("overlapping bookings on the same vehicle are refused", order_no_overlap,
         "Add an @api.constrains('scheduled_start','scheduled_end','vehicle_id') "
         "that searches for another non-cancelled order on the same vehicle whose "
         "window overlaps (start < other_end AND end > other_start)."),
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
