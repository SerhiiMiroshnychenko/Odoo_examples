from odoo import fields, models, api


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name='real.property',
        inverse_name='sales_id',
        string='Properties',
    )

    type_id = fields.Many2one(
        comodel_name='real.property.type',
        string='Property Type',
        required=False,
    )
