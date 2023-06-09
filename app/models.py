from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Users(models.Model):
    login = models.CharField('Логин пользователя', max_length=56)
    pas = models.CharField('Пароль пользователя', max_length=56)
    mail = models.CharField('Почта пользователя', max_length=56)

    def __str__(self):
        return self.login
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

