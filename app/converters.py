from werkzeug.routing import BaseConverter


class MrnConverter(BaseConverter):
    regex = r"\d{8}"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return str(value)
