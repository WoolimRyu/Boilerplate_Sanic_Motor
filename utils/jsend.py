from sanic import response


class JSendResponse(object):
    SUCCESS = 'success'
    FAIL = 'fail'
    ERROR = 'error'

    def __init__(self, status_code=200):
        self.status_code = status_code

    def success(self, data=None):
        return response.json({'status': self.SUCCESS, 'data': data or {}}, status=self.status_code)

    def fail(self, data=None):
        return response.json({'status': self.FAIL, 'data': data or {}}, status=self.status_code)

    def error(self, message=''):
        return response.json({'status': self.ERROR, 'message': message}, status=self.status_code)
