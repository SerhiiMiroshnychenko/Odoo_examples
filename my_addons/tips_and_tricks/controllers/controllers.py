# -*- coding: utf-8 -*-
# from odoo import http


# class TipsAndTricks(http.Controller):
#     @http.route('/tips_and_tricks/tips_and_tricks', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tips_and_tricks/tips_and_tricks/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tips_and_tricks.listing', {
#             'root': '/tips_and_tricks/tips_and_tricks',
#             'objects': http.request.env['tips_and_tricks.tips_and_tricks'].search([]),
#         })

#     @http.route('/tips_and_tricks/tips_and_tricks/objects/<model("tips_and_tricks.tips_and_tricks"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tips_and_tricks.object', {
#             'object': obj
#         })
