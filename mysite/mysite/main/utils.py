from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event, Log, Student


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user = None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        #events_per_day = events.filter(start_time__day=day)
        events_per_day = events.filter(date__day=day)
        d = ''
        for event in events_per_day:
            #d += f'<li> {event.get_html_url} </li>'
            #print(event.id_number.first_name)
            #d += f'<li> {event.location} </li>'
            if (event.location == "Entrance"):
                buf =event.id_number.first_name + " arrived in school at " + event.time.strftime("%I:%M %p") + " on " + str(event.date)
            if (event.location == "Exit"):
                buf = event.id_number.first_name + " left school at " + event.time.strftime("%I:%M %p") + " on " + str(event.date)
            if (event.location == "Clinic"):
                buf = event.id_number.first_name + " entered the clinic at " + event.time.strftime("%I:%M %p") + " on " + str(event.date)

            d += f'<li> {buf} </li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        print(self.year)
        print(self.month)
        #events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
        events = Log.objects.filter(date__year=self.year, date__month=self.month)
        print(events)
        print(self.user)
        #get only the logs of children of user logged in
        students = Student.objects.all()
        child_list = []
        child_cnt = 0
        for stu in students:
            for sp in stu.parent.all():
                if sp.user_id == self.user.id:
                    child_list.append(stu)
                    child_cnt = child_cnt + 1

        for ch in child_list:
            print(ch.id)
            print(events)
            events_all = Log.objects.filter(date__year=self.year, date__month=self.month)
            if(ch == child_list[0]):
                events = events_all.filter(id_number=ch.id)
            else:
                events_new = events_all.filter(id_number = ch.id)
                events = events_new | events

        print(events)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal



# class Calendar(HTMLCalendar):
#     def __init__(self, year=None, month=None):
#         self.year = year
#         self.month = month
#         super(Calendar, self).__init__()
#
#     # formats a day as a td
#     # filter events by day
#     def formatday(self, day, events):
#         events_per_day = events.filter(start_time__day=day)
#         d = ''
#         for event in events_per_day:
#             d += f'<li> {event.get_html_url} </li>'
#
#         if day != 0:
#             return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
#         return '<td></td>'
#
#     # formats a week as a tr
#     def formatweek(self, theweek, events):
#         week = ''
#         for d, weekday in theweek:
#             week += self.formatday(d, events)
#         return f'<tr> {week} </tr>'
#
#     # formats a month as a table
#     # filter events by year and month
#     def formatmonth(self, withyear=True):
#         events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
#
#         cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
#         cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
#         cal += f'{self.formatweekheader()}\n'
#         for week in self.monthdays2calendar(self.year, self.month):
#             cal += f'{self.formatweek(week, events)}\n'
#         return cal
