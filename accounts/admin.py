from django.contrib import admin

from .models import User, Contact


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'created_at']

admin.site.register(User, UserAdmin)

admin.site.register(Contact)


