# LibreFleet: the Zero to Odoo Expert capstone.
# Built chapter by chapter; this file is the ch10 state.
{
    "name": "LibreFleet",
    "summary": "Vehicle workshop & service booking management",
    "version": "19.0.1.2.0",
    "category": "Services",
    "author": "Zero to Odoo Expert readers",
    "website": "https://ronitjadhav.github.io/odoo-tutorial/",
    "license": "AGPL-3",
    "application": True,
    "depends": ["base"],
    "data": [
        "security/librefleet_security.xml",
        "security/ir.model.access.csv",
    ],

}
