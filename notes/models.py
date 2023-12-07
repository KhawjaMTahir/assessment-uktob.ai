"""
Notes Database models.
"""
from django.conf import settings
from django.db import models


class Note(models.Model):
    """Note model to storing user notes."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
