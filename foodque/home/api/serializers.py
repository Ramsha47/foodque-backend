from rest_framework import serializers
from home.models.users import Users
from home.models.profile import Profile
from home.models.meals import Meals
from home.models.feedback import Feedback
from djoser.serializers import UserCreateSerializer

# User = get_user_model()

class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model=Users
        fields=('id', 'email', 'name', 'password')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        managed = True
        fields = ['profile_id', 'user', 'user_age', 'user_weight', 'user_height', 'user_goals', 'user_exercise_level', 'user_gender']

class MealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meals
        managed = True
        fields = ['meal_id', 'user', 'meal_name', 'ingredient_list']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        managed = True
        fields = ['feedback_id', 'user', 'meal', 'feedback']

