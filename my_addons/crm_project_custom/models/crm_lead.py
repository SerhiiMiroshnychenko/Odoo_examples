from odoo import api, models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='lead_id',
        string='Tasks',
    )
    tasks_count = fields.Integer(
        compute='_compute_tasks_count',
        store=True,
    )

    @api.depends('task_ids')
    def _compute_tasks_count(self):
        """
        A method for calculating the number of tasks related to the lead
        """
        for lead in self:
            lead.tasks_count = self.env['project.task'].search_count([('lead_id', '=', lead.id)])

    def open_wizard(self):
        """
        This opens 'create.task.wizard'
        """
        active_id = self.env.context['active_id']
        return {
            'name': 'Create Task Wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'create.task.wizard',
            'target': 'new',
            'view_id': self.env.ref
            ('crm_project_custom.create_task_wizard_form').id,
            'context': {'active_id': active_id},
        }
