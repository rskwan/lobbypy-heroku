from socketio.namespace import BaseNamespace as Namespace
from flask import current_app

class BaseNamespace(Namespace):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('request', None)
        if request:
            self.ctx = current_app.request_context(request.environ)
            self.ctx.push()
            current_app.preprocess_request()
            del kwargs['request']
        super(BaseNamespace, self).__init__(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        self.ctx.pop()
        super(BaseNamespace, self).disconnect(*args, **kwargs)
