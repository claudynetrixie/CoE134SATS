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
    is_student = models.BooleanField(default = False)
    is_teacher = models.BooleanField(default = False)