from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import json
from .models import URL
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import F


def validate_url(url):
    validator = URLValidator()
    try:
        # Add http:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        validator(url)
        return url
    except ValidationError:
        return None


def home(request):
    return render(request, 'shortener/url_shortener.html')


def create_short_url(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            original_url = data.get('url')

            # Validate URL
            valid_url = validate_url(original_url)
            if not valid_url:
                return JsonResponse({'error': 'Invalid URL format'}, status=400)

            # Create new shortened URL using atomic operation
            try:
                url_obj = URL.create_short_url(valid_url)
                short_url = request.build_absolute_uri(
                    reverse('redirect_to_original', kwargs={
                        'short_code': url_obj.short_code})
                )
                return JsonResponse({'short_url': short_url})
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def redirect_to_original(request, short_code):
    try:
        url_obj = URL.objects.get(short_code=short_code)
        URL.objects.filter(id=url_obj.id).update(hits=F('hits') + 1)
        return redirect(url_obj.original_url, permanent=False)
    except URL.DoesNotExist:
        return JsonResponse({'error': 'URL not found'}, status=404)
