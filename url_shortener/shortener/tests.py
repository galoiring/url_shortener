from django.test import TestCase, Client
from django.urls import reverse
from .models import URL
import json


class URLShortenerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_url = "https://www.example.com"
        self.invalid_url = "not-a-valid-url"

    def test_home_page(self):
        """Test that home page loads correctly"""
        response = self.client.get(reverse('shortener:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shortener/url_shortener.html')

    def test_create_short_url_success(self):
        """Test successful URL shortening"""
        response = self.client.post(
            reverse('shortener:create_short_url'),
            data=json.dumps({'url': self.valid_url}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('short_url', data)

        # Verify URL was created in database
        short_code = data['short_url'].split('/')[-1]
        self.assertTrue(URL.objects.filter(short_code=short_code).exists())

    def test_create_short_url_invalid_url(self):
        """Test URL shortening with invalid URL"""
        response = self.client.post(
            reverse('shortener:create_short_url'),
            data=json.dumps({'url': self.invalid_url}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_create_short_url_duplicate(self):
        """Test that duplicate URLs return the same short code"""
        # Create first URL
        response1 = self.client.post(
            reverse('shortener:create_short_url'),
            data=json.dumps({'url': self.valid_url}),
            content_type='application/json'
        )

        # Create second URL with same original URL
        response2 = self.client.post(
            reverse('shortener:create_short_url'),
            data=json.dumps({'url': self.valid_url}),
            content_type='application/json'
        )

        self.assertEqual(response1.json()['short_url'],
                         response2.json()['short_url'])

    def test_redirect_to_original(self):
        """Test URL redirection works correctly"""
        # Create a URL first
        url_obj = URL.objects.create(
            original_url=self.valid_url,
            short_code='testcode'
        )

        response = self.client.get(
            reverse('shortener:redirect', args=['testcode']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.valid_url)

    def test_redirect_nonexistent_url(self):
        """Test handling of non-existent short URLs"""
        response = self.client.get(
            reverse('shortener:redirect', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)

    def test_short_code_generation(self):
        """Test that short code generation works and is unique"""
        code1 = URL.generate_short_code()
        code2 = URL.generate_short_code()

        self.assertNotEqual(code1, code2)
        self.assertEqual(len(code1), 6)  # Based on your current configuration
        self.assertTrue(all(c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                            for c in code1))

    def test_invalid_json_request(self):
        """Test handling of invalid JSON in request"""
        response = self.client.post(
            reverse('shortener:create_short_url'),
            data='invalid json',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_missing_url_parameter(self):
        """Test handling of missing URL parameter"""
        response = self.client.post(
            reverse('shortener:create_short_url'),
            data=json.dumps({}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
