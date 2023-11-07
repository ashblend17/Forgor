from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from .models import Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
        )


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            'number',
            'title',
            'user',
            'description',
            'resolution',
            'deadline',
            'state',
            'created_at',
        )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer