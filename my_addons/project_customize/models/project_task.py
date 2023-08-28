from datetime import timedelta
from odoo import _, api, fields, models


class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'

    code = fields.Char(copy=False, readonly=True, default=lambda self: _('T#0000'))

    def _set_deadline_if_use_delta_and_empty(self, vals):
        """
        If project use deadline delta days
        and deadline(date.deadline) is empty
        set today + delta from settings
        """
        delta = int(self.env['ir.config_parameter'].sudo().get_param('project_customize.deadline_delta_days'))
        if delta:
            for task in self:
                if not task.date_deadline:
                    vals['date_deadline'] = fields.Date.today() + timedelta(days=delta)

    def set_tag_for_overdue_task_if_used(self):
        """
        If project use deadline over tag
        and the task deadline has already passed
        and add tag into tag_ids from res.config.settings
        """
        tag_from_setting = self.env['ir.config_parameter'].sudo().get_param('project_customize.deadline_over_tag')
        if tag_from_setting:
            overdue_tasks = self.search([('date_deadline', '<', fields.Date.today())])
            tag = self.env['project.tags'].search([('id', '=', tag_from_setting)])
            overdue_tasks.write({'tag_ids': [(4, tag.id)]})

    @api.model
    def create(self, vals):
        """
        When creating a task, it adds code to it according to the sequence
        """
        if vals.get('code', _("T#0000") == _("T#0000")):
            vals['code'] = self.env['ir.sequence'].next_by_code('code') or _("T#0000")
        self._set_deadline_if_use_delta_and_empty(vals)
        return super().create(vals)

    @api.model
    def write(self, vals):
        """
        While changing the task it sets a deadline
        according to the defined rules
        if the deadline has passed or is not defined
        """
        self._set_deadline_if_use_delta_and_empty(vals)
        return super().write(vals)
