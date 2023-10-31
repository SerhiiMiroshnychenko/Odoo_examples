from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from .log_print import _print
from .log_trace import _trace


# Abstract, Transient, Regular Model


class AbstractOffer(models.AbstractModel):
    _name = 'abstract.offer'
    _description = 'Abstract Offer'

    partner_email = fields.Char(string='Email')
    partner_phone = fields.Char(string='Phone Number')


class TransientOffer(models.TransientModel):
    _name = 'transient.offer'
    _description = 'Transient Offer'
    _transient_max_count = 3  # If "0" then unlimited
    _transient_max_hours = 1  # If "0" then unlimited

    partner_address = fields.Char(string='Address')

    @api.autovacuum
    def _transient_vacuum(self):
        pass


class PropertyOffer(models.Model):
    _name = 'real.property.offer'
    _inherit = ['abstract.offer']
    _description = 'Property Offer Model'

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for offer in self:
            if offer.property_id and offer.partner_id:
                offer.name = f'{offer.property_id.name} - {offer.partner_id.name}'

    name = fields.Char(string='Description', compute=_compute_name)
    price = fields.Monetary(required=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=lambda self: self.env.user.company_id.currency_id,
    )

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
    partner_email = fields.Char(
        string='Customer Email',
        related='partner_id.email',
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
        _print(f'{self.env.context = }')
        _print(f'{self._context = }')
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
        _print(f'{self = }')
        _print(f'{self.env.cr = }')
        _print(f'{self.env.uid = }')
        _print(f'{self.env.context = }')

        _print(f'{vals = }')

        res_partner_ids = self.env['res.partner'].search([
            ('is_company', '=', True),
        ], order='name ASC').mapped('name')
        _print(f'Ordered and mapped by name {res_partner_ids = }')

        res_partner_ids = self.env['res.partner'].search([
            ('is_company', '=', True),
        ]).mapped('phone')
        _print(f'Mapped by phone {res_partner_ids = }')

        res_partner_ids = self.env['res.partner'].search([
            ('is_company', '=', True),
        ]).filtered(lambda x: x.phone == '(603)-996-3829')
        _print(f'Filtered by phone {res_partner_ids = }')

        res_partner_ids = self.env['res.partner'].search([
            ('is_company', '=', True),
        ], limit=1)
        _print(f'Limited 1 {res_partner_ids = }')

        res_partner_ids = self.env['res.partner'].browse([10, 14])
        _print(f'Browsed {res_partner_ids = }')

        res_partner_ids = self.env['res.partner'].browse(10)
        _print(f'Browsed {res_partner_ids.name = }')

        res_partner_number = self.env['res.partner'].search_count([
            ('is_company', '=', True),
        ])
        _print(f'Counted {res_partner_number = }')

        return super(PropertyOffer, self).write(vals)

    def action_accept_offer(self):
        """
        Sets the status of the offer to 'accepted'.
        """
        if self.property_id:
            self._validate_accepted_offer()
            self.property_id.selling_price = self.price / 1000
            _print(f'{self.property_id.selling_price = } thousand')
            self.property_id.write({
                'selling_price': self.price,
                'state': 'accepted'
            })
            _print(f'{self.property_id.selling_price = } (self.price)')
        self.status = 'accepted'

    def _validate_accepted_offer(self):
        if offer_ids := self.env['real.property.offer'].search(
                [
                    ('property_id', '=', self.property_id.id),
                    ('status', '=', 'accepted'),
                ]
        ):
            _trace(f'{offer_ids = }')
            raise ValidationError("You have an accepted offer already")

    def action_decline_offer(self):
        """
        Declines the offer by setting the status to 'refused'.
        """
        self.status = 'refused'
        _trace(f"{self.property_id.offer_ids.mapped('status') = }")
        if 'accepted' not in self.property_id.offer_ids.mapped('status'):
            # if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price': 0,
                'state': 'received'
            })

    def extend_offer_deadline(self):
        if activ_ids := self._context.get('active_ids', []):
            _trace(f'{activ_ids = }')
            offer_ids = self.env['real.property.offer'].browse(activ_ids)
            for offer in offer_ids:
                offer.validity = 15

    def _extend_offer_deadline(self):
        offer_ids = self.env['real.property.offer'].search([])
        for offer in offer_ids:
            offer.validity = offer.validity + 1
