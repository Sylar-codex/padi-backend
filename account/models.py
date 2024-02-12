from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class UserProfile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_profile')
    image =models.ImageField(upload_to="profile_image/", null=True,blank=True)
    description = models.CharField(max_length=100, validators=[MinLengthValidator(1,"This field cannot be empty")], default="You are using Padi")

    def __str__(self):
        return f'{self.user.username}'
