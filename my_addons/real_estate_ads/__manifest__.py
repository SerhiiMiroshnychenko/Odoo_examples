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
    "depends": ["base"],
    "data": [

        'security/ir.model.access.csv',
        'security/res_groups.xml',

        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/property_offer_view.xml',
        'views/property_view.xml',
        'views/menu_items.xml',

        # Data files
        'data/property_type.xml',
        'data/real.property.type.csv',

    ],
    "demo": [
        'demo/property_tag.xml',
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}