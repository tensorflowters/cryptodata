# Set default logging handler to avoid "No handler found" warnings.
import logging

try:  # Python 3.10+
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


logging.getLogger(__name__).addHandler(NullHandler())
