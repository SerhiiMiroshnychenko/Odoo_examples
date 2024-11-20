################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2024 Serhii Miroshnychenko (https://github.com/SerhiiMiroshnychenko).
#
################################################################################

{
    'name': 'Product Analysis',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Product stock analysis tools',
    'description': """
        Module for analyzing product metrics including stock history.
    """,
    'author': "Serhii Miroshnychenko",
    'website': "https://github.com/SerhiiMiroshnychenko",
    'depends': ['product', 'stock', 'web_widget_plotly_chart'],
    'data': [
        'views/product_views.xml',
    ],
    "assets": {
        "web.assets_frontend": [],
        "web.assets_backend": [
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'external_dependencies': {
        "python": ["plotly==5.13.1"],
    },
}
