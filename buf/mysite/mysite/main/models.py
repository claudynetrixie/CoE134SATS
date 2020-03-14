from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# class User(AbstractUser):
#     USER_TYPE_CHOICES = (
#         (1, 'parent'),
#         (2, 'teacher'),
#         (3, 'admin'),
#     )
#     user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
class User(AbstractUser):
    is_teacher = models.BooleanField(default = False)
    is_parent = models.BooleanField(default = False)

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    year_level = models.CharField(max_length=30)
    section = models.CharField(max_length=30)
    id_number = models.IntegerField()
    email = models.CharField(max_length=30)