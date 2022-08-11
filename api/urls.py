from django.urls import path, include
from rest_framework import routers

from api.views import ClientViewset, ContractViewset

app_name = 'api'

router = routers.SimpleRouter()

router.register('clients', ClientViewset, basename='client')
router.register('contracts', ContractViewset, basename='contract')

urlpatterns = [
    path('', include(router.urls))
]
