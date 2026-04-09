from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    doctor = models.ForeignKey(
        'doctors.Doctor', on_delete=models.CASCADE, related_name='reviews'
    )
    patient_name = models.CharField(max_length=200)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient_name} - Dr.{self.doctor.name} ({self.rating}/5)"
