"""
URL configuration for foodque project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from home.views.RegisteredUser_list_view import RegisteredUsers_list
from home.views.UserProfile_view import UsersProfile_list
from home.views.UserProfile_view import getUserProfile
from home.views.Meals_view import Meals_list
from home.views.Feedback_view import Feedback_list
from home.views.signup_view import signup_user
from home.views.loginuser_view import login_user
from home.views.createprofile_view import create_profile
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
     path('admin/', admin.site.urls),
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
     path('Users/',RegisteredUsers_list),
     path('Profile/',UsersProfile_list),
     path('Meals/',Meals_list),
     path('Feedback/',Feedback_list),
     path('register/', signup_user, name='signup'),
     path('login/', login_user, name='login'),
     path('create-profile/', create_profile, name='create_profile'),
     path('get-user-profile/', getUserProfile, name='getUserProfile'),
]
