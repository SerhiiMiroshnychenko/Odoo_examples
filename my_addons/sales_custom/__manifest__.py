{
    'name': "Sales custom",
    'version': '16.1.1',
    'depends': [
        'sale'
    ],
    'author': "Author Name",
    'category': '',
    'description': """
    Custom sales module
    """,
    # data files always loaded at installation
    'data': [
            'security/ir.model.access.csv',
            'security/res_groups.xml',

            "wizard/custom_sale_note.xml",
            'wizard/custom_sale_qty.xml',

            'views/res_config_settings_view.xml',
            "views/custom_sale_order_view.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
