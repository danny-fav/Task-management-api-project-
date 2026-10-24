from django.test import TestCase

# Create your tests here.

from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from .models import Task

User = get_user_model()


class TaskAPITests(APITestCase):
    """Verify task CRUD behavior and user-level access restrictions."""

    def setUp(self):
        # Give each test independent users and task records.
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="StrongTestPass123!",
        )
        self.other_user = User.objects.create_user(
            username="bob",
            email="bob@example.com",
            password="AnotherStrongPass123!",
        )

        self.task = Task.objects.create(
            user=self.user,
            title="My first task",
            description="Test task description",
            status=Task.Status.PENDING,
            due_date=date(2026, 11, 1),
        )

        # Authenticate using the same JWT mechanism as the real API.
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {AccessToken.for_user(self.user)}"
        )

    def test_authenticated_user_can_create_task(self):
        response = self.client.post(
            "/api/tasks/",
            {
                "title": "New task",
                "description": "Created through the API",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(user=self.user).count(), 2)

    def test_user_can_only_list_their_own_tasks(self):
        Task.objects.create(user=self.other_user, title="Bob's private task")

        response = self.client.get("/api/tasks/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "My first task")

    def test_user_cannot_retrieve_another_users_task(self):
        other_task = Task.objects.create(
            user=self.other_user,
            title="Private task",
        )

        response = self.client.get(f"/api/tasks/{other_task.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_update_another_users_task(self):
        other_task = Task.objects.create(
            user=self.other_user,
            title="Private task",
        )

        response = self.client.patch(
            f"/api/tasks/{other_task.id}/",
            {"title": "Attempted takeover"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        other_task.refresh_from_db()
        self.assertEqual(other_task.title, "Private task")

    def test_user_cannot_delete_another_users_task(self):
        other_task = Task.objects.create(
            user=self.other_user,
            title="Private task",
        )

        response = self.client.delete(f"/api/tasks/{other_task.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.filter(pk=other_task.pk).exists())

    def test_user_can_update_their_own_task(self):
        response = self.client.patch(
            f"/api/tasks/{self.task.id}/",
            {"status": Task.Status.COMPLETED},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.COMPLETED)

    def test_user_can_delete_their_own_task(self):
        response = self.client.delete(f"/api/tasks/{self.task.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_unauthenticated_user_cannot_access_tasks(self):
        self.client.credentials()

        response = self.client.get("/api/tasks/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
