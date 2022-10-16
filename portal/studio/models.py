import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.core.validators import FileExtensionValidator
from django.dispatch import Signal
from datetime import date


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
    def __str__(self):
        return str(self.name) + ' ' + str(self.surname)

    class Meta:
        ordering = ['name']


# Заявки
def get_name_file(instance, filename):
    return 'portal/file'.join([get_random_string(5) + '_' + filename])


class Category(models.Model):
    name = models.CharField(max_length=200, help_text="Укажите категорию")

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя', blank=False)
    summary = models.TextField(max_length=1000, help_text="Описание")
    category = models.ForeignKey('category', help_text="Выбор категории", on_delete=models.CASCADE)
    photo_file = models.ImageField(max_length=200, upload_to=get_name_file, blank=True, null=True,
                                   validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # new
        return reverse('order-detail', args=[str(self.id)])


class OrderInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный идентификатор заказа")
    order = models.ForeignKey('order', on_delete=models.SET_NULL, null=True)
    summary = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    customer_order = models.ForeignKey('user', on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('n', 'Новая'),
        ('a', 'Принято в работу'),
        ('c', 'Выполнено'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='n', help_text='Статус заказа')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Установите статус заказа"),)

    def __str__(self):
        """
        Строка для представления объекта Model
        """
        return '%s (%s)' % (self.id, self.order.name)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=200, verbose_name='Фамилия', blank=False)
    email = models.CharField(max_length=200, verbose_name='Почта', unique=True, blank=False)

    def __str__(self):
        return str(self.name) + ' ' + str(self.surname)

    class Meta:
        ordering = ['name']


user_registrated = Signal()
