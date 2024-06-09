# myproject/myapp/models.py
from django.db import models

class Dialogue(models.Model):
    dialogue_id = models.BigIntegerField(unique=True)  # Поддержка больших и отрицательных ID
    name = models.CharField(max_length=255)
    is_added = models.BooleanField(default=False)

    def __str__(self):
        return self.name

from django.db import models

class Message(models.Model):
    message_id = models.BigIntegerField(unique=True)  # Уникальный идентификатор сообщения
    user_id = models.BigIntegerField(null=True)  # ID пользователя, который отправил сообщение, может быть NULL
    date = models.DateTimeField()  # Дата и время отправки сообщения
    text = models.TextField(null=True, default='')  # Текст сообщения, по умолчанию пустой строкой
    dialogue = models.ForeignKey(Dialogue, on_delete=models.CASCADE, related_name='messages')  # Связь с диалогом

    def __str__(self):
        user_id_display = self.user_id if self.user_id is not None else "Unknown"
        return f'Message {self.message_id} by User {user_id_display} on {self.date}'
