# Generated by Django 4.1.2 on 2022-10-16 08:48

from django.db import migrations, models
import django.db.models.deletion
import studio.models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0004_rename_application_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=studio.models.get_name_file, verbose_name='Изображение')),
                ('order_bb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studio.order', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'Дополнительная иллюстрация',
                'verbose_name_plural': 'Дополнительные иллюстрации',
            },
        ),
    ]