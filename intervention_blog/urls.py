from django.urls import path
from . import views

urlpatterns = [
    path("blogs/", view=views.Blogs.as_view()),
    path("blogs/latest/", view=views.LatestBlog.as_view()),
    path("blogs/<str:pk>/", view=views.Blogs.as_view()),
    path("register/", view=views.Users.as_view()),
    path("users/<str:pk>/", view=views.Users.as_view())
]
