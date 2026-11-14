from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import RegistrationForm, EmailAuthenticationForm


class RegisterView(CreateView):
    """Handle new user registration."""

    form_class = RegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your account has been created successfully. Please log in."
        )
        return super().form_valid(form)


class UserLoginView(LoginView):
    """Handle email-based user authentication."""

    form_class = EmailAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """Handle secure user logout."""

    next_page = reverse_lazy("accounts:login")


class DashboardView(LoginRequiredMixin, TemplateView):
    """Display the authenticated user's dashboard."""

    template_name = "accounts/dashboard.html"
    login_url = reverse_lazy("accounts:login")


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Allow authenticated users to change their password."""

    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")


class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    """Display password change confirmation."""

    template_name = "accounts/password_change_done.html"


class UserPasswordResetView(PasswordResetView):
    """Send password reset email."""

    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class UserPasswordResetDoneView(PasswordResetDoneView):
    """Display password reset email confirmation."""

    template_name = "accounts/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """Allow users to set a new password using a valid reset link."""

    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """Display password reset completion."""

    template_name = "accounts/password_reset_complete.html"
