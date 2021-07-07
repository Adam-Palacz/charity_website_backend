import pytest

from django.test import Client
from .models import Category

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_register(client):
    response = client.post('/register/',
                           {'first_name': 'test11',
                            'last_name': 'test11',
                            'email': 'test11@test.pl',
                            'password': 'test11',
                            'password2': 'test11'})
    assert Category.objects.get(name='test11')
