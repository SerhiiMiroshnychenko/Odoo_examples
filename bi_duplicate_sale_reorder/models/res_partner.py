# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_order_ids = fields.One2many('sale.order','partner_id',string='Sale Orders')
    reorder_count = fields.Integer(compute='_compute_reorder_order_count', string='Reorder')

    def _compute_reorder_order_count(self):
        count = self.env['sale.order'].search_count([('partner_id','=',self.id),('state','=','sale'),('is_reorder','=',True)])
        self.reorder_count = count

    def open_sale_from_view_action(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_orders")
        action['domain'] = [('partner_id','=',self.id),('state','=','sale'),('is_reorder','=',True)]
        return action