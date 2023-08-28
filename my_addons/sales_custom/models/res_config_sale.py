from odoo import models, fields


class ResConfigSale(models.TransientModel):
    _inherit = 'res.config.settings'

    default_manager = fields.Many2one(
        'res.users',
        'Base manager',
        default=lambda self: self.env.uid,
        default_model='sale.order'
    )

    # Groups
    group_hide_custom_buttons = fields.Boolean(
        string="Allow custom",
        implied_group='sales_custom.group_hide_custom_buttons'
    )

    # Company setup
    test_company_days = fields.Integer(
        related='company_id.test_company_days',
        string="Default Test Company days",
        readonly=False)
    use_company_days = fields.Boolean(
        "Company test field",
        related='company_id.use_company_days',
        readonly=False
    )

    # Config parameter
    allow_view_notebook = fields.Boolean(
        string='Full order info',
        config_parameter='sale_custom.allow_view_notebook',
    )
