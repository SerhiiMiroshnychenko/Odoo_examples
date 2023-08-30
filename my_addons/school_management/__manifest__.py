{
    'name': 'School Management',
    'version': '16.0.1.0.0',
    'summary': 'School Management Software',
    'description': '''
        Treating Schools
     ''',

    'author': 'Serhii Miroshnychenko',
    'website': 'https://github.com/SerhiiMiroshnychenko',
    'category': 'Tools',
    'license': 'LGPL-3',
    # 'post_init_hook': 'create_student',

    'depends': [
        'base',
        'contacts',
        'hr',
        'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/school.xml',
        'views/student_list_template.xml',
        'report/school_report.xml',
        'report/student_template.xml',
    ],

    # 'assets': {
    #    'web.assets_backend':[
    #        'school_management/static/src/js/test.js'
    #    ]
    # },
    'demo': [

    ],
    # 'images': ['static/description/icon/png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
