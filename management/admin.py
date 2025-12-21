from django.contrib import admin
from .models import Internship, Application, UserProfile

admin.site.register(Internship)
admin.site.register(Application)
admin.site.register(UserProfile)