from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LogoutView,
)  # Used instead of FBV logout (redirect path specified in settings.py)

from users.views import (
    UserLoginView,
    UserRegistrationView,
    UserProfileView,
    EmailVerificationView,
)

app_name = "users"

urlpatterns = [
    # path("login/", login, name="login"),
    path("login/", UserLoginView.as_view(), name="login"),
    # path("registration/", registration, name="registration"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    # path("profile/", profile, name="profile"),
    path("profile/<int:pk>", login_required(UserProfileView.as_view()), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "verify/<str:email>/<uuid:code>/",
        EmailVerificationView.as_view(),
        name="email_verification",
    ),
]
