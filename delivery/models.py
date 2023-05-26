from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator

class Location(models.Model):
    zip = models.CharField(_('Address'), primary_key=True, max_length=5, validators=[MinLengthValidator(5)])
    city = models.CharField(_('City'), max_length=100)
    state_name = models.CharField(_('State'), max_length=100)
    lat = models.FloatField(_('LATITUDE'))
    lng = models.FloatField(_('LONGITUDE'))
    id = models.IntegerField()

    def __str__(self):
        return (self.lat, self.lng)

    class Meta:
        db_table = "app_delivery_location"
        ordering = ["id"]

    def save(self):
        "Get last value of Code and Number from database, and increment before save"
        top = Location.objects.order_by('-id')[0]
        if not self.id:
            self.id = top.id + 1
        super(Location, self).save()

class Cargo(models.Model):
    location_pick_up = models.ForeignKey(Location, verbose_name=_("Location pick-up"), on_delete=models.CASCADE, related_name="cargo_from_locations")
    location_delivery = models.ForeignKey(Location, verbose_name=_("Location delivery"), on_delete=models.CASCADE, related_name="cargo_to_locations")
    description = models.TextField(verbose_name=_("Template text"), default="")
    weight = models.IntegerField(_("Weight"), validators=[MaxValueValidator(1000), MinValueValidator(1)])

    def __str__(self):
        return self.description

    class Meta:
        db_table = "app_delivery_cargo"
        ordering = ["id"]

class Car(models.Model):
    car_number = models.CharField(_('Address'), max_length=5, validators=[MinLengthValidator(5)], unique=True)
    location = models.ForeignKey(Location, verbose_name=_("Location"), on_delete=models.CASCADE, related_name="cars")
    carrying_capacity = models.IntegerField(_("Carrying capacity"), validators=[MaxValueValidator(1000), MinValueValidator(1)])

    def __str__(self):
        return self.car_number

    class Meta:
        db_table = "app_delivery_car"
        ordering = ["id"]

# Create your models here.
