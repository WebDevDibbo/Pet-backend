from .models import Adoption, Review
from .serializers import AdoptionSerializer, ReviewSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from pet.models import Pet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import UserProfileModel

# Create your views here.
class AdoptionViewSet(viewsets.ModelViewSet):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print('self.req',self.request.user)
        print('self.reqprofile',self.request.user.profile)
        return Adoption.objects.filter(user=self.request.user.profile)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)

    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        data = request.data
        
        # user_profile = request.user.profile
        try:
           user_profile = request.user.profile
        except UserProfileModel.DoesNotExist:
           return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

        pet_id = data.get('pet')
        if not pet_id:
            return Response({'error': 'Pet ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({'error':'pet not found'},status=status.HTTP_404_NOT_FOUND)
        
        adopted = Adoption.objects.filter(user=user_profile,pet=pet).exists()

        if not adopted:
            return Response({'error':'you can only review the pets that you have adopted'},status=status.HTTP_400_BAD_REQUEST)
        
        review_data = {
            'review_text':data.get('review_text'),
            'ratings':data.get('ratings'),
            'user': user_profile.id,
            'pet': pet.id,
        }

        serializer = self.get_serializer(data=review_data)
        if serializer.is_valid():
            serializer.save(user=user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pet_id = self.kwargs.get('pet_id')
        # pet__id: Uses the __ (double underscore) to specify that you want to filter based on the id field of the related Pet model
        return Review.objects.filter(pet__id=pet_id)
    
    def list(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)