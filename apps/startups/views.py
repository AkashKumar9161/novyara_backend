import json
import logging
import os

from django.shortcuts import get_object_or_404
from openai import OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import BusinessPlan, StartupIdea, StartupProject
from .serializers import (
    BusinessPlanRequestSerializer, BusinessPlanSerializer,
    StartupIdeaSerializer, StartupProjectSerializer,
)


class StartupIdeaListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ideas = StartupIdea.objects.filter(user=request.user)
        serializer = StartupIdeaSerializer(ideas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StartupIdeaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StartupIdeaDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_object_or_404(
            StartupIdea,
            pk=pk,
            user=request.user,
        )

    def get(self, request, pk):
        idea = self.get_object(request, pk)
        serializer = StartupIdeaSerializer(idea)
        return Response(serializer.data)

    def put(self, request, pk):
        idea = self.get_object(request, pk)
        serializer = StartupIdeaSerializer(idea, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        idea = self.get_object(request, pk)
        serializer = StartupIdeaSerializer(
            idea,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        idea = self.get_object(request, pk)
        idea.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




logger = logging.getLogger(__name__)


class BusinessPlanGeneratorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BusinessPlanRequestSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            return Response(
                {"error": "AI service is not configured."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        data = serializer.validated_data

        prompt = f"""
Create a practical startup business plan.

Business idea: {data['business_idea']}
Industry: {data['industry']}
Target audience: {data.get('target_audience') or 'Suggest a suitable audience'}
Budget: {data.get('budget') or 'Suggest a lean starting budget'}

Return valid JSON with these keys:
business_overview, problem, solution, target_audience,
revenue_model, marketing_strategy, competitor_research,
mvp_features, launch_roadmap, risks.

Requirements:
- Be realistic and actionable.
- Do not invent verified market statistics.
- For competitor research, suggest what to investigate;
  do not claim research has been conducted.
- Label budget figures as estimates.
- Make the launch roadmap suitable for a first-time founder.
"""

        try:
            client = OpenAI(api_key=api_key)

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a startup planning assistant. "
                            "Return valid JSON only."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.5,
            )

            result = json.loads(
                completion.choices[0].message.content
            )

            return Response(
                {"business_plan": result},
                status=status.HTTP_200_OK,
            )

        except Exception:
            logger.exception("Business plan generation failed")
            return Response(
                {"error": "Business plan generation failed. Please try again."},
                status=status.HTTP_502_BAD_GATEWAY,
            )





class SavedBusinessPlanListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = BusinessPlan.objects.filter(user=request.user)
        serializer = BusinessPlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BusinessPlanSerializer(data=request.data)

        if serializer.is_valid():
            plan = serializer.save(user=request.user)
            return Response(
                BusinessPlanSerializer(plan).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class SavedBusinessPlanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_object_or_404(
            BusinessPlan,
            pk=pk,
            user=request.user,
        )

    def get(self, request, pk):
        plan = self.get_object(request, pk)
        serializer = BusinessPlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        plan = self.get_object(request, pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StartupProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = StartupProject.objects.filter(user=request.user).select_related(
            "idea", "brand", "business_plan"
        )
        return Response(
            StartupProjectSerializer(projects, many=True, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = StartupProjectSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            project = serializer.save(user=request.user)
            return Response(
                StartupProjectSerializer(project, context={"request": request}).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StartupProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_object_or_404(
            StartupProject.objects.select_related("idea", "brand", "business_plan"),
            pk=pk,
            user=request.user,
        )

    def get(self, request, pk):
        project = self.get_object(request, pk)
        return Response(
            StartupProjectSerializer(project, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        project = self.get_object(request, pk)
        serializer = StartupProjectSerializer(
            project, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            project = serializer.save()
            return Response(
                StartupProjectSerializer(project, context={"request": request}).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        project = self.get_object(request, pk)
        serializer = StartupProjectSerializer(
            project, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            project = serializer.save()
            return Response(
                StartupProjectSerializer(project, context={"request": request}).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(request, pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
