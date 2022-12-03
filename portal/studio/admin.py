from django.contrib import admin
from .models import User, Order, Category
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Post, Category
from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Post, Category





class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'surname', 'patronymic', 'email', 'role')


admin.site.register(User, UserAdmin)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'category', 'photo_file', 'comment')




class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)


class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)