from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from .log_check import _logger


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
    _sql_constraints = [
        ('check_max_validity', 'check(validity < 30)', 'Validity must be less than 30 days')
    ]

    deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')

    @api.model
    def _set_create_date(self):
        """
        Decorate a record-style method where self is a recordset,
        but its contents is not relevant, only the model is.

        This method returns today's date.
        :return: <class 'datetime.date'>
        """
        return fields.Date.today()

    creation_date = fields.Date(string='Create Date', default=_set_create_date)

    @api.depends('creation_date', 'validity')  # Викликається при зміні полів 'creation_date', 'validity'
    @api.depends_context('uid')  # Викликається при зміні поточного користувача
    def _compute_deadline(self):
        _logger.check(f'CONTEXT: {self.env.context}')
        _logger.check(f'_CONTEXT: {self._context}')
        for offer in self:
            if offer.creation_date and offer.validity:
                offer.deadline = offer.creation_date + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            if offer.deadline and offer.creation_date:
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

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if not val.get('validity'):
                val['validity'] = 10
        return super(PropertyOffer, self).create(vals_list)

    @api.constrains('validity')
    def _check_validity(self):
        for offer in self:
            if offer.deadline <= offer.creation_date:
                raise ValidationError(_('Deadline must be after creation date'))

    def write(self, vals):
        _logger.check(f'VALS: {vals}')
        return super(PropertyOffer, self).write(vals)
