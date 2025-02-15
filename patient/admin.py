from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Details)
admin.site.register(models.Complaint)
admin.site.register(models.Diagnosis)
admin.site.register(models.FollowUp)
