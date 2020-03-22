from __future__ import unicode_literals


from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from .models import Log, Student, Parent, Teacher, User

import datetime
import calendar
from django.urls import reverse
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe

# Register your models here.
admin.site.register(Log)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(User)

formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }


