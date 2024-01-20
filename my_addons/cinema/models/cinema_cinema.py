import logging
from random import randint, choice
from odoo import _, api, fields, models, Command
from odoo.exceptions import UserError
_logger = logging.getLogger()


class CinemaCinema(models.Model):
    _name = 'cinema.cinema'
    _order = 'state'
    _description = "A model representing cinema"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Cinema name", required=True, tracking=1)
    cinema_code = fields.Char(copy=False, readonly=True, default=lambda self: _('C№000'))
    description = fields.Text()
    note = fields.Text()
    user_id = fields.Many2one(
        comodel_name="res.users",
        required=True,
        string="Administrator",
        default=lambda self: self.env.uid
    )
    number_of_stuff = fields.Integer()
    hall_ids = fields.One2many(
        "cinema.cinema.hall",
        "cinema_id",
        string='Halls'
    )

    square_space = fields.Float()
    state = fields.Selection(
        selection=[('open', 'Open'),
                   ('close', 'Close')],
        required=True,
        default='close',
        tracking=1
    )

    restaurant = fields.Boolean(string='Restaurant', help='Availability of a restaurant in the cinema')
    total_seats = fields.Integer(compute='_compute_total_seats')
    movie_ids = fields.Many2many('cinema.cinema.movie', states={'close': [('invisible', True)]})
    vip_halls = fields.Integer(compute='_compute_vip_halls', store=True)
    movies_count = fields.Integer(
        compute='_compute_movies_count',
        store=True,
    )
    halls_count = fields.Integer(
        compute='_compute_halls_count',
        store=True,
    )
    active_halls = fields.Integer(
        compute='_compute_active_halls',
        string='Active Halls'
    )

    def _compute_active_halls(self):
        self.active_halls = self.hall_ids.search_count([('repair', '=', False), ('cinema_id', '=', self.id)])

    def create_new_movie(self):
        self.env['cinema.cinema.movie'].create(
            {
                'name': f'Terminator {randint(1,100)}',
                'premiere_date': fields.date.today(),
            }
        )

    def create_new_cinema(self):
        vals = {
            'name': 'NEW CINEMA',
            'state': 'open',
        }

        self.env['cinema.cinema'].create(vals)

    def create_vip_hall(self):
        if 'Vip hall' in self.hall_ids.mapped('name'):
            raise UserError(f'Vip hall already exists in {self.name}')
        self.update({
            'hall_ids': [(fields.Command.create({
                'name': 'Vip hall',
                'seats': randint(1, 100)
            }))]
        })

    def get_movies(self):
        return self.movie_ids

    @api.depends('movie_ids')
    def _compute_movies_count(self):
        for cinema in self:
            cinema.movies_count = self.env['cinema.cinema.movie'].search_count([('cinema_ids', 'in', cinema.id)])

    @api.depends('hall_ids')
    def _compute_halls_count(self):
        for cinema in self:
            cinema.halls_count = self.env['cinema.cinema.hall'].search_count([('cinema_id', '=', cinema.id)])

    def clear_movie_list(self):
        self.hall_ids.update({
            'movie_ids': [Command.clear()]
        })

    def add_seats(self):
        halls = self.hall_ids.search([('cinema_id', '=', self.id)])
        for hall in halls:
            hall.write({
                'seats': hall.seats + 5
            })

    def reserve_all(self):
        self.hall_ids.write({
            'reserved': True
        })

    def pin_newer_movies(self):
        # self.movie_ids.filtered_domain([('premiere_date', '>=',  fields.date.today())])
        filtered_records = self.movie_ids.filtered(lambda record: record.premiere_date >= fields.date.today())
        for index in filtered_records.ids:
            self.hall_ids.update({
                'movie_ids': [Command.link(index)]
            })

    def create_playbill(self):
        halls = self.hall_ids.search([('cinema_id', '=', self.id)])
        movies = self.movie_ids.search([('cinema_ids', 'in', self.id)])
        halls_alias = halls.mapped(lambda record: f"{record.name} - {record.seats} seats\n")
        movies_alias = movies.mapped(lambda record: f"{record.name}: premier date: {record.premiere_date},"
                                                    f" deadline date: {record.deadline_date}\n")
        text = f"Our cinema {self.name} has such halls:\n{''.join(halls_alias)}{''.join(movies_alias)} "
        self.write({
            'description': text
        })

    def action_show_vip_halls(self):
        vip_halls = self.env['cinema.cinema.hall'].search([('cinema_id', '=', self.id), ('name', 'ilike', 'Vip')])
        action = self.env.ref('cinema.action_cinema_cinema_hall').read()[0]
        action['domain'] = [('id', 'in', vip_halls.ids)]
        return action

    def add_3d_hall(self):
        if (
            hall_ids := self.env['cinema.cinema.hall']
            .search([('cinema_id', '=', self.id), ('name', 'not like', '3D')])
            .ids
        ):
            hall = self.env['cinema.cinema.hall'].browse(choice(hall_ids))
            hall.name += ' - 3D'
        else:
            self.update({
                'hall_ids': [(fields.Command.create({
                    'name': '3D hall',
                    'seats': randint(1, 100)
                }))]
            })

    @api.depends('hall_ids')
    def _compute_total_seats(self):
        for theater in self:
            theater.total_seats = sum(theater.hall_ids.mapped('seats'))

    @api.depends('hall_ids')
    def _compute_vip_halls(self):
        for hall in self:
            hall.vip_halls = self.env['cinema.cinema.hall'].search_count([('cinema_id', '=', hall.id),
                                                                          ('name', 'ilike', 'Vip')])

    @api.model
    def create(self, vals):
        if vals.get('cinema_code', _("C№000") == _("C№000")):
            vals['cinema_code'] = self.env['ir.sequence'].next_by_code('cinema.code') or _("C№000")
        return super(CinemaCinema, self.with_context(default_number_of_stuff=100)).create(vals)

    @api.onchange('state')
    def _state_opened_status(self):
        for cinema in self:
            if cinema.state == 'open' and cinema.halls_count  == 0:
                raise UserError("The cinema without halls cannot be opened. Please add at least one hall.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_closed(self):
        for cinema in self:
            if cinema.state == 'open':
                raise UserError("Can't delete an opened cinema!\nClose it before.")

    def close_for_lunch(self):
        cinemas_to_close = self.search([('state', '=', 'open')])
        cinemas_to_close.write({
            'state': 'close'
        })

    def open_after_lunch(self):
        cinemas_to_open = self.search([('state', '=', 'close'),
                                        ('halls_count', '>', '0'),
                                        ('movies_count', '>', '0')])
        cinemas_to_open.write({
          'state': 'open'
        })

    def update_closed_cinema_stuff(self):
        cinemas_to_update = self.search([('state', '=', 'close')])
        cinemas_to_update.write({
            'number_of_stuff': 0
        })

    def cron_close_cinema(self):
        _logger.info("Close cinemas")
        total_time = fields.Datetime.now().hour
        if total_time >= 20 or total_time <= 8:
            records = self.search([('state', '!=', 'close')])
            records.state = 'close'

    group_fields_notebook = fields.Boolean(
        string='Notebook',
        default=True)

    description_visible = fields.Boolean(default=True)
    halls_visible = fields.Boolean(default=True)
    movies_visible = fields.Boolean(default=True)
