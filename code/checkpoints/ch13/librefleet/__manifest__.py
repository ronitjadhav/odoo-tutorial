# LibreFleet: the Zero to Odoo Expert capstone.
# Built chapter by chapter; this file is the ch13 state.
{
    "name": "LibreFleet",
    "summary": "Vehicle workshop & service booking management",
    "version": "19.0.1.5.0",
    "category": "Services",
    "author": "Zero to Odoo Expert readers",
    "website": "https://ronitjadhav.github.io/odoo-tutorial/",
    "license": "AGPL-3",
    "application": True,
    "depends": ["base"],
    "data": [
        "security/librefleet_security.xml",
        "security/ir.model.access.csv",
        "views/vehicle_views.xml",
        "views/service_type_views.xml",
        "views/service_order_views.xml",
        "views/part_views.xml",
        "views/librefleet_menus.xml",
    ],

}
