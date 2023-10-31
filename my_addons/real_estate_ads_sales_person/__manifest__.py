{
    'name': 'Real Estate Ads - Sales Person',
    'version': '16.0.0.0.0',
    'summary': 'Real Estate Ads - Sales Person',
    'description': '''
        Show real estate properties linked to a sales person
     ''',
    'category': 'Sales',
    
    'author': 'Serhii Miroshnychenko',
    'website': 'https://github.com/SerhiiMiroshnychenko/Odoo_examples',
    'license': 'LGPL-3',
    
    'depends': [
        'real_estate_ads',
        'base'
    ],
    'data': [
       'views/res_users.xml',
    ],
    # 'demo': [
    #     'demo/document_page.xml'
    # ],
    #'assets': {
    #    '':[
    #        ''
    #    ]
    #}
    'installable': True,
    'application': False,
    'auto_install': False,
}