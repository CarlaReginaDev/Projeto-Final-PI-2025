import pytest
from django.test import TestCase

class ConsolesTest(TestCase):
    def test_model_creation(self):
        """Test that we can create a sample model"""
        # Import inside the test method to avoid early loading
        from workapp.usuarios.models import Consoles
        sample = Consoles.objects.create(name="Test", description="Test description")
        self.assertEqual(sample.name, "Test")
        self.assertEqual(str(sample), "Test")