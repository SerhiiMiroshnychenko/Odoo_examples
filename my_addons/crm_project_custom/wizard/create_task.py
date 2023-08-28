from odoo import models, fields


class CreateTask(models.TransientModel):
    _name = 'create.task.wizard'
    _description = 'Create Task Wizard'

    project_id = fields.Many2one(comodel_name='project.project', string='Project', required=True)

    def create_task(self):
        """
        Creates a task related to the lead
        """
        lead = self.env['crm.lead'].browse(self._context.get('active_id'))

        new_task = self.env['project.task'].create({
            'name': lead.name,
            'user_ids': [(4, lead.user_id.id)],
            'partner_id': lead.partner_id.id,
            'project_id': self.project_id.id,
        })

        lead.write({'task_ids': [(4, new_task.id)]})
