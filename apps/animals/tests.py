import pytest
from django.urls import reverse
from apps.animals.models import Animal

@pytest.mark.django_db
def test_animal_creation():

    animal = Animal.objects.create(
        name='Leo',
        species='Lion',
        family='Cats',
        age=5,
        gender='male',
        country='Kenya'
    )

    assert animal.name == 'Leo'
    assert animal.species == 'Lion'
    assert animal.family == 'Cats'
    assert animal.age == 5
    assert animal.gender == 'male'


@pytest.mark.django_db
def test_animal_str():

    animal = Animal.objects.create(
        name='Tiger',
        species='Big Cat'
    )
    assert str(animal) == 'Tiger - Big Cat'

@pytest.mark.parametrize(
    'gender',
    [
        'male',
        'female',
    ]
)
@pytest.mark.django_db
def test_gender_choices(gender):

    animal = Animal.objects.create(
        name='Test',
        species='Test Species',
        gender=gender
    )
    assert animal.gender == gender


@pytest.mark.django_db
def test_animal_list_view(client):

    Animal.objects.create(
        name='Wolf',
        species='Gray Wolf'
    )

    response = client.get(
        reverse('animals:list')
    )

    assert response.status_code == 200

    assert 'Wolf' in (
        response.content.decode()
    )


@pytest.mark.django_db
def test_animal_detail_view(client):

    animal = Animal.objects.create(
        name='Fox',
        species='Red Fox'
    )

    response = client.get(
        reverse(
            'animals:detail',
            args=[animal.pk]
        )
    )

    assert response.status_code == 200

    assert 'Fox' in (
        response.content.decode()
    )


@pytest.mark.django_db
def test_animal_create_view(client):

    response = client.post(
        reverse('animals:create'),
        {
            'name': 'Bear',
            'species': 'Brown Bear',
            'family': 'Bears',
            'age': 10,
            'gender': 'male',
            'country': 'Canada',
        }
    )

    assert response.status_code == 302
    assert Animal.objects.count() == 1
    animal = Animal.objects.first()
    assert animal.name == 'Bear'


@pytest.mark.django_db
def test_animal_update_view(client):

    animal = Animal.objects.create(
        name='Old Name',
        species='Wolf'
    )

    response = client.post(
        reverse('animals:update',
            args=[animal.pk]
        ),
        {
            'name': 'New Name',
            'species': 'Wolf',
            'family': 'Canidae',
            'age': 4,
            'gender': 'male',
            'country': 'USA',
        }
    )

    animal.refresh_from_db()
    assert response.status_code == 302
    assert animal.name == 'New Name'

@pytest.mark.django_db
def test_animal_delete_view(client):

    animal = Animal.objects.create(
        name='Delete Animal',
        species='Test'
    )

    response = client.post(
        reverse(
            'animals:delete',
            args=[animal.pk]
        )
    )

    assert response.status_code == 302
    assert Animal.objects.count() == 0