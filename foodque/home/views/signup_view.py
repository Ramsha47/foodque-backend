from home.models.users import Users
from home.api.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse


@api_view(['POST'])
def signup_user(request):
    username = request.data.get('username')
    useremail = request.data.get('useremail')
    password = request.data.get('password')
    # Debug print statements
    print(f"Received data: username={username}, useremail={useremail}, password={password}")

    if Users.objects.filter(username=username).exists():
        return Response({'message': 'Username already taken'}, status=status.HTTP_200_OK)
    if Users.objects.filter(useremail=useremail).exists():
        return Response({'message': 'Email already registered'}, status=status.HTTP_200_OK)

    user = Users.objects.create(username=username, useremail=useremail, password=password)
    user.save()
    return Response({'message': 'Your account is created. You can login now.'}, status=status.HTTP_201_CREATED)