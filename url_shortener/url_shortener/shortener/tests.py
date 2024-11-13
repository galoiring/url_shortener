from django.test import TestCase, Client
from django.urls import reverse
from .models import URL
import json


class URLShortenerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_url = "https://ravkavonline.co.il"

    def test_create_short_url(self):
        response = self.client.post(
            reverse('create_short_url'),
            data=json.dumps({'url': self.valid_url}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue('short_url' in response.json())

    def test_redirect_to_original(self):
        # Create a URL object first
        url_obj = URL.objects.create(
            original_url=self.valid_url,
            short_code='testcode'
        )

        # Test the redirect
        response = self.client.get(
            reverse('redirect_to_original', args=['testcode']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.valid_url)

        # Verify hit counter increased
        url_obj.refresh_from_db()
        self.assertEqual(url_obj.hits, 1)

    def test_nonexistent_short_url(self):
        response = self.client.get(
            reverse('redirect_to_original', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)
