
from django.contrib import admin

from .models import (
    Portfolio,
    PortfolioSection,
    Education,
    Experience,
    Project,
    Skill,
)


class PortfolioSectionInline(admin.TabularInline):
    model = PortfolioSection
    extra = 0


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "slug",
        "is_public",
        "created_at",
    )

    search_fields = (
        "title",
        "user__email",
        "full_name",
        "slug",
    )

    list_filter = (
        "is_public",
        "allow_endorsements",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    inlines = [
        PortfolioSectionInline,
        EducationInline,
        ExperienceInline,
        ProjectInline,
        SkillInline,
    ]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "institution",
        "degree",
        "portfolio",
        "start_date",
        "end_date",
    )

    search_fields = (
        "institution",
        "degree",
        "portfolio__user__email",
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "position",
        "company",
        "portfolio",
        "employment_type",
        "is_current",
    )

    list_filter = (
        "employment_type",
        "is_current",
    )

    search_fields = (
        "position",
        "company",
        "portfolio__user__email",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "portfolio",
        "start_date",
        "end_date",
    )

    search_fields = (
        "title",
        "technologies",
        "portfolio__user__email",
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "portfolio",
        "proficiency",
        "sort_order",
    )

    list_filter = (
        "proficiency",
    )

    search_fields = (
        "name",
        "portfolio__user__email",
    )


@admin.register(PortfolioSection)
class PortfolioSectionAdmin(admin.ModelAdmin):
    list_display = (
        "portfolio",
        "section_type",
        "sort_order",
        "is_visible",
    )

    list_filter = (
        "section_type",
        "is_visible",
    )

