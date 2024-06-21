from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

def my_view(request):
    try:
        user, _ = JWTAuthentication().authenticate(request)
        print(f"Authenticated user: {user}")  # Check if user object is correctly retrieved
        return Response({'message': 'Authenticated successfully!'})
    except AuthenticationFailed as e:
        print(f"Authentication failed: {e}")
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
