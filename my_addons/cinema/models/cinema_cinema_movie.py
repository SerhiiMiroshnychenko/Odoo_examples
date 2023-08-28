import logging
from odoo import _, fields, models, api
from datetime import timedelta
_logger = logging.getLogger(__name__)


class CinemaCinemaMovie(models.Model):
    _name = "cinema.cinema.movie"
    _description = "A model representing movies"
    _order = "name"
    _rec_name = 'description'
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Movie name already exists!"),
        ('check_dates', 'CHECK (deadline_date >= premiere_date)', "Deadline date must be later than premiere date.")
    ]

    active = fields.Boolean(default=True)
    name = fields.Char(required=True, copy=False, default=lambda self: _('New'))
    premiere_date = fields.Date(default=lambda self: fields.Date.today())
    deadline_date = fields.Date()
    color = fields.Integer()
    description = fields.Text(copy=False)
    cinema_ids = fields.Many2many('cinema.cinema')
    cinema_count = fields.Integer(compute='_compute_cinema_count', store=True)
    is_over = fields.Boolean(compute='_compute_is_over')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    def write_description(self):
        for movie in self:
            if not movie.description:
                movie.description = f'This is "{movie.name}" movie.'

    def copy(self, default=None):
        return super().copy({'name': f"{self.name} (copy)"})

    def _compute_is_over(self):
        for movie in self:
            movie.is_over = bool(movie.deadline_date and movie.deadline_date < fields.Date.today())

    @api.onchange("premiere_date")
    def _onchange_premiere_date(self):
        for movie in self:
            if not movie.deadline_date:
                movie.deadline_date = movie.premiere_date + timedelta(days=14)
            movie.check_and_set_deadline()

    @api.depends('cinema_ids')
    def _compute_cinema_count(self):
        for movie in self:
            movie.cinema_count = self.env['cinema.cinema'].search_count([('movie_ids', 'in', movie.id)])

    def copy(self, default=None):
        self_color = self._context['color']
        return super().copy({'name': f"{self.name} (copy)", 'color': self_color})

    def copy_with_color(self):
        self.with_context(color=self.color + 1).copy()

    @api.model
    def create(self, vals):
        if vals.get('name', _("New")) == _("New"):
            vals['name'] = self.env['ir.sequence'].next_by_code('cinema.movie') or _("New")
        new_description = self.env['ir.config_parameter'].sudo().get_param('cinema.auto_description')
        is_description = vals.get('description')
        if new_description and not is_description:
            vals['description'] = new_description
        return super(CinemaCinemaMovie, self).create(vals)

    def archive_old_movie(self):
        _logger.info("Start archive")
        movies = self.search([('deadline_date', '<', fields.Date.today())])
        movies.write({
            'active': False
        })
        return True

    def add_movie_to_open_cinemas(self):
        if movie := self.env['cinema.cinema.movie'].browse(self.env.context.get('active_id')):
            open_cinemas = self.env['cinema.cinema'].search([('state', '=', 'open'), ('halls_count', '>', 0)])
            cinemas_to_add = open_cinemas.filtered(lambda c: movie not in c.movie_ids)
            cinemas_to_add.movie_ids = [(4, movie.id)]

    def check_and_set_deadline(self):
        if limit := int(self.env['ir.config_parameter'].sudo().get_param('cinema.days_limit')):
            for movie in self:
                if (movie.deadline_date - movie.premiere_date).days > limit:
                    movie.deadline_date = movie.premiere_date + timedelta(days=limit)

    @api.model
    def create_demo_movie_after_module_installing(self):
        self.create(dict(name='DemoMovie', premiere_date=fields.Date.today()))

    @api.model
    def create_movie_with_name_after_module_installing(self, name):
        self.create(dict(name=name, premiere_date=fields.Date.today()))
