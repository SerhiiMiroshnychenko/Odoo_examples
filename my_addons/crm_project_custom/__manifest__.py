{
    'name': "CRM and Project customization",
    'author': "Serhii Miroshnychenko",
    'category': 'CRM',
    'version': '16.0.1.0.0',
    'depends': ['crm', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'wizard/create_task_views.xml',
        'data/ir_actions_server.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
