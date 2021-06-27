from .models import Message,User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

admin.site.register(Message)
admin.site.register(User,UserAdmin)