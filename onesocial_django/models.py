import json

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy

from .utils import generate_account_token


class SocialAccount(models.Model):
    """
    Модель социального аккаунта.
    Помимо перечисленных полей содержит ссылку на SocialProfile (атрибут profile).
    """
    # Уникальный токен, который может быть использован, чтобы сослаться на этот аккаунт,
    # не используя последовательный ID.
    account_token = models.CharField(
        max_length=32,
        unique=True,
        verbose_name=gettext_lazy("account token"),
    )

    # Ссыла на пользователя, которому принадлежит этот аккаунт.
    # Может быть None, если аккаунт еще не привязан к пользователю.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=gettext_lazy("user"),
    )

    # Токен доступа к OneSocial.
    access_token = models.TextField(
        verbose_name=gettext_lazy("access token"),
    )
    # Срок действия токена.
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=gettext_lazy("access token expires at"),
    )

    # Время создания объекта.
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=gettext_lazy("created at"),
    )

    # Дополнительные данные аккаунта, закодированные в JSON.
    # См. методы get_extra_dict, set_extra_dict, get_extra и set_extra.
    extra_json = models.TextField(
        null=True,
        blank=True,
        verbose_name=gettext_lazy("extra data JSON"),
    )

    def get_extra_dict(self) -> dict:
        """
        Возвращает словарь дополнительных данных, привязанных к этому аккаунту.

        Дополнительные данные могут быть использованы для передачи информации
        между ONESOCIAL_VALIDATE_FUNC и ONESOCIAL_REGISTER_FUNC.
        Все значения в словаре должны быть объектами, сериализуемыми в JSON.
        """
        try:
            extra_dict = json.loads(self.extra_json)
        except (TypeError, ValueError):
            return {}

        if not isinstance(extra_dict, dict):
            return {}

        return extra_dict

    def set_extra_dict(self, extra_dict: dict):
        """
        Сохраняет словарь дополнительных данных в этот объект.

        Дополнительные данные могут быть использованы для передачи информации
        между ONESOCIAL_VALIDATE_FUNC и ONESOCIAL_REGISTER_FUNC.
        Все значения в словаре должны быть объектами, сериализуемыми в JSON.
        """
        self.extra_json = json.dumps(extra_dict)

    def get_extra(self, key, default=None):
        """
        Возвращает значение по ключу из словаря дополнительных данных.
        default - необязательное значение по-умолчанию.
        Если ключ отсутствует в словаре, возвращает None.

        Дополнительные данные могут быть использованы для передачи информации
        между ONESOCIAL_VALIDATE_FUNC и ONESOCIAL_REGISTER_FUNC.
        Все значения в словаре должны быть объектами, сериализуемыми в JSON.
        """
        return self.get_extra_dict().get(key, default)

    def set_extra(self, key, value):
        """
        Задает значение по ключу в словаре дополнительных данных.

        Дополнительные данные могут быть использованы для передачи информации
        между ONESOCIAL_VALIDATE_FUNC и ONESOCIAL_REGISTER_FUNC.
        Все значения в словаре должны быть объектами, сериализуемыми в JSON.
        """
        extra_dict = self.get_extra_dict()
        extra_dict[key] = value
        self.set_extra_dict(extra_dict)

    def save(self, *args, **kwargs):
        if not self.account_token:
            self.account_token = generate_account_token()

        return super().save(*args, **kwargs)

    def __str__(self):
        return "{} @ {}".format(self.profile.uid, self.profile.network)

    class Meta:
        verbose_name = gettext_lazy("social account")
        verbose_name_plural = gettext_lazy("social accounts")


class SocialProfile(models.Model):
    """
    Профиль социального аккаунта.
    См. https://onesocial.dev/panel/docs/users-api/#get-me
    """
    account = models.OneToOneField(
        SocialAccount,
        on_delete=models.CASCADE,
        related_name='profile',
        related_query_name='profile',
        verbose_name=gettext_lazy("social account"),
    )

    # ID аккаунта в социальной сети.
    uid = models.CharField(
        max_length=255,
        verbose_name=gettext_lazy("UID"),
        help_text=gettext_lazy("User ID in the social network"),
    )
    # Код социальной сети.
    # См. https://onesocial.dev/panel/docs/sociallogin/#networks
    network = models.CharField(
        max_length=255,
        verbose_name=gettext_lazy("network"),
        help_text=gettext_lazy("Social network ID"),
    )

    # Человеко-читаемое имя.
    human_name = models.CharField(
        max_length=255,
        verbose_name=gettext_lazy("human-readable name"),
    )
    # Латинизированный юзернейм.
    username = models.CharField(
        max_length=255,
        verbose_name=gettext_lazy("latinized username"),
    )
    # Email (опционально, если доступен)
    email = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=gettext_lazy("email"),
    )
    # URL аватарки профиля
    picture = models.TextField(
        null=True,
        blank=True,
        verbose_name=gettext_lazy("picture URL"),
    )

    def __str__(self):
        return "{} @ {}".format(self.uid, self.network)

    class Meta:
        unique_together = [('network', 'uid')]
        verbose_name = gettext_lazy("social profile")
        verbose_name_plural = gettext_lazy("social profiles")
