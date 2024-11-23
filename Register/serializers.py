from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django import forms
from .models import MyUser
from django.contrib.auth.password_validation import validate_password

class MyUserSerializer(ModelSerializer):
    password1 = serializers.CharField(write_only=True, label="Mot de passe", style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, label="Confirmez le mot de passe", style={'input_type': 'password'})
    
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'password1', 'password2', 'image']
        extra_kwargs = {'password': {'write_only': True}}
          
    def validate(self, data):
        # Vérifier que les mots de passe correspondent
        password1 = data.get("password1")
        password2 = data.get("password2")
        
        if password1 != password2:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        
            # Appliquer la validation Django standard des mots de passe
        validate_password(password1)  # Vérifie la conformité avec les critères d'authentification
        return data  

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2', None)
        
        user = MyUser.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            image=validated_data.get('image', None),
        )
        return user