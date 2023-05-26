import random

from django_project.celery import app
from celery import shared_task
from .models import Car, Location

@shared_task
def sample_task():
    print('Запущено обновление локации машин')
    pks = Location.objects.values_list('pk', flat=True)
    cars = Car.objects.all()
    for car in cars:
        car.location = Location.objects.order_by("?").first()
        car.save(update_fields=["location"])
    return "Обновлены локации машин"