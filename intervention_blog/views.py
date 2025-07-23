from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics 
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt import authentication

from intervention_blog.filters import BlogFilter

from .serializers import BlogSerializer, UserProfileSerializer
from .models import Blog, UserProfile

# Create your views here.

class Blogs(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    filterset_classes = BlogFilter
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    authentication_classes = [authentication.JWTAuthentication]


class SingleBlog(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.JWTAuthentication]


class Users(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
