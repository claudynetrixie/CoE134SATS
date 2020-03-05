from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models


# Register your models here.
# admin.site.register(UserBuf)

formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }