from home.models.meals import Meals
from home.api.serializers import MealsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse


@api_view(['GET', 'POST'])
def Meals_list(request):
    if request.method == 'GET':
        recommendedMeals = Meals.objects.all()
        serializer = MealsSerializer(recommendedMeals, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        serializer = MealsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
