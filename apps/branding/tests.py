from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

from .models import LogoDesign


class LogoDesignApiTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="logo_user", password="test-password-123")
        self.other_user = User.objects.create_user(username="other_logo_user", password="test-password-123")
        self.client.force_authenticate(self.user)
        self.list_url = "/api/branding/logos/"

    def test_user_can_create_and_list_logo_design(self):
        payload = {
            "name": "Novyra", "tagline": "Ideas into impact", "industry": "Technology",
            "style": "modern", "symbol": "orbit", "palette": "violet",
        }
        create_response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        list_response = self.client.get(self.list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]["name"], "Novyra")

    def test_user_cannot_access_another_users_logo(self):
        design = LogoDesign.objects.create(user=self.other_user, name="Private Brand")
        response = self.client.delete(f"{self.list_url}{design.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(LogoDesign.objects.filter(pk=design.pk).exists())

    def test_invalid_palette_is_rejected(self):
        response = self.client.post(
            self.list_url,
            {"name": "Test", "palette": "not-a-palette"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoPromptConceptApiTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="prompt_user", password="test-password-123")
        self.client.force_authenticate(self.user)
        self.url = "/api/branding/logo-concepts/"

    @patch.dict("os.environ", {"OPENAI_API_KEY": ""})
    def test_prompt_returns_four_local_concepts_without_ai_key(self):
        response = self.client.post(
            self.url,
            {"prompt": "A premium black and gold lion logo", "name": "Aurum"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["mode"], "local_fallback")
        self.assertEqual(len(response.data["concepts"]), 4)
        self.assertEqual(response.data["concepts"][0]["symbol"], "lion")
        self.assertEqual(response.data["concepts"][0]["palette"], "gold")

    def test_prompt_is_required(self):
        response = self.client.post(self.url, {"name": "Aurum"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
