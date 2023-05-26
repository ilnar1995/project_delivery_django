import django
from django.urls import path, include
from django.contrib.auth import views

from rest_framework.routers import SimpleRouter


from .views import CargoModelListUpdateViewSet, CarModelViewSet, CargoModelRetrieveCreateViewSet

# ## cargo_router/
# cargo_router = SimpleRouter()
# cargo_router.register(r"cargo", CargoModelListUpdateViewSet)
## car_router/
car_router = SimpleRouter()
car_router.register(r"car", CarModelViewSet)
from .views import *

urlpatterns = [
    # path("", include(cargo_router.urls)),
    path("", include(car_router.urls)),
    path('get_cargos/', CargoModelListUpdateViewSet.as_view({'get': 'list'}), name='get_cargo'),
    path('create_cargo/', CargoModelRetrieveCreateViewSet.as_view({'post': 'create'}), name='createcargo'),
    path('update_cargo/<int:pk>/', CargoModelListUpdateViewSet.as_view({'patch': 'partial_update'}), name='update_cargo'),
    path('get_cargo/<int:pk>/', CargoModelRetrieveCreateViewSet.as_view({'get': 'retrieve'}), name='retrieve_cargo'),
    path('delete_cargo/<int:pk>/', CargoModelListUpdateViewSet.as_view({'delete': 'destroy'}), name='destroy_cargo'),
    # path('', UsersListView.as_view(), name='home'),
    # path('registrationcode/<int:pk>/', verivicate_code, name='registration_code'),
    # path('reset_email/<slug:id>/', reset_email_views, name='reset_email'),
    # path('registration/', RegisterUser.as_view(), name='registration'),
    # path('accounts/login/', LoginUser.as_view(), name='login'),
    # path('accounts/logout/', logout_user, name='logout'),
    # path("accounts/password_reset/", UserPasswordResetView.as_view(), name="password_reset"),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/<slug:id>/', AccountDetailView.as_view(), name="prifile"),
    # path('edit/<slug:id>/', EditUserProfile.as_view(), name="edit"),
]
