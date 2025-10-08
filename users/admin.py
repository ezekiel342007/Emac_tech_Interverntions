from django.contrib import admin

from users.models import CustomUser, Watchings


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Watchings)
class WatchingsAdmin(admin.ModelAdmin):
    pass
