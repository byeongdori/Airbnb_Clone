from django.contrib import admin
from django.db.migrations.operations import models
from . import models

# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    pass