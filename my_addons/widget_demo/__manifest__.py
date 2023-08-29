# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

# flake8: noqa: E501

{
    'name': 'Odoo Widgets Demo',
    'version': '16.0.1.0.0',
    'category': 'Extra Tools',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz',
    'license': 'LGPL-3',
    'summary': 'Odoo Widgets Demo',
    'depends': [
        'base',
    ],
    'data': [
        'views/demo_widget_views.xml',
        'security/ir.model.access.csv',
    ],
    'external_dependencies': {
    },
    'support': 'support@garazd.biz',
    'application': True,
    'installable': True,
    'auto_install': False,
}
