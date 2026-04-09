from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200)
    experience = models.PositiveIntegerField(help_text="Yillar soni")
    education = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    patients = models.PositiveIntegerField(default=0)
    languages = models.JSONField(default=list)
    work_schedule = models.JSONField(default=dict)
    is_available = models.BooleanField(default=True)
    telegram_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return self.name
