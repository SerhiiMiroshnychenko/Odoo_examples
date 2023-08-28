# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class tips_and_tricks(models.Model):
#     _name = 'tips_and_tricks.tips_and_tricks'
#     _description = 'tips_and_tricks.tips_and_tricks'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
from odoo import fields, models


class TipsTricks(models.Model):
    _name = 'tips.tricks'

    name = fields.Char()
    number = fields.Integer()
    float_no = fields.Float(string='Float Number')
    document = fields.Binary()
    true = fields.Boolean(string='True?')
    image = fields.Image()
    date = fields.Date()
    date_time = fields.Datetime()
    yes_no = fields.Selection(
        string='Yes or No',
        selection=[
            ('yes', 'Yes'),
            ('no', 'No'),
        ],)
    product_id = fields.Many2one(comodel_name='product.product')
    product_ids = fields.Many2many(comodel_name='product.product')
    tips_tricks_line_ids = fields.One2many(
        comodel_name='tips.tricks.line',
        inverse_name='tips_id',
    )
    tips_tricks_tag_ids = fields.Many2many(
        comodel_name='tips.tricks.tag',
    )
    price = fields.Monetary()
    currency_id = fields.Many2one(comodel_name='res.currency')


class TipsTricksLine(models.Model):
    _name = 'tips.tricks.line'

    line_name = fields.Char()
    tips_id = fields.Many2one('tips.tricks')


class TipsTricksTag(models.Model):
    _name = 'tips.tricks.tag'
    _rec_name = 'tag_name'

    tag_name = fields.Char()
    tip_ids = fields.Many2many('tips.tricks')
