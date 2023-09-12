# -*- coding: utf-8 -*-
{
    'name': 'Hospital Management System',
    'version': '16.0.1.0.0',
    'summary': 'Odoo 16 Hospital Management System',
    'sequence': -100,
    'description': """
Clinic Administration Software
==============================
An Odoo module for automation of hospital system management
""",
    'category': 'Uncategorized',
    'author': 'Serhii Miroshnychenko',
    'website': 'https://github.com/SerhiiMiroshnychenko/Odoo_examples/tree/main/my_addons/om_hospital',
    'depends': ['mail', 'estate'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
