from rest_framework import serializers

from EndUserManagement.models import Case

from . import CustomModelSerializer

class CustomFileListField(serializers.ListField):
    def __init__(self, **kwargs):
        # Allowing the file lists to be empty
        kwargs['allow_empty'] = kwargs.get('allow_empty', True)
        super().__init__(**kwargs)

class CustomVoiceRecordingListField(serializers.ListField):
    def __init__(self, **kwargs):
        # Allowing the file lists to be empty
        kwargs['allow_empty'] = kwargs.get('allow_empty', True)
        super().__init__(**kwargs)

class CaseCreateValidator(CustomModelSerializer):
    File = CustomFileListField(child = serializers.FileField())
    VoiceRecording = CustomVoiceRecordingListField(child = serializers.FileField())

    class Meta:
        model = Case
        # Status is not required because it will be OPEN initially
        # User is not required because it is always logged in user for the end user
        exclude = ['User', 'Status', 'UpdatedAt', 'CreatedAt']

    # This function makes the CaseTypes and PsnTypes values list if they are not.
    # Many to many field input should be a list of IDs as default for DRF serializers.
    def to_internal_value(self, data):
        if 'CaseTypes' in data and not isinstance(data['CaseTypes'], list):
            data['CaseTypes'] = [data['CaseTypes']]
        if 'PsnTypes' in data and not isinstance(data['PsnTypes'], list):
            data['PsnTypes'] = [data['PsnTypes']]
        return super(CaseCreateValidator, self).to_internal_value(data)