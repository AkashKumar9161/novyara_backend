from django.urls import path
from .views import (
    BusinessPlanGeneratorView, SavedBusinessPlanDetailView,
    SavedBusinessPlanListCreateView, StartupIdeaListCreateView,
    StartupIdeaDetailView, StartupProjectListCreateView, StartupProjectDetailView,
)

urlpatterns = [
    path("projects/", StartupProjectListCreateView.as_view(), name="startup-project-list-create"),
    path("projects/<int:pk>/", StartupProjectDetailView.as_view(), name="startup-project-detail"),
    path("", StartupIdeaListCreateView.as_view(), name="startup-ideas"),
    path("<int:pk>/", StartupIdeaDetailView.as_view(), name="startup-idea-detail"),
    path(
    "generate-plan/",
    BusinessPlanGeneratorView.as_view(),
    name="generate-business-plan",
),
    path(
    "saved-plans/",
    SavedBusinessPlanListCreateView.as_view(),
    name="saved-business-plan-list",
),
path(
    "saved-plans/<int:pk>/",
    SavedBusinessPlanDetailView.as_view(),
    name="saved-business-plan-detail",
),
]