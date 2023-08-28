from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    company_use_days_limit = fields.Boolean(
        string="Limit of movie showing days",
        readonly=False,
        default=False,
        help="Enable the use of a limit of movie showing days"
    )

    company_use_auto_description = fields.Boolean(
        string="Use Auto Description",
        readonly=False,
        default=False,
        help="Enable the use of a description of new movies"
    )
