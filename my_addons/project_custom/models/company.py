from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    project_use_task_limit = fields.Boolean(
        string="Task Days Limit", readonly=False,
        default=False,
        help="Enable the use of a limit of days for the task.")
