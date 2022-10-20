from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        'название тега',
        max_length=100,
        unique=True,
        help_text='Введите название тега'
    )
    hexcolor = models.CharField(
        'цветовой HEX-код',
        max_length=7,
        unique=True,
        help_text='Введите HEX-код тега'
    )
    slug = models.SlugField(
        'слаг',
        max_length=100,
        unique=True,
        help_text='Введите слаг'
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
        unique=True,
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=100,
        unique=True,
        help_text='Введите единицу измерения'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Выберите автора рецепта',
        null=True
    )
    name = models.CharField(
        'название рецепта',
        max_length=200,
        help_text='Введите название рецепта'
    )
    text = models.TextField(
        help_text='Введите описание рецепта'
    )
    image = models.ImageField(
        'картинка',
        upload_to='recipes/',
        blank=True,
        help_text='Выберите изображение'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Тэг',
        help_text='Выберите тэги'
    )
    ingredients = models.ManyToManyField(
        'Ingredients',
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты'
    )
    cooking_time = models.IntegerField(
        'время приготовления',
        help_text='Введите время приготовления',
        validators=(MinValueValidator(1),)
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


# class ShoppingCart(models.Model):
#     pass
#
#
class Favorite(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Списки Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_user_favorite_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} -> {self.recipe}'
