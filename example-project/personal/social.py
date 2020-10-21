from django.shortcuts import redirect

from onesocial_django.models import SocialAccount


def validate_func(social_account: SocialAccount):
    return redirect('personal:confirm-username', account_token=social_account.account_token)
