"""
Tests for user model.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Note


def create_user(email="testuser@example.com", password="testpass123"):
    """Create and return new user."""
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):
    """Test Models."""

    def test_create_tag(self):
        """Test creating a tag is succesful."""
        user = create_user()
        tag = Note.objects.create(
            user=user, title="Note1", description="Note1 Description"
        )

        self.assertEqual(str(tag), tag.title)
