from odoo import models, fields


class SaleCustom(models.Model):
    _inherit = 'sale.order'
    manager = fields.Many2one(
        'res.users'
    )
    products_type_quantity = fields.Integer(
        string='Products quantity',
        compute='_compute_pruducts_quantity'
    )
    manager_note = fields.Char(string='Manager note')

    full_view = fields.Boolean(
        compute='_compute_full_order_view'
    )

    def _compute_pruducts_quantity(self):
        self.products_type_quantity = self.order_line.search_count([('order_id', '=', self.id)])

    def _compute_full_order_view(self):
        self.full_view = self.env['ir.config_parameter'].sudo().get_param(
            'sale_custom.allow_view_notebook', False)
