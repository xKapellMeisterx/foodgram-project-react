# Generated by Django 3.2.8 on 2022-11-04 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20221104_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(help_text='Выберите изображение', upload_to='recipes/', verbose_name='изображение'),
        ),
    ]