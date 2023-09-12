from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "A model representing offers for real estate objects"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        help="The status of offer for real estate object"
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        required=True,
        ondelete='cascade'
        # inverse_name='offer_ids'
    )

    validity = fields.Integer(default=7, string='Validity (days)')

    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        string='Deadline'
    )

    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or date.today()
            offer.date_deadline = create_date + relativedelta(
                days=offer.validity)

    @api.constrains('price')
    def _check_price(self):
        max_price = max(offer.price for offer in self.property_id.offer_ids)
        print(f'{max_price=}')
        print(f'{self.price=}')
        if self.price < max_price:
            raise UserError(f"The offer must be more than {max_price}")

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or date.today()
            date_difference = offer.date_deadline - create_date.date()
            offer.validity = date_difference.days
            print(f'Create date: {create_date}\n'
                  f'Date deadline: {offer.date_deadline}\n'
                  f'Date difference: {date_difference}\n'
                  f'Validity (days): {offer.validity}')

    def action_accept(self):
        print('self.property_id.best_price ==', self.property_id.selling_price)
        if self.property_id.selling_price == 0:
            self.status = 'accepted'
            self.property_id.state = 'offer accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            return True
        raise UserError("No more than one offer may be accepted.")

    def action_refuse(self):
        self.status = 'refused'
        # for offer in self.property_id.offer_ids:
        #     if offer.status == 'accepted':
        #         return True
        # self.property_id.selling_price = None
        # self.property_id.buyer_id = None
        return True

    _sql_constraints = [
        ('check_price',
         'CHECK(price > 0)',
         'The offer price must be strictly more then 0.')
    ]
