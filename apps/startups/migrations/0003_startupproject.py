# Generated for the Novyra startup project workspace.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("branding", "0001_initial"),
        ("startups", "0002_businessplan"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="StartupProject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("industry", models.CharField(blank=True, max_length=100)),
                ("stage", models.CharField(
                    choices=[
                        ("idea", "Idea"),
                        ("branding", "Branding"),
                        ("planning", "Planning"),
                        ("building", "Building"),
                        ("launch", "Launch"),
                        ("live", "Live"),
                    ],
                    default="idea",
                    max_length=20,
                )),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("brand", models.ForeignKey(
                    blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                    related_name="startup_projects", to="branding.savedbrand",
                )),
                ("business_plan", models.ForeignKey(
                    blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                    related_name="startup_projects", to="startups.businessplan",
                )),
                ("idea", models.ForeignKey(
                    blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                    related_name="projects", to="startups.startupidea",
                )),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="startup_projects", to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={"ordering": ["-updated_at", "-created_at"]},
        ),
    ]
