from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Users(models.Model):
    user_name = models.CharField('Логин пользователя', max_length=56)
    user_pass = models.CharField('Пароль пользователя', max_length=56)
    user_mail = models.CharField('Почта пользователя', max_length=56)
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True)

    def __str__(self):
        return self.user_name
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Routers(models.Model):
    user_id = models.CharField('Id пользователя', max_length=256)
    public_url = models.CharField('публичная ссылка', max_length=256, default="none")
    privat_url = models.CharField('пользовательская ссылка', max_length=256)

    def __str__(self):
        return self.user_id  

    class Meta:
        verbose_name = 'Роут'
        verbose_name_plural = 'Роуты'