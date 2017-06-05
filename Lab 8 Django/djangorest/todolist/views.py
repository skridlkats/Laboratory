from rest_framework import generics
from .serializers import TaskSerializer, TasklistSerializer, TagSerializer
from .models import Task, Tasklist
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

class TagCreateView(generics.ListCreateAPIView):
    # Вид, который отображает форму для создания объекта
    serializer_class = TagSerializer

    def get_queryset(self):
        #итератор, при итерации будет произведен запрос к базе данных
        queryset = Task.objects.all()
        return queryset


class TasklistCreateView(generics.ListCreateAPIView):
    #Этот класс обрабатывает GET и POST запросы нашего rest api
    queryset = Tasklist.objects.all()
    serializer_class = TasklistSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Tasklist.objects.all().filter(owner=self.request.user, )

    def perform_create(self, serializer):
        # Сохранить запись данных при создании нового tasklist
        serializer.save(owner=self.request.user)

class TasklistDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasklist.objects.all()
    serializer_class = TasklistSerializer


class TaskCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None:
            queryset = queryset.filter(tasklist_id = list_id, tasklist_owner =self.request.user)
        return queryset

    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id', None)
        try:
            tasklist = Tasklist.objects.get(pk=list_id) # ошибка! выводит только номера
        except Tasklist.DoesNotExist:
            raise NotFound()
        serializer.save(tasklist=tasklist)
        serializer.save(owner=self.request.user)


class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):
    #Этот класс обрабатывает GET, PUT, DELETE PATCH и запросы.
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        list_id = self.kwargs.get('tasklist_id', None)
        task_id = self.kwargs.get('pk', None)
        if list_id is not None:
            queryset = queryset.filter(tasklist_id = list_id, tasklist_owner =self.request.user, pk=task_id)
        return queryset


class Users(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

