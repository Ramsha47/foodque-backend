from home.models.users import Users
from home.api.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse


@api_view(['GET', 'POST'])
def RegisteredUsers_list(request):
    if request.method == 'GET':
        registerusers = Users.objects.all()
        serializer = UserSerializer(registerusers, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
