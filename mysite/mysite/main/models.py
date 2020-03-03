from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserBuf(models.Model):
    user_name = models.CharField(max_length=20)
    user_pass = models.CharField(max_length=20)


