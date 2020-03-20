from .filters import StudentFilter, LogFilter

from .models import User, Student, Teacher, Parent, Log

import datetime
from datetime import date

def attendance_filter(request, stu_list, att_list, log):
    class user_attendance:
        def __init__(self, name, present_cnt, late_cnt):
            self.name = name
            self.present_cnt = present_cnt
            self.late_cnt = late_cnt

    if (request.GET):
        after = request.GET['date_after'].split("-", 3)
        before = request.GET['date_before'].split("-", 3)
        d1 = date(int(after[0]), int(after[1]), int(after[2]))
        d0 = date(int(before[0]), int(before[1]), int(before[2]))
        num_days = (d0 - d1).days + 1

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
                abs_list.append(num_days - stu.present_cnt)
                late_list.append(stu.late_cnt)

            att_list = zip(name_list, abs_list, late_list)
            return att_list



def disp_logs(request):
    stu_list = Student.objects.filter(section=Teacher.objects.get(user_id=request.user.id).section_name)

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
