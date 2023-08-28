from odoo import fields, models


class School(models.Model):
    _name = 'school.student'
    _description = 'School_student model'

    name = fields.Many2one(comodel_name='res.partner', string='Student')
    class_id = fields.Integer(string='Class')
    division = fields.Char()
