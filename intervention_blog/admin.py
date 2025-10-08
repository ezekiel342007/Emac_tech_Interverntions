from django.contrib import admin

from intervention_blog.models import Blog, Tag

# Register your models here.

admin.site.register(Blog)
admin.site.register(Tag)
