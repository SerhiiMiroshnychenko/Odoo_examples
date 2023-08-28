from odoo import models, fields
from odoo.exceptions import ValidationError


class CustomSaleNote(models.TransientModel):
    _name = 'custom.sale.note'

    note = fields.Char()

    def add_note(self):
        model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        order = self.env[model].browse(active_id)
        if order.exists():
            if self.note:
                order.manager_note = self.note
            else:
                raise ValidationError('Blank note, check that you have entered text')
