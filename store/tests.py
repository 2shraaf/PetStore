from django.urls import reverse
from rest_framework import status
from store.models import Order, Pet
from django.test import TestCase
from rest_framework.test import APITestCase

"""
Testing Models
"""


class PetTestCase(TestCase):
    def test_pet(self):
        self.assertEquals(
            Pet.objects.count(),
            0
        )
        Pet.objects.create(breed=Pet.DogBreed.BULLDOG)
        Pet.objects.create(breed=Pet.DogBreed.ROTTWEILER)
        self.assertEquals(
            Pet.objects.count(),
            2
        )
        self.assertEquals(
            Pet.objects.filter(breed=Pet.DogBreed.ROTTWEILER).count(),
            1
        )
        self.assertEquals(
            Pet.objects.filter(breed=Pet.DogBreed.BULLDOG).count(),
            1
        )


class OrderTestCase(TestCase):
    def test_order(self):
        self.assertEquals(
            Pet.objects.count(),
            0
        )
        self.assertEquals(
            Order.objects.count(),
            0
        )
        pet = Pet.objects.create(breed=Pet.DogBreed.BULLDOG)
        Order.objects.create(pet=pet)
        self.assertEquals(
            Pet.objects.count(),
            1
        )
        self.assertEquals(
            Order.objects.count(),
            1
        )


"""
Testing Endpoints
"""
dummy_pet_data = {
    'type': Pet.PetType.DOG,
    'breed': Pet.DogBreed.BULLDOG,
    'age': 2
}


class PetListCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api-pet-list')

    def test_create_pet(self):
        self.assertEquals(
            Pet.objects.count(),
            0
        )
        response = self.client.post(
            self.url, data=dummy_pet_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            Pet.objects.count(),
            1
        )
        pet = Pet.objects.first()

        self.assertEquals(
            pet.type,
            dummy_pet_data['type']
        )
        self.assertEquals(
            pet.breed,
            dummy_pet_data['breed']
        )
        self.assertEquals(
            pet.age,
            dummy_pet_data['age']
        )

    def test_get_pet_list(self):
        pet = Pet.objects.create(
            type=dummy_pet_data['type'], breed=dummy_pet_data['breed'], age=dummy_pet_data['age'])
        self.assertEquals(
            Pet.objects.count(),
            1
        )
        response = self.client.get(self.url)
        response_json = response.json()
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            len(response_json),
            1
        )
        data = response_json[0]
        self.assertEquals(
            data['type'],
            pet.type
        )
        self.assertEquals(
            data['breed'],
            pet.breed
        )
        self.assertEquals(
            data['age'],
            pet.age
        )

    def test_get_pet_list_dog_breed(self):
        Pet.objects.create(
            type=dummy_pet_data['type'], breed=Pet.DogBreed.BULLDOG, age=dummy_pet_data['age'])
        Pet.objects.create(
            type=dummy_pet_data['type'], breed=Pet.DogBreed.ROTTWEILER, age=dummy_pet_data['age'])

        self.assertEquals(
            Pet.objects.count(),
            2
        )
        response = self.client.get(self.url, {'breed': Pet.DogBreed.BULLDOG})
        response_json = response.json()
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            len(response_json),
            1
        )
        data = response_json[0]
        self.assertEquals(
            data['type'],
            dummy_pet_data['type']
        )
        self.assertEquals(
            data['breed'],
            Pet.DogBreed.BULLDOG
        )
        self.assertEquals(
            data['age'],
            dummy_pet_data['age']
        )


class PetDetailsAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.pet = Pet(
            type=dummy_pet_data['type'], breed=dummy_pet_data['breed'], age=dummy_pet_data['age'])
        self.pet.save()
        self.url = reverse('api-pet-details',
                           kwargs={'pk': self.pet.pk})

    def test_get_pet_details(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        self.assertEquals(
            data['id'],
            self.pet.id
        )
        self.assertEquals(
            data['type'],
            self.pet.type
        )
        self.assertEquals(
            data['breed'],
            self.pet.breed
        )
        self.assertEquals(
            data['age'],
            self.pet.age
        )

    def test_update_pet(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        data = response.json()
        data['age'] = 2
        data['breed'] = Pet.DogBreed.ROTTWEILER
        response = self.client.put(self.url, data=data, format='json')
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.pet.refresh_from_db()
        self.assertEquals(
            self.pet.breed,
            data['breed']
        )
        self.assertEquals(
            self.pet.age,
            data['age']
        )

    def test_delete_pet(self):
        self.assertEquals(
            Pet.objects.count(),
            1
        )
        response = self.client.delete(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEquals(
            Pet.objects.count(),
            0
        )


class OrderListCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api-order-list')

    def test_create_order(self):
        self.assertEquals(
            Order.objects.count(),
            0
        )
        pet = Pet.objects.create(
            type=dummy_pet_data['type'], breed=dummy_pet_data['breed'], age=dummy_pet_data['age'])
        self.assertEquals(
            Pet.objects.count(),
            1
        )
        dummy_order_data = {
            'pet': pet.id,
            'price': 22.0,
            'currency': 'EGP'

        }
        response = self.client.post(
            self.url, data=dummy_order_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            Order.objects.count(),
            1
        )

        order = Order.objects.first()

        self.assertEquals(
            order.price,
            dummy_order_data['price']
        )
        self.assertEquals(
            order.currency,
            dummy_order_data['currency']
        )
        self.assertEquals(
            order.pet,
            pet
        )

    def test_create_wrong_order(self):
        """
        Test creating order with wrong pet id
        """
        self.assertEquals(
            Order.objects.count(),
            0
        )
        dummy_order_data = {
            'pet': 11,
            'price': 22.0,
            'currency': 'EGP'

        }
        response = self.client.post(
            self.url, data=dummy_order_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            Order.objects.count(),
            0
        )

    def test_get_order_list(self):
        self.assertEquals(
            Order.objects.count(),
            0
        )
        pet = Pet.objects.create(
            type=dummy_pet_data['type'], breed=dummy_pet_data['breed'], age=dummy_pet_data['age'])
        self.assertEquals(
            Pet.objects.count(),
            1
        )
        dummy_order_data = {
            'pet': pet.id,
            'price': 22.0,
            'currency': 'EGP'

        }
        Order.objects.create(
            pet=pet, price=dummy_order_data['price'], currency=dummy_order_data['currency'])
        self.assertEquals(
            Order.objects.count(),
            1
        )
        response = self.client.get(self.url)
        response_json = response.json()
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            len(response_json),
            1
        )
        data = response_json[0]
        self.assertEquals(
            float(data['price']),
            dummy_order_data['price']
        )
        self.assertEquals(
            data['currency'],
            dummy_order_data['currency']
        )
        self.assertEquals(
            data['pet']['id'],
            pet.id
        )
