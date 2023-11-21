from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    ordering = ('date_joined',)
    list_display = ('name', 'email', 'last_login', 'date_joined')
    fieldsets = (
        ('Personal Info', {'fields': ('name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )


admin.site.register(Customer, UserAdminConfig)
admin.site.register(AccountInfo)

