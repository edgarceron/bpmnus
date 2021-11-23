"""Serializer for projects module"""
from rest_framework import serializers
from .models import Projects

class ProjectsSerializer(serializers.ModelSerializer):
    """Serializer for Projects model"""
    class Meta:
        """Meta data for the model serializer"""
        model = Projects
        fields = ['id','name','desc','creation_date']

    def create(self, validated_data):
        obj = Projects(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.desc = validated_data['desc']
        instance.creation_date = validated_data['creation_date'].split("T")[0]
        instance.save()
        return instance
