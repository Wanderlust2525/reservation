from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField

from account.manages import UserManager


class User(AbstractUser):
    CLIENT = 'client'        
    WORKER = 'worker'        
    DIRECTOR = 'director'    

    ROLE = (
        (CLIENT, 'Пользователь'),
        (WORKER, 'Сотрудник'),
        (DIRECTOR, 'Директор'),
    )

    avatar = ResizedImageField(
        'аватарка', size=[500, 500], crop=['middle', 'center'],
        upload_to='avatars/', force_format='WEBP', quality=90,
        null=True, blank=True
    )

    role = models.CharField('роль', choices=ROLE, default=CLIENT, max_length=15)

    
    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def __str__(self):
        return self.get_full_name or self.username
