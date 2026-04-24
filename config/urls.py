from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('eventos/', include('eventos.urls')), # Conectamos las rutas de tu app
]