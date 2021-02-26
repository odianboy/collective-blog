from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthorProfile(AbstractUser):
    phone = models.CharField(max_length=16, verbose_name='Телефон автора')
    skype = models.CharField(max_length=30, verbose_name='Skype автора')
    avatar = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, verbose_name='Аватар автора')

    def __str__(self):
        return f'{self.username}'
