from django.contrib import admin
from .models import User, Application, Category


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'surname', 'patronymic', 'email', 'role')


admin.site.register(User, UserAdmin)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'category', 'photo_file')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
