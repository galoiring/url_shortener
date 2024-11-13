# shortener/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, redirect, get_object_or_404
from .models import URL
import json


@ensure_csrf_cookie
def home(request):
    return render(request, 'shortener/home.html')


def create_url(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        if url:
            url_obj = URL.objects.create(original_url=url)
            return JsonResponse({
                'short_url': url_obj.short_url,
                'original_url': url_obj.original_url
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_urls(request):
    urls = URL.objects.all().order_by('-created_at')[:10]
    return JsonResponse([{
        'original_url': url.original_url,
        'short_url': url.short_url,
        'hits': url.hits,
        'created_at': url.created_at.isoformat()
    } for url in urls], safe=False)


def redirect_url(request, short_url):
    url_obj = get_object_or_404(URL, short_url=short_url)
    url_obj.hits += 1
    url_obj.save()
    return redirect(url_obj.original_url)
