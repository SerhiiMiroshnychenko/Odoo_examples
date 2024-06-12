# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class Saleorder(models.Model):
    _inherit = 'sale.order'

    is_reorder = fields.Boolean('Is Reorder')

    def def_reorder_sale(self):
        new_order = self.copy(default={
            'name': self.env['ir.sequence'].next_by_code('sale.order') or '/',
            'is_reorder': True,            
            'order_line': False,
        })
        for line in self.order_line:
            line.copy(default={
                'order_id': new_order.id,
            })
        return {
            'name': 'Reorder',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': new_order.id,
            'target': 'new',
        }