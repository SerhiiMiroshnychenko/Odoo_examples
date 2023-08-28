{
    'name': "Project customization",
    'version': '16.1.1',
    'depends': [
        'project',
    ],
    'author': "Author Name",
    'category': '',
    # data files always loaded at installation
    'data': [
        'data/ir_sequence.xml',
        'views/project_task_view.xml',
        'views/res_config_settings_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'pre_init_hook': 'pre_install_func'
}
