from odoo import api, fields, models


class Property(models.Model):
    _name = 'real.property'
    _description = 'Real Estate Property Model'

    name = fields.Char(required=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancel', 'Canceled'),
        ], default='new'
    )
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
    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('is_company', '=', True)]
    )
    phone = fields.Char(related='buyer_id.phone', string='Buyer phone')

    total_area = fields.Integer()

    @api.onchange('living_area', 'garden_area')
    def _compute_total_area(self):
        self.total_area = self.living_area + self.garden_area

    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'cancel'

    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for prop in self:
            prop.offer_count = len(prop.offer_ids)

    def action_property_view_offer_for_button(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f'{self.name} - Offers',
            'domain': [('property_id', '=', self.id)],
            'view_mode': 'tree',
            'res_model': 'real.property.offer',
        }


class PropertyType(models.Model):
    _name = 'real.property.type'
    _description = 'Property Type Model'

    name = fields.Char(required=True)


class PropertyTag(models.Model):
    _name = 'real.property.tag'
    _description = 'Property Tag Model'

    name = fields.Char(required=True)
