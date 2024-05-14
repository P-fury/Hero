import pytest

from django.test import TestCase
from django.test import Client
from django.urls import reverse


# Create your tests here.
@pytest.mark.django_db
def test_main_get():
    client = Client()
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_char_create_get():
    client = Client()
    url = reverse('char-create')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_char_get():
    client = Client()
    url = reverse('char')
    response = client.get(url)
    assert response.status_code == 200
