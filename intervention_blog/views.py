from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt import authentication
from rest_framework import generics


from .serializers import BlogSerializer, TagSerializer
from .models import Blog, Tag

# Create your views here.


class GetAllTags(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class Blogs(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination


class TrendingBlog(generics.ListAPIView):
    queryset = Blog.objects.all().order_by("-likes")
    serializer_class = BlogSerializer
    pagination_class = LimitOffsetPagination


class LatestBlog(generics.ListAPIView):
    queryset = Blog.objects.all().order_by("-posted_on")[0:4]
    serializer_class = BlogSerializer
    pagination_class = LimitOffsetPagination


class SingleBlog(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.JWTAuthentication]
