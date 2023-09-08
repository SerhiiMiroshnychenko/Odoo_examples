from odoo import fields, models


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = 'mail.thread'
    _description = 'Patient Records'

    name = fields.Char(string='Patient name', required=True, tracking=True)
    age = fields.Integer(string='Patient age', required=False, tracking=True)
    is_child = fields.Boolean(string='Is child?', tracking=True)
    notes = fields.Text(tracking=True)
    gender = fields.Selection(
        string='Patient gender',
        selection=[
            ('mail', 'Mail'),
            ('female', 'Female'),
        ],
    )
