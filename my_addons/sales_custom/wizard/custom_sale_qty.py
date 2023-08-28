from odoo import models, fields
from odoo.exceptions import ValidationError


class CustomSaleQty(models.TransientModel):
    _name = 'custom.sale.qty'

    products = fields.Many2many(
        'sale.order.line'
    )
    operation = fields.Selection(
        selection=[('increase', 'Increase'), ('reduce', 'Reduce')],
        default='increase'
    )
    value = fields.Float(
        default=0.00,
    )

    def change_qty(self):
        if not self.value:
            raise ValidationError('Empty value field')
        for product in self.products:
            if self.operation == 'increase':
                product.product_uom_qty += self.value
            else:
                product.product_uom_qty += self.value
