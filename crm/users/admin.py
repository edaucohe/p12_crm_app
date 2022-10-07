from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from users.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name',
                    'email', 'is_staff', 'role')

    fieldsets = (
        ('Login info', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'last_name', 'first_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Team user', {'fields': ('role',)}),
    )

    search_help_text = "Username and roles"
    search_fields = ['username', 'role']


admin.site.register(User, UserAdmin)
