from odoo import fields, models


class Book(models.Model):
    """
    - Add support to ISBN10
    """
    _inherit = "library.book"

    is_available = fields.Boolean("Is Available?")

    isbn = fields.Char(help="Use a valid ISBN-13 or ISBN-10.")
    publisher_id = fields.Many2one(index=True)

    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) != 10:
            return super()._check_isbn()
        ponderators = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return digits[-1] == sum(a * b for a, b in zip(digits[:9], ponderators)) % 11
