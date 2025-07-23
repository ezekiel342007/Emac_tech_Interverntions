import django_filters

from intervention_blog.models import Blog


class BlogFilter(django_filters.Filter):
    posted_on = django_filters.DateTimeFilter()

    class Meta:
        model = Blog
        fields = ["title", "posted_on"]
