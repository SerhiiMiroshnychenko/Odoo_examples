# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class FishHome(http.Controller):

    @http.route('/fish/home/', type='http', auth='user', website=True)
    def index(self, **kw):
        fishes = request.env['fish.fish'].search([])
        return http.request.render('fish.index', {
            'fishes': fishes,
        })

    @http.route('/fish/<model("fish.fish"):fish>/', type='http', auth='user', website=True)
    def fish(self, fish):
        return http.request.render('fish.remarks', {'fish': fish})