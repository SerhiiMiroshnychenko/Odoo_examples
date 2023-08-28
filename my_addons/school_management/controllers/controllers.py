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
