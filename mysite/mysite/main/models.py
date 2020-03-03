from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_pass = models.CharField(max_length=20)


