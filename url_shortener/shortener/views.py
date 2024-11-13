from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import json
from .models import URL


def home(request):
    return render(request, 'shortener/url_shortener.html')


def create_short_url(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            original_url = data.get('url')

            # Check if URL already exists
            existing_url = URL.objects.filter(
                original_url=original_url).first()
            if existing_url:
                short_url = request.build_absolute_uri(
                    f'/s/{existing_url.short_code}')
                return JsonResponse({'short_url': short_url})

            # Create new shortened URL
            short_code = URL.generate_short_code()
            URL.objects.create(
                original_url=original_url,
                short_code=short_code
            )

            short_url = request.build_absolute_uri(f'/s/{short_code}')
            return JsonResponse({'short_url': short_url})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def redirect_to_original(request, short_code):
    try:
        url_obj = URL.objects.get(short_code=short_code)
        return redirect(url_obj.original_url)
    except URL.DoesNotExist:
        return JsonResponse({'error': 'URL not found'}, status=404)
