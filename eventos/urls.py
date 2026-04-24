from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import EventoViewSet


router = DefaultRouter()
router.register(r'api/v1/eventos', EventoViewSet, basename='api_eventos')

urlpatterns = [

    path('', views.panel_principal, name='panel_principal'),
    path('crear/<str:tipo>/', views.crear_evento_builder, name='crear_evento'),
    path('clonar/<int:evento_id>/', views.clonar_evento_prototype, name='clonar_evento'),
    path('configuracion/', views.panel_configuracion, name='panel_configuracion'),
    

    path('', include(router.urls)), 
]