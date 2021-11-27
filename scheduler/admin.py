from django.contrib import admin

from .models import User, Event


class UserAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
