from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Daqiqalar")
    price = models.PositiveIntegerField(default=0, help_text="So'm")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.name
