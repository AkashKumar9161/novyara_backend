from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("branding", "0002_logodesign")]

    operations = [
        migrations.AlterField(
            model_name="logodesign",
            name="style",
            field=models.CharField(
                choices=[("modern", "Modern"), ("minimal", "Minimal"), ("premium", "Premium"), ("creative", "Creative"), ("professional", "Professional"), ("geometric", "Geometric"), ("elegant", "Elegant"), ("futuristic", "Futuristic"), ("playful", "Playful"), ("organic", "Organic"), ("vintage", "Vintage")],
                default="modern", max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="logodesign",
            name="symbol",
            field=models.CharField(
                choices=[("monogram", "Monogram"), ("orbit", "Orbit"), ("bloom", "Bloom"), ("mountain", "Mountain"), ("spark", "Spark"), ("leaf", "Leaf"), ("lion", "Lion"), ("shield", "Shield"), ("wave", "Wave"), ("flame", "Flame"), ("hexagon", "Hexagon"), ("globe", "Globe"), ("cube", "Cube"), ("crown", "Crown"), ("bolt", "Bolt"), ("flower", "Flower")],
                default="monogram", max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="logodesign",
            name="palette",
            field=models.CharField(
                choices=[("violet", "Nova Violet"), ("ocean", "Ocean Blue"), ("ember", "Ember"), ("forest", "Forest"), ("mono", "Monochrome"), ("gold", "Black & Gold"), ("rose", "Rose Quartz"), ("sunset", "Sunset"), ("midnight", "Midnight Neon"), ("earth", "Earth Tones"), ("citrus", "Citrus Pop")],
                default="violet", max_length=20,
            ),
        ),
    ]
