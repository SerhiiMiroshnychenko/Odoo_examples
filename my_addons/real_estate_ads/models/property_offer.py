from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = 'real.property.offer'
    _description = 'Property Offer Model'

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name='real.property',
        required=True,
    )
    validity = fields.Integer()
    deadline = fields.Date()
