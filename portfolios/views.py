import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    UpdateView,
    TemplateView,
    ListView,
    DeleteView,
    DetailView,
)

from .forms import (
    PortfolioForm,
    EducationForm,
    ExperienceForm,
    ProjectForm,
    SkillForm,
)

from .models import (
    Portfolio,
    PortfolioSection,
    Education,
    Experience,
    Project,
    Skill,
)


class PortfolioDashboardView(LoginRequiredMixin, TemplateView):
    """Display the logged-in user's portfolio dashboard."""

    template_name = "portfolios/dashboard.html"
    login_url = reverse_lazy("accounts:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["portfolio"] = Portfolio.objects.filter(
            user=self.request.user
        ).first()

        return context


class PortfolioCreateView(LoginRequiredMixin, CreateView):
    """Allow a user to create their own portfolio."""

    model = Portfolio
    form_class = PortfolioForm
    template_name = "portfolios/portfolio_form.html"
    success_url = reverse_lazy("portfolios:dashboard")
    login_url = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        existing_portfolio = Portfolio.objects.filter(
            user=request.user
        ).first()

        if existing_portfolio:
            return redirect("portfolios:portfolio_update")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PortfolioUpdateView(LoginRequiredMixin, UpdateView):
    """Allow a user to update only their own portfolio."""

    model = Portfolio
    form_class = PortfolioForm
    template_name = "portfolios/portfolio_form.html"
    success_url = reverse_lazy("portfolios:dashboard")
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Portfolio.objects.filter(
            user=self.request.user
        )

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        return get_object_or_404(queryset)


class EducationListView(LoginRequiredMixin, ListView):
    """Display education records belonging to the logged-in user."""

    model = Education
    template_name = "portfolios/education_list.html"
    context_object_name = "educations"
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Education.objects.filter(
            portfolio__user=self.request.user
        )


class EducationCreateView(LoginRequiredMixin, CreateView):
    """Allow users to add education to their own portfolio."""

    model = Education
    form_class = EducationForm
    template_name = "portfolios/education_form.html"
    success_url = reverse_lazy("portfolios:education_list")
    login_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        portfolio = get_object_or_404(
            Portfolio,
            user=self.request.user,
        )
        form.instance.portfolio = portfolio

        return super().form_valid(form)


class EducationUpdateView(LoginRequiredMixin, UpdateView):
    """Allow users to update only their own education records."""

    model = Education
    form_class = EducationForm
    template_name = "portfolios/education_form.html"
    success_url = reverse_lazy("portfolios:education_list")
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Education.objects.filter(
            portfolio__user=self.request.user
        )


class EducationDeleteView(LoginRequiredMixin, DeleteView):
    """Allow users to delete only their own education records."""

    model = Education
    template_name = "portfolios/education_confirm_delete.html"
    success_url = reverse_lazy("portfolios:education_list")
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Education.objects.filter(
            portfolio__user=self.request.user
        )


class ExperienceListView(LoginRequiredMixin, ListView):
    """Display work experience belonging to the logged-in user."""

    model = Experience
    template_name = "portfolios/experience_list.html"
    context_object_name = "experiences"
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Experience.objects.filter(
            portfolio__user=self.request.user
        )


class ExperienceCreateView(LoginRequiredMixin, CreateView):
    """Allow users to add experience to their own portfolio."""

    model = Experience
    form_class = ExperienceForm
    template_name = "portfolios/experience_form.html"
    success_url = reverse_lazy("portfolios:experience_list")
    login_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        portfolio = get_object_or_404(
            Portfolio,
            user=self.request.user,
        )
        form.instance.portfolio = portfolio

        return super().form_valid(form)


class ExperienceUpdateView(LoginRequiredMixin, UpdateView):
    """Allow users to update only their own experience."""

    model = Experience
    form_class = ExperienceForm
    template_name = "portfolios/experience_form.html"
    success_url = reverse_lazy("portfolios:experience_list")
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Experience.objects.filter(
            portfolio__user=self.request.user
        )


class ExperienceDeleteView(LoginRequiredMixin, DeleteView):
    """Allow users to delete only their own experience."""

    model = Experience
    template_name = "portfolios/experience_confirm_delete.html"
    success_url = reverse_lazy("portfolios:experience_list")
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Experience.objects.filter(
            portfolio__user=self.request.user
        )


class ProjectListView(LoginRequiredMixin, ListView):
    """Display projects belonging to the logged-in user."""

    model = Project
    template_name = "portfolios/project_list.html"
    context_object_name = "projects"
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Project.objects.filter(
            portfolio__user=self.request.user
        )


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Allow users to add projects to their own portfolio."""

    model = Project
    form_class = ProjectForm
    template_name = "portfolios/project_form.html"
    success_url = reverse_lazy("portfolios:project_list")
    login_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        portfolio = get_object_or_404(
            Portfolio,
            user=self.request.user,
        )
        form.instance.portfolio = portfolio

        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """Allow users to update only their own projects."""

    model = Project
    form_class = ProjectForm
    template_name = "portfolios/project_form.html"
    success_url = reverse_lazy("portfolios:project_list")
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Project.objects.filter(
            portfolio__user=self.request.user
        )


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Allow users to delete only their own projects."""

    model = Project
    template_name = "portfolios/project_confirm_delete.html"
    success_url = reverse_lazy("portfolios:project_list")
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Project.objects.filter(
            portfolio__user=self.request.user
        )


class SkillListView(LoginRequiredMixin, ListView):
    """Display skills belonging to the logged-in user."""

    model = Skill
    template_name = "portfolios/skill_list.html"
    context_object_name = "skills"
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Skill.objects.filter(
            portfolio__user=self.request.user
        )


