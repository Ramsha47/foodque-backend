from home.models.profile import Profile
from home.api.serializers import ProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse

@api_view(['GET', 'POST'])
def UsersProfile_list(request):
    if request.method == 'GET':
        usersprofile = Profile.objects.all()
        serializer = ProfileSerializer(usersprofile, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)