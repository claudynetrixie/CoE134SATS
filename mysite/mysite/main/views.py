from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from datetime import date, timedelta, datetime
import datetime

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
# from .forms import NewUserForm
from .filters import StudentFilter, LogFilter

from .attendance_count_t import attendance_filter,disp_logs

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

def child_stats(request):
    students = Student.objects.all()
    myFilter = StudentFilter(request.GET, queryset=students)
    stud = myFilter.qs
    class user_attendance:
        def __init__(self, name, present_cnt, late_cnt):
            self.name = name
            self.present_cnt = present_cnt
            self.late_cnt = late_cnt


    #get # of children
    child_cnt = 0
    child_list = []
    for stu in students:
        for sp in stu.parent.all():
            if(sp.user_id == request.user.id):
                print(stu.first_name)
                child_list.append(stu)
                child_cnt = child_cnt + 1

    print(child_cnt)
    child_log = []
    att_list = []
    ontime = datetime.time(7, 30, 00)
    #disp logs of all children but separated into columns
    for ch in child_list:
        ch_log = Log.objects.filter(id_number = ch.id)
        print(ch_log)
        child_log.append(ch_log)
        user = user_attendance(ch.first_name, 0, 0)
        att_list.append(user)

    for l, stu in zip(child_log, att_list):
        print(l[0].id_number.first_name)
        for log in l:
            #print(log)
            if (log.location == "Entrance"):
                stu.present_cnt = stu.present_cnt + 1
                if (ontime < log.time):
                    stu.late_cnt = stu.late_cnt + 1

        print(stu.late_cnt)
        print(stu.present_cnt)

    name_list = []
    abs_list = []
    late_list = []
    pres_list = []

    d1 = date.today()
    d0 = date(2020, 3, 1)
    # num_days = (d0 - d1).days + 1
    daygenerator = (d0 + timedelta(x + 1) for x in range((d1 - d0).days + 1))
    num_days = sum(1 for day in daygenerator if day.weekday() < 5)

    print(num_days)

    for stu in att_list:
        name_list.append(stu.name)
        abs_list.append(num_days - stu.present_cnt)
        late_list.append(stu.late_cnt)
        pres_list.append(num_days - (num_days - stu.present_cnt) - stu.late_cnt)

    user_list = att_list
    att_list = zip(name_list, abs_list, late_list, pres_list)

    print("Parser")
    #parse logs into strings
    logs_parsed = []
    for l, stu in zip(child_log, user_list):
        print(l[0].id_number.first_name)
        name = l[0].id_number.first_name
        log_p = []
        for log in l:
            if (log.location == "Entrance"):
                buf = name + " arrived in school at " + log.time.strftime("%I:%M %p")
                print(buf)
                log_p.append(buf)
            if(log.location == "Exit"):
                buf = name + " left school at " + log.time.strftime("%I:%M %p")
                print(buf)
                log_p.append(buf)
            if (log.location == "Clinic"):
                buf = name + " entered the clinic at " + log.time.strftime("%I:%M %p")
                print(buf)
                log_p.append(buf)

        logs_parsed.append(log_p)


    for l in logs_parsed:
        print(l)








    return render(request=request,
                  context={"students": stud, "att_list": att_list, "logs_parsed": logs_parsed},
                  template_name='templates/main/child_stats.html')

def stud_attendance(request):
    students = Student.objects.all()
    logs = Log.objects.all()

    if request.user.is_authenticated and request.user.is_teacher:
        logs, stu_list, id_num = disp_logs(request)

    att_list = []
    myFilter = LogFilter(request.GET, queryset= logs)
    log = myFilter.qs

    if(request.GET):
        att_list = attendance_filter(request, stu_list, att_list, log)

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