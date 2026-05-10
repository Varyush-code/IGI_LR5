import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.employees.models import Employee
from apps.accounts.models import Profile

@pytest.mark.django_db
def test_animal_creation():

    user = User.objects.create_user(username='john_doe', password='12345')
    profile = Profile.objects.get(user=user)
    profile.role = 'employee'
    profile.save()

    employee = Employee.objects.create(
        name='Пупупу',
        profile=profile,
        phone='+375 (29) 123-45-67',
    )

    assert employee.name == 'Пупупу'
    assert employee.phone == '+375 (29) 123-45-67'
    assert employee.profile == profile

@pytest.mark.django_db
def test_employee_str():
    user = User.objects.create_user(username='john_doe', password='12345')
    profile = Profile.objects.get(user=user)
    profile.role = 'employee'
    profile.save()
    
    employee = Employee.objects.create(
        name='Пупупу',
        profile=profile,
        phone='+375 (29) 123-45-67',
    )
    
    assert str(employee) == 'Пупупу'

@pytest.mark.django_db
def test_employee_list_view(client):
    user = User.objects.create_user(username='john_doe', password='12345')
    profile = Profile.objects.get(user=user)
    profile.role = 'employee'
    profile.save()
    
    Employee.objects.create(
        name='Пупупу',
        profile=profile,
        phone='+375 (29) 123-45-67',
    )
    
    response = client.get(reverse('employees:contacts'))
    
    assert response.status_code == 200
    assert 'Пупупу' in response.content.decode()

@pytest.mark.django_db
def test_employee_update_view(client):
    user = User.objects.create_user(username='john_doe', password='12345')
    profile = Profile.objects.get(user=user)
    profile.role = 'employee'
    profile.save()
    
    employee = Employee.objects.create(
        name='Пупупу',
        profile=profile,
        phone='+375 (29) 123-45-67',
    )
    
    response = client.post(
        reverse('employees:update', args=[employee.pk]),
        {
            'name': '2',
            'profile': profile.id, 
            'phone': '+375 (29) 999-88-77',
            'description': 'ляляля, я хочу спать'
        }
    )
    
    employee.refresh_from_db()
    assert response.status_code == 302
    assert employee.name == '2'
    assert employee.phone == '+375 (29) 999-88-77'

@pytest.mark.django_db
def test_employee_delete_view(client):
    user = User.objects.create_user(username='john_doe', password='12345')
    profile = Profile.objects.get(user=user)
    profile.role = 'employee'
    profile.save()
    
    employee = Employee.objects.create(
        name='Пупупу',
        profile=profile,
        phone='+375 (29) 123-45-67',
    )
    
    response = client.post(
        reverse('employees:delete', args=[employee.pk])
    )
    
    assert response.status_code == 302
    assert Employee.objects.count() == 0
