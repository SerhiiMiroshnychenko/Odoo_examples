from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    project_use_deadline_delta_days = fields.Boolean(
        string="Task Days Limit", readonly=False,
        default=False,
        help="Enable the use of a limit of days for the task")

    project_use_deadline_over_tag = fields.Boolean(
        string="Tag For Overdue Tasks", readonly=False,
        default=False,
        help="Enable the use of a tag for overdue tasks")
