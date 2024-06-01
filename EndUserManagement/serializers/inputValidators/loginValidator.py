from rest_framework import serializers

from EndUserManagement.models import User

class LoginValidator(serializers.Serializer):
    
    # This is the clear text password. We can do validation here (Min. char count, must have special chars etc.)
    Password = serializers.CharField(max_length = 20)
    EmailAddress = serializers.EmailField()