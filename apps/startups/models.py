from django.conf import settings
from django.db import models


class StartupIdea(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="startup_ideas",
    )
    idea = models.CharField(max_length=500)
    industry = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.idea[:50]}"



class BusinessPlan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="business_plans",
    )
    business_idea = models.CharField(max_length=1000)
    industry = models.CharField(max_length=100)
    plan_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.business_idea[:50]} - {self.user}"


class StartupProject(models.Model):
    """A user's startup workspace that can connect existing ideas, brands and plans."""

    class Stage(models.TextChoices):
        IDEA = "idea", "Idea"
        BRANDING = "branding", "Branding"
        PLANNING = "planning", "Planning"
        BUILDING = "building", "Building"
        LAUNCH = "launch", "Launch"
        LIVE = "live", "Live"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="startup_projects",
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    stage = models.CharField(
        max_length=20,
        choices=Stage.choices,
        default=Stage.IDEA,
    )
    idea = models.ForeignKey(
        StartupIdea,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects",
    )
    brand = models.ForeignKey(
        "branding.SavedBrand",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="startup_projects",
    )
    business_plan = models.ForeignKey(
        BusinessPlan,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="startup_projects",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return f"{self.name} - {self.user}"
