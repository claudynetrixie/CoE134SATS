from .filters import StudentFilter, LogFilter

from .models import User, Student, Teacher, Parent, Log

import datetime
import numpy as np
import pandas as pd
#from datetime import timedelta, date


def attendance_filter(request, stu_list, att_list, log):
    class user_attendance:
        def __init__(self, name, present_cnt, late_cnt):
            self.name = name
            self.present_cnt = present_cnt
            self.late_cnt = late_cnt

    if (request.GET):
        after = request.GET['date_after'].split("-", 3)
        before = request.GET['date_before'].split("-", 3)
        d1 = datetime.date(int(after[0]), int(after[1]), int(after[2]))
        d0 = datetime.date(int(before[0]), int(before[1]), int(before[2]))
        #num_days = (d0 - d1).days + 1
        num_days = (np.busday_count(d1,d0))
        #.weekday (0-monday, 6-sunday)

        if(d1.weekday() < 5):
            if(d0.weekday() < 5):
                num_days = num_days + 1
            else:
                num_days = num_days
        else:
            if (d0.weekday() < 5):
                num_days = num_days + 1
            else:
                num_days = num_days


        print("num_days")
        print(num_days)

        if request.user.is_authenticated and request.user.is_teacher:
            for stu in stu_list:
                user = user_attendance(stu.first_name, 0, 0)
                att_list.append(user)

            ontime = datetime.time(7, 30, 00)

            for l in log:
                for stu in att_list:
                    if (stu.name == l.id_number.first_name):
                        if (l.location == "Entrance"):
                            stu.present_cnt = stu.present_cnt + 1
                            if (ontime < l.time):
                                stu.late_cnt = stu.late_cnt + 1

            name_list = []
            abs_list = []
            late_list = []
            for stu in att_list:
                name_list.append(stu.name)
                print(stu.present_cnt)
                abs_list.append(num_days - stu.present_cnt)
                late_list.append(stu.late_cnt)

            att_list = zip(name_list, abs_list, late_list)
            return att_list


def disp_logs(request):
    print(request.user.id)
    teachers = Teacher.objects.all()
    teacher = teachers.filter(user_id = request.user.id)[0]
    section = teacher.section_name
    stu_list = Student.objects.filter(section = section)

    print(stu_list)

    if(not stu_list):
        logs =[]
        id_num = []
        return logs, stu_list, id_num

    id_num = []
    for stu in stu_list:
        id_num.append(stu.id)
    # get the logs of all those students
    for id in id_num:
        if (id == id_num[0]):
            log_b = Log.objects.filter(id_number=id)
        else:
            log_b = log_b | Log.objects.filter(id_number=id)
    logs = log_b

    return logs, stu_list, id_num


def get_childstats(students, request):
    class user_attendance:
        def __init__(self, name, present_cnt, late_cnt, present_today):
            self.name = name
            self.present_cnt = present_cnt
            self.late_cnt = late_cnt
            self.present_today = present_today

    # get # of children
    child_cnt = 0
    child_list = []
    for stu in students:
        for sp in stu.parent.all():
            if sp.user_id == request.user.id:
                child_list.append(stu)
                child_cnt = child_cnt + 1

    print(child_cnt)
    child_log = []
    att_list = []
    ontime = datetime.time(7, 30, 00)
    # disp logs of all children but separated into columns
    for ch in child_list:
        ch_log = Log.objects.filter(id_number=ch.id)
        child_log.append(ch_log)
        user = user_attendance(ch.first_name, 0, 0, 0)
        att_list.append(user)

    for l, stu in zip(child_log, att_list):
        print(l[0].id_number.first_name)
        for log in l:
            # print(log)
            if log.location == "Entrance":
                stu.present_cnt = stu.present_cnt + 1
                if ontime < log.time:
                    stu.late_cnt = stu.late_cnt + 1

                if log.date == datetime.date.today():
                    stu.present_today = 1

        print(stu.late_cnt)
        print(stu.present_cnt)
        print(stu.present_today)

    name_list = []
    abs_list = []
    late_list = []
    pres_list = []
    pres_today_list = []

    d1 = datetime.date.today()
    #############################################
    d0 = datetime.date(2020, 3, 1)
    daygenerator = (d0 + datetime.timedelta(x + 1) for x in range((d1 - d0).days + 1))
    num_days = sum(1 for day in daygenerator if day.weekday() < 5)

    for stu in att_list:
        name_list.append(stu.name)
        abs_list.append(num_days - stu.present_cnt)

        late_list.append(stu.late_cnt)
        pres_list.append(num_days - (num_days - stu.present_cnt) - stu.late_cnt)
        if (stu.present_today == 0):
            pres_today_list.append("Absent")
        else:
            pres_today_list.append("Present")

    user_list = att_list
    data = [abs_list[0], late_list[0], pres_list[0]]
    att_list = zip(name_list, abs_list, late_list, pres_list, pres_today_list)

    # parse logs into strings
    logs_parsed = []
    for l, stu in zip(child_log, user_list):
        name = l[0].id_number.first_name
        log_p = []
        for log in l:
            if (log.location == "Entrance"):
                buf = name + " arrived in school at " + log.time.strftime("%I:%M %p") + " on " + str(log.date)
                log_p.append(buf)
            if (log.location == "Exit"):
                buf = name + " left school at " + log.time.strftime("%I:%M %p") + " on " + str(log.date)
                log_p.append(buf)
            if (log.location == "Clinic"):
                buf = name + " entered the clinic at " + log.time.strftime("%I:%M %p") + " on " + str(log.date)
                log_p.append(buf)

        logs_parsed.append(log_p)

    return att_list, logs_parsed, data


