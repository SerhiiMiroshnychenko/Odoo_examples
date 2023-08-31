from odoo import http
from odoo.http import request


class PayrollController(http.Controller):
    @http.route(route=['/payroll_custom/payrolls/all'], type='http', auth='user', website=True)
    def all_payroll_list(self, **kw):
        print(f'{kw=}')
        all_payrolls = request.env['payroll.payroll'].search([])
        return request.render(template='payroll_custom.payroll_list_template',
                              qcontext={'payrolls': all_payrolls})

    @http.route(route='/payroll_custom/payrolls/objects', type='http', auth='user', website=True)
    def objects_payroll_list(self, **kw):
        print(f'{kw=}')
        return http.request.render(template='payroll_custom.listing',
                                   qcontext={
                                       'root': 'payroll_custom/payrolls',
                                       'objects': http.request.env['payroll.payroll'].search([]),
                                   })

    @http.route('/payroll_custom/payrolls/payroll_custom/payrolls/objects/<model("payroll.payroll"):obj>',
                type='http', auth='user', website=True)
    def object(self, obj, **kw):
        print(f'____________________________________{obj=}')
        return http.request.render('payroll_custom.object', {
            'object': obj
        })


# class UserPayrollController(http.Controller):
#     @http.route(route=['/payroll_custom/payrolls/#{object.employee_id.id}'], type='http', auth='user', website=True)
#     def user_payroll_list(self, **kw):
#         print(f'{kw=}')
#         employee_id = request.params.get('employee_id')
#         print(f'{employee_id=}')
#         employee_id1 = kw.get('default_employee_id')
#         print(f'{employee_id1=}')
#         employee_id2 = request.context.get('default_employee_id')
#         print(f'{employee_id2=}')
#         if employee_id:
#             user_payrolls = request.env['payroll.payroll'].search([('employee_id', '=', employee_id)])
#             print(f'{user_payrolls=}')
#             return request.render(template='payroll_custom.payroll_list_template',
#                                   qcontext={'payrolls': user_payrolls})
#         else:
#             return http.request.redirect('/')
