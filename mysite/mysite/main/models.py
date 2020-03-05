from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserBuf(models.Model):
    user_name = models.CharField(max_length=20)
    user_pass = models.CharField(max_length=20)


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)