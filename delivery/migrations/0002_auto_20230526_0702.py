# Generated by Django 4.1 on 2023-05-26 07:02
# Generated by Django 4.1 on 2023-05-25 09:03
import csv
import random
import string

from django.db import migrations
from django_project.settings import BASE_DIR


def load_csv(apps):
    # запись из CSV файла в БД локации
    Location = apps.get_model('delivery', 'Location')
    print('')
    print('Подождите идет запись из CSV файла в БД')
    fhand = open(str(BASE_DIR) + '/delivery/uszips.csv')
    reader = csv.reader(fhand)
    count = 0
    for row in reader:
        if count == 0:
            pass
        else:
            Location.objects.create(zip=row[0], lat=row[1], lng=row[2], city=row[3], state_name=row[5], id=count)
        count += 1


def add_default(apps, schema_editor):
    # Запись в БД дефолтных данных
    load_csv(apps)
    Cars = apps.get_model('delivery', 'Car')
    Location = apps.get_model('delivery', 'Location')
    Cargo = apps.get_model('delivery', 'Cargo')
    print('Подождите. Идет генерация 20 случайных машин')
    for i in range(20):
        random_nomber = str(random.randint(1000, 9999)) + random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        Cars.objects.update_or_create(car_number=random_nomber, location=Location.objects.order_by("?").first(),
                            carrying_capacity=random.randint(1, 1000))
    print('Подождите. Идет генерация 10 случайных грузов')
    for i in range(10):
        letters = string.ascii_lowercase
        random_length = random.randint(20, 100)
        random_description="".join(random.choice(letters) for i in range(random_length))
        Cargo.objects.create(location_pick_up=Location.objects.order_by("?").first(),
                             location_delivery=Location.objects.order_by("?").first(),
                             weight=random.randint(1, 1000), description=random_description)


class Migration(migrations.Migration):
    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default),
    ]