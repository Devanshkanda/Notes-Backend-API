from rest_framework import serializers
from django.contrib.auth.models import User
import re
from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'



class LoginSerializer(serializers.ModelSerializer):

    user_username = serializers.CharField()
    user_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_username', 'user_password']
    

    def validate(self, validated_data):
        print("i am in validated func of login serializer")
        username = validated_data.get('user_username')
        password = validated_data.get('user_password')

        print(validated_data)

        if username is None or password is None:
            raise serializers.ValidationError("Username or password not entered")
        
        if len(username) < 3 or len(password) < 8:
            raise serializers.ValidationError("Username or password length must be minimum 8 characters")
        
        return validated_data


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']

    
    def create(self, validated_data):

        print("i am in create func of serializer")

        user = User.objects.create(
            username = validated_data.get('username'),
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            email = validated_data.get('email')
        )

        user.set_password(validated_data.get('password'))
        user.save()
        return user

        
    def validate(self, validated_data):

            print("i am in validate func of serializer")
            print(validated_data.get('username'))
            print(validated_data.get('password'))
            print(validated_data.get('first_name'))
            print(validated_data)


            username: str = validated_data.get('username')
            password: str = validated_data.get('password')
            email: str = validated_data.get('email')
            first_name: str = validated_data.get('first_name')
            last_name: str = validated_data.get('last_name')

            regex = re.compile('[^a-zA-Z0-9\s]')

            if username is None or password is None:
                raise serializers.ValidationError("Username or password not entered")
            
            if first_name is None:
                raise serializers.ValidationError("First name not entered. first name is required")
            
            if last_name is None:
                raise serializers.ValidationError("Last name not entered. last name is required")
            
            if len(username) < 3 or len(password) < 8:
                raise serializers.ValidationError("Username or password length must be minimum 8 characters")
            
            if (email is None):
                raise serializers.ValidationError("Email not Entered. Email is required")
            
            if ("@" not in email) or (not email.endswith(".com")):
                raise serializers.ValidationError("Invalid email entered")
            
            if regex.search(first_name) or regex.search(last_name):
                raise serializers.ValidationError("First name or last name should only contains aplphabet characters")
            
            return validated_data


class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notes
        fields = ['notes_title', 'notes_desc', 'is_done', 'user']

    

    def validate(self, validated_data):

        notes_title = validated_data.get('notes_title')
        notes_desc = validated_data.get('notes_desc')
        user = validated_data.get('user')

        if notes_title is None or notes_desc is None:
            raise serializers.ValidationError("Notes title or desc missing")
        
        if user is None:
            raise serializers.ValidationError("User not mentioned")
        
        return validated_data
    

    def update(self, instance, validated_data):
        instance.notes_title = validated_data.get('notes_title')
        instance.notes_desc = validated_data.get('notes_desc')
        instance.is_done = validated_data.get('is_done')

        instance.save()
        return instance