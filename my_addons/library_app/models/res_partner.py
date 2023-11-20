from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    published_book_ids = fields.One2many(
        "library.book",
        "publisher_id",
        string="Published Books",
    )

    book_ids = fields.Many2many(
        "library.book",
        string="Authored Books")
