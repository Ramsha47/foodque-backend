from django.db import models
import logging

class Users(models.Model):
    
    username = models.CharField(max_length=50, unique=True)
    useremail = models.EmailField(verbose_name='email', max_length=255, unique=True)
    password = models.CharField(max_length=128)
    
    def save(self, *args, **kwargs):
        logger = logging.getLogger(__name__)
        if not self.pk:  # Check if the instance is being saved for the first time
            logger.info(f'New User ID: {self.id}')  # Print the newly assigned user_id
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'users'
        app_label = 'home'