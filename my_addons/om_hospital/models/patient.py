from odoo import fields, models, api


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
    uppercase_name = fields.Char(compute='_compute_uppercase_name', store=True)

    @api.depends('name')
    def _compute_uppercase_name(self):
        """
        Compute and set the 'uppercase_name' field value by uppercase the 'name' field.
        """
        for patient in self:
            if patient.name:
                patient.uppercase_name = patient.name.upper()

    @api.onchange('age')
    def _onchange_age(self):
        """
        Automatically called when the 'age' field is changed.
        Checks the patient's age and sets the 'is_child' field accordingly.
        """
        self.is_child = True if self.age <= 10 else False