class SkillCreateView(LoginRequiredMixin, CreateView):
    """Allow users to add skills to their own portfolio."""

    model = Skill
    form_class = SkillForm
    template_name = "portfolios/skill_form.html"
    success_url = reverse_lazy("portfolios:skill_list")
    login_url = reverse_lazy("accounts:login")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["portfolio"] = get_object_or_404(
            Portfolio,
            user=self.request.user,
        )

        return kwargs

    def form_valid(self, form):
        form.instance.portfolio = get_object_or_404(
            Portfolio,
            user=self.request.user,
        )

        return super().form_valid(form)


class SkillUpdateView(LoginRequiredMixin, UpdateView):
    """Allow users to update only their own skills."""

    model = Skill
    form_class = SkillForm
    template_name = "portfolios/skill_form.html"
    success_url = reverse_lazy("portfolios:skill_list")
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Skill.objects.filter(
            portfolio__user=self.request.user
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["portfolio"] = self.object.portfolio
        return kwargs


class SkillDeleteView(LoginRequiredMixin, DeleteView):
    """Allow users to delete only their own skills."""

    model = Skill
    template_name = "portfolios/skill_confirm_delete.html"
    success_url = reverse_lazy("portfolios:skill_list")
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        return Skill.objects.filter(
            portfolio__user=self.request.user
        )


class SectionOrderView(LoginRequiredMixin, ListView):
    """Display portfolio sections for drag-and-drop ordering."""

    model = PortfolioSection
    template_name = "portfolios/section_order.html"
    context_object_name = "sections"
    login_url = reverse_lazy("accounts:login")

    def get_queryset(self):
        portfolio = get_object_or_404(
            Portfolio,
            user=self.request.user,
        )

        for order, (section_type, _) in enumerate(
            PortfolioSection.SectionType.choices
        ):
            PortfolioSection.objects.get_or_create(
                portfolio=portfolio,
                section_type=section_type,
                defaults={"sort_order": order},
            )

        return PortfolioSection.objects.filter(
            portfolio=portfolio,
        ).order_by("sort_order", "id")


class SectionReorderView(LoginRequiredMixin, View):
    """Save the updated order of portfolio sections."""

    login_url = reverse_lazy("accounts:login")

    def post(self, request, *args, **kwargs):
        portfolio = get_object_or_404(
            Portfolio,
            user=request.user,
        )

        try:
            raw_section_ids = request.POST.get("section_ids")

            if not raw_section_ids:
                return JsonResponse(
                    {"error": "Section order is required."},
                    status=400,
                )

            section_ids = json.loads(raw_section_ids)

            if not isinstance(section_ids, list):
                return JsonResponse(
                    {"error": "Invalid section order."},
                    status=400,
                )

            if not all(
                isinstance(section_id, int)
                and not isinstance(section_id, bool)
                for section_id in section_ids
            ):
                return JsonResponse(
                    {"error": "Invalid section IDs."},
                    status=400,
                )

            if len(section_ids) != len(set(section_ids)):
                return JsonResponse(
                    {"error": "Duplicate section IDs are not allowed."},
                    status=400,
                )

            sections = list(
                PortfolioSection.objects.filter(
                    portfolio=portfolio,
                )
            )

            existing_ids = {section.pk for section in sections}

            if set(section_ids) != existing_ids:
                return JsonResponse(
                    {"error": "Invalid section selection."},
                    status=400,
                )

            sections_by_id = {
                section.pk: section
                for section in sections
            }

            ordered_sections = []
            for position, section_id in enumerate(section_ids):
                section = sections_by_id[section_id]
                section.sort_order = position
                ordered_sections.append(section)

            with transaction.atomic():
                PortfolioSection.objects.bulk_update(
                    ordered_sections,
                    ["sort_order"],
                )

            return JsonResponse({
                "success": True,
                "message": "Section order saved successfully.",
            })

        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse(
                {"error": "Invalid request data."},
                status=400,
            )


class SectionToggleVisibilityView(LoginRequiredMixin, View):
    """Show or hide one of the logged-in user's portfolio sections."""

    login_url = reverse_lazy("accounts:login")

    def post(self, request, pk, *args, **kwargs):
        section = get_object_or_404(
            PortfolioSection,
            pk=pk,
            portfolio__user=request.user,
        )
        section.is_visible = not section.is_visible
        section.save(update_fields=["is_visible"])

        return redirect("portfolios:section_order")


class PublicPortfolioDetailView(DetailView):
    """Display a portfolio publicly using its unique slug."""

    model = Portfolio
    template_name = "portfolios/public_portfolio.html"
    context_object_name = "portfolio"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Portfolio.objects.filter(
            is_public=True
        ).prefetch_related(
            "educations",
            "experiences",
            "projects",
            "skills__endorsements",
            "sections",
        )

    def get_object(self, queryset=None):
        portfolio = super().get_object(queryset)

        Portfolio.objects.filter(
            pk=portfolio.pk,
            is_public=True,
        ).update(
            view_count=F("view_count") + 1
        )

        portfolio.refresh_from_db(
            fields=["view_count"]
        )

        return portfolio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        portfolio = self.object
        user = self.request.user

        can_endorse = False

        if user.is_authenticated and user != portfolio.user:
            from connections.models import Connection

            can_endorse = Connection.objects.filter(
                Q(requester=user, receiver=portfolio.user)
                | Q(requester=portfolio.user, receiver=user),
                status=Connection.Status.ACCEPTED,
            ).exists()

        context["can_endorse"] = (
            can_endorse and portfolio.allow_endorsements
        )
        context["sections"] = portfolio.get_section_layout()

        return context
