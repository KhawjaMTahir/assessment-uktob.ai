"""
Tests for Tags APIs.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Note
from ..serializers import NoteDetailSerializer

NOTES_URL = reverse("note:note-list")


def detail_url(note_id):
    """Create and return a note detail URL."""
    return reverse("note:note-detail", args=[note_id])


def create_note(user, **params):
    "Create and return a sample note."
    defaults = {
        "title": "Sample title",
        "description": "Sample description",
    }
    defaults.update(params)

    note = Note.objects.create(user=user, **defaults)
    return note


def create_user(email="testuser@example.com", password="testpass123"):
    """Create and return new user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicNoteApiTest(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving notes."""
        res = self.client.get(NOTES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):
    """Test for Authenticated API Requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrive_notes(self):
        """Test retrieving a list of notes"""
        create_note(user=self.user)
        create_note(user=self.user)

        res = self.client.get(NOTES_URL)

        notes = Note.objects.all().order_by("-id")
        serializer = NoteDetailSerializer(notes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_notes_list_limited_to_user(self):
        """Test list of notes is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            email="other@example.com", password="otherpass123"
        )
        create_note(user=other_user)
        create_note(user=self.user)

        res = self.client.get(NOTES_URL)

        notes = Note.objects.filter(user=self.user)
        serializer = NoteDetailSerializer(notes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_note_detail(self):
        """Test get note detail."""
        note = create_note(user=self.user)

        url = detail_url(note.id)
        res = self.client.get(url)

        serializer = NoteDetailSerializer(note)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_note(self):
        """Test creating a note."""
        payload = {
            "title": "Sample note",
        }

        res = self.client.post(NOTES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        note = Note.objects.get(id=res.data["id"])
        for k, v in payload.items():
            self.assertEqual(getattr(note, k), v)
        self.assertEqual(note.user, self.user)

    def test_partial_update(self):
        """Test partial update of a recipe."""
        note = create_note(
            user=self.user,
            title="Sample note title",
        )
        payload = {"title": "New note title"}
        url = detail_url(note.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        note.refresh_from_db()
        self.assertEqual(note.title, payload["title"])
        self.assertEqual(note.user, self.user)

    def test_full_update(self):
        """Test full update of note."""
        note = create_note(
            user=self.user,
            title="Sample note title",
            description="Sample note description",
        )
        payload = {
            "title": "New note title",
            "description": "New note description",
        }
        url = detail_url(note.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        note.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(note, k), v)
        self.assertEqual(note.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the note user returns an error."""
        new_user = create_user(
            email="new_user@example.com",
            password="test123"
        )
        note = create_note(user=self.user)

        payload = {"user": new_user.id}
        url = detail_url(note.id)
        self.client.patch(url, payload)

        note.refresh_from_db()
        self.assertEqual(note.user, self.user)

    def test_delete_recipe(self):
        """Test for deleting a note success."""
        note = create_note(user=self.user)

        url = detail_url(note.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(id=note.id).exists())

    def test_delete_other_users_note_error(self):
        """Test trying to delete another users note gives error."""
        new_user = create_user(email="user2@example.com", password="test123")
        note = create_note(user=new_user)

        url = detail_url(note.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Note.objects.filter(id=note.id).exists())
