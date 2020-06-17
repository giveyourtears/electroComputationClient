from django.db import models
from auditlog.registry import auditlog
# Create your models here.
from django.core.validators import RegexValidator

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class AskueUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # user.password = password # bad - do not do this

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username, password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class AskueUser(AbstractBaseUser):
    username = models.CharField(
        max_length=300,
        validators=[
            RegexValidator(regex=USERNAME_REGEX,
                           message='Имя пользователя должно быть буквенно-цифровым или содержать цифры',
                           code='неверное имя пользователя'
                           )],
        unique=True,
        verbose_name="Имя пользователя"
    )
    fullname = models.CharField(max_length=30, default="", verbose_name="Полное имя")
    filter_department = models.TextField(default="", verbose_name="Фильтр разрешения")
    inhibit_filter = models.TextField(default="", null=True, blank=True, verbose_name="Запрещающий фильтр")
    edit_permission = models.BooleanField(default=False, verbose_name="Право на изменение")
    is_admin = models.BooleanField(default=False, verbose_name="Админ?")
    is_staff = models.BooleanField(default=False, verbose_name="Доступ к интерфейсу администратора")

    objects = AskueUserManager()
    USERNAME_FIELD = 'username'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        verbose_name = "Пользователи"  # Не обязательный?
        verbose_name_plural = "Пользователи"  # Обязательный


class FilialModel(models.Model):
    short_name = models.TextField(default="", verbose_name="Сокращенное название")
    full_name = models.TextField(default="", verbose_name="Полное наименование")

    class Meta:
        verbose_name = "Модуль именования филиалов"  # Не обязательный?
        verbose_name_plural = "Модуль именования филиалов"  # Обязательный

    def __str__(self):
        return self.short_name


class PSModel(models.Model):
    short_name = models.TextField(default="", verbose_name="Сокращенное название")
    full_name = models.TextField(default="", verbose_name="Полное наименование")

    class Meta:
        verbose_name = "Модуль именования подстанций"  # Не обязательный?
        verbose_name_plural = "Модуль именования подстанций"  # Обязательный

    def __str__(self):
        return self.short_name


auditlog.register(AskueUser)
