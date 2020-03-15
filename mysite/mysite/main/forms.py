from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import User, Teacher, Parent


# class NewUserForm(UserCreationForm):
#     #type = forms.CharField(required=True)
#
#     type = forms.CharField()
#
#     email = forms.EmailField(required=True)
#
#     class Meta:
#         model = User
#         fields = ("username", "email", "type", "password1", "password2")
#
#     def save(self, commit=True):
#         user = super(NewUserForm, self).save(commit=False)
#         user.email = self.cleaned_data["email"]
#         user.type = self.cleaned_data["type"]
#         if commit:
#             user.save()
#         return user

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(TeacherSignUpForm, self).save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
            Teacher.objects.create(user=user)
        return user


class ParentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(ParentSignUpForm, self).save(commit=False)
        user.is_parent = True
        if commit:
            user.save()
            Parent.objects.create(user=user)
        return user
