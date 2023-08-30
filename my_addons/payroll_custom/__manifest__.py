{
    'name': 'Payroll Custom',
    'version': '16.0.0.0.0',
    'author': 'Serhii Miroshnychenko',
    'depends': [
        'base',
        'hr',
        'hr_timesheet',
        'hr_hourly_cost',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/payroll_payroll_views.xml',
        'views/payroll_list_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
