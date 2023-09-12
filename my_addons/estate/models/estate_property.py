from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A model representing real estate objects"
    _order = "id desc"

    title = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,
                                    default=lambda self: fields.Datetime.add(
                                        value=fields.Datetime.today(),
                                        months=3
                                    ))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, default=None)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="The side of the world on which the garden is oriented")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        default='new',
        help="The state of the real estate object"
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    total_area = fields.Float(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for estate in self:
            if estate.offer_ids:
                estate.best_price = max(estate.offer_ids.mapped('price'))
                if estate.state == 'new':
                    estate.state = 'offer received'
            else:
                estate.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north'

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        for estate in self:
            if estate.state not in ('new', 'canceled'):
                raise UserError("Can't delete an active property!")

    def action_set_canceled_status(self):
        if self.state == 'sold':
            raise UserError("Sold properties cannot be canceled.")
        self.state = 'canceled'
        self.active = False
        return True

    def action_set_sold_status(self):
        if self.state == 'canceled':
            raise UserError("Canceled properties cannot be sold.")
        self.state = 'sold'
        self.active = False
        print(f'{self.title} is sold! (In Estate)')
        return True

    _sql_constraints = [
        ('check_expected_price',
         'CHECK(expected_price > 0)',
         'The expected price must be strictly more then 0.'),
        ('check_selling_price',
         'CHECK(selling_price > 0)',
         'The selling price must be strictly positive.')
    ]

    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        for estate in self:
            compare_result = float_compare(estate.selling_price, estate.expected_price * 0.9, 2)
            if compare_result < 0 and estate.selling_price:
                raise ValidationError("The selling price must be at least 90% of the expected price!")
