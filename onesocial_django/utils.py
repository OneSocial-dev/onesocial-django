import secrets

from django.contrib.auth import get_user_model, login
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from .settings import get_func, get_setting


def generate_account_token():
    return secrets.token_hex(16)


def get_redirect_uri(request):
    return request.build_absolute_uri(reverse('onesocial:complete-login'))


def default_validate(social_account):
    return None


def find_free_username(original_username):
    User = get_user_model()

    counter = 0
    while True:
        if counter == 0:
            username = original_username
        else:
            username = original_username + str(counter)

        if User.objects.filter(username=username).exists():
            counter += 1
            continue
        else:
            return username


def default_register(social_account):
    User = get_user_model()

    # Prepare fields
    username = User.normalize_username(social_account.profile.username)
    email = User.objects.normalize_email(social_account.profile.email)

    # Try to load an existing user by email
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        pass

    # Create a new user
    free_username = find_free_username(username)
    user = User.objects.create(
        username=free_username,
        email=email,
    )

    return user


def complete_registration(request, social_account):
    register_func = get_func(get_setting('ONESOCIAL_REGISTER_FUNC'))

    user = register_func(social_account)

    social_account.user = user
    social_account.save()

    login(request, user)

    return HttpResponseRedirect(get_setting('ONESOCIAL_LOGGED_IN_URL'))
