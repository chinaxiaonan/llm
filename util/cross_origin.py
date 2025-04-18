from werkzeug.datastructures import Headers
from flask import Response


class MyResponse(Response):
    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')

        origin = ('Access-Control-Allow-Origin', '*')
        methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        allow_headers = ('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')
        if headers:
            headers.add(*origin)
            headers.add(*methods)
            headers.add(*allow_headers)
        else:
            headers = Headers([origin, methods, allow_headers])
        kwargs['headers'] = headers
        return super(MyResponse, self).__init__(response, **kwargs)