
from rest_framework import serializers
from .models import BusinessPlan, StartupIdea, StartupProject
from apps.branding.models import SavedBrand


class StartupIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupIdea
        fields = ["id", "idea", "industry", "created_at"]
        read_only_fields = ["id", "created_at"]



class BusinessPlanRequestSerializer(serializers.Serializer):
    business_idea = serializers.CharField(max_length=1000)
    industry = serializers.CharField(max_length=100)
    target_audience = serializers.CharField(
        max_length=300,
        required=False,
        allow_blank=True,
    )
    budget = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )




class BusinessPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPlan
        fields = [
            "id",
            "business_idea",
            "industry",
            "plan_data",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class StartupProjectSerializer(serializers.ModelSerializer):
    idea_title = serializers.CharField(source="idea.idea", read_only=True, default=None)
    brand_name = serializers.CharField(source="brand.name", read_only=True, default=None)
    business_plan_title = serializers.CharField(
        source="business_plan.business_idea", read_only=True, default=None
    )

    class Meta:
        model = StartupProject
        fields = [
            "id", "name", "description", "industry", "stage",
            "idea", "idea_title", "brand", "brand_name",
            "business_plan", "business_plan_title",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "idea_title", "brand_name", "business_plan_title",
            "created_at", "updated_at",
        ]

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            raise serializers.ValidationError("Authentication is required.")

        linked_models = (
            ("idea", StartupIdea),
            ("brand", SavedBrand),
            ("business_plan", BusinessPlan),
        )
        for field, model in linked_models:
            # On partial updates, validate only fields included in the payload.
            if field in attrs and attrs[field] is not None:
                if not model.objects.filter(pk=attrs[field].pk, user=user).exists():
                    raise serializers.ValidationError({
                        field: "Choose an item belonging to your account."
                    })
        return attrs
