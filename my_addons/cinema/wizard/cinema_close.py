from odoo import models, fields


class CinemaClose(models.TransientModel):
    _name = 'cinema.close.wizard'

    reason = fields.Text(string='Explanation of the reason')

    def close_cinema(self):
        self.ensure_one()
        model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        cinema = self.env[model].browse(active_id)
        if cinema.exists():
            cinema.status = 'close'
            cinema.description = f'The cinema is closed for the following reason: {self.reason}'
