from django.shortcuts import render

from rest_framework import mixins, generics


class APIView(mixins.RetrieveModelMixin,
              mixins.ListModelMixin,
              mixins.CreateModelMixin,
              mixins.UpdateModelMixin,
              mixins.DestroyModelMixin,
              generics.GenericAPIView):
    """
    Aggregates all the mixin classes"""
    pass