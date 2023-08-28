import logging
from odoo import models, fields
from datetime import timedelta
_logger = logging.getLogger(__name__)


class CinemaCinemaRepair(models.Model):
    _name = "cinema.cinema.repair"
    _description = 'List of repaired cinema halls'

    cinema_id = fields.Many2one(
        'cinema.cinema'
    )
    hall_id = fields.Many2one(
        'cinema.cinema.hall'
    )
    repair_start = fields.Date(
        default=lambda self: fields.Date.today()
    )
    repair_end = fields.Date(
        default=lambda self: fields.Date.today() + timedelta(14)
    )

    def unlink(self,):
        for record in self.hall_id:
            record.update({
                'repair': False,
            })
        super(CinemaCinemaRepair, self).unlink()
        return True

    def prevent_repair(self):
        _logger.info('Prevent repair halls')
        records = self.search([('repair_end', '<=', fields.Date.today())])
        records.hall_id.write({
            'repair': False
        })
        records.unlink()
