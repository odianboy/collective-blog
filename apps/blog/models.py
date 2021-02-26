from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.conf import settings


class Publication(models.Model):
    class STATUS:
        MODERATION = 0
        APPROVED = 1
        DECLINED = 2
        CHOICES = (
            (MODERATION, 'На модерации'),
            (APPROVED, 'Промодерированно'),
            (DECLINED, 'Отклонено')
        )

    title = models.CharField(max_length=120, verbose_name='Заголовок публикации')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    short_description = models.CharField(max_length=255, verbose_name='Короткое описание')
    text = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='publications',
        verbose_name='Автор публикации',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.PositiveSmallIntegerField(choices=STATUS.CHOICES, default=STATUS.MODERATION)
    rejection_reason = models.CharField(
        blank=True, null=True,
        max_length=120,
        verbose_name='Причина отклонения'
    )
    rejection_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_rating(self):
        rating = PublicationRating.objects.filter(
            publication=self
        ).aggregate(rating=models.Avg('rating'))['rating']

        return round(rating, 1) if rating else None


class CommentPublication(models.Model):
    publication = models.ForeignKey(Publication, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(verbose_name='Текст комментария')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Комментарий от {self.author} к посту {self.publication}'


class PublicationRating(models.Model):
    rating = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, related_name='ratings', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'publication')


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
