# Generated by Django 2.0.7 on 2022-04-11 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0007_auto_20220411_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='ufullname',
            field=models.CharField(blank=True, max_length=20, verbose_name='用户姓名'),
        ),
    ]
