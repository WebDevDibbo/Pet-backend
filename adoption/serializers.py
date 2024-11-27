from rest_framework import serializers
from .models import Adoption, Review



class AdoptionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='pet.name', read_only=True)
    price = serializers.CharField(source='pet.price', read_only=True)
    image = serializers.CharField(source='pet.image', read_only=True)
    age = serializers.CharField(source='pet.age', read_only=True)

    class Meta:
        model = Adoption
        fields = "__all__"



class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.user.username',read_only=True)
    class Meta:
        model = Review
        fields = "__all__"