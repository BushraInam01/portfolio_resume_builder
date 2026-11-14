from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import (
    Portfolio,
    PortfolioSection,
    Education,
    Experience,
    Project,
    Skill,
)

User = get_user_model()


class PortfolioViewTests(TestCase):
    """Test portfolio authentication, ownership and CRUD operations."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPass123!",
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="StrongPass123!",
        )

        self.portfolio = Portfolio.objects.create(
            user=self.user,
            title="My Portfolio",
            slug="my-portfolio",
            full_name="Portfolio Owner",
            professional_title="Python Developer",
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("portfolios:dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('portfolios:dashboard')}",
        )

    def test_dashboard_displays_own_portfolio(self):
        self.client.login(
            email="owner@example.com",
            password="StrongPass123!",
        )

        response = self.client.get(reverse("portfolios:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["portfolio"], self.portfolio)

    def test_dashboard_does_not_display_another_users_portfolio(self):
        self.client.login(
            email="other@example.com",
            password="StrongPass123!",
        )

        response = self.client.get(reverse("portfolios:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["portfolio"])

    def test_user_can_create_portfolio(self):
        self.client.login(
            email="other@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("portfolios:portfolio_create"),
            {
                "title": "New Portfolio",
                "slug": "new-portfolio",
                "full_name": "New User",
                "professional_title": "Django Learner",
                "bio": "Learning Django development.",
                "location": "Pakistan",
                "phone": "",
                "website": "",
                "linkedin_url": "",
                "github_url": "",
                "is_public": False,
                "allow_endorsements": True,
            },
        )

        self.assertRedirects(response, reverse("portfolios:dashboard"))

        portfolio = Portfolio.objects.get(user=self.other_user)

        self.assertEqual(portfolio.title, "New Portfolio")
        self.assertEqual(portfolio.slug, "new-portfolio")

    def test_created_portfolio_is_assigned_to_logged_in_user(self):
        self.client.login(
            email="other@example.com",
            password="StrongPass123!",
        )

        self.client.post(
            reverse("portfolios:portfolio_create"),
            {
                "title": "New Portfolio",
                "slug": "assigned-portfolio",
                "full_name": "New User",
                "professional_title": "Python Developer",
                "bio": "",
                "location": "",
                "phone": "",
                "website": "",
                "linkedin_url": "",
                "github_url": "",
                "is_public": False,
                "allow_endorsements": True,
            },
        )

        portfolio = Portfolio.objects.get(slug="assigned-portfolio")

        self.assertEqual(portfolio.user, self.other_user)

    def test_user_cannot_create_second_portfolio(self):
        self.client.login(
            email="owner@example.com",
            password="StrongPass123!",
        )

        response = self.client.get(
            reverse("portfolios:portfolio_create")
        )

        self.assertRedirects(
            response,
            reverse("portfolios:portfolio_update"),
        )

        self.assertEqual(
            Portfolio.objects.filter(user=self.user).count(),
            1,
        )

    def test_user_can_update_own_portfolio(self):
        self.client.login(
            email="owner@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("portfolios:portfolio_update"),
            {
                "title": "Updated Portfolio",
                "slug": "updated-portfolio",
                "full_name": "Updated Owner",
                "professional_title": "Python Backend Developer",
                "bio": "Updated biography.",
                "location": "Bahawalpur",
                "phone": "",
                "website": "",
                "linkedin_url": "",
                "github_url": "",
                "is_public": False,
                "allow_endorsements": True,
            },
        )

        self.assertRedirects(response, reverse("portfolios:dashboard"))

        self.portfolio.refresh_from_db()

        self.assertEqual(self.portfolio.title, "Updated Portfolio")
        self.assertEqual(self.portfolio.full_name, "Updated Owner")

    def test_user_cannot_access_another_users_portfolio_update(self):
        self.client.login(
            email="other@example.com",
            password="StrongPass123!",
        )

        response = self.client.get(
            reverse("portfolios:portfolio_update")
        )

        self.assertEqual(response.status_code, 404)

    def test_invalid_portfolio_form_is_rejected(self):
        self.client.login(
            email="other@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("portfolios:portfolio_create"),
            {
                "title": "",
                "slug": "invalid-portfolio",
                "full_name": "New User",
                "professional_title": "Developer",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Portfolio.objects.filter(user=self.other_user).exists()
        )

    def test_portfolio_create_page_requires_login(self):
        response = self.client.get(
            reverse("portfolios:portfolio_create")
        )

        self.assertEqual(response.status_code, 302)

    def test_portfolio_update_page_requires_login(self):
        response = self.client.get(
            reverse("portfolios:portfolio_update")
        )

        self.assertEqual(response.status_code, 302)


class EducationViewTests(TestCase):
    """Test education CRUD, authentication and ownership."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="education@example.com",
            password="StrongPass123!",
        )

        self.other_user = User.objects.create_user(
            email="othereducation@example.com",
            password="StrongPass123!",
        )

        self.portfolio = Portfolio.objects.create(
            user=self.user,
            title="Education Portfolio",
            slug="education-portfolio",
        )

        self.other_portfolio = Portfolio.objects.create(
            user=self.other_user,
            title="Other Portfolio",
            slug="other-portfolio",
        )

        self.education = Education.objects.create(
            portfolio=self.portfolio,
            institution="Virtual University",
            degree="BS",
            field_of_study="Information Technology",
            start_date="2021-03-24",
            end_date="2025-03-10",
            is_current=False,
        )

        self.client.login(
            email="education@example.com",
            password="StrongPass123!",
        )

    def education_data(self):
        return {
            "institution": "Virtual University of Pakistan",
            "degree": "BS",
            "field_of_study": "Information Technology",
            "start_date": "2021-03-24",
            "end_date": "2025-03-10",
            "is_current": False,
            "description": "Bachelor degree in Information Technology.",
        }

    def test_education_list_requires_login(self):
        self.client.logout()

        response = self.client.get(
            reverse("portfolios:education_list")
        )

        self.assertEqual(response.status_code, 302)

    def test_user_can_view_own_education(self):
        response = self.client.get(
            reverse("portfolios:education_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Virtual University")
        self.assertEqual(
            list(response.context["educations"]),
            [self.education],
        )

    def test_user_cannot_view_another_users_education(self):
        other_education = Education.objects.create(
            portfolio=self.other_portfolio,
            institution="Other University",
            degree="BS",
            start_date="2020-01-01",
            end_date="2024-01-01",
        )

        response = self.client.get(
            reverse("portfolios:education_list")
        )

        self.assertNotContains(response, "Other University")
        self.assertNotIn(
            other_education,
            response.context["educations"],
        )

    def test_user_can_add_education(self):
        response = self.client.post(
            reverse("portfolios:education_create"),
            self.education_data(),
        )

        self.assertRedirects(
            response,
            reverse("portfolios:education_list"),
        )

        education = Education.objects.get(
            institution="Virtual University of Pakistan"
        )

        self.assertEqual(education.portfolio, self.portfolio)

    def test_user_cannot_add_education_without_portfolio(self):
        self.client.logout()

        User.objects.create_user(
            email="noportfolio@example.com",
            password="StrongPass123!",
        )

        self.client.login(
            email="noportfolio@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("portfolios:education_create"),
            self.education_data(),
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_update_own_education(self):
        response = self.client.post(
            reverse(
                "portfolios:education_update",
                args=[self.education.pk],
            ),
            {
                **self.education_data(),
                "institution": "Updated University",
            },
        )

        self.assertRedirects(
            response,
            reverse("portfolios:education_list"),
        )

        self.education.refresh_from_db()

        self.assertEqual(
            self.education.institution,
            "Updated University",
        )

    def test_user_cannot_update_another_users_education(self):
        other_education = Education.objects.create(
            portfolio=self.other_portfolio,
            institution="Other University",
            degree="BS",
            start_date="2020-01-01",
            end_date="2024-01-01",
        )

        response = self.client.get(
            reverse(
                "portfolios:education_update",
                args=[other_education.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_own_education(self):
        response = self.client.post(
            reverse(
                "portfolios:education_delete",
                args=[self.education.pk],
            )
        )

        self.assertRedirects(
            response,
            reverse("portfolios:education_list"),
        )

        self.assertFalse(
            Education.objects.filter(pk=self.education.pk).exists()
        )

    def test_user_cannot_delete_another_users_education(self):
        other_education = Education.objects.create(
            portfolio=self.other_portfolio,
            institution="Other University",
            degree="BS",
            start_date="2020-01-01",
            end_date="2024-01-01",
        )

        response = self.client.post(
            reverse(
                "portfolios:education_delete",
                args=[other_education.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            Education.objects.filter(pk=other_education.pk).exists()
        )

    def test_invalid_education_dates_are_rejected(self):
        data = self.education_data()
        data["start_date"] = "2025-03-10"
        data["end_date"] = "2021-03-24"

        response = self.client.post(
            reverse("portfolios:education_create"),
            data,
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Education.objects.filter(
                institution="Virtual University of Pakistan"
            ).exists()
        )


class ExperienceViewTests(TestCase):
    """Test experience CRUD, authentication and ownership."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="experience@example.com",
            password="StrongPass123!",
        )

        self.other_user = User.objects.create_user(
            email="otherexperience@example.com",
            password="StrongPass123!",
        )

        self.portfolio = Portfolio.objects.create(
            user=self.user,
            title="Experience Portfolio",
            slug="experience-portfolio",
        )

        self.other_portfolio = Portfolio.objects.create(
            user=self.other_user,
            title="Other Experience Portfolio",
            slug="other-experience-portfolio",
        )

        self.experience = Experience.objects.create(
            portfolio=self.portfolio,
            company="ABC Software House",
            position="Python Developer",
            employment_type="full_time",
            location="Bahawalpur",
            start_date="2024-01-01",
            end_date="2025-01-01",
            is_current=False,
            description="Worked on backend development.",
        )

        self.client.login(
            email="experience@example.com",
            password="StrongPass123!",
        )

    def experience_data(self):
        return {
            "company": "XYZ Technologies",
            "position": "Django Developer",
            "employment_type": "full_time",
            "location": "Lahore",
            "start_date": "2025-01-01",
            "end_date": "2026-01-01",
            "is_current": False,
            "description": "Developed Django applications.",
        }

    def test_experience_list_requires_login(self):
        self.client.logout()

        response = self.client.get(
            reverse("portfolios:experience_list")
        )

        self.assertEqual(response.status_code, 302)

    def test_user_can_view_own_experience(self):
        response = self.client.get(
            reverse("portfolios:experience_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABC Software House")
        self.assertEqual(
            list(response.context["experiences"]),
            [self.experience],
        )

    def test_user_cannot_view_another_users_experience(self):
        other_experience = Experience.objects.create(
            portfolio=self.other_portfolio,
            company="Other Company",
            position="Developer",
            start_date="2020-01-01",
        )

        response = self.client.get(
            reverse("portfolios:experience_list")
        )

        self.assertNotContains(response, "Other Company")
        self.assertNotIn(
            other_experience,
            response.context["experiences"],
        )

    def test_user_can_add_experience(self):
        response = self.client.post(
            reverse("portfolios:experience_create"),
            self.experience_data(),
        )

        self.assertRedirects(
            response,
            reverse("portfolios:experience_list"),
        )

        experience = Experience.objects.get(
            company="XYZ Technologies"
        )

        self.assertEqual(experience.portfolio, self.portfolio)

    def test_user_cannot_add_experience_without_portfolio(self):
        self.client.logout()

        User.objects.create_user(
            email="noexperience@example.com",
            password="StrongPass123!",
        )

        self.client.login(
            email="noexperience@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("portfolios:experience_create"),
            self.experience_data(),
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_update_own_experience(self):
        response = self.client.post(
            reverse(
                "portfolios:experience_update",
                args=[self.experience.pk],
            ),
            {
                **self.experience_data(),
                "company": "Updated Company",
            },
        )

        self.assertRedirects(
            response,
            reverse("portfolios:experience_list"),
        )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.company,
            "Updated Company",
        )

    def test_user_cannot_update_another_users_experience(self):
        other_experience = Experience.objects.create(
            portfolio=self.other_portfolio,
            company="Other Company",
            position="Developer",
            start_date="2020-01-01",
        )

        response = self.client.get(
            reverse(
                "portfolios:experience_update",
                args=[other_experience.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_own_experience(self):
        response = self.client.post(
            reverse(
                "portfolios:experience_delete",
                args=[self.experience.pk],
            )
        )

        self.assertRedirects(
            response,
            reverse("portfolios:experience_list"),
        )

        self.assertFalse(
            Experience.objects.filter(
                pk=self.experience.pk
            ).exists()
        )

    def test_user_cannot_delete_another_users_experience(self):
        other_experience = Experience.objects.create(
            portfolio=self.other_portfolio,
            company="Other Company",
            position="Developer",
            start_date="2020-01-01",
        )

        response = self.client.post(
            reverse(
                "portfolios:experience_delete",
                args=[other_experience.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            Experience.objects.filter(
                pk=other_experience.pk
            ).exists()
        )

    def test_invalid_experience_dates_are_rejected(self):
        data = self.experience_data()
        data["start_date"] = "2026-01-01"
        data["end_date"] = "2025-01-01"

        response = self.client.post(
            reverse("portfolios:experience_create"),
            data,
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Experience.objects.filter(
                company="XYZ Technologies"
            ).exists()
        )

class ProjectViewTests(TestCase):
    """Test project authentication, ownership and CRUD operations."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="project@example.com",
            password="StrongPass123!",
        )

        self.other_user = User.objects.create_user(
            email="otherproject@example.com",
            password="StrongPass123!",
        )

        self.portfolio = Portfolio.objects.create(
            user=self.user,
            title="Project Portfolio",
            slug="project-portfolio",
        )

        self.other_portfolio = Portfolio.objects.create(
            user=self.other_user,
            title="Other Project Portfolio",
            slug="other-project-portfolio",
        )

        self.project = Project.objects.create(
            portfolio=self.portfolio,
            title="My First Project",
            description="A sample Django project.",
            technologies="Python, Django",
            start_date="2025-01-01",
            end_date="2025-06-01",
        )

        self.client.login(
            email="project@example.com",
            password="StrongPass123!",
        )

    def project_data(self):
        return {
            "title": "Portfolio Website",
            "description": "Built using Python and Django.",
            "technologies": "Python, Django, HTML, CSS",
            "project_url": "https://example.com",
            "source_code_url": "https://github.com/example/project",
            "start_date": "2025-01-01",
            "end_date": "2025-12-01",
        }

    def test_project_list_requires_login(self):
        self.client.logout()

        response = self.client.get(
            reverse("portfolios:project_list")
        )

        self.assertEqual(response.status_code, 302)

    def test_user_can_view_own_projects(self):
        response = self.client.get(
            reverse("portfolios:project_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My First Project")

    def test_user_cannot_view_other_users_projects(self):
        Project.objects.create(
            portfolio=self.other_portfolio,
            title="Private Project",
            description="This belongs to another user.",
        )

        response = self.client.get(
            reverse("portfolios:project_list")
        )

        self.assertNotContains(response, "Private Project")

    def test_user_can_create_project(self):
        response = self.client.post(
            reverse("portfolios:project_create"),
            self.project_data(),
        )

        self.assertRedirects(
            response,
            reverse("portfolios:project_list"),
        )

        self.assertTrue(
            Project.objects.filter(
                portfolio=self.portfolio,
                title="Portfolio Website",
            ).exists()
        )

    def test_user_cannot_create_project_without_portfolio(self):
        self.client.logout()

        user_without_portfolio = User.objects.create_user(
            email="noportfolio@example.com",
            password="StrongPass123!",
        )

        self.client.login(
            email="noportfolio@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("portfolios:project_create"),
            self.project_data(),
        )

        self.assertEqual(response.status_code, 404)

        self.assertFalse(
            Project.objects.filter(
                title="Portfolio Website"
            ).exists()
        )

    def test_user_can_update_own_project(self):
        data = self.project_data()
        data["title"] = "Updated Project"

        response = self.client.post(
            reverse(
                "portfolios:project_update",
                args=[self.project.pk],
            ),
            data,
        )

        self.assertRedirects(
            response,
            reverse("portfolios:project_list"),
        )

        self.project.refresh_from_db()

        self.assertEqual(
            self.project.title,
            "Updated Project",
        )

    def test_user_cannot_update_other_users_project(self):
        other_project = Project.objects.create(
            portfolio=self.other_portfolio,
            title="Other User Project",
            description="Private project.",
        )

        response = self.client.post(
            reverse(
                "portfolios:project_update",
                args=[other_project.pk],
            ),
            self.project_data(),
        )

        self.assertEqual(response.status_code, 404)

        other_project.refresh_from_db()

        self.assertEqual(
            other_project.title,
            "Other User Project",
        )

    def test_user_can_delete_own_project(self):
        response = self.client.post(
            reverse(
                "portfolios:project_delete",
                args=[self.project.pk],
            )
        )

        self.assertRedirects(
            response,
            reverse("portfolios:project_list"),
        )

        self.assertFalse(
            Project.objects.filter(
                pk=self.project.pk
            ).exists()
        )

    def test_user_cannot_delete_other_users_project(self):
        other_project = Project.objects.create(
            portfolio=self.other_portfolio,
            title="Protected Project",
            description="This project must remain safe.",
        )

        response = self.client.post(
            reverse(
                "portfolios:project_delete",
                args=[other_project.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            Project.objects.filter(
                pk=other_project.pk
            ).exists()
        )

    def test_invalid_project_dates_are_rejected(self):
        data = self.project_data()
        data["start_date"] = "2026-01-01"
        data["end_date"] = "2025-01-01"

        response = self.client.post(
            reverse("portfolios:project_create"),
            data,
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Project.objects.filter(
                title="Portfolio Website"
            ).exists()
        )

class SkillViewTests(TestCase):
    """Test skill authentication, ownership and CRUD operations."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="skill@example.com",
            password="StrongPass123!",
        )

        self.other_user = User.objects.create_user(
            email="otherskill@example.com",
            password="StrongPass123!",
        )

        self.portfolio = Portfolio.objects.create(
            user=self.user,
            title="Skill Portfolio",
            slug="skill-portfolio",
        )

        self.other_portfolio = Portfolio.objects.create(
            user=self.other_user,
            title="Other Skill Portfolio",
            slug="other-skill-portfolio",
        )

        self.skill = Skill.objects.create(
            portfolio=self.portfolio,
            name="Python",
            proficiency="advanced",
        )

        self.client.login(
            email="skill@example.com",
            password="StrongPass123!",
        )

    def skill_data(self):
        return {
            "name": "Django",
            "proficiency": "intermediate",
        }

    def test_skill_list_requires_login(self):
        self.client.logout()

        response = self.client.get(
            reverse("portfolios:skill_list")
        )

        self.assertEqual(response.status_code, 302)

    def test_user_can_view_own_skills(self):
        response = self.client.get(
            reverse("portfolios:skill_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")

    
    def test_user_cannot_view_other_users_skills(self):
        Skill.objects.create(
            portfolio=self.other_portfolio,
            name="Java",
            proficiency="beginner",
        )

        response = self.client.get(
            reverse("portfolios:skill_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<h3>Java</h3>")

        self.assertEqual(
            list(response.context["skills"]),
            [self.skill],
        )


    def test_user_can_add_skill(self):
        response = self.client.post(
            reverse("portfolios:skill_create"),
            self.skill_data(),
        )

        self.assertRedirects(
            response,
            reverse("portfolios:skill_list"),
        )

        self.assertTrue(
            Skill.objects.filter(
                portfolio=self.portfolio,
                name="Django",
            ).exists()
        )

    def test_user_without_portfolio_cannot_add_skill(self):
        new_user = User.objects.create_user(
            email="noportfolio@example.com",
            password="StrongPass123!",
        )

        self.client.force_login(new_user)

        response = self.client.post(
            reverse("portfolios:skill_create"),
            self.skill_data(),
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_update_own_skill(self):
        response = self.client.post(
            reverse(
                "portfolios:skill_update",
                args=[self.skill.pk],
            ),
            {
                "name": "Python Programming",
                "proficiency": "expert",
            },
        )

        self.assertRedirects(
            response,
            reverse("portfolios:skill_list"),
        )

        self.skill.refresh_from_db()

        self.assertEqual(
            self.skill.name,
            "Python Programming",
        )

        self.assertEqual(
            self.skill.proficiency,
            "expert",
        )

    def test_user_cannot_update_other_users_skill(self):
        other_skill = Skill.objects.create(
            portfolio=self.other_portfolio,
            name="Java",
            proficiency="beginner",
        )

        response = self.client.post(
            reverse(
                "portfolios:skill_update",
                args=[other_skill.pk],
            ),
            self.skill_data(),
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_own_skill(self):
        response = self.client.post(
            reverse(
                "portfolios:skill_delete",
                args=[self.skill.pk],
            )
        )

        self.assertRedirects(
            response,
            reverse("portfolios:skill_list"),
        )

        self.assertFalse(
            Skill.objects.filter(
                pk=self.skill.pk
            ).exists()
        )

    def test_user_cannot_delete_other_users_skill(self):
        other_skill = Skill.objects.create(
            portfolio=self.other_portfolio,
            name="Java",
            proficiency="beginner",
        )

        response = self.client.post(
            reverse(
                "portfolios:skill_delete",
                args=[other_skill.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            Skill.objects.filter(
                pk=other_skill.pk
            ).exists()
        )

    def test_duplicate_skill_name_is_rejected_case_insensitively(self):
        response = self.client.post(
            reverse("portfolios:skill_create"),
            {
                "name": "python",
                "proficiency": "advanced",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Skill.objects.filter(
                portfolio=self.portfolio
            ).count(),
            1,
        )

    def test_invalid_proficiency_is_rejected(self):
        response = self.client.post(
            reverse("portfolios:skill_create"),
            {
                "name": "HTML",
                "proficiency": "master",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Skill.objects.filter(
                portfolio=self.portfolio,
                name="HTML",
            ).exists()
        )


class SectionOrderingTests(TestCase):
    """Test section ordering, authentication and ownership."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="sections@example.com",
            password="StrongPass123!",
        )

        self.other_user = User.objects.create_user(
            email="othersections@example.com",
            password="StrongPass123!",
        )

        self.portfolio = Portfolio.objects.create(
            user=self.user,
            title="Section Portfolio",
            slug="section-portfolio",
        )

        self.other_portfolio = Portfolio.objects.create(
            user=self.other_user,
            title="Other Section Portfolio",
            slug="other-section-portfolio",
        )

        self.client.login(
            email="sections@example.com",
            password="StrongPass123!",
        )

    def create_sections(self, portfolio):
        sections = []

        for order, (section_type, _) in enumerate(
            PortfolioSection.SectionType.choices
        ):
            section = PortfolioSection.objects.create(
                portfolio=portfolio,
                section_type=section_type,
                sort_order=order,
            )
            sections.append(section)

        return sections

    def test_section_order_page_requires_login(self):
        self.client.logout()

        response = self.client.get(
            reverse("portfolios:section_order")
        )

        self.assertEqual(response.status_code, 302)

    def test_section_order_page_creates_default_sections(self):
        response = self.client.get(
            reverse("portfolios:section_order")
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            PortfolioSection.objects.filter(
                portfolio=self.portfolio
            ).count(),
            len(PortfolioSection.SectionType.choices),
        )

    def test_user_only_sees_own_sections(self):
        self.create_sections(self.other_portfolio)

        response = self.client.get(
            reverse("portfolios:section_order")
        )

        self.assertEqual(response.status_code, 200)

        displayed_sections = list(response.context["sections"])

        self.assertTrue(
            all(
                section.portfolio == self.portfolio
                for section in displayed_sections
            )
        )

    def test_user_can_reorder_own_sections(self):
        sections = self.create_sections(self.portfolio)

        reordered_ids = [
            section.pk for section in reversed(sections)
        ]

        response = self.client.post(
            reverse("portfolios:section_reorder"),
            {
                "section_ids": __import__("json").dumps(
                    reordered_ids
                )
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "success": True,
                "message": "Section order saved successfully.",
            },
        )

        for position, section_id in enumerate(reordered_ids):
            section = PortfolioSection.objects.get(pk=section_id)
            self.assertEqual(section.sort_order, position)

    def test_user_cannot_reorder_another_users_sections(self):
        own_sections = self.create_sections(self.portfolio)
        other_sections = self.create_sections(self.other_portfolio)

        invalid_ids = [
            section.pk for section in other_sections
        ]

        response = self.client.post(
            reverse("portfolios:section_reorder"),
            {
                "section_ids": __import__("json").dumps(
                    invalid_ids
                )
            },
        )

        self.assertEqual(response.status_code, 400)

        for section in own_sections:
            section.refresh_from_db()
            self.assertEqual(
                section.sort_order,
                own_sections.index(section),
            )

    def test_duplicate_section_ids_are_rejected(self):
        sections = self.create_sections(self.portfolio)

        section_ids = [section.pk for section in sections]
        section_ids[-1] = section_ids[0]

        response = self.client.post(
            reverse("portfolios:section_reorder"),
            {
                "section_ids": __import__("json").dumps(
                    section_ids
                )
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_section_data_is_rejected(self):
        response = self.client.post(
            reverse("portfolios:section_reorder"),
            {"section_ids": "invalid-json"},
        )

        self.assertEqual(response.status_code, 400)

    def test_user_without_portfolio_cannot_reorder_sections(self):
        self.client.logout()

        user = User.objects.create_user(
            email="noportfolio-sections@example.com",
            password="StrongPass123!",
        )

        self.client.force_login(user)

        response = self.client.post(
            reverse("portfolios:section_reorder"),
            {"section_ids": "[]"},
        )

        self.assertEqual(response.status_code, 404)


class PortfolioViewCounterTests(TestCase):
    """Test public portfolio view counting."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="viewcounter@example.com",
            password="StrongPass123!",
        )

        self.portfolio = Portfolio.objects.create(
            user=self.user,
            title="View Counter Portfolio",
            slug="view-counter-portfolio",
            is_public=True,
        )

        self.public_url = reverse(
            "portfolios:public_detail",
            kwargs={"slug": self.portfolio.slug},
        )

    def test_anonymous_visitor_increments_view_count(self):
        response = self.client.get(self.public_url)

        self.assertEqual(response.status_code, 200)

        self.portfolio.refresh_from_db()

        self.assertEqual(self.portfolio.view_count, 1)

    def test_each_public_visit_increments_view_count(self):
        self.client.get(self.public_url)
        self.client.get(self.public_url)
        self.client.get(self.public_url)

        self.portfolio.refresh_from_db()

        self.assertEqual(self.portfolio.view_count, 3)

    def test_private_portfolio_does_not_increment_view_count(self):
        self.portfolio.is_public = False
        self.portfolio.save(update_fields=["is_public"])

        response = self.client.get(self.public_url)

        self.assertEqual(response.status_code, 404)

        self.portfolio.refresh_from_db()

        self.assertEqual(self.portfolio.view_count, 0)

    def test_owner_visit_increments_view_count(self):
        self.client.force_login(self.user)

        response = self.client.get(self.public_url)

        self.assertEqual(response.status_code, 200)

        self.portfolio.refresh_from_db()

        self.assertEqual(self.portfolio.view_count, 1)
