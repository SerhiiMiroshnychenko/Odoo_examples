from odoo import models, fields
from datetime import timedelta


class CinemaRepair(models.TransientModel):
    _name = 'cinema.repair.wizard'
    _description = 'Wizard of Cinema module'

    cinema_id = fields.Many2one(
        'cinema.cinema',
        default=lambda self: self.env.context.get('active_id')
    )
    hall_ids = fields.Many2one(
        'cinema.cinema.hall',
        required=True
    )
    repair_start = fields.Date(
        default=lambda self: fields.Date.today()
    )
    repair_end = fields.Date(
        default=lambda self: fields.Date.today() + timedelta(14)
    )

    def cinema_repair(self):
        self.hall_ids.update({
            'repair': True
        })
        self.env['cinema.cinema.repair'].create([
            {
                'cinema_id': self.env.context.get('active_id'),
                'hall_id': self.hall_ids.id,
                'repair_start': self.repair_start,
                'repair_end': self.repair_end
            }
        ])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Repair',
            'view_mode': 'tree',
            'res_model': 'cinema.cinema.repair',
        }
