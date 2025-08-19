from datetime import datetime, timedelta, timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics 
from rest_framework.request import Request 
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenObtainPairView

from intervention_blog.filters import BlogFilter

from .serializers import BlogSerializer, UserProfileSerializer, UserRegistrationSerializer
from .models import Blog, UserProfile

# Create your views here.

class Blogs(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    filterset_classes = BlogFilter
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    authentication_classes = [authentication.JWTAuthentication]
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


class CurrentUser(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = response.data.get("refresh")

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                expires=datetime.now(timezone.utc) + timedelta(days=7)
            )

            response.data.pop("refresh")

        return response


