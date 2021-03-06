from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserBuf
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
# Create your views here.

@login_required(login_url = 'login')
@admin_only
def homepage(request):
    return render(request=request,
                  template_name='templates/main/home.html',
                  context = {"users": UserBuf.objects.all})

def contactus(request):
    return render(request=request,
                  template_name='templates/main/contactus.html',
                  context = {"users": UserBuf.objects.all})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name = 'user')
            user.groups.add(group)

            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="templates/main/register.html",
                          context={"form": form})

    form = NewUserForm
    return render(request = request,
                  template_name = "templates/main/register.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

@unauthenticated_user
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "templates/main/login.html",
                    context={"form":form})



