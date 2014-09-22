"""
serializers.py

Contains the serializer classes used for the API.
"""

from rest_framework import serializers
from studies.models import Data


class DataSerializer(serializers.Serializer):
    """
    A serializer for an object representing a command for adding a new record
    into the database.
    """
    
    class Meta:
        model = Data