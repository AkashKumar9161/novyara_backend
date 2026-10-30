from django.conf import settings
from django.db import models


class SavedBrand(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_brands",
    )
    name = models.CharField(max_length=100)
    meaning = models.TextField()
    tagline = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_saved_brand_per_user",
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.user}"


class LogoDesign(models.Model):
    STYLE_CHOICES = [
        ("modern", "Modern"),
        ("minimal", "Minimal"),
        ("premium", "Premium"),
        ("creative", "Creative"),
        ("professional", "Professional"),
        ("geometric", "Geometric"),
        ("elegant", "Elegant"),
        ("futuristic", "Futuristic"),
        ("playful", "Playful"),
        ("organic", "Organic"),
        ("vintage", "Vintage"),
    ]
    SYMBOL_CHOICES = [
        ("monogram", "Monogram"),
        ("orbit", "Orbit"),
        ("bloom", "Bloom"),
        ("mountain", "Mountain"),
        ("spark", "Spark"),
        ("leaf", "Leaf"),
        ("lion", "Lion"),
        ("shield", "Shield"),
        ("wave", "Wave"),
        ("flame", "Flame"),
        ("hexagon", "Hexagon"),
        ("globe", "Globe"),
        ("cube", "Cube"),
        ("crown", "Crown"),
        ("bolt", "Bolt"),
        ("flower", "Flower"),
    ]
    PALETTE_CHOICES = [
        ("violet", "Nova Violet"),
        ("ocean", "Ocean Blue"),
        ("ember", "Ember"),
        ("forest", "Forest"),
        ("mono", "Monochrome"),
        ("gold", "Black & Gold"),
        ("rose", "Rose Quartz"),
        ("sunset", "Sunset"),
        ("midnight", "Midnight Neon"),
        ("earth", "Earth Tones"),
        ("citrus", "Citrus Pop"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="logo_designs",
    )
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, default="modern")
    symbol = models.CharField(max_length=20, choices=SYMBOL_CHOICES, default="monogram")
    palette = models.CharField(max_length=20, choices=PALETTE_CHOICES, default="violet")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Logo: {self.name} - {self.user}"
