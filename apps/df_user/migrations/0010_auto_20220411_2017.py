# Generated by Django 2.0.7 on 2022-04-11 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0009_auto_20220411_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uemail',
            field=models.EmailField(max_length=254, unique=True, verbose_name='邮箱'),
        ),
    ]
