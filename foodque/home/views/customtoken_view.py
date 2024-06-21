# home/customtokenviews.py
from rest_framework_simplejwt.views import TokenObtainPairView
from home.api.serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
