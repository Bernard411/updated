from django.urls import path
from . import views

urlpatterns = [
    path('welcome', views.home, name='home'),
    path('ai_doctor/', views.ai_doctor, name='ai_doctor'),
    path('health_records/', views.health_records, name='health_records'),
    path('geo_mapping/', views.geo_mapping, name='geo_mapping'),
    path('medicine/', views.medicine, name='medicine'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