def attendance_counter(child_list):
    class user_attendance:
        def __init__(self, name, present_cnt, late_cnt, present_today):
            self.name = name
            self.present_cnt = present_cnt
            self.late_cnt = late_cnt
            self.present_today = present_today


    child_log = []
    att_list = []
    ontime = datetime.time(7, 30, 00)
    # disp logs of all children but separated into columns
    for ch in child_list:
        ch_log = Log.objects.filter(id_number=ch.id)
        child_log.append(ch_log)
        user = user_attendance(ch.first_name, 0, 0, 0)
        att_list.append(user)

    for l, stu in zip(child_log, att_list):
        print(l[0].id_number.first_name)
        for log in l:
            # print(log)
            if log.location == "Entrance":
                stu.present_cnt = stu.present_cnt + 1
                if ontime < log.time:
                    stu.late_cnt = stu.late_cnt + 1

                if log.date == datetime.date.today():
                    stu.present_today = 1

        print(stu.late_cnt)
        print(stu.present_cnt)
        print(stu.present_today)

    name_list = []
    abs_list = []
    late_list = []
    pres_list = []
    pres_today_list = []

    d1 = datetime.date.today()
    #############################################
    d0 = datetime.date(2020, 3, 1)
    daygenerator = (d0 + datetime.timedelta(x + 1) for x in range((d1 - d0).days + 1))
    num_days = sum(1 for day in daygenerator if day.weekday() < 5)

    for stu in att_list:
        name_list.append(stu.name)
        abs_list.append(num_days - stu.present_cnt)
        late_list.append(stu.late_cnt)
        pres_list.append(num_days - (num_days - stu.present_cnt) - stu.late_cnt)
        if (stu.present_today == 0):
            pres_today_list.append("Absent")
        else:
            pres_today_list.append("Present")

    user_list = att_list
    #att_list = zip(name_list, abs_list, late_list, pres_list, pres_today_list)

    return name_list, abs_list, late_list, pres_list, pres_today_list


def disp_logs_a(stu_list):

    id_num = []
    for stu in stu_list:
        id_num.append(stu.id)
    # get the logs of all those students
    for id in id_num:
        if (id == id_num[0]):
            log_b = Log.objects.filter(id_number=id)
        else:
            log_b = log_b | Log.objects.filter(id_number=id)
    logs = log_b

    return logs, stu_list, id_num

def attendance_filter_a(request, stu_list, att_list, log):
    class user_attendance:
        def __init__(self, name, present_cnt, late_cnt):
            self.name = name
            self.present_cnt = present_cnt
            self.late_cnt = late_cnt

    if (request.GET):
        after = request.GET['date_after'].split("-", 3)
        before = request.GET['date_before'].split("-", 3)
        d1 = datetime.date(int(after[0]), int(after[1]), int(after[2]))
        d0 = datetime.date(int(before[0]), int(before[1]), int(before[2]))
        #num_days = (d0 - d1).days + 1
        num_days = (np.busday_count(d1,d0))
        #.weekday (0-monday, 6-sunday)

        if(d1.weekday() < 5):
            if(d0.weekday() < 5):
                num_days = num_days + 1
            else:
                num_days = num_days
        else:
            if (d0.weekday() < 5):
                num_days = num_days + 1
            else:
                num_days = num_days


        print("num_days")
        print(num_days)

        if request.user.is_authenticated:
            for stu in stu_list:
                user = user_attendance(stu.first_name, 0, 0)
                att_list.append(user)

            ontime = datetime.time(7, 30, 00)

            for l in log:
                for stu in att_list:
                    if (stu.name == l.id_number.first_name):
                        if (l.location == "Entrance"):
                            stu.present_cnt = stu.present_cnt + 1
                            if (ontime < l.time):
                                stu.late_cnt = stu.late_cnt + 1

            name_list = []
            abs_list = []
            late_list = []
            for stu in att_list:
                name_list.append(stu.name)
                print(stu.present_cnt)
                abs_list.append(num_days - stu.present_cnt)
                late_list.append(stu.late_cnt)

            att_list = zip(name_list, abs_list, late_list)
            return att_list