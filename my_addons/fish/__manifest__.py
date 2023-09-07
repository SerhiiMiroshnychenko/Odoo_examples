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
        'website'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fish_views.xml',
        'views/fish_templates.xml',
    ],
    'demo': [
            'demo/demo.xml',
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
}