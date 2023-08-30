from odoo import http
from odoo.http import request


class PayrollController(http.Controller):
    @http.route(route=['/payrolls'], type='http', auth='user', website=True)
    def payroll_list(self, **kw):
        payrolls = request.env['payroll.payroll'].search([])
        return request.render(template='payroll_custom.payroll_list_template',
                              qcontext={'payrolls': payrolls})
