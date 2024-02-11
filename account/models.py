from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_profile')
    image =models.ImageField
    description = models.CharField(max_length=100, min_length=1)
