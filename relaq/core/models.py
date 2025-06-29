from datetime import datetime

from django.db import models
from django.utils import timezone


class TimeStamped(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="建立時間",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新時間",
    )

    class Meta:
        abstract = True
        verbose_name = "時間戳"
        verbose_name_plural = "時間戳"

    def created_at_local(self) -> datetime:
        return timezone.localtime(self.created_at)

    def updated_at_local(self) -> datetime:
        return timezone.localtime(self.updated_at)
