from rest_framework import serializers
from .models import UserProfileModel
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError 
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email') 

    class Meta:
        model = UserProfileModel
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        # Extract user-related data
        user_data = validated_data.pop('user', {})
        user = instance.user  # Access the related User instance

        # Update the User fields if provided
        user.username = user_data.get('username', user.username)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()  # Save changes to the User instance

        # No changes to the UserProfileModel
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data.get('new_password') != data.get('confirm_password'):
            raise ValidationError("New passwords do not match.")
        return data
    
    def save(self,user):
        old_password = self.validated_data['old_password']
        new_password = self.validated_data['new_password']

        if not user.check_password(old_password):
            raise ValidationError('Old password is incorrect')
        
        user.set_password(new_password)
        user.save()


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Already Exists")
        return value
    
    def validate_password(self,value):
        validate_password(value)
        return value
    
    def validate(self,data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            return serializers.ValidationError({'password':"Password do not match"})
        return data
    
    def create(self,validated_data):
        validated_data.pop('confirm_password')

        user = User(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )
        user.set_password(validated_data['password'])

        user.is_active = False
        user.save()
        UserProfileModel.objects.create(user=user)
        return user
    


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
