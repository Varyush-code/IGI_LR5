
import pytest
from apps.enclosures.models import Enclosure


# ============================================================
# 1. МОДУЛЬНЫЕ ТЕСТЫ (UNIT TESTS)
# Проверка отдельных свойств и методов модели Enclosure
# ============================================================


# Проверка строкового представления вольера
def test_enclosure_string_representation():
    # Arrange
    enclosure = Enclosure(
        number=1,
        name='Саванна'
    )

    # Act
    result = str(enclosure)

    # Assert
    assert result == 'Саванна'


# Проверка значений полей по умолчанию
def test_enclosure_default_values():
    # Arrange
    enclosure = Enclosure(
        number=1,
        name='Аквариум'
    )

    # Assert
    assert enclosure.enclosure_type == 'savanna'
    assert enclosure.capacity == 1
    assert enclosure.description == ''


# Проверка допустимых типов вольеров
@pytest.mark.parametrize(
    'enclosure_type',
    ['savanna', 'aquarium', 'jungle', 'forest']
)
def test_enclosure_accepts_valid_types(enclosure_type):
    # Arrange
    enclosure = Enclosure(
        number=1,
        name='Тестовый вольер',
        enclosure_type=enclosure_type
    )

    # Act
    enclosure.full_clean()

    # Assert
    assert enclosure.enclosure_type == enclosure_type


# Проверка недопустимых типов вольеров
@pytest.mark.parametrize(
    'enclosure_type',
    ['desert', 'mountain', 'river', 'unknown']
)
def test_enclosure_rejects_invalid_types(enclosure_type):
    # Arrange
    enclosure = Enclosure(
        number=1,
        name='Тестовый вольер',
        enclosure_type=enclosure_type
    )

    # Act / Assert
    with pytest.raises(Exception):
        enclosure.full_clean()


# Проверка разных названий вольеров
@pytest.mark.parametrize(
    'name',
    ['Саванна', 'Аквариум', 'Джунгли', 'Лес']
)
def test_enclosure_string_representation_for_different_names(name):
    # Arrange
    enclosure = Enclosure(number=1, name=name)

    # Act
    result = str(enclosure)

    # Assert
    assert result == name


# Проверка допустимых значений вместимости
@pytest.mark.parametrize(
    'capacity',
    [1, 5, 10, 50, 100]
)
def test_enclosure_accepts_capacity(capacity):
    # Arrange
    enclosure = Enclosure(
        number=1,
        name='Саванна',
        capacity=capacity
    )

    # Act
    enclosure.full_clean()

    # Assert
    assert enclosure.capacity == capacity


# Проверка обязательных полей модели
def test_enclosure_requires_number_and_name():
    # Arrange
    enclosure = Enclosure()

    # Act / Assert
    with pytest.raises(Exception):
        enclosure.full_clean()
