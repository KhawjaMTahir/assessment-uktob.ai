"""
Urls mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from .views import NoteViewSet


router = DefaultRouter()
router.register("notes", NoteViewSet)

app_name = "note"

urlpatterns = [
    path("", include(router.urls)),
]
