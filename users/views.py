from .serializers import UserSerializer, RegistrationSerializer, UserLoginSerializer, ChangePasswordSerializer
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string 
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework import viewsets 
from .models import UserProfileModel
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


# Create your views here.
class UsersViewSet(viewsets.ModelViewSet):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)
            except ValidationError:
                return Response({"error": "old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationAPIView(APIView):
    
    serializer_class = RegistrationSerializer

    def post(self,request,format=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/users/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('users/confirm_email.html',{'confirm_link' : confirm_link})
            email = EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()
            return Response("Check your mail for confirmation",status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)

    except (User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('register')
    else:
        return redirect('register') 






class UserLoginView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username,password=password)

            if user:
                token,_ = Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({'token':token.key,'user_id':user.id},status=status.HTTP_200_OK)
            else:
                if not User.objects.filter(username=username).exists():
                    return Response({'errors': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                return Response({'errors':'Incorrect password'},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        print(request)
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')