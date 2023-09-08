from odoo import fields, models


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Records'

    name = fields.Char(string='Patient name', required=True)
    age = fields.Integer(string='Patient age', required=False)
    is_child = fields.Boolean(string='Is child?')
    notes = fields.Text()
    gender = fields.Selection(
        string='Patient gender',
        selection=[
            ('mail', 'Mail'),
            ('femail', 'Femail'),
        ],
    )
