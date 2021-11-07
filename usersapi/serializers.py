from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        """Meta data for the model serializer"""
        model = User
        fields = ['id','username','password','email', 'first_name', 'last_name']

    def create(self, validated_data):
        obj = User(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.password = validated_data['password']
        instance.email = validated_data['email']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.save()
        return instance
