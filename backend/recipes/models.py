from django.db import models


class Tag(models.Model):
    name = models.CharField(
        'название тега',
        max_length=100,
        unique=True
    )
    hexcolor = models.CharField(
        'цветовой HEX-код',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        'слаг',
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(
        'название ингредиента',
        max_length=100,
        unique=True
    )
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name



# class Recipes(models.Model):
#     pass
#
#
# class ShoppingCart(models.Model):
#     pass
#
#
# class Favorites(models.Model):
#     pass
#
#
# class Follow(models.Model):
#     pass
#
#
# class Ingredients(models.Model):
#     pass
