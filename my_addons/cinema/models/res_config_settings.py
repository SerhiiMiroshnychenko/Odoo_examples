from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    days_limit = fields.Integer(
        string='Limit of movie showing days',
        default=30,
        config_parameter='cinema.days_limit',
    )

    company_use_days_limit = fields.Boolean(
        string="Task Days Limit", readonly=False,
        related="company_id.company_use_days_limit",
        help="Enable the use of a limit of movie showing days")

    auto_description = fields.Char(
        string="Auto Description",
        default=False,
        config_parameter='cinema.auto_description',
    )

    company_use_auto_description = fields.Boolean(
        string="Use Auto Description", readonly=False,
        related="company_id.company_use_auto_description",
        help="Enable the use of a description of new movies")

    @api.model
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('cinema.days_limit', str(self.days_limit))
        ICPSudo.set_param('cinema.auto_description', str(self.auto_description))
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            task_limit=ICPSudo.get_param('cinema.days_limit'),
            auto_description=ICPSudo.get_param('cinema.auto_description')
        )
        return res
