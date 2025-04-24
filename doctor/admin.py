from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Treatment)
admin.site.register(models.Prescription)
