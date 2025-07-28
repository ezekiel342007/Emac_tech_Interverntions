from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics 
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework_simplejwt import authentication

from intervention_blog.filters import BlogFilter

from .serializers import BlogSerializer, UserRegistrationSerializer
from .models import Blog, UserProfile

# Create your views here.

class Blogs(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    filterset_classes = BlogFilter
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    authentication_classes = [authentication.JWTAuthentication]


class LatestBlog(generics.ListAPIView):
    queryset = Blog.objects.all().order_by("-posted_on")[0:4]
    serializer_class = BlogSerializer


class SingleBlog(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.JWTAuthentication]


class Users(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Account Registerd Successfully"},
            headers=headers,
            status=HTTP_201_CREATED
        )
# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1Mzc4NjEyMywiaWF0IjoxNzUzNjk5NzIzLCJqdGkiOiI1NGZiMjBjZDVjZTg0MWRmOWU1MmNkN2U4NDdkNjE1ZSIsInVzZXJfaWQiOjZ9.TvF2M298IVLgxDiKjxI804iBViVz-8y4E8hJVZTb3nY",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUzNzAwMDIzLCJpYXQiOjE3NTM2OTk3MjMsImp0aSI6Ijc3OGE2MmU5YWQzYjQ4MjA4MjE2ZTg1NDYwODk5N2I0IiwidXNlcl9pZCI6Nn0.7R9qO3Ms1PN0K1y6NTqGTiIAWJ49o5U5p2FK-atRTyI"
# }

# 957db919-d515-4cc2-934d-70535655a9f8
# fae03bb2-40bc-4e5b-b4f3-d05548cb5531
