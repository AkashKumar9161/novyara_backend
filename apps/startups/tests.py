from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from .models import StartupIdea, StartupProject, BusinessPlan
from apps.branding.models import SavedBrand

User = get_user_model()


class StartupProjectAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="founder1", password="SafePass123!")
        self.other_user = User.objects.create_user(username="founder2", password="SafePass123!")
        self.client.force_authenticate(user=self.user)
        self.list_url = "/api/startups/projects/"

    def test_create_and_list_project_for_authenticated_user(self):
        response = self.client.post(self.list_url, {
            "name": "Novyra",
            "industry": "SaaS",
            "stage": "idea",
            "description": "Startup launch workspace",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Novyra")
        self.assertEqual(StartupProject.objects.get().user, self.user)

        list_response = self.client.get(self.list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

    def test_project_can_link_owned_idea_brand_and_plan(self):
        idea = StartupIdea.objects.create(user=self.user, idea="AI startup", industry="SaaS")
        brand = SavedBrand.objects.create(
            user=self.user, name="NovaForge", meaning="New beginnings",
            tagline="Build what comes next", industry="SaaS",
        )
        plan = BusinessPlan.objects.create(
            user=self.user, business_idea="AI startup", industry="SaaS",
            plan_data={"business_overview": "A test plan"},
        )
        response = self.client.post(self.list_url, {
            "name": "AI Startup",
            "idea": idea.id,
            "brand": brand.id,
            "business_plan": plan.id,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["idea_title"], "AI startup")
        self.assertEqual(response.data["brand_name"], "NovaForge")
        self.assertEqual(response.data["business_plan_title"], "AI startup")

    def test_cannot_link_another_users_resources(self):
        foreign_idea = StartupIdea.objects.create(
            user=self.other_user, idea="Private idea", industry="Other"
        )
        response = self.client.post(self.list_url, {
            "name": "Invalid link",
            "idea": foreign_idea.id,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_read_or_delete_another_users_project(self):
        foreign_project = StartupProject.objects.create(
            user=self.other_user, name="Private workspace"
        )
        detail_url = f"{self.list_url}{foreign_project.id}/"
        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.delete(detail_url).status_code, status.HTTP_404_NOT_FOUND)

    def test_stage_can_be_updated(self):
        project = StartupProject.objects.create(user=self.user, name="Novyra")
        response = self.client.patch(
            f"{self.list_url}{project.id}/",
            {"stage": "building"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.stage, "building")
