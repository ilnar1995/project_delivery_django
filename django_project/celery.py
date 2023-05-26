import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = Celery('django_project')  # в скобках имя приложения
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# # CELERY_BEAT_SCHEDULE = {
# #     "sample_task": {
# #         "task": "delivery.tasks.sample_task",
# #         "schedule": crontab(minute="*/1"),
# #     },
# # }
# #
#
# # заносим таски в очередь
# app.conf.beat_schedule = {
#     'every': {
#         'task': 'delivery.tasks.repeat_order_make',
#         'schedule': crontab(),# по умолчанию выполняет каждую минуту, очень гибко
#     },                                                              # настраивается
#
# }