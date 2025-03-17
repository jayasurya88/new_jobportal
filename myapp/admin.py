from django.contrib import admin
from .models import CustomUser
from .models import Job,JobApplication
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Job)
admin.site.register(JobApplication)