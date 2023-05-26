from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import CargoCreateRetrieveSerializer, CarSerializer, CargoPatchSerializer, CargoListSerializer
from geopy.distance import geodesic
from .models import Car, Cargo, Location
from rest_framework import views


class CargoModelListUpdateViewSet(ModelViewSet):
    queryset = Cargo.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ["get", "patch", "delete", ]
    # serializer_class = CargoSerializer


    def get_queryset(self):
        if max_weight := self.request.query_params.get("max_weight"):
            self.queryset = self.queryset.filter(weight__lte=max_weight)
        return self.queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(name="max_weight", description="Filter by weight", required=False, type=int),
            OpenApiParameter(name="max_car_distance", description="Filter by weight", required=False, type=int),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # def get_serializer(self, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return super(CargoModelViewSet, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.action in ('list',):
            return CargoListSerializer
        return CargoPatchSerializer


class CargoModelRetrieveCreateViewSet(ModelViewSet):
    queryset = Cargo.objects.all()
    http_method_names = ["post", "get", ]
    serializer_class = CargoCreateRetrieveSerializer

    def get_queryset(self):
        instance = Cargo.objects.all()
        return instance

    # def get_serializer(self, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return super(CargoModelViewSet, self).get_serializer(*args, **kwargs)


class CarModelViewSet(ModelViewSet):
    queryset = Car.objects.all()
    http_method_names = ["patch"]
    serializer_class = CarSerializer

    def get_queryset(self):
        instance = Car.objects.all()
        return instance


    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(CarModelViewSet, self).get_serializer(*args, **kwargs)
