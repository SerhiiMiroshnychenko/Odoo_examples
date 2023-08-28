import logging
from datetime import timedelta
from odoo import api, SUPERUSER_ID
_logger = logging.getLogger()


def pre_install_func(cr):
    """
    Fills in the date_deadline fields for all models
    that do not have this field, or it is less than
    days of the create_date field
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    tasks = env['project.task'].search([])

    for task in tasks:
        if not task.date_deadline or task.date_deadline < task.create_date.date():
            _logger.info(f'Create day: {task.create_date.date()} Old deadline: {task.date_deadline}')
            task.write({'date_deadline': task.create_date.date() + timedelta(days=5)})
            _logger.info(f'New deadline: {task.date_deadline}')
