# Generated by Django 2.0.7 on 2022-04-11 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0010_auto_20220411_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uemail',
            field=models.EmailField(max_length=254, verbose_name='邮箱'),
        ),
    ]