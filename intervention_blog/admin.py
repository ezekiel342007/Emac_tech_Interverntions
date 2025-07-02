from django.contrib import admin

from intervention_blog.models import Blog, Tag, UserProfile, Watchings

# Register your models here.

admin.site.register(Blog)
admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Watchings)
