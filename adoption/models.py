from django.db import models
from users.models import UserProfileModel
from pet.models import Pet

# Create your models here.

STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]


class Adoption(models.Model):
    user = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE, related_name='adoptions')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adoption_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.user.username} adopt {self.pet.name}'
    

class Review(models.Model):
    user = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    ratings = models.CharField(max_length=10,choices=STAR_CHOICES)