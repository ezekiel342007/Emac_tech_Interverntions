from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken

from .serializers import (
    CustomUserSerializer,
    LoginUserSerializer,
    RegisterUserSerializer,
    WatchingSerializer,
)

from .models import Watchings

# Create your views here.


class UserWatchings(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = WatchingSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"

    def get_queryset(self):
        return Watchings.objects.get(watcher=self.request.user)


class UserInfo(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user


class UserRegistrationView(CreateAPIView):
    serializer_class = RegisterUserSerializer


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)

        # generating tokens for user
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            acces_token = str(refresh.access_token)

            response = Response(
                CustomUserSerializer(user).data, status=status.HTTP_200_OK
            )

            response.set_cookie(
                key="access_token",
                value=acces_token,
                httponly=True,
                secure=True,
                samesite="None",
                partitioned=True,
            )

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="None",
                partitioned=True,
            )

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as e:
                return Response(
                    {"error": "Error invalidating token" + str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        response = Response(
            {"message": "Successfully logged out"}, status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class CookieTokenRefreshView(TokenRefreshView):
    authentication_classes = ()

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        request.COOKIES.delete_cookie
        if not refresh_token:
            return Response(
                {"error": "Refresh token not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response(
                {"message": "Access token refreshed Successfully"},
                status=status.HTTP_200_OK,
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="None",
            )
            return response
        except InvalidToken:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )
