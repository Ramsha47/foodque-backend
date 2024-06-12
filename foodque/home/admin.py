from django.contrib import admin
from .models.users import Users
from .models.profile import Profile
from .models.meals import Meals
from .models.feedback import Feedback

# Register your models here.
admin.site.register(Users)
admin.site.register(Profile)
admin.site.register(Meals)
admin.site.register(Feedback)
