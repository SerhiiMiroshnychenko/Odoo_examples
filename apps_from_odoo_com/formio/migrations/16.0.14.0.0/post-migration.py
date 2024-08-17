# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import uuid

from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    builders = {}
    for rec in env['formio.builder'].search([]):
        if not builders.get(rec.name):
            builders[rec.name] = rec
        else:
            builders[rec.name] |= rec
    for name, records in builders.items():
        records.write({'current_uuid': str(uuid.uuid4())})
