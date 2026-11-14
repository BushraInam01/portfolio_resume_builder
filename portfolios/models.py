
from django.conf import settings
from django.db import models
from colorfield.fields import ColorField


class Portfolio(models.Model):
    """Main portfolio owned by a single user."""

    class ResumeTheme(models.TextChoices):
        CLASSIC = "classic", "Classic"
        MODERN = "modern", "Modern"
        MINIMAL = "minimal", "Minimal"
        PROFESSIONAL = "professional", "Professional"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolio",
    )

    title = models.CharField(
        max_length=120,
        default="My Portfolio",
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    full_name = models.CharField(
        max_length=150,
        blank=True,
    )

    professional_title = models.CharField(
        max_length=150,
        blank=True,
    )

    bio = models.TextField(
        blank=True,
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    linkedin_url = models.URLField(
        blank=True,
    )

    github_url = models.URLField(
        blank=True,
    )

    is_public = models.BooleanField(
        default=False,
    )

    view_count = models.PositiveBigIntegerField(
        default=0,
    )

    allow_endorsements = models.BooleanField(
        default=True,
    )

    # Resume Theme Customization

    resume_theme = models.CharField(
        max_length=20,
        choices=ResumeTheme.choices,
        default=ResumeTheme.CLASSIC,
    )

    accent_color = ColorField(
        default="#2563EB",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    def get_section_layout(self, visible_only=True):
        """Return sections in the owner's chosen order.

        Section types without a saved row yet fall back to their default
        position and are visible, so public pages never need to write to
        the database just to render.
        """
        saved = {s.section_type: s for s in self.sections.all()}
        layout = []

        for default_order, (section_type, _) in enumerate(
            PortfolioSection.SectionType.choices
        ):
            layout.append(
                saved.get(section_type)
                or PortfolioSection(
                    portfolio=self,
                    section_type=section_type,
                    sort_order=default_order,
                )
            )

        layout.sort(key=lambda s: s.sort_order)

        if visible_only:
            layout = [s for s in layout if s.is_visible]

        return layout


class PortfolioSection(models.Model):
    """Manage portfolio section visibility and ordering."""

    class SectionType(models.TextChoices):
        ABOUT = "about", "About"
        EDUCATION = "education", "Education"
        EXPERIENCE = "experience", "Experience"
        PROJECTS = "projects", "Projects"
        SKILLS = "skills", "Skills"
        CONTACT = "contact", "Contact"

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="sections",
    )

    section_type = models.CharField(
        max_length=30,
        choices=SectionType.choices,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    is_visible = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["sort_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["portfolio", "section_type"],
                name="unique_portfolio_section_type",
            ),
        ]

    def __str__(self):
        return f"{self.portfolio.title} - {self.get_section_type_display()}"


class Education(models.Model):
    """Store portfolio owner's education records."""

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="educations",
    )

    institution = models.CharField(
        max_length=200,
    )

    degree = models.CharField(
        max_length=150,
    )

    field_of_study = models.CharField(
        max_length=150,
        blank=True,
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    is_current = models.BooleanField(
        default=False,
    )

    description = models.TextField(
        blank=True,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["sort_order", "-start_date"]

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Experience(models.Model):
    """Store portfolio owner's professional experience."""

    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full-time"
        PART_TIME = "part_time", "Part-time"
        INTERNSHIP = "internship", "Internship"
        FREELANCE = "freelance", "Freelance"
        CONTRACT = "contract", "Contract"

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="experiences",
    )

    company = models.CharField(
        max_length=200,
    )

    position = models.CharField(
        max_length=150,
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        blank=True,
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    is_current = models.BooleanField(
        default=False,
    )

    description = models.TextField(
        blank=True,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["sort_order", "-start_date"]

    def __str__(self):
        return f"{self.position} - {self.company}"


class Project(models.Model):
    """Store portfolio owner's projects."""

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField()

    technologies = models.CharField(
        max_length=300,
        blank=True,
    )

    project_url = models.URLField(
        blank=True,
    )

    source_code_url = models.URLField(
        blank=True,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["sort_order", "-start_date"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    """Store skills that can receive endorsements."""

    class ProficiencyLevel(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"
        EXPERT = "expert", "Expert"

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="skills",
    )

    name = models.CharField(
        max_length=100,
    )

    proficiency = models.CharField(
        max_length=20,
        choices=ProficiencyLevel.choices,
        default=ProficiencyLevel.INTERMEDIATE,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["sort_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["portfolio", "name"],
                name="unique_portfolio_skill",
            ),
        ]

    def __str__(self):
        return self.name
