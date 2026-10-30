from rest_framework import serializers

from .models import LogoDesign, SavedBrand


class BrandNameRequestSerializer(serializers.Serializer):
    business_idea = serializers.CharField(max_length=500)
    industry = serializers.CharField(max_length=100)
    style = serializers.ChoiceField(
        choices=["modern", "premium", "creative", "minimal", "professional"],
        default="modern",
    )


class SavedBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedBrand
        fields = ["id", "name", "meaning", "tagline", "industry", "created_at"]
        read_only_fields = ["id", "created_at"]


class LogoDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogoDesign
        fields = [
            "id", "name", "tagline", "industry", "style", "symbol", "palette",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class LogoPromptSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=2000, trim_whitespace=True)
    name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    tagline = serializers.CharField(max_length=255, required=False, allow_blank=True)
    industry = serializers.CharField(max_length=100, required=False, allow_blank=True)
