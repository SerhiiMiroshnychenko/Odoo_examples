from datetime import timedelta

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
    deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')
    creation_date = fields.Date(string='Create Date')

    @api.depends('creation_date', 'validity')
    def _compute_deadline(self):
        for offer in self:
            if offer.creation_date and offer.validity:
                offer.deadline = offer.creation_date + timedelta(days=offer.validity)
            else:
                offer.deadline = False

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.deadline - offer.creation_date).days

    @api.autovacuum
    def _clean_offers(self):
        """
        Decorate a method so that it is called by the daily vacuum cron job (model ir.autovacuum).
        This is typically used for garbage-collection-like tasks that do not deserve a specific cron job.

        Прикрасьте метод так, щоб він викликався щоденним завданням вакуумної синхронізації (модель ir.autovacuum).
        Це зазвичай використовується для завдань, подібних до збирання сміття,
        які не заслуговують на певне завдання cron.
        """
        self.search([('status', '=', 'refused')]).unlink()
