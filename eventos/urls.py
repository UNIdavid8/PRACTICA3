from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_principal, name='panel_principal'),
    path('crear/<str:tipo>/', views.crear_evento_builder, name='crear_evento'),
    path('clonar/<int:evento_id>/', views.clonar_evento_prototype, name='clonar_evento'),
    path('configuracion/', views.panel_configuracion, name='panel_configuracion'),
]