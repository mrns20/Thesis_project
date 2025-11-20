from django.urls import path
from .views import register
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),  # POST username, password -> returns token
]