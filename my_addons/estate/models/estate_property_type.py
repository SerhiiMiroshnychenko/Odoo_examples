from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "A model representing types of real estate objects"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(
        'Sequence',
        default=1,
        help="Used to order stages. Lower is better."
    )

    property_ids = fields.One2many('estate.property', 'property_type_id')

    offers_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string='Offers'
    )

    offer_count = fields.Integer(
        compute='_compute_offer_count',
        string='Offer Count'
    )

    @api.depends('offers_ids')
    def _compute_offer_count(self):
        for prop_type in self:
            prop_type.offer_count = len(prop_type.offers_ids)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Type name already exists !"),
    ]
