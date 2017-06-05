from rest_framework import serializers
from .models import Task, Tasklist, Tag
from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):
    # Serializer отобразить экземпляр модели в формате JSON
    class Meta:
        # Карта это сериалайзер к модели и их поля
        model = Tag
        fields = ('id', 'name')


class TaskSerializer(serializers.ModelSerializer):
    # Serializer отобразить экземпляр модели в формате JSON
    # SlugRelatedField (газетные заголовки) то же, что и charFields
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        # Карта это сериалайзер к модели и их поля
        model = Task
        fields = ('id', 'name', 'owner', 'tags', 'description', 'completed', 'date_created', 'date_modified', 'due_date', 'priority')
        read_only_fields = ('date_created', 'date_modified')


class TasklistSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tasklist
        fields = ('id', 'name', 'owner', 'tasks')#,'description', 'date_created', 'date_modified', 'due_date', 'priority')
        #read_only_fields = ('date_created', 'date_modified')


class UserSerializer(serializers.ModelSerializer):
    lists = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'lists', 'password')
        write_only_fields = ('password', )
        read_only_fields = ('id', )

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username']) # проверка на пользователя
        user.set_password(validated_data['password'])
        user.save()
        return user