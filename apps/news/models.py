from django.db import models

class News(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )

    content = models.TextField(
        verbose_name='Текст новости'
    )

    image = models.ImageField(
        upload_to='news/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'