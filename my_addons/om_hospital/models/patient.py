from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


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
            ('male', 'Male'),
            ('female', 'Female'),
        ],
    )
    uppercase_name = fields.Char(compute='_compute_uppercase_name', store=True)
    ref = fields.Char(string='Reference', default=lambda self: _('New'))
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Doctor',
        required=False,
    )
    tag_ids = fields.Many2many(comodel_name='res.partner.category', string='Tags')
    property_tag_ids = fields.Many2many(
        comodel_name='estate.property.tag',
        relation='hospital_patient_property_tag_rel',
        column1='patient_id',
        column2='property_tag_id',
        string='Property Tags'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = vals['name'].title()
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals_list)

    @api.constrains('age', 'is_child')
    def _check_age(self):
        for patient in self:
            if patient.age < 1:
                message = "The child age has to be recorded!" if patient.is_child \
                    else "The patient age has to be recorded!"
                raise ValidationError(_(message))

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
