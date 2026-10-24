from django.shortcuts import render


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


# Create your views here.
class TaskListCreateView(generics.ListCreateAPIView):
    """
    Allow authenticated users to create tasks and list their own tasks.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Never expose tasks belonging to another user."""
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Assign ownership from the authenticated JWT, not request data."""
        serializer.save(user=self.request.user)
