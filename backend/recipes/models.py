from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    HEX_CODE = (
        ('Red', '#FF0000'),
        ('Orange', '#FFA500'),
        ('Yellow', '#FFFF00'),
        ('Green', '#00FF00'),
        ('Blue', '#0000FF'),
        ('Dark blue', '#00008b'),
        ('Purple', '#A020F0')
    )
    name = models.CharField(
        'название тэга',
        max_length=100,
        unique=True,
        help_text='Введите название тэга'
    )
    hexcolor = models.CharField(
        'цвет тэга',
        max_length=100,
        choices=HEX_CODE,
        help_text='Выберите цветовой HEX-код'
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


class Ingredient(models.Model):
    name = models.CharField(
        'название ингредиента',
        max_length=100,
        unique=True,
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=100,
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
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Выберите автора рецепта',
        null=True
    )
    name = models.CharField(
        'название рецепта',
        max_length=200,
        help_text='Введите название рецепта'
    )
    text = models.TextField(
        'описание',
        help_text='Введите текстовое описание рецепта'
    )
    image = models.ImageField(
        'изображение',
        upload_to='recipes/',
        help_text='Выберите изображение'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
        help_text='Выберите тэги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты рецепта'
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


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
        help_text='Выберите пользователя'

    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
        help_text='Выберите рецепты'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_user_cart_recipe',
            ),
        )


class IngredientMount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Продукты рецепта',
        help_text='Добавьте ингредиеты для рецепта'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
        help_text='Введите количество продукта',
        validators=[MinValueValidator(1), ],
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Продукты в рецепте'
        verbose_name_plural = 'Продукты в рецепте'

    def __str__(self):
        return f'{self.ingredient} {self.recipe} {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Списки избранного'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_user_favorite_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} take {self.recipe}'
