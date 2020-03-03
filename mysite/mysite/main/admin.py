from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from .models import User

# Register your models here.
admin.site.register(User)

formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }