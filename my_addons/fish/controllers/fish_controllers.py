# -*- coding: utf-8 -*-
import logging

from odoo import http
from odoo.http import request

logger = logging.getLogger(__name__)


class FishHome(http.Controller):

    @http.route('/fish/home/', type='http', auth='user', website=True)
    def index(self, **kw):
        fishes = request.env['fish.fish'].search([])
        return http.request.render('fish.index', {
            'fishes': fishes,
        })

    @http.route('/fish/<model("fish.fish"):fish>/', type='http', auth='user', website=True)
    def fish(self, fish):
        print(f"\n\n{fish = }\n\n")
        logger.info(f"\n\n{fish = }\n")
        return http.request.render('fish.remarks', {'fish': fish})