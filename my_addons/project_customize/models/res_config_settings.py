from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deadline_delta_days = fields.Integer(
        string='Deadline delta days',
        config_parameter='project_customize.deadline_delta_days',
    )

    project_use_deadline_delta_days = fields.Boolean(
        string="Set deadline delta days", readonly=False,
        related="company_id.project_use_deadline_delta_days",
        help="Enable the set of a deadline delta days for the task."
    )

    deadline_over_tag = fields.Many2one(
        comodel_name='project.tags',
        string="Overdue Task Tag",
        config_parameter='project_customize.deadline_over_tag')

    project_use_deadline_over_tag = fields.Boolean(
        string="Use a tag for overdue tasks", readonly=False,
        related="company_id.project_use_deadline_over_tag",
        help="Enable the use of a a tag for overdue tasks")
