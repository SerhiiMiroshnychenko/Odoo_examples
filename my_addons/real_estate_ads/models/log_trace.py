import logging
import colorlog

TRACE = 35
logging.addLevelName(TRACE, 'TRACE')


def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE):
        self._log(TRACE, message, args, **kwargs)


logging.Logger.trace = trace
formatter = colorlog.ColoredFormatter(
    fmt='%(message_log_color)s%(message)s%(reset)s',
    secondary_log_colors={
        'message': {
            'TRACE': 'red'
        }
    }
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
tracer = logging.getLogger(__name__)
tracer.addHandler(handler)

_trace = tracer.trace
