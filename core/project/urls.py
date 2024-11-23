from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/292332c24a3027a360ab3761d3918a2e20dbac71/admin/', admin.site.urls),
    path('api/v1/', include('core.clients.urls'))
]
