from rest_framework import serializers

from EndUserManagement.models import User

def createUserFetchResponseSerializer(role = 'EndUser'):
    if role == 'Admin':
        return UserFetchResponseAdminSerializer
    return UserFetchResponseEndUserSerializer

class UserFetchResponseAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserFetchResponseEndUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'