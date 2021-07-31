from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('measurements/get', views.get_measurements, name='get_measurements'),
    path('measurements/post', views.post_measurements, name='post_measurements')
]