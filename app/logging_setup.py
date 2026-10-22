import logging
import sys

from flask import g, has_request_context, request


class RequestContextFilter(logging.Filter):
    def filter(self, record):
        record.user = "-"
        record.path = "-"
        if has_request_context():
            user = getattr(g, "user", None)
            record.user = user["username"] if user is not None else "anonymous"
            record.path = request.path
        return True


def configure_logging(app):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s user=%(user)s path=%(path)s %(message)s")
    )
    handler.addFilter(RequestContextFilter())
    app.logger.handlers = [handler]
    app.logger.setLevel(logging.INFO)
