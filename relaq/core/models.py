from datetime import datetime

from django.db import models
from django.utils import timezone


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name = "時間戳"
        verbose_name_plural = "時間戳"

    def created_at_local(self) -> datetime:
        return timezone.localtime(self.created_at)

    def updated_at_local(self) -> datetime:
        return timezone.localtime(self.updated_at)
