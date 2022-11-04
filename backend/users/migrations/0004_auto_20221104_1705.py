# Generated by Django 3.2.8 on 2022-11-04 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_follow_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-id'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_subscribed',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='Введите email пользователя', max_length=100, verbose_name='почта пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(help_text='Введите имя пользователя', max_length=100, verbose_name='имя пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(help_text='Введите фамилию пользователя', max_length=100, verbose_name='фамилия пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='Введите пароль пользователя', max_length=100, verbose_name='пароль пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('USER', 'user'), ('ADMIN', 'admin')], default='USER', help_text='Выберите роль для пользователя', max_length=10, verbose_name='роль пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Введите username пользователя', max_length=100, unique=True, verbose_name='логин пользователя'),
        ),
    ]