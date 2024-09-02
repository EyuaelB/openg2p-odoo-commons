# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
{
    "name": "OpenG2P Superset Dashboard",
    "category": "G2P",
    "version": "17.0.1.2.0",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://openg2p.org",
    "license": "Other OSI approved licence",
    "depends": ["base"],
    "external_dependencies": {},
    "data": ["views/res_config_settings.xml", "views/superset_dashboard.xml"],
    "assets": {
        "web.assets_backend": [
            "g2p_superset_dashboard/static/src/components/**/*.js",
            "g2p_superset_dashboard/static/src/components/**/*.xml",
            "g2p_superset_dashboard/static/src/components/**/*.css",
            "g2p_superset_dashboard/static/src/components/**/*.scss",
        ],
    },
}
