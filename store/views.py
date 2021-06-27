from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from store.serializers import OrderSerializer, PetSerializer
from django.core.exceptions import ObjectDoesNotExist
from .models import Pet, Order


class PetListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of pets or create new one
    """
    serializer_class = PetSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned pets to a given user,
        by filtering against a `breed` query parameter in the URL.
        """
        queryset = Pet.objects.all()
        breed = self.request.query_params.get('breed')
        if breed is not None:
            queryset = queryset.filter(breed=breed)
        return queryset


class PetDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a pet
    """
    serializer_class = PetSerializer
    queryset = Pet.objects.all()


class OrderListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of orders or create new one
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        try:
            request_body = self.request.data
            pet = Pet.objects.get(pk=request_body.get('pet'))
            serializer.save(pet=pet)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Pet not found")
