#models.py

from django.db import models

class Dialogue(models.Model):
    dialogue_id = models.BigIntegerField(unique=True)  # Поддержка больших и отрицательных ID
    name = models.CharField(max_length=255)
    is_added = models.BooleanField(default=False)

    def __str__(self):
        return self.name
