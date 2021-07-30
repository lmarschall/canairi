from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('measurements', views.measurements, name='measurements')
]