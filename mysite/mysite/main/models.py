from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    section_name = models.CharField(max_length=30)


class Student(models.Model):
    STATUS = (
        ('GR1', 'GR1'),
        ('GR2', 'GR2'),
        ('GR3', 'GR3'),
    )
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    year_level = models.CharField(max_length=30, choices=STATUS)
    section = models.CharField(max_length=30)
    id_number = models.IntegerField()
    email = models.CharField(max_length=30)
    parent = models.ManyToManyField(Parent)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Log(models.Model):
    id_number = models.ForeignKey(Student, on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()
    location = models.CharField(max_length=30)

    @property
    def get_html_url(self):
        url = reverse('main:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.location} </a>'


class Employee(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('main:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'