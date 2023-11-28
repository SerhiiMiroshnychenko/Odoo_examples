{
    'name': 'Search Panel Tooltip',
    'version': '16.0.1.0.0',
    'description': 'Search Panel Customization',
    'author': 'Serhii Miroshnychenko',
    'website': 'https://github.com/SerhiiMiroshnychenko/Odoo_examples',
    'license': 'AGPL-3',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'search_panel_tooltip/static/src/search_panel/search_panel.js',
            'search_panel_tooltip/static/src/search_panel/search_panel.xml',
        ]},
    'installable': True,
    'auto_install': False
}
