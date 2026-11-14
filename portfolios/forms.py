
from django import forms

from .models import (
    Portfolio,
    Education,
    Experience,
    Project,
    Skill,
)

class PortfolioForm(forms.ModelForm):
    """Form for creating and updating a portfolio."""

    class Meta:
        model = Portfolio
        fields = (
            "title",
            "slug",
            "full_name",
            "professional_title",
            "bio",
            "location",
            "phone",
            "website",
            "linkedin_url",
            "github_url",
            "is_public",
            "allow_endorsements",
        )

        widgets = {
            "bio": forms.Textarea(attrs={"rows": 5}),
        }

class EducationForm(forms.ModelForm):
    """Form for adding and updating education records."""

    class Meta:
        model = Education
        exclude = ("portfolio", "sort_order")

        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        is_current = cleaned_data.get("is_current")

        if start_date and end_date and end_date < start_date:
            self.add_error(
                "end_date",
                "End date cannot be earlier than start date.",
            )

        if is_current and end_date:
            self.add_error(
                "end_date",
                "Remove the end date for current education.",
            )

        return cleaned_data

class ExperienceForm(forms.ModelForm):
    """Form for adding and updating work experience."""

    class Meta:
        model = Experience
        exclude = ("portfolio", "sort_order")

        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        is_current = cleaned_data.get("is_current")

        if start_date and end_date and end_date < start_date:
            self.add_error(
                "end_date",
                "End date cannot be earlier than start date.",
            )

        if is_current and end_date:
            self.add_error(
                "end_date",
                "Remove the end date for a current position.",
            )

        return cleaned_data

class ProjectForm(forms.ModelForm):
    """Form for adding and updating projects."""

    class Meta:
        model = Project
        exclude = ("portfolio", "sort_order")

        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 5}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            self.add_error(
                "end_date",
                "End date cannot be earlier than start date.",
            )

        return cleaned_data

class SkillForm(forms.ModelForm):
    """Form for adding and updating portfolio skills."""

    def __init__(self, *args, portfolio=None, **kwargs):
        self.portfolio = portfolio
        super().__init__(*args, **kwargs)

    class Meta:
        model = Skill
        fields = ("name", "proficiency")

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if self.portfolio:
            existing_skill = Skill.objects.filter(
                portfolio=self.portfolio,
                name__iexact=name,
            )

            if self.instance.pk:
                existing_skill = existing_skill.exclude(
                    pk=self.instance.pk
                )

            if existing_skill.exists():
                raise forms.ValidationError(
                    "This skill has already been added to your portfolio."
                )

        return name