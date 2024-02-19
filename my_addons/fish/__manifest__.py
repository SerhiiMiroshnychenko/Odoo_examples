{
    'name': 'Fish',
    'version': '16.0.1.0.0',
    'summary': 'Fish',
    'description': '''
        Fish
     ''',

    'author': 'Serhii Miroshnychenko',
    'website': 'https://github.com/SerhiiMiroshnychenko',
    'license': 'LGPL-3',

    'depends': [
        'base',
        'website',
        'stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fish_info_views.xml',
        'views/fish_views.xml',
        'views/fish_templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'fish/static/src/xml/fish_templates.xml',
        ],
        'web.assets_backend': [
            'fish/static/src/css/fish_style.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
