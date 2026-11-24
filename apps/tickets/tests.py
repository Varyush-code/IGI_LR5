
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse

from apps.tickets.models import Ticket, PromoCode

# МОДУЛЬНЫЕ ТЕСТЫ

@pytest.mark.parametrize(
    'discount',
    [1, 5, 10, 25, 50, 100]
)
@pytest.mark.django_db
def test_promocode_accepts_valid_discount(discount):
    promocode = PromoCode(
        code='ZOO2026',
        discount_percent=discount
    )
    promocode.full_clean()
    assert promocode.discount_percent == discount


@pytest.mark.django_db
def test_promocode_rejects_negative_discount():
    promocode = PromoCode(
        code='ZOO2026',
        discount_percent=-10
    )
    with pytest.raises(ValidationError):
        promocode.full_clean()

@pytest.mark.django_db
def test_ticket_string_representation():
    user = User.objects.create_user(username='zookeeper')
    ticket = Ticket(user=user, day_type='weekday')
    result = str(ticket)
    assert result == 'zookeeper'


@pytest.mark.django_db
def test_ticket_default_values():
    user = User.objects.create_user(username='visitor')
    ticket = Ticket.objects.create(
        user=user,
        day_type='weekday'
    )

    assert ticket.feeding_show is False
    assert ticket.active_hours is False
    assert ticket.final_price == Decimal('0.00')
    assert ticket.created_at is not None


@pytest.mark.parametrize(
    'day_type',
    ['weekday', 'weekend']
)
@pytest.mark.django_db
def test_ticket_accepts_valid_day_types(day_type):
    user = User.objects.create_user(username='visitor')

    ticket = Ticket(
        user=user,
        day_type=day_type
    )

    ticket.full_clean()
    assert ticket.day_type == day_type


@pytest.mark.django_db
def test_ticket_rejects_invalid_day_type():
    user = User.objects.create_user(username='visitor')

    ticket = Ticket(
        user=user,
        day_type='holiday'
    )
    with pytest.raises(ValidationError):
        ticket.full_clean()


def test_promocode_string_representation():
    promocode = PromoCode(
        code='ZOO2026',
        discount_percent=10
    )
    result = str(promocode)
    assert result == 'ZOO2026'


@pytest.mark.django_db
def test_promocode_default_active_value():
    promocode = PromoCode.objects.create(
        code='ZOO2026',
        discount_percent=10
    )
    assert promocode.active is True


# ИНТЕГРАЦИОННЫЕ ТЕСТЫ

@pytest.mark.django_db
def test_ticket_home_displays_active_promocodes(client):
    PromoCode.objects.create(
        code='ACTIVE10',
        discount_percent=10,
        active=True
    )

    PromoCode.objects.create(
        code='INACTIVE10',
        discount_percent=10,
        active=False
    )

    response = client.get(reverse('tickets'))

    assert response.status_code == 200
    assert 'ACTIVE10' in response.content.decode()
    assert 'INACTIVE10' not in response.content.decode()


@pytest.mark.django_db
def test_my_tickets_requires_login(client):
    response = client.get(reverse('my_tickets'))

    assert response.status_code == 302
    assert '/login/' in response.url


@pytest.mark.django_db
def test_ticket_create_requires_login(client):
    response = client.get(reverse('ticket_create'))
    assert response.status_code == 302
    assert '/login/' in response.url


@pytest.mark.django_db
def test_my_tickets_displays_only_current_user_tickets(client):
    user1 = User.objects.create_user(username='visitor1')
    user2 = User.objects.create_user(username='visitor2')

    Ticket.objects.create(user=user1, day_type='weekday')
    Ticket.objects.create(user=user2, day_type='weekend')

    client.force_login(user1)
    response = client.get(reverse('my_tickets'))
    assert response.status_code == 200
    tickets = response.context['tickets']

    assert tickets.count() == 1
    assert tickets.first().user == user1


# ИНТЕГРАЦИОННЫЕ ТЕСТЫ

@pytest.mark.django_db
def test_ticket_create_weekday_price(client):
    user = User.objects.create_user(username='visitor')
    client.force_login(user)

    data = {
        'day_type': 'weekday',
        'feeding_show': False,
        'active_hours': False,
    }

    response = client.post(reverse('ticket_create'), data)
    assert response.status_code == 302
    ticket = Ticket.objects.get(user=user)
    assert ticket.final_price == Decimal('20.00')


@pytest.mark.django_db
def test_ticket_create_weekend_price(client):
    user = User.objects.create_user(username='visitor')
    client.force_login(user)

    data = {
        'day_type': 'weekend',
        'feeding_show': False,
        'active_hours': False,
    }

    response = client.post(reverse('ticket_create'), data)
    assert response.status_code == 302

    ticket = Ticket.objects.get(user=user)
    assert ticket.final_price == Decimal('30.00')


@pytest.mark.django_db
def test_ticket_create_with_feeding_show(client):
    user = User.objects.create_user(username='visitor')
    client.force_login(user)

    data = {
        'day_type': 'weekday',
        'feeding_show': True,
        'active_hours': False,
    }

    response = client.post(reverse('ticket_create'), data)
    assert response.status_code == 302

    ticket = Ticket.objects.get(user=user)
    assert ticket.final_price == Decimal('30.00')


@pytest.mark.django_db
def test_ticket_create_with_active_hours(client):
    user = User.objects.create_user(username='visitor')
    client.force_login(user)

    data = {
        'day_type': 'weekday',
        'feeding_show': False,
        'active_hours': True,
    }

    response = client.post(reverse('ticket_create'), data)
    assert response.status_code == 302

    ticket = Ticket.objects.get(user=user)
    assert ticket.final_price == Decimal('35.00')


@pytest.mark.django_db
def test_ticket_create_with_all_services(client):
    user = User.objects.create_user(username='visitor')
    client.force_login(user)

    data = {
        'day_type': 'weekend',
        'feeding_show': True,
        'active_hours': True,
    }

    response = client.post(reverse('ticket_create'), data)
    assert response.status_code == 302

    ticket = Ticket.objects.get(user=user)
    assert ticket.final_price == Decimal('55.00')


@pytest.mark.django_db
def test_ticket_create_with_promocode(client):
    user = User.objects.create_user(username='visitor')
    client.force_login(user)

    promocode = PromoCode.objects.create(
        code='ZOO10',
        discount_percent=10,
        active=True
    )

    data = {
        'day_type': 'weekday',
        'feeding_show': False,
        'active_hours': False,
        'promocode': promocode.pk,
    }

    response = client.post(reverse('ticket_create'), data)
    assert response.status_code == 302

    ticket = Ticket.objects.get(user=user)
    assert ticket.final_price == Decimal('18.00')


# СЦЕНАРНЫЕ ТЕСТЫ
  
@pytest.mark.django_db
def test_user_ticket_purchase_scenario(client):
    user = User.objects.create_user(username='visitor')
    client.force_login(user)

    promocode = PromoCode.objects.create(
        code='ZOO20',
        discount_percent=20,
        active=True
    )

    data = {
        'day_type': 'weekend',
        'feeding_show': True,
        'active_hours': True,
        'promocode': promocode.pk,
    }

    response = client.post(reverse('ticket_create'), data)
    if response.status_code != 302:
        print(response.context['form'].errors)

    assert response.status_code == 302
    ticket = Ticket.objects.get(user=user)

    assert ticket.final_price == Decimal('44.00')
    assert ticket.day_type == 'weekend'
    assert ticket.feeding_show is True
    assert ticket.active_hours is True
    assert user.tickets.count() == 1
