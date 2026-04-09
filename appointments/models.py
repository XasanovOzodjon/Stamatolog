from django.db import models
from django.core.validators import RegexValidator


PHONE_REGEX = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak"
)

STATUS_CHOICES = [
    ('pending', 'Kutilmoqda'),
    ('confirmed', 'Tasdiqlangan'),
    ('cancelled', 'Bekor qilingan'),
    ('completed', 'Bajarilgan'),
]


class Appointment(models.Model):
    service = models.ForeignKey('services.Service', on_delete=models.PROTECT)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField()
    patient_name = models.CharField(max_length=200)
    patient_phone = models.CharField(max_length=20, validators=[PHONE_REGEX])
    patient_email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']
        # Bir doktor, bir vaqtda bitta appointment
        unique_together = [['doctor', 'date', 'time']]

    def __str__(self):
        return f"{self.patient_name} - {self.date} {self.time}"
