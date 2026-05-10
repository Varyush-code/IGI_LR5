import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.reviews.models import Review

@pytest.mark.django_db
def test_review_creation():
    user = User.objects.create_user(username='john_doe', password='12345')
    
    # Создаем отзыв
    review = Review.objects.create(
        user=user,
        text='Отличный зоопарк! Очень понравилось.',
        rating=5
    )
    
    assert review.user == user
    assert review.text == 'Отличный зоопарк! Очень понравилось.'
    assert review.rating == 5
    assert review.created_at is not None

@pytest.mark.django_db
def test_review_str():
    user = User.objects.create_user(username='jane_smith', password='12345')
    
    review = Review.objects.create(
        user=user,
        text='Хорошее место',
        rating=4
    )
    
    assert str(review) == 'jane_smith - 4'