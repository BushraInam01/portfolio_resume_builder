
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import UpdateView, DetailView, View

from weasyprint import HTML

from portfolios.models import Portfolio
from .forms import ResumeCustomizationForm


class ResumeCustomizationView(LoginRequiredMixin, UpdateView):
    """Allow authenticated users to customize their own resume."""

    model = Portfolio
    form_class = ResumeCustomizationForm
    template_name = "resumes/customize.html"
    success_url = reverse_lazy("resumes:customize")

    def get_object(self, queryset=None):
        return Portfolio.objects.filter(
            user=self.request.user
        ).first()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            portfolio_exists = Portfolio.objects.filter(
                user=request.user
            ).exists()

            if not portfolio_exists:
                messages.warning(
                    request,
                    "Please create your portfolio before customizing your resume.",
                )
                return redirect("portfolios:portfolio_create")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your resume customization has been saved successfully.",
        )
        return super().form_valid(form)


class ResumePreviewView(LoginRequiredMixin, DetailView):
    """Display the logged-in user's customized resume."""

    model = Portfolio
    template_name = "resumes/preview.html"
    context_object_name = "portfolio"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Portfolio,
            user=self.request.user,
        )


class ResumePDFDownloadView(LoginRequiredMixin, View):
    """Generate and download the logged-in user's resume as a PDF."""

    def get(self, request, *args, **kwargs):
        portfolio = get_object_or_404(
            Portfolio.objects.prefetch_related(
                "educations",
                "experiences",
                "projects",
                "skills",
            ),
            user=request.user,
        )

        html_string = render_to_string(
            "resumes/preview.html",
            {"portfolio": portfolio},
            request=request,
        )

        pdf_file = HTML(
            string=html_string,
            base_url=request.build_absolute_uri("/"),
        ).write_pdf()

        filename = slugify(portfolio.full_name or portfolio.title)
        filename = filename or "resume"

        response = HttpResponse(
            pdf_file,
            content_type="application/pdf",
        )

        response["Content-Disposition"] = (
            f'attachment; filename="{filename}-resume.pdf"'
        )

        return response
