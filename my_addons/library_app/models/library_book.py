from googletrans import Translator

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Book(models.Model):
    """
    Describes a Book catalogue.
    """
    _name = "library.book"
    _description = "Book"

    name = fields.Char("Title", required=True)
    isbn = fields.Char("ISBN")
    active = fields.Boolean("Active?", default=True)
    date_published = fields.Date()
    image = fields.Binary("Cover")
    publisher_id = fields.Many2one("res.partner", string="Publisher")
    author_ids = fields.Many2many("res.partner", string="Authors")
    english_description = fields.Text()
    description_language = fields.Char(default="en")
    description = fields.Text(compute="_compute_description")
    
    @api.depends('english_description', 'description_language')
    def _compute_description(self):
        # context_lang = self._context.get("lang")
        # print(f'{context_lang = }')
        for book in self:
            if book.english_description and book.description_language:
                try:
                    book.description = Translator().translate(
                        book.english_description,
                        src='en',
                        dest=book.description_language
                    ).text
                except ValueError as e:
                    print(e.__class__, e)
                    book.description = e
            elif book.english_description:
                book.description = 'No description language selected'
            elif book.description_language:
                book.description = 'No description provided'
            else:
                book.description = 'No description and language provided'

    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise ValidationError("Please provide an ISBN for %s" % book.name)
            if book.isbn and not book._check_isbn():
                raise ValidationError("%s ISBN is invalid" % book.isbn)
        return True
