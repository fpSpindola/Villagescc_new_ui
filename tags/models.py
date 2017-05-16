from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
