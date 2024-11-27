from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PetSerializer
from .models import Pet
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get_queryset(self):
        queryset = super().get_queryset() # it return all object of pet
        species = self.request.query_params.get('species')
        if species:
            queryset = queryset.filter(species=species)
        return queryset
    
    def perform_create(self, serializer):
        user_profile = self.request.user.profile  
        serializer.save(owner=user_profile)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, *args, **kwargs)