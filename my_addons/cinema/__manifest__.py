{
    'name': "Cinema module",
    'version': '16.0.16.1.9',
    'depends': [
        'base',
        'mail'
    ],
    'author': "Author Name",
    'category': '',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'data/cinema_movie_demo_data.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings_view.xml',

        'wizard/cinema_note_views.xml',
        'wizard/cinema_close_views.xml',
        'wizard/hall_seat_views.xml',
        'wizard/cinema_hall_views.xml',
        'wizard/cinema_repair_views.xml',

        'views/cinema_cinema_hall_views.xml',
        'views/cinema_cinema_movie_views.xml',
        'views/cinema_cinema_repair.xml',
        'views/cinema_cinema_views.xml',

        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'data/ir_actions_server.xml',

        'report/cinema_cinema_report.xml',
        'report/report_cinema.xml'

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
