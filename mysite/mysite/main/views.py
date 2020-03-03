from django.shortcuts import render
from django.http import HttpResponse
from .models import User
# Create your views here.

def homepage(request):
    return render(request=request,
                  template_name='templates/main/home.html',
                  context = {"users": User.objects.all})

