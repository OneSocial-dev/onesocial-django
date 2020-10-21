from django.contrib import admin
from django.utils.translation import gettext_lazy

from .models import SocialAccount, SocialProfile


class SocialProfileInline(admin.StackedInline):
    model = SocialProfile
    extra = 0


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_profile_network', 'created_at']

    readonly_fields = ['account_token', 'access_token', 'expires_at']

    inlines = [SocialProfileInline]

    def get_profile_network(self, obj):
        return obj.profile.network
    get_profile_network.short_description = gettext_lazy('network')
