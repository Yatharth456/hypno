from django.db import models
from django.contrib.auth.models import AbstractUser  
from user_auth.manager import UserManager

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=250, blank=True)
    email = models.EmailField(('email_address'), unique=True, max_length = 200)  
    password = models.CharField(max_length=100, blank=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()


