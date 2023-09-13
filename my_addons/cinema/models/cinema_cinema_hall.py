from odoo import api, fields, models, Command


class CinemaCinemaHall(models.Model):
    _name = 'cinema.cinema.hall'
    _description = "A model representing hall"

    name = fields.Char(string="Cinema hall name", required=True)
    seats = fields.Integer(required=True)
    cinema_id = fields.Many2one('cinema.cinema', required=True, ondelete='cascade')

    movie_ids = fields.Many2many(
        'cinema.cinema.movie',
    )

    reserved = fields.Boolean(
        default=False,
        string='Reserved'
    )
    repair = fields.Boolean(
        default=False
    )
    article = fields.Char(required=True, copy=False, default='CH0000')

    def increase_seats(self):
        self.ensure_one()
        self.seats = self.seats + 10

    def decrease_seats(self):
        self.ensure_one()
        self.seats = max(self.seats - 10, 0)

    @api.model
    def create(self, vals):
        hall = super(CinemaCinemaHall, self).create(vals)
        hall.article = self.env['ir.sequence'].next_by_code('cinema.hall') or "CH0000"
        hall.cinema_id.create_playbill()
        return hall

    # @api.model
    # def create(self, vals_list):
    #     """
    #     Create one or more records based on a list of dictionaries.
    #
    #     :param vals_list: List of dictionaries containing field values for each record.
    #     :return: List of created record(s).
    #     """
    #     created_halls = self.env['cinema.cinema.hall']
    #     for vals in vals_list:
    #         hall = super(CinemaCinemaHall, self).create(vals)
    #         hall.article = self.env['ir.sequence'].next_by_code('cinema.hall') or "CH0000"
    #         hall.cinema_id.create_playbill()
    #         created_halls += hall
    #     return created_halls

    def _pin_newest_movies(self):
        newest = self.movie_ids.search([('premiere_date', '>=', fields.Date.today())])
        for record in self:
            record.update({
                'movie_ids': [Command.link(index) for index in newest.ids]
            })

    def _unlink_old_movies(self):
        for record in self:
            old_movies = record.movie_ids.search([('deadline_date', '<', fields.Date.today())])
            record.update({
                'movie_ids': [Command.unlink(index) for index in old_movies.ids]
            })
