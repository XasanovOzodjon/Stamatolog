from django.db import models


class GalleryItem(models.Model):
    category = models.CharField(max_length=200)
    before_image = models.ImageField(upload_to='gallery/before/')
    after_image = models.ImageField(upload_to='gallery/after/')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category} #{self.id}"
