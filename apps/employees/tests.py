import pytest
from django.core.exceptions import ValidationError
from apps.employees.models import Employee


def test_employee_string_representation():
    employee = Employee(name='Иван')
    result = str(employee)
    assert result == 'Иван'


@pytest.mark.parametrize(
    'name',
    [
        'Иван',
        'Александр',
        'Мария',
        'John',
    ]
)
def test_employee_string_representation_for_different_names(name):
    # Arrange
    employee = Employee(name=name)

    # Act
    result = str(employee)

    # Assert
    assert result == name


@pytest.mark.parametrize(
    'phone',
    [
        '+375 (29) 123-45-67',
        '+375 (33) 987-65-43',
        '+375 (44) 111-22-33',
    ]
)
def test_employee_phone_validator_accepts_valid_numbers(phone):
    validator = Employee.phone_regex
    validator(phone)
    assert True


@pytest.mark.parametrize(
    'phone',
    [
        '123456789',
        '+375291234567',
        '+375 (29) 1234567',
        'invalid',
        '',
    ]
)
def test_employee_phone_validator_rejects_invalid_numbers(phone):
    validator = Employee.phone_regex
    with pytest.raises(ValidationError):
        validator(phone)