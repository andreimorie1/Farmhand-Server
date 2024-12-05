from .models import Farmer
from rest_framework import serializers

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['firstname', 'lastname', 'password']
        extra_kwargs = {'password': {'write_only': True}}
