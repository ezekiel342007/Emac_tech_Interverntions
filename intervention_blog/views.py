from rest_framework import generics 
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt import authentication

from .serializers import BlogSerializer, UserProfileSerializer
from .models import Blog, UserProfile

# Create your views here.

class Blogs(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
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
