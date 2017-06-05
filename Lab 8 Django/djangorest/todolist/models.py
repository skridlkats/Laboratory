from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.name)

# ForeignKey Связь многое-к-одному
class Tasklist(models.Model):
    # Этот класс представляет собой модель tasklist
    name = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, blank=True)
    owner = models.ForeignKey('auth.User', default='', related_name='lists', on_delete=models.CASCADE)

    def __str__(self):
        #Вернуть удобочитаемое представление экземпляра модели
        return "{}".format(self.name)


class Task(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    date_modified = models.DateField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks')
    tasklist = models.ForeignKey(Tasklist, related_name='tasks', on_delete=models.CASCADE, null=True)

    PRIORITY = (
        ('h', 'High'),
        ('m', 'Medium'),
        ('l', 'Low'),
        ('n', 'None')
    )

    priority = models.CharField(max_length=1, choices=PRIORITY, default='n')

    def __str__(self):
        return "{}".format(self.name)


