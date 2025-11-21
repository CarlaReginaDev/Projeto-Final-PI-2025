import pytest
from django.test import TestCase, Client
from django.urls import reverse

class ViewTests(TestCase):
    def setUp(self):
        # Import inside setUp method
        from workapp.usuarios.models import Consoles
        self.client = Client()
        self.sample = Consoles.objects.create(name="Test", description="Test description")

    def test_sample_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)