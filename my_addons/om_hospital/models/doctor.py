from odoo import fields, models, api, _


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = 'mail.thread'
    _description = 'Doctor Records'

    name = fields.Char(string='Doctor name', required=True, tracking=True)
    ref = fields.Char(string='Reference', default=lambda self: _('New'))
    gender = fields.Selection(
        string='Doctor gender',
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = vals['name'].title()
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.doctor')
        return super(HospitalDoctor, self).create(vals_list)
