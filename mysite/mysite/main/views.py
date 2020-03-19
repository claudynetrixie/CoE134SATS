from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from datetime import date

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
# from .forms import NewUserForm
from .filters import StudentFilter, LogFilter

from .models import User, Student, Teacher, Parent, Log

from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Employee
from .serializers import employeeSerializer

# Create your views here.
class employeeList(APIView):

    def get(self, request):
        employee1 = Employee.objects.all()
        serializer = employeeSerializer(employee1, many = True)
        return Response(serializer.data)

    def post(self, request):
        employee1 = Employee.objects.all()[0]
        serializer = employeeSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status = status.HTTP_400_BAD_REQUEST)









def homepage(request):
    return render(request=request,
                  template_name='templates/main/home.html')


def welcome(request):
    return render(request=request,
                  template_name='templates/main/welcome.html')


def welcome_parent(request):
    return render(request=request,
                  template_name='templates/main/welcome_parent.html')


def list_students(request):
    students = Student.objects.all()
    myFilter = StudentFilter(request.GET, queryset=students)
    stud = myFilter.qs

    return render(request=request,
                  context={"students": stud, "myFilter": myFilter, "filter": myFilter},
                  template_name='templates/main/listofstudents.html')


def stud_attendance(request):
    students = Student.objects.all()
    logs = Log.objects.all()
    #get a list of students that teacher is handling
    if request.user.is_authenticated and request.user.is_teacher:
        #list of students
        stu_list = Student.objects.filter(section = Teacher.objects.get(user_id = request.user.id).section_name)
        print(stu_list)
        print(stu_list[0].first_name)
        id_num = []
        for stu in stu_list:
            id_num.append(stu.id)
        #get the logs of all those students
        for id in id_num:
            if(id == id_num[0]):
                log_b = Log.objects.filter(id_number=id)
            else:
                log_b = log_b | Log.objects.filter(id_number=id)
        logs = log_b




    myFilter = LogFilter(request.GET, queryset= logs)
    log = myFilter.qs


    #get the num of days queried
    print(request.GET)
    after =request.GET['date_after'].split("-", 3)
    before = request.GET['date_before'].split("-", 3)
    d1 = date( int(after[0]) , int(after[1]), int(after[2]))
    d0 = date(int(before[0]), int(before[1]), int(before[2]))
    num_days = (d0 - d1).days + 1

    #count the number of entrance of all student
    class user_attendance:
        def __init__(self, name, present_cnt):
            self.name = name
            self.present_cnt = present_cnt

    att_list = []

    if request.user.is_authenticated and request.user.is_teacher:
        for stu in stu_list:
            user = user_attendance(stu.first_name, 0)
            att_list.append(user)

        for l in log:
            for stu in att_list:
                if(stu.name == l.id_number.first_name):
                    if(l.location == "Entrance"):
                        stu.present_cnt = stu.present_cnt + 1

        name_list = []
        abs_list = []
        print(num_days)
        for stu in att_list:
            name_list.append(stu.name)
            abs_list.append(num_days - stu.present_cnt)

        att_list = zip(name_list, abs_list)
        print(att_list)


    print(log)
    return render(request=request,
                  context={"logs": log, "myFilter": myFilter, "filter": myFilter, "students": students, "att_list": att_list},
                  template_name='templates/main/stud_attendance.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username} {user.is_teacher}")

                if user.is_teacher is True:
                    return redirect('main:welcome')
                else:
                    return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="templates/main/login.html",
                  context={"form": form})