from datetime import timedelta
from odoo import _, api, fields, models


class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'
    _sql_constraints = [
        ('check_dates', 'CHECK (date_deadline >= date_create)', "Deadline date must be later than create date.")
    ]

    task_code = fields.Char(copy=False, readonly=True, default=lambda self: _('T#000'))

    date_deadline = fields.Date(string='Deadline', index=True, copy=False, tracking=True, task_dependency_tracking=True)
    date_create = fields.Date(string='Create Date', compute='_compute_date_create',
                              # store=True,
                              index=True, copy=False, tracking=True)

    qa_id = fields.Many2one(
        comodel_name="res.users",
        string="Quality Assurance",
    )

    is_approved_state = fields.Selection(
        selection=[('not_set', 'Not set'),
                   ('approved', 'Approved'),
                   ('rejected', 'Rejected')],
        default='not_set'
    )

    days_count = fields.Integer(
        compute='_compute_days_count',
        readonly=True,
        copy=False,
    )

    @api.depends('create_date')
    def _compute_date_create(self):
        for task in self:
            task.date_create = task.create_date.date()

    def check_deadline(self):
        if limit := int(self.env['ir.config_parameter'].sudo().get_param('project_custom.days_limit')):
            for task in self:
                task.date_deadline = max(task.date_deadline, task.date_create)
                if (task.date_deadline - task.date_create).days > limit:
                    task.date_deadline = task.date_create + timedelta(days=limit)

    def add_day(self):
        for task in self:
            task.date_deadline = task.date_deadline + timedelta(days=1)
            self.check_deadline()

    @api.depends('create_date', 'date_deadline')
    def _compute_days_count(self):
        for task in self:
            if task.create_date and task.date_deadline:
                task.days_count = (task.date_deadline - task.date_create).days
            else:
                task.days_count = 0

    @api.model
    def create(self, vals):
        if vals.get('task_code', _("T#000") == _("T#000")):
            vals['task_code'] = self.env['ir.sequence'].next_by_code('task.code') or _("T#000")
        return super().create(vals)

    @api.onchange('date_deadline')
    def _check_deadline(self):
        self.check_deadline()
