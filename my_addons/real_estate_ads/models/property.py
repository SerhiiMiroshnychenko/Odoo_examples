import base64

from odoo import api, fields, models, _

from .log_trace import _trace


class Property(models.Model):
    _name = 'real.property'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        # 'mail.alias.mixin',
        'utm.mixin',
        'website.published.mixin',
        'website.seo.metadata'
    ]
    _description = 'Real Estate Property Model'

    name = fields.Char(required=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancel', 'Canceled'),
        ],
        default='new',
        string='Status',
        group_expand='_expand_state'
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string='Available From')
    expected_price = fields.Float(tracking=True)
    best_offer = fields.Float(compute='_compute_best_offer')
    selling_price = fields.Float(readonly=True)
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
    sales_phone = fields.Char(related='sales_id.phone', string='Salesman phone')
    sales_email = fields.Char(related='sales_id.email', string='Salesman email')

    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('is_company', '=', True)]
    )
    phone = fields.Char(related='buyer_id.phone', string='Buyer phone')
    email = fields.Char(related='buyer_id.email', string='Buyer email')

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

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for prop in self:
            prop.best_offer = max(prop.offer_ids.mapped('price')) if prop.offer_ids else 0

    def action_client_action(self):
        return {
            'type': 'ir.actions.client',
            # 'tag': 'reload',  # перезавантаження сторінки
            # 'tag': 'apps',  # перехід на Apps Store
            'tag': 'display_notification',  # повідомлення що спливає
            'params': {
                'title': _('Salesman'),
                'message': f'Email: {self.sales_email} Phone: {self.sales_phone}',
                'type': 'success',  # warning, danger
                'sticky': True  # чи залишається на екрані
            }

        }

    def action_url_action(self):
        language = self._context.get("lang")
        _trace(f'{language = }')
        return {
            'type': 'ir.actions.act_url',
            'url': f'https://odoo.com/{language}',
            # 'target': 'self',
            'target': 'new',
        }

    def _get_report_base_filename(self):
        self.ensure_one()
        return f'Estate Property - {self.name}'

    def _compute_website_url(self):
        for rec in self:
            # rec.website_url = '/properties/%s' % rec.id
            rec.website_url = f'/properties/{rec.id}'

    def action_send_email(self):
        mail_template = self.env.ref('real_estate_ads.offer_mail_template')
        mail_template.send_mail(self.id, force_send=True)

    def _get_emails(self):
        # return self.mapped('buyer_id').mapped('email')
        return ','.join(self.offer_ids.mapped('partner_email'))

    def _expand_state(self, states, domain, order):
        return [
            key for key, dummy in type(self).state.selection
        ]


class PropertyType(models.Model):
    _name = 'real.property.type'
    _description = 'Property Type Model'

    name = fields.Char(required=True)


class PropertyTag(models.Model):
    _name = 'real.property.tag'
    _description = 'Property Tag Model'

    name = fields.Char(required=True)
    color = fields.Integer()
