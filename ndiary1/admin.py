from django.contrib import admin
from django.db import models
from .models import Diary, Category
from .widgets import FileUploadableTextArea


class DiaryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': FileUploadableTextArea},
    }


admin.site.register(Diary, DiaryAdmin)
admin.site.register(Category)
