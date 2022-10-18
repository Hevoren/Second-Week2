# Generated by Django 3.2.16 on 2022-10-18 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0004_user_consent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='consent',
            field=models.CharField(default='0', help_text='Согласие на обработку персональных данных', max_length=200),
        ),
    ]
