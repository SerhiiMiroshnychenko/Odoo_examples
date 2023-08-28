from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    task_limit = fields.Integer(
        string='Task Days Limit',
        default=30,
        config_parameter='project_custom.days_limit',
    )

    project_use_task_limit = fields.Boolean(
        string="Task Days Limit", readonly=False,
        related="company_id.project_use_task_limit",
        help="Enable the use of a limit of days for the task.")

    @api.model
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('project_custom.days_limit', str(self.task_limit))
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            task_limit=ICPSudo.get_param('project_custom.days_limit'),
        )
        return res
