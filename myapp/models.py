from django.db import models

class Dialogue(models.Model):
    dialogue_id = models.BigIntegerField(unique=True)  # Поддержка больших и отрицательных ID
    name = models.CharField(max_length=255)
    is_added = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Message(models.Model):
    message_id = models.BigIntegerField(unique=True)  # Уникальный идентификатор сообщения
    user_id = models.BigIntegerField()  # ID пользователя, который отправил сообщение
    date = models.DateTimeField()  # Дата и время отправки сообщения
    text = models.TextField()  # Текст сообщения
    dialogue = models.ForeignKey(Dialogue, on_delete=models.CASCADE, related_name='messages')  # Связь с диалогом

    def __str__(self):
        return f'Message {self.message_id} by User {self.user_id} on {self.date}'
