{
    'name': 'Hospital Management System',
    'author': 'Serhii Miroshnychenko',
    'website': 'https://github.com/SerhiiMiroshnychenko',
    'summary': 'Odoo 16 Hospital Management System',
    'depends': ['mail', 'estate'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/menu.xml',
    ]
}