from rest_framework import serializers

from EndUserManagement.models import User

class SignUpValidator(serializers.ModelSerializer):
    Password = serializers.CharField(max_length = 20)

    class Meta:
        model = User
        exclude = ['password']