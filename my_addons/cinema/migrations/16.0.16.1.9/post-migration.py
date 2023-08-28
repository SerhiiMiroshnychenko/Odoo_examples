import logging
from datetime import timedelta
from odoo import api, SUPERUSER_ID
_logger = logging.getLogger()


def migrate(cr, version):
    """
   The total_seats data from temporary field stored to the new total_seats field
   temporary field removed from the table

   Set deadline_date as the day after premiere_date for each cinema.cinema.movie record
   """
    # Set total_seats field
    _logger.info('POST-migration!')
    cr.execute('UPDATE cinema_cinema SET total_seats=temp_total_seats')
    cr.execute('ALTER TABLE cinema_cinema DROP COLUMN temp_total_seats')

    # Set deadline_date field
    env = api.Environment(cr, SUPERUSER_ID, {})
    movies = env['cinema.cinema.movie'].search([])
    for movie in movies:
        if movie.premiere_date:
            movie.write({'deadline_date': movie.premiere_date + timedelta(days=1)})
