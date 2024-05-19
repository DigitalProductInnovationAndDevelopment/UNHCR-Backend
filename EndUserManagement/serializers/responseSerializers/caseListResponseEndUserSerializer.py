from rest_framework import serializers

from EndUserManagement.models import Case

def createCaseListResponseEndUserSerializer(role = 'EndUser'):
    if role == 'EndUser':
        return CaseListResponseEndUserSerializer
    return CaseListResponseAdminSerializer
    

class CaseListResponseEndUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class CaseListResponseAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'