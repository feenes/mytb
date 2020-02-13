def get_log_settings(basedir='', basename='log', level='DEBUG', **kwargs):
    log_settings = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)-8s %(asctime)s %(name)s:%(lineno)d '
                          '%(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(module)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            # root loggers
            '': {
                'level': level,
                'handlers': ['console'],
                'propagate': False,
            },
        }
    }
    return log_settings
