from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from api.serializers import ClaimsObtainPairSerializer

# Create your views here.
class ClaimsTokenObtainPairView(TokenObtainPairView):
    serializer_class = ClaimsObtainPairSerializer