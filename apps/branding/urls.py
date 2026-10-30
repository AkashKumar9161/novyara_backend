from django.urls import path
from .views import (
    BrandNameGeneratorView,
    SavedBrandListCreateView,
    SavedBrandDeleteView,
    LogoDesignListCreateView,
    LogoDesignDetailView,
    LogoConceptGeneratorView,
)

urlpatterns = [
    path("generate/", BrandNameGeneratorView.as_view(), name="brand-generate"),
    path("saved/", SavedBrandListCreateView.as_view(), name="saved-brand-list-create"),
    path("saved/<int:pk>/", SavedBrandDeleteView.as_view(), name="saved-brand-delete"),
    path("logo-concepts/", LogoConceptGeneratorView.as_view(), name="logo-concept-generator"),
    path("logos/", LogoDesignListCreateView.as_view(), name="logo-design-list-create"),
    path("logos/<int:pk>/", LogoDesignDetailView.as_view(), name="logo-design-detail"),
]
