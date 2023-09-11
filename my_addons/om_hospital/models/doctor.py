from odoo import fields, models, api, _


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = 'mail.thread'
    _description = 'Doctor Records'
    _rec_name = 'ref'

    name = fields.Char(string='Doctor name', required=True, tracking=True)
    ref = fields.Char(string='Reference', default=lambda self: _('New'), required=True)
    gender = fields.Selection(
        string='Doctor gender',
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
    )

    def name_get(self):
        res = []
        for doctor in self:
            name = f'{doctor.ref} - {doctor.name}'
            res.append((doctor.id, name))
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = vals['name'].title()
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.doctor')
        return super(HospitalDoctor, self).create(vals_list)
