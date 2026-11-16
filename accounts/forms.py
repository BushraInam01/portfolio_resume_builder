from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


User = get_user_model()


class RegistrationForm(forms.ModelForm):
    """Form for registering new users."""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        ),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        ),
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }

    def clean_email(self):
        email = User.objects.normalize_email(
            self.cleaned_data["email"]
        ).lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error(
                    "password2",
                    "Passwords do not match."
                )
            else:
                try:
                    validate_password(password1)
                except ValidationError as error:
                    self.add_error("password1", error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = User.objects.normalize_email(
            user.email
        ).lower()

        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class EmailAuthenticationForm(AuthenticationForm):
    """Authentication form using email as login identity."""

    username = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
            }
        ),
    )

    def clean_username(self):
        email = self.cleaned_data.get("username", "")
        return email.strip().lower()
