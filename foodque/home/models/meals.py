from django.db import models
from .users import Users

class Meals(models.Model):
    meal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)
    ingredient_list = models.TextField()

    def __str__(self):
        return self.meal_name
    
    class Meta:
        db_table = 'meals'
        app_label = 'home'