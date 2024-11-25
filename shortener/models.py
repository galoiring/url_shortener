from django.db import models
import random
import string
from django.db.utils import IntegrityError


class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hits = models.PositiveIntegerField(default=0)

    @classmethod
    def create_short_url(cls, original_url):
        max_attempts = 10
        length = 6
        max_length = 10  # Maximum length we'll try before giving up

        while length <= max_length:
            for _ in range(max_attempts):
                try:
                    code = ''.join(random.choices(
                        string.ascii_letters + string.digits, k=length))
                    url_obj, created = cls.objects.get_or_create(
                        short_code=code,
                        defaults={'original_url': original_url}
                    )
                    if created:
                        return url_obj
                except IntegrityError:
                    continue

            length += 1  # Try a longer length

        # If we get here, we've exhausted our options
        raise ValueError(
            "URL shortener capacity reached. Please contact administrator."
        )
