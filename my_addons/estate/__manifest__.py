{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Real estate advertising module',
    'description': """
    A simple real estate advertising module was created for educational purposes
    """,
    'depends': ['base'],
    'author': 'Serhii Miroshnychenko',
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_tree.xml',
        'views/estate_property_form.xml',
        'views/estate_property_kanban.xml',
        'views/estate_property_search.xml',
        'views/estate_property_tag_tree.xml',
        'views/estate_property_type_tree.xml',
        'views/estate_property_type_form.xml',
        'views/estate_property_offer_tree.xml',
        'views/estate_property_offer_form.xml',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}