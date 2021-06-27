from django.urls import path
from . import views

urlpatterns = [
    path(
        'pets/',
        views.PetListCreateAPIView.as_view(),
        name='api-pet-list'
    ),
    path(
        'pets/<int:pk>/',
        views.PetDetailsAPIView.as_view(),
        name='api-pet-details',
    ),
    path(
        'orders/',
        views.OrderListCreateAPIView.as_view(),
        name='api-order-list'
    ),

]
