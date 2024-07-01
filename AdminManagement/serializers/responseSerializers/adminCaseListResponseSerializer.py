from rest_framework import serializers

from EndUserManagement.models import Case

class AdminCaseListReponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'