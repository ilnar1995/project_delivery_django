import random

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from . import models
from .models import Car, Location
from geopy.distance import geodesic


class CargoBaseSerializer(serializers.ModelSerializer):
    location_pick_up = serializers.SlugRelatedField(queryset=models.Location.objects.all(), slug_field='zip', read_only=False, many=False)
    location_delivery = serializers.SlugRelatedField(queryset=models.Location.objects.all(), slug_field='zip', read_only=False, many=False)

    class Meta:
        model = models.Cargo
        fields = ['location_pick_up', 'location_delivery']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            if self.context['request'].method in ['POST', 'PUT']:
                self.fields['location_pick_up'] = serializers.PrimaryKeyRelatedField(queryset=models.Location.objects.all())
                self.fields['location_delivery'] = serializers.PrimaryKeyRelatedField(queryset=models.Location.objects.all())
        except KeyError:
            pass

class CargoCreateRetrieveSerializer(CargoBaseSerializer):

    class Meta:
        model = models.Cargo
        fields = '__all__'

class CargoListSerializer(CargoBaseSerializer):
    kolichestvo = serializers.SerializerMethodField()
    class Meta:
        model = models.Cargo
        fields = ['location_pick_up', 'location_delivery', 'kolichestvo']

    def get_kolichestvo(self, obj):
        mile = 450.0
        gradus = mile / 54
        user_latitude = obj.location_pick_up.lat #18.16586
        user_longitude = obj.location_pick_up.lng #-66.93716
        user_location = (user_latitude, user_longitude)
        cars = Car.objects.values('location__lng', 'location__lat').filter(location__lat__range=(user_latitude - gradus, user_latitude + gradus),
                                            location__lng__range=(user_longitude - gradus, user_longitude + gradus))

        count = 0
        for car in cars:
            if geodesic(user_location, (car.get('location__lat'), car.get('location__lng'))).miles <= mile:
                count += 1

        return count


class CargoPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cargo
        fields = [
            'description',
            'weight'
        ]

class CarSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(queryset=models.Location.objects.all(), slug_field='zip', read_only=False, many=False)

    class Meta:
        model = models.Car
        fields = '__all__'



    def __init__(self, *args, **kwargs):
        super(CarSerializer, self).__init__(*args, **kwargs)

        try:
            if self.context['request'].method in ['POST', 'PUT']:
                self.fields['location'] = serializers.PrimaryKeyRelatedField(queryset=models.Location.objects.all())
        except KeyError:
            pass

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = '__all__'