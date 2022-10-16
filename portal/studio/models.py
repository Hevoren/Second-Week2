from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.core.validators import FileExtensionValidator
from django.dispatch import Signal


# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=200, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=200, verbose_name='Отчество', blank=True)
    username = models.CharField(max_length=200, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=200, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=200, verbose_name='Пароль', blank=False)
    role = models.CharField(max_length=200, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь')), default='user')
    USERNAME_FIELD = 'username'

    def delete(self, *args, **kwargs):
        for order_bb in self.order_bb_set.all():
            order_bb.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.name) + ' ' + str(self.surname)

    class Meta:
        ordering = ['name']


# Заявки
def get_name_file(instance, filename):
    return 'portal/file'.join([get_random_string(5) + '_' + filename])


class Order(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя', blank=False)
    summary = models.TextField(max_length=1000, help_text="Описание")
    category = models.ForeignKey('Category', help_text="Выбор категории", on_delete=models.CASCADE)
    photo_file = models.ImageField(max_length=200, upload_to=get_name_file, blank=True, null=True,
                                   validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    def get_absolute_url(self):  # new
        return reverse('order-create', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=200, help_text="Укажите категорию")

    def __str__(self):
        return self.name


# ----------------------------------------------------------------------------------------------------------------------
# Регистрация
user_registrated = Signal()


# ----------------------------------------------------------------------------------------------------------------------

class AdditionalImage(models.Model):
    order_bb = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_name_file, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'
