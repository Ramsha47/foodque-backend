from django.urls import path,include
from . import views  # Import views from the same directory

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
