from odoo import api, fields, models


class Property(models.Model):
    _name = 'real.property'
    _description = 'Real Estate Property Model'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string='Available From')
    expected_price = fields.Float()
    best_offer = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
    )
