import pytest
from django.test import TestCase, Client
from django.urls import reverse
from WorkApp.usuarios.models import Consoles

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.sample = Consoles.objects.create(name="Test", description="Test description")

    def test_sample_list_view(self):
        response = self.client.get(reverse('sample-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")