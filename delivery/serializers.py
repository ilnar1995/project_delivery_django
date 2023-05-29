from typing import List

from rest_framework import serializers
from . import models
from .models import Car, Location
from geopy.distance import geodesic


class CargoBaseSerializer(serializers.ModelSerializer):
    location_pick_up = serializers.SlugRelatedField(queryset=models.Location.objects.all(), slug_field='zip', read_only=False, many=False)
    location_delivery = serializers.SlugRelatedField(queryset=models.Location.objects.all(), slug_field='zip', read_only=False, many=False)

    class Meta:
        model = models.Cargo
        fields = ['location_pick_up', 'location_delivery']

class CargoCreateRetrieveSerializer(CargoBaseSerializer):
    distances_of_cars = serializers.SerializerMethodField()

    class Meta:
        model = models.Cargo
        fields = '__all__'

    def get_distances_of_cars(self, obj)-> List[float]:
        user_latitude = obj.location_pick_up.lat #18.16586
        user_longitude = obj.location_pick_up.lng #-66.93716
        user_location = (user_latitude, user_longitude)
        cars = Car.objects.values('location__lng', 'location__lat').all()
        cars_list = []
        for car in cars:
            distance = geodesic(user_location, (car.get('location__lat'), car.get('location__lng'))).miles
            cars_list.append(round(distance, 2))
        return cars_list

class CargoListSerializer(CargoBaseSerializer):
    distances_of_close_cars = serializers.SerializerMethodField()
    class Meta:
        model = models.Cargo
        fields = ['location_pick_up', 'location_delivery', 'distances_of_close_cars']

    def get_distances_of_close_cars(self, obj)-> int:
        mile = 450.0
        if new_mile := self.context.get('request').query_params.get('max_car_distance', None):
            mile = float(new_mile)
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


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = '__all__'