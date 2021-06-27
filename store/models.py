from django.db import models


class Pet(models.Model):
    class PetType(models.TextChoices):
        DOG = ('dog', 'Dog')

    class DogBreed(models.TextChoices):
        ROTTWEILER = ('rottweiler', 'Rottweiler')
        BULLDOG = ('bulldog', 'Bulldog')

    type = models.CharField(
        max_length=50,
        choices=PetType.choices,
        default=PetType.DOG
    )
    breed = models.CharField(
        max_length=50,
        choices=DogBreed.choices,
        default=DogBreed.BULLDOG
    )
    age = models.PositiveIntegerField(default=1)


class Order(models.Model):
    class Currency(models.TextChoices):
        USD = ('USD', 'United States dollar')
        EUR = ('EUR', 'Euro')
        EGP = ('EGP', 'Egyptian pound')

    pet = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name='orders')
    price = models.DecimalField(
        decimal_places=2,
        default=0.0,
        max_digits=10
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD
    )
