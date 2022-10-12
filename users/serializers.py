
from django.db import models
from rest_framework import serializers
from users.models import NewUser
from rest_framework.validators import UniqueValidator



class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=NewUser.objects.all())])
    user_name = serializers.CharField(required=True, validators=[
        UniqueValidator(queryset=NewUser.objects.all())])
    phone = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'password','phone' )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UpdateUserSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = NewUser
        fields = ('first_name', 'last_name', 'about' )
    
