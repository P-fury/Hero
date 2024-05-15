import pytest

from django.test import TestCase
from django.test import Client
from django.urls import reverse


# Create your tests here.


"""GET METHOD TESTS FOR HERO APP
Returns:
    SIMPLE CHECK FOR EVERY PAGE FROM VIEWS  
"""
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


@pytest.mark.django_db
def test_add_activity_type_get():
    client = Client()
    url = reverse('add-activity-type')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_activity_types_get():
    client = Client()
    url = reverse('activity-types')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_activities_get():
    client = Client()
    url = reverse('activities')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_day_get():
    client = Client()
    url = reverse('add-day')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_day_get():
    client = Client()
    url = reverse('day')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_day_get(day_fix):
    client = Client()
    url = reverse('edit-day', args=[day_fix.pk])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_char_page_get():
    client = Client()
    url = reverse('char-page')
    response = client.get(url)
    assert response.status_code == 200
