"""
masters serializers
"""
from rest_framework import serializers
from masters.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    User Profile Serializer
    """

    class Meta:        
        model = UserProfile
        fields = "__all__"
