from django.db import models
from .users import Users
class Profile(models.Model):
    GOALS_CHOICES = [
        ('LW', 'Lose Weight'),
        ('GW', 'Gain Weight'),
        ('MW', 'Maintain Weight'),
        ('IF', 'Improve Fitness'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    EXERCISE_LEVEL_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('A', 'Active'),
    ]

    profile_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    user_age = models.IntegerField()
    user_weight = models.FloatField(help_text="Weight in kilograms")
    user_height = models.FloatField(help_text="Height in inches")
    user_goals = models.CharField(max_length=2, choices=GOALS_CHOICES, default='IF')
    user_exercise_level = models.CharField(max_length=1, choices=EXERCISE_LEVEL_CHOICES, default='M')
    user_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        db_table = 'profile'
        app_label = 'home'