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
    type_id = fields.Many2one(
        comodel_name='real.property.type',
        string='Property Type',
        required=False,
    )
    tag_ids = fields.Many2many(
        comodel_name='real.property.tag',
        string='Property Tag'
    )
    offer_ids = fields.One2many(
        comodel_name='real.property.offer',
        inverse_name='property_id',
        string='Offers'
    )
    sales_id = fields.Many2one('res.users', string='Salesman')
    buyer_id = fields.Many2one('res.partner', required=False)

    total_area = fields.Integer()

    @api.onchange('living_area', 'garden_area')
    def _compute_total_area(self):
        self.total_area = self.living_area + self.garden_area


class PropertyType(models.Model):
    _name = 'real.property.type'
    _description = 'Property Type Model'

    name = fields.Char(required=True)


class PropertyTag(models.Model):
    _name = 'real.property.tag'
    _description = 'Property Tag Model'

    name = fields.Char(required=True)
