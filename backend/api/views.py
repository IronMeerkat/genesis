import datetime

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin ,DestroyModelMixin
from django.contrib.auth.models import User
from api.serializers import MessageSerializer, UserSerializer
from api.models import Message
from djongo.models import Q


# Create your views here.


class MessageView(CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin, generics.GenericAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        This is an overridden GenericAPIView function. 
        It ensures that only messages that the user is associated with are visible to said user.
        """
        queryset = super(MessageView, self).get_queryset()
        return queryset.filter(Q(sender=self.request.user) | Q(recepient=self.request.user))

    def get(self, request, *args, **kwargs):
        """
        One GET method for all GET operations. Append the URL positive integer to retrieve a single message,
        or with a mailbox string to get that particular list of messages. Default (unappended) will return the list
        of unread and undeleted incoming messages. Important note: Individually-retrieved messages will marked as
        read by the retrieving user (user will be appended to message.read), otherwise the method is "safe".
        """
        if kwargs.get('pk'):
            message = self.get_object()
            message.read.add(self.request.user)
            return self.retrieve(request, *args, **kwargs)
        elif kwargs.get('mode') == 'all':
            pass  # No filtration beyond what's mandatory in get_queryset
        elif not kwargs.get('mode'):
            self.queryset = self.filter_queryset(self.get_queryset().filter(
                Q(recepient=self.request.user) & ~Q(read=request.user) & ~Q(deleted=request.user)))
            #   Default GET operation. User's incoming mail, excluding read and deleted messages.
        else:
            self.queryset = self.get_queryset().filter(**{kwargs.get('mode'): self.request.user})
        return self.list(request, *args, **kwargs)

    def post(self, request):
        """
        Used for sending messages via POST operation. It creates a message instance with the sending user as the
        sender, and the recepient looked up by username. The request requires a logged in user's token in the header,
        and a recepient, title, and body as a JSON string in the request's data payload.
        """
        request.data['recepient'] = User.objects.get(username=request.data['recepient'])
        message = Message(sender=request.user, **request.data)
        message.save()
        serializer = MessageSerializer(message)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def delete(self, request, *args, **kwargs):
        """
        Append the URL with the message's id and call DELETE. The user will be added to the message instance's
        'deleted' field.
        """
        message = self.get_object()
        message.deleted.add(self.request.user)
        return Response(status=204)


class UserView(CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin, generics.GenericAPIView):
    
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = User(
            username=request.data['username']
        )
        user.set_password(request.data['password'])
        user.save()

        return Response(status=201)