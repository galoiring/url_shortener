from django.db import models
import random
import string


class URL(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=50, unique=True, blank=True)
    hits = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = self._generate_short_url()
        super().save(*args, **kwargs)

    def _generate_short_url(self):
        length = 6
        chars = string.ascii_letters + string.digits
        while True:
            short_url = ''.join(random.choices(chars, k=length))
            if not URL.objects.filter(short_url=short_url).exists():
                return short_url

    def __str__(self):
        return f"{self.original_url} -> {self.short_url}"

    class Meta:
        ordering = ['-created_at']
