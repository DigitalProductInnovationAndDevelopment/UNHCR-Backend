from rest_framework import serializers

from EndUserManagement.models import Case

class AdminCaseCreateReponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'