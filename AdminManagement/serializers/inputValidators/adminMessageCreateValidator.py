from rest_framework import serializers

from EndUserManagement.models import Message

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

class AdminMessageCreateValidator(CustomModelSerializer):
    File = CustomFileListField(child = serializers.FileField())
    VoiceRecording = CustomVoiceRecordingListField(child = serializers.FileField())
    
    class Meta:
        model = Message
        exclude = ['ID', 'Case', 'HasMedia', 'SenderRole', 'CreatedAt', 'UpdatedAt']
    

