from rest_framework import serializers

from EndUserManagement.models import User

def createUserListResponseSerializer(role = 'EndUser'):
    if role == 'Admin':
        return UserListReponseAdminSerializer

class UserListReponseAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'