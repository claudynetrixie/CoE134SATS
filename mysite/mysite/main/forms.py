from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import User, Teacher, Parent

from django.forms import ModelForm, DateInput
from .models import Event, Contact_Message
from django.utils import timezone

import datetime, pytz

from phonenumber_field.formfields import PhoneNumberField


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "middle_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(TeacherSignUpForm, self).save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
            Teacher.objects.create(user=user)
        return user


class ParentSignUpForm(UserCreationForm):
    phone = PhoneNumberField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "middle_name", "last_name", "password1", "password2", "phone")

    def save(self, commit=True):
        user = super(ParentSignUpForm, self).save(commit=False)
        user.is_parent = True
        if commit:
            user.save()
            Parent.objects.create(user=user)
        return user


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)


class ContactForm(ModelForm):
    class Meta:
        model = Contact_Message
        fields = '__all__'
        exclude = ['date']

    def save(self, commit=True):
        message = super(ContactForm, self).save(commit=False)
        message.date = datetime.datetime.now(pytz.timezone("Asia/Singapore"))
        print(message.date)
        if commit:
            message.save()
        return message
