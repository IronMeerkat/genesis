from django.shortcuts import render

from rest_framework import mixins, generics


class APIView(mixins.ListModelMixin,
              mixins.CreateModelMixin,
              mixins.UpdateModelMixin,
              mixins.DestroyModelMixin,
              generics.GenericAPIView):
    pass