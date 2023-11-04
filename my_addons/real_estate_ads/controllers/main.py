import json

from odoo import http
from odoo.http import request


class PropertyController(http.Controller):

    @http.route(['/properties'], type="http", auth="public", website=True)
    def show_properties(self):
        property_ids = request.env['real.property'].sudo().search([])
        print(f'{property_ids = }')


# class ModelName(http.Controller):
#
#     @http.route(['/api/APiRoute/<int:Var>'], type="http", auth="public", website=True, method=['POST'],
#                 csrf=False)
#     def example(self, Var):
#         values = {}
#
#         data = request.env['ProjectName.TableName'].sudo().search([("id", "=", int(Var))])
#
#         if data:
#             values['success'] = True
#             values['return'] = "Something"
#         else:
#             values['success'] = False
#             values['error_code'] = 1
#             values['error_data'] = 'No data found!'
#
#         return json.dumps(values)
