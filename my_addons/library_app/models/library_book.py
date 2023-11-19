from deep_translator import GoogleTranslator

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Book(models.Model):
    """
    Describes a Book catalogue.
    """
    _name = "library.book"
    _description = "Book"
    _order = "name, date_published desc"
    _rec_name = "name"
    _table = "library_book"
    _log_access = True
    _auto = True

    # String fields:
    name = fields.Char(
        "Title",
        default=None,
        help="Book cover title.",
        readonly=False,
        required=True,
        index=True,
        copy=False,
        groups="",
        states={},
    )
    isbn = fields.Char("ISBN")
    book_type = fields.Selection(
        [("paper", "Paperback"),
         ("hard", "Hardcover"),
         ("electronic", "Electronic"),
         ("other", "Other")],
        "Type",
    )
    notes = fields.Text("Internal Notes")
    descr = fields.Html("Description")

    description_language = fields.Many2one(
        "res.lang",
        # delegate=True,  # delegation inheritance
        ondelete='restrict'
    )
    description = fields.Text()

    def translate_description(self):
        # context_lang = self._context.get("lang")
        # print(f'{context_lang = }')
        # user_lang = self.env.user.lang
        # print(f'{user_lang = }')
        # langs = self.env['res.lang'].search([])
        # for lang in langs:
        #     print(f'{lang = }')
        for book in self:
            if book.description and book.description_language:
                try:
                    translated = GoogleTranslator(
                        source='auto',
                        target=book.description_language.iso_code).translate(book.description)

                    book.description = translated

                except ValueError as e:
                    book.description = str(e).title()
            elif book.description:
                book.description = 'No description language selected'
            elif book.description_language:
                book.description = 'No description provided'
            else:
                book.description = 'No description and language provided'

    # Numeric fields:
    copies = fields.Integer(default=1)
    avg_rating = fields.Float("Average Rating", (3, 2))
    price = fields.Monetary("Price", "currency_id")
    currency_id = fields.Many2one("res.currency")  # price helper

    # Date and time fields:
    date_published = fields.Date()

    def _default_last_borrow_date(self):
        return fields.Datetime.now()

    last_borrow_date = fields.Datetime(
        "Last Borrowed On",
        # default=lambda self: fields.Datetime.now(),
        default=_default_last_borrow_date,
    )

    # Other fields:
    active = fields.Boolean("Active?")
    image = fields.Binary("Cover")

    # Relational Fields
    publisher_id = fields.Many2one("res.partner", string="Publisher", index=True)
    author_ids = fields.Many2many("res.partner", string="Authors")

    # Book <-> Authors relation (using positional args)
    # author_ids = fields.Many2many(
    #     "res.partner",
    #     "library_book_res_partner_rel",
    #     "a_id",
    #     "b_id",
    #     "Authors",
    # )
    # Book <-> Authors relation (using keyword args)
    # author_ids = fields.Many2many(
    #     comodel_name="res.partner",
    #     relation="library_book_res_partner_rel",
    #     column1="a_id",
    #     column2="b_id",
    #     string="Authors")

    @api.depends("publisher_id.country_id")
    def _compute_publisher_country(self):
        for book in self:
            book.publisher_country_id = book.publisher_id.country_id

    def _inverse_publisher_country(self):
        for book in self:
            book.publisher_id.country_id = book.publisher_country_id

    def _search_publisher_country(self, operator, value):
        return [("publisher_id.country_id", operator, value)]

    publisher_country_id = fields.Many2one(
        "res.country", string="Publisher Country",
        # related="publisher_id.country_id",
        compute="_compute_publisher_country",
        inverse="_inverse_publisher_country",
        search="_search_publisher_country",
    )

    _sql_constraints = [
        ("library_book_name_date_uq",
         "UNIQUE (name, date_published)",
         "Book title and publication date must be unique."),
        ("library_book_check_date",
         "CHECK (date_published <= current_date)",
         "Publication date must not be in the future."),
    ]

    @api.constrains("isbn")
    def _constrain_isbn_valid(self):
        for book in self:
            if book.isbn and not book._check_isbn():
                raise ValidationError(
                    "%s is an invalid ISBN" % book.isbn)

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
