from .models import Transaction
from users.models import UserProfileModel
from pet.models import Pet
from adoption.models import Adoption
from .serializers import TransactionSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal

# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self,request,*args,**kwargs):
        # print('requse-user',request.user) #goes
        data = request.data
        amount = Decimal(data.get('amount',0))
        transaction_type = data.get('transaction_type')
        user_profile = UserProfileModel.objects.get(user = request.user)
        pet_id = data.get('id')
        # print(user_profile) #goes
        balance_after_transaction  = user_profile.balance
        print('bal',user_profile.balance)


        if transaction_type == 'deposit':
            if amount > 0:
                balance_after_transaction += amount
            else:
                return Response({'error':'deposit money cannot be negative'},status=status.HTTP_400_BAD_REQUEST)


        elif transaction_type == 'adoption':
            try:
                pet = Pet.objects.get(id=pet_id)
            except Pet.DoesNotExist:
                return Response({'error':'pet not found'},status=status.HTTP_404_NOT_FOUND)
            
            if user_profile.balance < pet.price:
                return Response({'error':'Insufficient balance to adopt the pet'},status=status.HTTP_400_BAD_REQUEST)

            amount = pet.price
            balance_after_transaction -= amount

            adopt = Adoption.objects.create(user=user_profile,pet=pet)

        # updating user balance in user profile
        user_profile.balance = balance_after_transaction
        user_profile.save()

        transaction_data = {
            'user':user_profile.id,
            'amount':amount,
            'transaction_type':transaction_type,
            'balance_after_transaction': balance_after_transaction,
        }

        serializer = self.get_serializer(data=transaction_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    
