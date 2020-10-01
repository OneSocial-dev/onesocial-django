from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy


class SocialAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=gettext_lazy("user"),
    )

    access_token = models.TextField(
        verbose_name=gettext_lazy("access token"),
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=gettext_lazy("access token expires at"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=gettext_lazy("created at"),
    )

    class Meta:
        verbose_name = gettext_lazy("social account")
        verbose_name_plural = gettext_lazy("social accounts")


class SocialProfile(models.Model):
    account = models.OneToOneField(
        SocialAccount,
        on_delete=models.CASCADE,
        related_name='profile',
        related_query_name='profile',
        verbose_name=gettext_lazy("social account"),
    )

    uid = models.CharField(
        max_length=255,
        verbose_name=gettext_lazy("UID"),
        help_text=gettext_lazy("User ID in the social network"),
    )
    network = models.CharField(
        max_length=255,
        verbose_name=gettext_lazy("network"),
        help_text=gettext_lazy("Social network ID"),
    )

    human_name = models.CharField(
        max_length=255,
        verbose_name=gettext_lazy("human-readable name"),
    )
    username = models.CharField(
        max_length=255,
        verbose_name=gettext_lazy("latinized username"),
    )
    email = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=gettext_lazy("email"),
    )
    picture = models.TextField(
        null=True,
        blank=True,
        verbose_name=gettext_lazy("picture URL"),
    )

    class Meta:
        verbose_name = gettext_lazy("social profile")
        verbose_name_plural = gettext_lazy("social profiles")
