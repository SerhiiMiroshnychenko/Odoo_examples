{
    "name": "Real Estate Ads",
    "version": "16.0.1.0.0",
    "website": "https://github.com/SerhiiMiroshnychenko/Odoo_examples/tree/main/my_addons/real_estate_ads",
    "author": "Serhii Miroshnychenko",
    "summary": "Real estate module to show available properties",
    "sequence": -101,
    "description": """
Real estate module to show available properties
    """,
    "category": "Sales",
    "depends": [],
    "data": [
        'security/ir.model.access.csv',
        'views/property_view.xml',
        'views/menu_items.xml',

    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}