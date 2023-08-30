# -*- coding: utf-8 -*-
# from odoo import http


# class ScaffoldModule(http.Controller):
#     @http.route('/scaffold_module/scaffold_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/scaffold_module/scaffold_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('scaffold_module.listing', {
#             'root': '/scaffold_module/scaffold_module',
#             'objects': http.request.env['scaffold_module.scaffold_module'].search([]),
#         })

#     @http.route('/scaffold_module/scaffold_module/objects/<model("scaffold_module.scaffold_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('scaffold_module.object', {
#             'object': obj
#         })

from odoo import http
from odoo.http import request


class SchoolController(http.Controller):
    @http.route(route=['/school/students'], type='http', auth='user', website=True)
    def student_list(self, **kw):
        students = request.env['school.student'].search([])
        return request.render(template='school_management.student_list_template', qcontext={'students': students})
