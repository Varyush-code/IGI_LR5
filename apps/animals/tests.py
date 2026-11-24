import pytest
from django.urls import reverse
from apps.animals.models import Animal
from django.contrib.auth.models import User
from apps.accounts.models import Profile
from apps.employees.models import Employee
from django.core.exceptions import ValidationError

# МОДУЛЬНЫЕ ТЕСТЫ 

def test_animal_string_representation():
    animal = Animal(name='Tiger', species='Big Cat')
    result = str(animal)
    assert result == 'Tiger - Big Cat'


@pytest.mark.parametrize('age', [0, 1, 5, 50, 100])
def test_animal_accepts_valid_age(age):
    animal = Animal(name='Leo', species='Lion', age=age)
    animal.full_clean()
    assert animal.age == age


@pytest.mark.parametrize('age', [-1, -10, -100, 101, 150])
def test_animal_rejects_invalid_age(age):
    animal = Animal(name='Leo', species='Lion', age=age)

    with pytest.raises(ValidationError):
        animal.full_clean()


def test_animal_rejects_age_above_maximum():
    animal = Animal(name='Leo', species='Lion', age=101)

    with pytest.raises(ValidationError) as error:
        animal.full_clean()

    assert 'age' in error.value.message_dict


def test_animal_rejects_negative_age():
    animal = Animal(name='Leo', species='Lion', age=-1)

    with pytest.raises(ValidationError) as error:
        animal.full_clean()

    assert 'age' in error.value.message_dict


@pytest.mark.parametrize(
    'name, species, expected',
    [
        ('Leo', 'Lion', 'Leo - Lion'),
        ('Fox', 'Red Fox', 'Fox - Red Fox'),
        ('Bear', 'Brown Bear', 'Bear - Brown Bear'),
        ('Wolf', 'Gray Wolf', 'Wolf - Gray Wolf'),
    ]
)
def test_animal_string_representation_for_different_animals( name, species, expected):

    animal = Animal(name=name, species=species)
    result = str(animal)
    assert result == expected


def test_animal_default_values():
    animal = Animal()
    
    assert animal.name == 'неизвестно'
    assert animal.species == 'неизвестно'
    assert animal.family == 'неизвестно'
    assert animal.age == 0
    assert animal.gender == 'male'
    assert animal.country == 'неизвестно'
    assert animal.description == ''

@pytest.mark.parametrize('gender', ['male', 'female'])
def test_animal_gender_choices(gender):
    animal = Animal(gender=gender)

    result = animal.gender
    
    assert result == gender
    assert gender in dict(Animal.GENDER_CHOICES)


# ИНТЕГРАЦИОННЫЕ ТЕСТЫ

@pytest.mark.django_db
def test_animal_delete_removes_only_selected_animal(client):
    animal1 = Animal.objects.create(name='Leo', species='Lion')
    animal2 = Animal.objects.create(name='Tiger', species='Tiger')

    response = client.post(
        reverse('animals:delete', args=[animal1.pk])
    )

    assert response.status_code == 302
    assert not Animal.objects.filter(pk=animal1.pk).exists()
    assert Animal.objects.filter(pk=animal2.pk).exists()


@pytest.mark.django_db
def test_animal_list_contains_multiple_animals(client):
    Animal.objects.create(name='Leo', species='Lion')
    Animal.objects.create(name='Tiger', species='Tiger')
    Animal.objects.create(name='Fox', species='Fox')

    response = client.get(reverse('animals:list'))
    content = response.content.decode()

    assert response.status_code == 200
    assert 'Leo' in content
    assert 'Tiger' in content
    assert 'Fox' in content


@pytest.mark.django_db
@pytest.mark.parametrize('age', ['-1', '101', '-50'])
def test_animal_create_rejects_invalid_age(client, age):
    data = {
        'name': 'Leo',
        'species': 'Lion',
        'family': 'Cats',
        'age': age,
        'gender': 'male',
        'country': 'Kenya',
    }
    
    response = client.post(reverse('animals:create'), data)

    assert response.status_code == 400
    assert Animal.objects.count() == 0

@pytest.mark.django_db
@pytest.mark.parametrize('age', ['0', '5', '50', '100'])
def test_animal_create_accepts_valid_age(client, age):
    data = {
        'name': 'Leo',
        'species': 'Lion',
        'family': 'Cats',
        'age': age,
        'gender': 'male',
        'country': 'Kenya',
    }

    response = client.post(reverse('animals:create'), data)

    assert response.status_code == 302

    animal = Animal.objects.get(name='Leo')
    assert animal.age == int(age)


# СЦЕНАРНЫЕ ТЕСТЫ
@pytest.mark.django_db
def test_animal_registration_and_employee_assignment_scenario():
    user = User.objects.create_user(
        username='zookeeper',
        password='test12345'
    )

    profile = Profile.objects.get(user=user)
    profile.role = 'employee'
    profile.save()

    employee = Employee.objects.create(
        name='Иван',
        profile=profile,
        phone='+375 (29) 123-45-67'
    )

    animal = Animal.objects.create(
        name='Leo',
        species='Lion',
        family='Cats',
        age=5,
        gender='male',
        country='Kenya'
    )

    animal.employee.add(employee)

    animal.age = 6
    animal.save()

    animal.refresh_from_db()

    assert animal.age == 6
    assert animal.employee.count() == 1
    assert animal.employee.get() == employee
    assert employee.animals.filter(pk=animal.pk).exists()