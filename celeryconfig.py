BROKER_URL = 'amqp://admin:Brightc0ve1@bc1.local/bc1.local'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1'
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
#CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'US/Eastern'
CELERY_ENABLE_UTC = True
broker_api = 'http://admin:Brightc0ve1@bc1.local:15672/api/'
