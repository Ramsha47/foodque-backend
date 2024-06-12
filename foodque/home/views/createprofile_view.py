from home.models.users import Users
from home.api.serializers import ProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse


@api_view(['POST'])
def create_profile(request):
    user_id = request.session.get('id')
    print("User ID from request data:", user_id)
    if not user_id:
        return Response({'message': 'User ID not provided,','user_id':user_id}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['user'] = user_id  # Assuming the field in Profile model is named 'user'

    serializer = ProfileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Profile created successfully!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)