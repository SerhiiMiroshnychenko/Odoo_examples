import logging
_logger = logging.getLogger()


def migrate(cr, version):
    """
    Creating a temporary field to store the total_seats data
    """
    _logger.info('PRE-migration!')
    cr.execute('ALTER TABLE cinema_cinema ADD COLUMN temp_total_seats integer')
    cr.execute("UPDATE cinema_cinema SET temp_total_seats=total_seats")
