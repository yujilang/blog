from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class EmployeeInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmins(UserAdmin):
    inlines = (EmployeeInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmins)
# Register your models here.
