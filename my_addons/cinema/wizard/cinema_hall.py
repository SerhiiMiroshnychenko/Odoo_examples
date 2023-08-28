from odoo import models, fields


class CinemaNewHall(models.TransientModel):
    _name = 'cinema.hall.wizard'

    name = fields.Char(string="Cinema hall name", required=True)

    def create_hall(self):
        self.ensure_one()
        model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        cinema = self.env[model].browse(active_id)

        new_hall = cinema.hall_ids.create({
                'name': self.name,
                'seats': 0,
                'cinema_id': cinema.id,
            }) if cinema.exists() else None

        action = self.env.ref('cinema.action_hall_seat_wizard').read()[0]
        action['context'] = {'active_hall_id': new_hall.id,}
        return action
