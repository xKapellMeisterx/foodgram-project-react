# Generated by Django 3.2.8 on 2022-11-04 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20221102_1824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['-id'], 'verbose_name': 'Избранное', 'verbose_name_plural': 'Списки избранного'},
        ),
        migrations.AlterModelOptions(
            name='ingredientmount',
            options={'ordering': ['-id'], 'verbose_name': 'Продукты в рецепте', 'verbose_name_plural': 'Продукты в рецепте'},
        ),
    ]
