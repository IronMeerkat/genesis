from django.urls import path
from api.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(r'messages/', MessageView.as_view()),
    path(r'messages/<int:pk>', MessageView.as_view()),
    path(r'messages/<slug:mode>', MessageView.as_view()),
    path(r'users/', UserView.as_view()),
]