from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import URL


@csrf_exempt
@require_http_methods(["POST"])
def create_short_url(request):
    try:
        data = json.loads(request.body)
        original_url = data.get('url')

        if not original_url:
            return JsonResponse({'error': 'URL is required'}, status=400)

        # Generate a unique short code
        short_code = URL.generate_short_code()

        # Create the URL object
        url_obj = URL.objects.create(
            original_url=original_url,
            short_code=short_code
        )

        # Construct the short URL
        short_url = f"http://localhost:8000/s/{short_code}"
        return JsonResponse({'short_url': short_url})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def redirect_to_original(request, short_code):
    try:
        url_obj = URL.objects.get(short_code=short_code)
        url_obj.hits += 1
        url_obj.save()
        return HttpResponseRedirect(url_obj.original_url)
    except URL.DoesNotExist:
        return HttpResponseNotFound("Short URL not found")
