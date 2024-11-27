from django.db import models
from users.models import UserProfileModel


# Create your models here.

SPECIES_CHOICES = [
    ('dog', 'Dog'),
    ('cat', 'Cat'),
    ('bird', 'Bird'),
]
GENDER_CHOICES= [
    ('male','Male'),
    ('female','Female')
]

class Pet(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    species = models.CharField(max_length=50,choices=SPECIES_CHOICES)
    age = models.PositiveIntegerField()
    description = models.TextField()
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='pet/images/')
    owner = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE, related_name='pet')

    def __str__(self):
        return self.name