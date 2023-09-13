from odoo import models, fields


class HallSeatWizard(models.TransientModel):
    _name = 'hall.seat.wizard'
    _description = 'Wizard of Cinema module'

    seats = fields.Integer(string="Number of seats", required=True)

    def create_seats(self):
        self.ensure_one()
        active_hall_id = self.env.context.get('active_hall_id')
        hall = self.env['cinema.cinema.hall'].browse(active_hall_id)

        if hall.exists():
            hall.update({'seats': self.seats})

        action_id = self.env.ref('cinema.action_cinema_cinema_smart_hall').id
        cinema = self.env['cinema.cinema'].browse(hall.cinema_id.id)

        return {
            'id': action_id,
            'type': 'ir.actions.act_window',
            'name': 'Halls',
            'view_mode': 'kanban',
            'res_id': hall.cinema_id.id,
            'res_model': 'cinema.cinema.hall',
            'domain': [('id', 'in', cinema.hall_ids.ids)]
        }
