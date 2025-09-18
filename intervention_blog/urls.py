from django.urls import path
from . import views

urlpatterns = [
    path("blogs/", view=views.Blogs.as_view()),
    path("tags/", view=views.GetAllTags.as_view()),
    path("blogs/latest/", view=views.LatestBlog.as_view()),
    path("blogs/trending/", view=views.TrendingBlog.as_view()),
    path("blogs/<str:pk>/", view=views.SingleBlog.as_view()),
]
