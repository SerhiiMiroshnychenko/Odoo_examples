from odoo import models, fields


class CinemaNote(models.TransientModel):
    _name = 'cinema.note.wizard'

    note = fields.Text()

    def update_note(self):
        self.ensure_one()
        model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        cinema = self.env[model].browse(active_id)
        if cinema.exists():
            cinema.note = self.note
            cinema.description += self.note

        return {
            'type': 'ir.actions.act_window',
            'name': 'Manager',
            'view_mode': 'form',
            'res_id': cinema.user_id.id,
            'res_model': 'res.users',
        }
