from django.urls import path, include

from .views import (
    register_view,
    reset_password_view,
    forgot_password_view,
    login_view,
    logout_view,
    UserProfileView,
)

account_paths = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("forgot-password/", forgot_password_view, name="forgot-password"),
    path(
        "<str:user>/reset-password/",
        reset_password_view,
        name="reset-password",
    ),
]

urlpatterns = [
    path("<int:pk>/", UserProfileView.as_view(), name="user-profile"),
    path("account/", include(account_paths)),
]
