from django.contrib.auth import get_user_model
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    latitude = models.DecimalField(max_digits=16, decimal_places=6)
    longitude = models.DecimalField(max_digits=16, decimal_places=6)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="locations", null=False, default=None)

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"

    class Meta:
        unique_together = (('name', 'user'),)
        verbose_name_plural = "Locations"
        verbose_name = "Location"
        ordering = ['-id']