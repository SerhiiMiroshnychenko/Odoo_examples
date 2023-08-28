{
    'name': "Project customization",
    'version': '16.0.0.0.1',
    'depends': ['project',],
    'author': "Serhii Miroshnychenko",
    'category': 'Services/Project',
    'data': [
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'views/project_task_view.xml',
        'views/res_config_settings_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
