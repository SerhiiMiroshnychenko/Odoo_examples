from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PayrollPayroll(models.Model):
    _name = 'payroll.payroll'
    _description = 'A custom payroll'
    _order = 'amount DESC'

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=True,
    )

    date_from = fields.Date(
        string='Date From',
        required=True,
        default=fields.Date.context_today,
    )

    date_to = fields.Date(
        string='Date To',
        required=True,
        default=fields.Date.context_today,
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        required=True,
    )

    amount = fields.Monetary(
        string='Amount',
        currency_field='currency_id',
        required=False,
    )

    amount2 = fields.Monetary(
        string='Amount 2',
        currency_field='currency_id',
        required=False,
    )

    state = fields.Selection(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('calculated', 'Calculated'),
            ('conformed', 'Conformed'),
        ],
        required=True,
        default='draft'
    )

    def calculate_payroll(self):
        """
        The alternative method
        """
        timesheets = self.env['account.analytic.line'].search([
                    ('employee_id', '=', self.employee_id.id),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to),
                ])
        total_hours = sum(timesheets.mapped(lambda r: r.unit_amount))
        hour_cost = self.env['hr.employee'].search([('id', '=', self.employee_id.id)]).hourly_cost
        self.amount2 = total_hours * hour_cost
        self.state = 'calculated'

    def action_calculate_timesheets(self):
        """
        Calculation of the amount based on employee's timesheets and dates
        """
        for payroll in self:
            if payroll.state == 'draft':
                employee = payroll.employee_id
                hourly_cost = employee.hourly_cost

                timesheets = self.env['account.analytic.line'].search([
                    ('employee_id', '=', employee.id),
                    ('date', '>=', payroll.date_from),
                    ('date', '<=', payroll.date_to),
                ])
                total_amount = sum([timesheet.unit_amount * hourly_cost for timesheet in timesheets])

                # Call calculate_payroll method
                self.calculate_payroll()

                payroll.write({
                    'amount': total_amount,
                    'state': 'calculated',
                })

    def action_validate(self):
        """
        Validates calculation and changes status into “Confirmed”
        """
        for payroll in self:
            if payroll.state == 'calculated':
                payroll.write({'state': 'conformed'})

    @api.constrains('date_from', 'date_to')
    def _date_constraint(self):
        if self.date_from >= self.date_to:
            raise ValidationError('The start date must be greater than the end date')
