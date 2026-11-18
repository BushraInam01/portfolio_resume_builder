from django.db import migrations


def create_default_sections(apps, schema_editor):
    Portfolio = apps.get_model("portfolios", "Portfolio")
    PortfolioSection = apps.get_model("portfolios", "PortfolioSection")

    section_choices = [
        "about",
        "education",
        "experience",
        "projects",
        "skills",
        "contact",
    ]

    for portfolio in Portfolio.objects.all().iterator():
        for order, section_type in enumerate(section_choices):
            PortfolioSection.objects.get_or_create(
                portfolio_id=portfolio.pk,
                section_type=section_type,
                defaults={
                    "sort_order": order,
                    "is_visible": True,
                },
            )


class Migration(migrations.Migration):

    dependencies = [
        ("portfolios", "0003_portfolio_view_count"),
    ]

    operations = [
        migrations.RunPython(
            create_default_sections,
            migrations.RunPython.noop,
        ),
    ]