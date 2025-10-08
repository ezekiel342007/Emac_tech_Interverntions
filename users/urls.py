from django.urls import path

from users.views import (
    CookieTokenRefreshView,
    LoginView,
    LogoutView,
    UserInfo,
    UserRegistrationView,
    UserWatchings,
)

urlpatterns = [
    path("user_info/", UserInfo.as_view(), name="user-info"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="token-refresh"),
    path("watchings/", UserWatchings.as_view(), name="watchings"),
]

# emac342007@gmail.com
# {"email":"emac342007@gmail.com","password":"presence"}
