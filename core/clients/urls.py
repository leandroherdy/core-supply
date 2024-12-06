from django.urls import path

from .views import get_filtered_clients as get_filtered_clients_v1

urlpatterns = [
    path('clients/', get_filtered_clients_v1, name='get_filtered_clients'),
]
