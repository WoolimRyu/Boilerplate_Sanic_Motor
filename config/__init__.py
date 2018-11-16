import os

from sanic.log import LOGGING_CONFIG_DEFAULTS


# configuration features
PROFILE = os.getenv('PROFILE', 'prod')

MONGO_CONF_SONNY = {
    'host': 'localhost',
    'port': 27017,
    'replica_set': '',
    'auth_db': 'admin',
    'username': '',
    'password': '',
    'database': 'sonny'
}

LOG_PATH = os.getenv('LOG_PATH', './logs')
LOGGING_CONFIG = LOGGING_CONFIG_DEFAULTS.copy()
LOGGING_CONFIG['loggers'].update({
    'trace': {
        'level': 'INFO',
        'handlers': ['trace']
    }
})
LOGGING_CONFIG['handlers'].update({
    'trace': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'formatter': 'trace',
        'when': 'W0',
        'backupCount': 12,
        'filename': f'{LOG_PATH}/trace.log'
    }
})
LOGGING_CONFIG['formatters'].update({
    'trace': {
        'format': '%(asctime)s.%(msecs)03d [%(levelname)s] [%(marker)s] - [footprint=%(footprint)s] %(data)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
        'class': 'logging.Formatter'
    }
})


# helpers
def mongo_uri(conf):
    conf_copy = conf.copy()
    creds = '{username}:{password}@'.format(**conf)
    conf_copy.update({'creds': creds if creds != ':@' else ''})
    return 'mongodb://{creds}{host}:{port}/{database}?authSource={auth_db}&replicaSet={replica_set}'.format(**conf_copy)


# load and override conf features from the specific conf file by profile
from importlib import import_module
profile_conf = import_module(f'.{PROFILE}', __name__)
for key in filter(lambda x: not x.startswith('__'), dir(profile_conf)):
    locals()[key] = getattr(profile_conf, key)
