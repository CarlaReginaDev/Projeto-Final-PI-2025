import pytest
from django.test import TestCase
from workapp.usuarios.models import Consoles

class ConsolesTest(TestCase):
    def test_model_creation(self):
        """Test that we can create a sample model"""
        sample = Consoles.objects.create(name="Test", description="Test description")
        self.assertEqual(sample.name, "Test")
        self.assertEqual(str(sample), "Test")