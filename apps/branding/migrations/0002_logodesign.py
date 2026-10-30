from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("branding", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogoDesign",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("tagline", models.CharField(blank=True, max_length=255)),
                ("industry", models.CharField(blank=True, max_length=100)),
                ("style", models.CharField(choices=[("modern", "Modern"), ("minimal", "Minimal"), ("premium", "Premium"), ("creative", "Creative"), ("professional", "Professional")], default="modern", max_length=20)),
                ("symbol", models.CharField(choices=[("monogram", "Monogram"), ("orbit", "Orbit"), ("bloom", "Bloom"), ("mountain", "Mountain"), ("spark", "Spark"), ("leaf", "Leaf")], default="monogram", max_length=20)),
                ("palette", models.CharField(choices=[("violet", "Nova Violet"), ("ocean", "Ocean Blue"), ("ember", "Ember"), ("forest", "Forest"), ("mono", "Monochrome")], default="violet", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="logo_designs", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-updated_at"]},
        ),
    ]
