from rest_framework import serializers

from EndUserManagement.models import Message, MessageMedia

class MessageMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageMedia
        fields = ['ID']

class MessageListResponseSerializer(serializers.ModelSerializer):
    Media = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ['UpdatedAt', 'Case']

    def get_Media(self, obj):
        if obj.HasMedia:
            media = MessageMedia.objects.filter(Message = obj)
            return MessageMediaSerializer(media, many=True).data
        return []