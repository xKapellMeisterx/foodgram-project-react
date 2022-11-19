from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    ROLE_USERS = (
        ('USER', 'user'),
        ('ADMIN', 'admin')
    )

    email = models.EmailField(
        'почта пользователя',
        max_length=100,
        help_text='Введите email пользователя'
    )
    username = models.CharField(
        'логин пользователя',
        max_length=100,
        unique=True,
        help_text='Введите username пользователя'
    )
    first_name = models.CharField(
        'имя пользователя',
        max_length=100,
        help_text='Введите имя пользователя'
    )
    last_name = models.CharField(
        'фамилия пользователя',
        max_length=100,
        help_text='Введите фамилию пользователя'
    )
    password = models.CharField(
        'пароль пользователя',
        max_length=100,
        help_text='Введите пароль пользователя'
    )
    role = models.CharField(
        'роль пользователя',
        max_length=10,
        choices=ROLE_USERS,
        default='USER',
        help_text='Выберите роль для пользователя'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == 'ADMIN'

    @property
    def is_user(self):
        return self.role == 'USER'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """
    Подписка на авторов.
    Пользователь (user) связан с моделю User.
    Автор рецепта (following) связан с моделю User.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Выберете пользователя, который подписывается'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Выберите автора, на которого подписываются'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

