from django.db import models
from .users import Users
from .meals import Meals


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE, default=1)
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback from {self.user.username} for {self.meal.meal_name}"
class Meta:
        db_table = 'feedback'
        app_label = 'home'