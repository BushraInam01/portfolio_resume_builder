from django import forms
from portfolios.models import Portfolio


class ResumeCustomizationForm(forms.ModelForm):
    """Form for customizing resume theme and accent color."""

    class Meta:
        model = Portfolio
        fields = [
            "resume_theme",
            "accent_color",
        ]

        widgets = {
            "resume_theme": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "accent_color": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control color-picker",
                }
            ),
        }

        labels = {
            "resume_theme": "Resume Theme",
            "accent_color": "Accent Color",
        }

        help_texts = {
            "resume_theme": "Choose the design style for your resume.",
            "accent_color": "Select the primary color for your resume.",
        }
