from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from .usermanager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 120, verbose_name='Никнейм')
    email = models.EmailField(unique = True,verbose_name='Эмейл')
    code = models.CharField(max_length = 6)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "Обычные пользователи"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    