from django.shortcuts import render
from django.http import HttpResponse
from .models import UserBuf
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def homepage(request):
    return render(request=request,
                  template_name='templates/main/home.html',
                  context = {"users": UserBuf.objects.all})

def register(request):
    form = UserCreationForm
    return render(request = request,
                  template_name = "templates/main/register.html",
                  context={"form":form})

