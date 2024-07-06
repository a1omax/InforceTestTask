from datetime import datetime

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from employees.models import Vote, Employee
from restaurants.models import Restaurant, Menu


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def employee(db):
    return Employee.objects.create(username='testuser', password='thehardestpass', email='user@mail.com')


@pytest.fixture
def authenticated_client(api_client, employee):
    api_client.force_authenticate(user=employee)
    return api_client


@pytest.fixture
def restaurant():
    return Restaurant.objects.create(name="testrestaurant", address="testaddress")


@pytest.mark.django_db
def test_registration(api_client):
    response = api_client.post('/api/registration/', {
        'username': 'newuser1',
        'password': 'thehardestpass',
        'email': 'test@test.test'
    })
    assert response.status_code == 200
    assert 'username' in response.data


@pytest.mark.django_db
def test_profile(authenticated_client, employee):
    response = authenticated_client.get('/api/profile/')
    assert response.status_code == 200
    assert response.data['username'] == employee.username


@pytest.mark.django_db
def test_today_votes(authenticated_client, employee, restaurant):

    Vote.objects.create(user=employee, date=datetime.now().date(), restaurant=restaurant)

    response = authenticated_client.get('/api/today-votes/')

    assert response.status_code == 200
    assert response.data['results'][0]['restaurant'] == restaurant.name


@pytest.mark.django_db
def test_vote_create(authenticated_client, restaurant, employee):

    response = authenticated_client.post('/api/vote/', {"restaurant": restaurant.id})
    assert response.status_code == 201
    assert response.data['restaurant'] == restaurant.id
    assert response.data['date'] == datetime.now().date().strftime('%Y-%m-%d')

