from odoo import fields, models


class FishFish(models.Model):
    _name = 'fish.fish'
    _description = 'Fish model'

    common_name = fields.Char(required=True)
    scientific_name = fields.Char()
    average_size = fields.Integer(string='Average size, mm')
    image = fields.Image()
    remarks = fields.Html()
