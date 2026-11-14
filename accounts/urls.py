
from django.urls import path

from .views import (
    RegisterView,
    UserLoginView,
    UserLogoutView,
    DashboardView,
    UserPasswordChangeView,
    PasswordChangeDoneView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView,
)


app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("password/change/", UserPasswordChangeView.as_view(), name="password_change"),
    path("password/change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password/reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path("password/reset/done/", UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password/reset/confirm/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password/reset/complete/", UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]