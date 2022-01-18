"""Serializer for diagrams module"""
from rest_framework import serializers
from .models import Diagrams

class DiagramsSerializer(serializers.ModelSerializer):
    """Serializer for Diagrams model"""
    class Meta:
        """Meta data for the model serializer"""
        model = Diagrams
        fields = ['id', 'project', 'name', 'desc', 'xml', 'propierties', 'creation_date']

    def create(self, validated_data):
        obj = Diagrams(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.project = validated_data['project']
        instance.name = validated_data['name']
        instance.desc = validated_data['desc']
        instance.xml = validated_data['xml']
        instance.propierties = validated_data['propierties']
        instance.creation_date = validated_data['creation_date']
        instance.save()
        return instance
