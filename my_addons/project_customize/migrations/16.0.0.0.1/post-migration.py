import logging
from odoo import api, SUPERUSER_ID
_logger = logging.getLogger()


def migrate(cr, version):
    """
    Adds a code field to all tasks
    in the sequence of their creation date
    """
    _logger.info('Start of migration!')
    env = api.Environment(cr, SUPERUSER_ID, {})
    tasks = env['project.task'].search([], order='create_date')

    sequence = env['ir.sequence'].next_by_code('code')
    for task in tasks:
        task.write({'code': sequence})
        _logger.info(f'Task name: {task.name} --- Created: {task.create_date} --- Code: {task.code}')
        sequence = env['ir.sequence'].next_by_code('code')

# def migrate(cr, version):
#     env = api.Environment(cr, SUPERUSER_ID, {})
#     tasks = env['project.task'].search([('code', '=', False)])
#     _logger.info('Post-migration: set codes for project_task')
#     for task in tasks:
#         next_code = env['ir.sequence'].next_by_code('project.task')
#         cr.execute("update project_task set code = %s where id = %s",
#                    [next_code, task.id])
