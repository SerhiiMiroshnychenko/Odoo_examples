from odoo import fields, models


class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'

    lead_id = fields.Many2one(comodel_name='crm.lead', string='Lead')
