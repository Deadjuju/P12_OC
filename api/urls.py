from django.urls import path, include
from rest_framework import routers

from api.views import ClientViewset

app_name = 'api'

router = routers.SimpleRouter()

router.register('client', ClientViewset, basename='client')

urlpatterns = [
    path('', include(router.urls))
]
