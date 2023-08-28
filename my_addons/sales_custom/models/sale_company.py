from odoo import fields, models


class ResCompanySale(models.Model):
    _inherit = 'res.company'

    test_company_days = fields.Integer(
        string='Test company days'
    )
    use_company_days = fields.Boolean(
        default=False
    )
