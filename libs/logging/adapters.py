import logging
import json
import uuid
import inspect


class FootprintTraceAdapter(logging.LoggerAdapter):
    def trace(self, evt, *args, **kwargs):
        msg, kwargs = self.process(evt, kwargs)
        self.logger.info(msg, *args, **kwargs)

    def process(self, msg, kwargs):
        request = self.extra.get('request')
        return '', {
            'extra': {
                'marker': inspect.stack()[2][0].f_code.co_name,
                'footprint': request.headers.get('X-Chappie-Footprint', f'mirage-{uuid.uuid4().hex}'),
                'data': json.dumps({'logEvent': msg, 'logData': kwargs['data']})
            }
        }
