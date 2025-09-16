from django.urls import path
from . import views

app_name = 'places'
urlpatterns = [
    path('', views.index, name='index'),
    path('places/', views.places_list, name='places_list'),
    path('place/<int:place_id>/', views.place_detail, name='place_detail'),
    path('add/', views.add_place, name='add_place'),
    path('random/', views.random_place, name='random_place'),
]