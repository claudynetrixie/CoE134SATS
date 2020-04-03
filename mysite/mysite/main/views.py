from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .filters import StudentFilter, LogFilter

from .attendance_count_t import attendance_filter, disp_logs, get_childstats, attendance_counter, disp_logs_a, attendance_filter_a

from .models import User, Student, Teacher, Parent, Log

from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Employee
from .serializers import employeeSerializer, logSerializer

from datetime import timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar as cal_var

from .models import *
from .utils import Calendar
from .forms import EventForm, ContactForm

from django.conf import settings
from twilio.rest import Client

from django.core.mail import send_mail




# Create your views here.
def broadcast_sms(request):
    message_to_broadcast = ("Guess whoooooo")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    recipient = '+639175126253'
    client.messages.create(to=recipient,from_=settings.TWILIO_NUMBER, body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)


def account(request):
    students = Student.objects.all()
    return render(request=request,
                  context={'students': students},
                  template_name='templates/main/account.html')

class LogList(APIView):
    def get(self, request):
        log1 = Log.objects.all()
        serializer = logSerializer(log1, many = True)
        return Response(serializer.data)

    def post(self, request):
        log1 = Log.objects.all()[0]
        serializer = logSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)



def homepage(request):
    students = Student.objects.all()
    return render(request=request,
                  context= {'students': students},
                  template_name='templates/main/home.html')


def welcome(request):
    return render(request=request,
                  template_name='templates/main/welcome.html')


def welcome_parent(request):
    return render(request=request,
                  template_name='templates/main/welcome_parent.html')

def class_list(request, section= 'Default'):
    print(section)
    #get all the students in this class
    students = Student.objects.all()
    class_list = students.filter(section = section)

    logs, stu_list, id_num = disp_logs_a(class_list)
    print(logs)
    myFilter = LogFilter(request.GET, queryset=logs)
    log = myFilter.qs

    att_list =[]
    if (request.GET):
        att_list = attendance_filter_a(request, stu_list, att_list, log)
        print(myFilter.form)
        print(dir(request.GET))
        if(request.GET.keys):
            after = request.GET['date_after'].split("-")
            date_after = datetime.date(int(after[0]), int(after[1]), int(after[2]))
            before = request.GET['date_before'].split("-")
            date_before = datetime.date(int(before[0]), int(before[1]), int(before[2]))
        else:
            date_after = datetime.date.today()
            date_before = datetime.date(2020, 3, 1)
    else:
        date_before = []
        date_after = []


    return render(request=request,
                  context = {"section":section, "logs": log, "filter": myFilter, "att_list": att_list,
                             "date_before": date_before, "date_after": date_after},
                  template_name='templates/main/class_list.html')

def list_students(request):
    students = Student.objects.all()
    myFilter = StudentFilter(request.GET, queryset=students)
    print(request.GET)
    stud = myFilter.qs
    print(stud)
    sections = []

    if(request.GET):
        year_level = request.GET['year_level']
        year_level_obj = YearLevel.objects.filter(level = year_level)[0]
        section_q = year_level_obj.section.all()
        for sec in section_q:
            sections.append(sec.name)

        print(sections)

    return render(request=request,
                  context={"students": stud, "myFilter": myFilter, "filter": myFilter, "section_list": sections},
                  template_name='templates/main/listofstudents.html')


def child_stats(request):
    students = Student.objects.all()
    # myFilter = StudentFilter(request.GET, queryset=students)
    # stud = myFilter.qs
    # print(stud)
    user = request.user
    if user.is_authenticated and user.is_parent:
        child_list = []
        for stu in students:
            for sp in stu.parent.all():
                if sp.user_id == request.user.id:
                    child_list.append(stu)
                    break

        if(child_list):
            stud = [child_list[0]]
            att_list, logs_parsed, data = get_childstats(stud, request)
            labels = ['Absent', 'Late', 'Ontime']
            logs_parsed[0].reverse()
            print(logs_parsed)
            logs_parsed = [logs_parsed[0][0:5]]

            return render(request=request,
                  context={"students": students, "att_list": att_list, "logs_parsed": logs_parsed,
                           "labels": labels, "data": data},
                  template_name='templates/main/child_stats.html')

        else:
            return render(request=request,
                          context={"students": students,},
                          template_name='templates/main/child_stats.html')


def indiv_stats(request, name = 'Default'):
    print(name)
    students = Student.objects.all()
    stud = Student.objects.get(first_name = name)
    stud = [stud]
    labels = ['Absent', 'Late', 'Ontime']

    att_list, logs_parsed, data = get_childstats(stud, request)
    logs_parsed[0].reverse()
    print(logs_parsed)
    logs_parsed = [logs_parsed[0][0:5]]

    return render(request=request,
                  context={"students": students, "att_list": att_list, "logs_parsed": logs_parsed,
                           "labels": labels, "data": data},
                  template_name='templates/main/indiv_stats.html')


def stud_attendance(request):
    students = Student.objects.all()
    logs = Log.objects.all()

    if request.user.is_authenticated and request.user.is_teacher:
        logs, stu_list, id_num = disp_logs(request)
        if(stu_list):
            att_list = []
            myFilter = LogFilter(request.GET, queryset=logs)
            log = myFilter.qs

            if (request.GET):
                att_list = attendance_filter(request, stu_list, att_list, log)

                print(myFilter.form)

            return render(request=request,
                          context={"logs": log, "myFilter": myFilter, "filter": myFilter, "students": students,
                                   "att_list": att_list},
                          template_name='templates/main/stud_attendance.html')

        else:
            return render(request=request, template_name='templates/main/stud_attendance.html')


    else:
        return render(request = request, template_name='templates/main/stud_attendance.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        print(form)

        if form.is_valid():
            print("valid")
            username = form.cleaned_data.get('username')
            print(username)
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")

                if user.is_teacher is True:
                    return redirect('main:stud_attendance')
                elif user.is_parent is True:
                    return redirect('main:child_stats')
                else:
                    return redirect('main:list_students')
            else:
                messages.error(request, "Invalid username or password.")

        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    print(form)
    return render(request=request,
                  template_name="templates/main/login.html",
                  context={"form": form})



class CalendarView(generic.ListView):
    model = Event
    template_name = 'templates/main/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))

        cal = Calendar(d.year, d.month, self.request.user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['students'] = Student.objects.all()
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return date.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = cal_var.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

#
def event(request, event_id=None):
    instance = Event()

    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('main:calendar'))
    return render(request, 'templates/main/event.html', {'form': form})

def contact_us(request):
    form = ContactForm(request.POST)
    print(form)
    if request.user.is_authenticated and request.user.is_parent:
        students = Student.objects.all()
    else:
        students = []

    if request.POST and form.is_valid():
        form.save()
        print(request.POST)
        print("valid")
        recipient = request.POST['email_address']
        subject = request.POST['subject']
        message = request.POST['message']
        print(settings.EMAIL_HOST_USER)

        send_mail(subject,message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
        return HttpResponseRedirect(reverse('main:homepage'))

    return render(request, 'templates/main/contact_us.html', {'form': form, 'students': students})
