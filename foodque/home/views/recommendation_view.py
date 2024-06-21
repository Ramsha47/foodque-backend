# foodque/home/views/recommendation_view.py
import os
import sys
import pickle
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Add the current directory to sys.path for importing recommend_pickle if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
recommender_dir = os.path.join(current_dir, '..', 'recommender')
if recommender_dir not in sys.path:
    sys.path.append(recommender_dir)

print("Dir: ", recommender_dir)

# Load the serialized functions from the file
# dump_file_path = os.path.join(recommender_dir, 'recommender_function.pkl')
dump_file_path = 'recommender_function.pkl'
print("Dir: ", dump_file_path)
with open(dump_file_path, 'rb') as f:
    loaded_functions = pickle.load(f)



# Extract the function from the loaded functions
recommendation = loaded_functions['recommender']

@api_view(['POST'])
@permission_classes([])
def get_recommendations(request):
    if request.method == 'POST':
        try:
            data = request.data
            userid = data['userid']
            user_info = data['user_info']
            calorie_range = data.get('calorie_range', None)

            # Call the recommendation function
            loaded_user_info, loaded_recipes, coldstart_flag = recommendation(userid, user_info, calorie_range)

            # Prepare the response
            if coldstart_flag == "User doesn't exist":
                response = {
                    'status': 'error',
                    'message': 'User profile is necessary to make personalized recommendations. Please create an account.'
                }
            elif coldstart_flag == "Not enough Userdata":
                response = {
                    'status': 'warning',
                    'message': 'Not enough user reviews. Popular meals are being recommended to collect reviews.',
                    'recommendations': loaded_recipes.to_dict('records') if loaded_recipes is not None else []
                }
            else:
                response = {
                    'status': 'success',
                    'user_info': loaded_user_info,
                    'recommendations': loaded_recipes.to_dict('records') if loaded_recipes is not None else []
                }

            return JsonResponse(response)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
