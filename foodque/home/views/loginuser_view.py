from home.models.users import Users
from home.api.serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([]) 
def login_user(request):
    useremail = request.data.get('useremail')
    password = request.data.get('password')
    
    try:
        user = Users.objects.get(useremail=useremail)
    except Users.DoesNotExist:
        return Response({'message': 'Invalid email or password'}, status=status.HTTP_200_OK)
    
    if user.password == password:  # If passwords are hashed, use check_password(password, user.password)
        request.session['user_id'] = user.id
        request.session.save()  # Manually save the session
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'user': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
        
    else:
        return Response({'message': 'Invalid email or password'}, status=status.HTTP_200_OK) 