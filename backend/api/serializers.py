from api.models import Message
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    """Safe return of a user model
    """
    class Meta:
        model = User
        fields = ['id', 'username']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'username': {
                'read_only': True
            },
        }


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(default=serializers.CurrentUserDefault())
    recepient = UserSerializer()

    class Meta:
        model = Message
        depth = 1
        fields = ['id', 'sender', 'recepient', 'timestamp', 'title', 'body']


