import logging
import colorlog

CHECK = 25
logging.addLevelName(CHECK, ' PRINT:')


def check(self, message, *args, **kwargs):
    if self.isEnabledFor(CHECK):
        self._log(CHECK, message, args, **kwargs)


logging.Logger.check = check
formatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s%(bg_yellow)s%(levelname)s %(reset)s %(message_log_color)s%(message)s %(reset)s',
    log_colors={' PRINT:': 'black'},
    secondary_log_colors={
        'message': {
            ' PRINT:': 'blue'
        }
    }
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
_logger = logging.getLogger(__name__)
_logger.addHandler(handler)

_print = _logger.check
