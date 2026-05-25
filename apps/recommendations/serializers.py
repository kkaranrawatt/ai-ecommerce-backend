from rest_framework import serializers
from .models import UserProductInteraction

class UserProductInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserProductInteraction
        fields= '__all__'
        