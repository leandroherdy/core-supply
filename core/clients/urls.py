from django.urls import path

from .views import process_data_view

urlpatterns = [
    path('clients/<path:external_url>/', process_data_view, name='process_data'),
]
