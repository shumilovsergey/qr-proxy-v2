from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Users(models.Model):
    user_name = models.CharField('Логин пользователя', max_length=56)
    user_pass = models.CharField('Пароль пользователя', max_length=56)
    user_mail = models.CharField('Почта пользователя', max_length=56)

    def __str__(self):
        return self.user_name
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

