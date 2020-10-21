import secrets

from django.http.response import HttpResponse
from django.urls import reverse


def generate_account_token():
    return secrets.token_hex(16)


def get_redirect_uri(request):
    return request.build_absolute_uri(reverse('onesocial:complete-login'))


def default_validate(social_account):
    return None


def complete_registration(social_account):
    return HttpResponse(social_account.profile.username + ', ' + social_account.extra_json)
