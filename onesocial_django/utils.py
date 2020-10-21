import secrets

from django.contrib.auth import get_user_model, login
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from .settings import get_func, get_setting


def generate_account_token():
    """
    Генерирует токен аккаунта для использования в поле SocialAccount.account_token.
    """
    return secrets.token_hex(16)


def get_redirect_uri(request):
    """
    Возвращает полный redirect URI, для использования с OneSocial API.
    """
    return request.build_absolute_uri(reverse('onesocial:complete-login'))


def default_validate(social_account):
    """
    Функция по-умолчанию для ONESOCIAL_VALIDATE_FUNC. Ничего не делает.
    """
    return None


def find_free_username(original_username):
    """
    Если original_username не занят ни одним пользователем - возвращает его же.
    Если он занят - добавляет наименьшее число в его конец, чтобы получить свободный
    username.

    Например:
    find_free_username('test')  # => 'test12'
    """
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
    """
    Функция по-умолчанию для ONESOCIAL_REGISTER_FUNC.
    Нормализует username и email, возвращает существующий объект User с таким же email
    как у social_account.profile, либо создает новый User с полученными username и email,
    без пароля.
    """
    User = get_user_model()

    # Prepare fields
    username = User.normalize_username(social_account.profile.username)
    if social_account.profile.email:
        email = User.objects.normalize_email(social_account.profile.email)
    else:
        email = None

    if email:
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
    """
    Регистрирует социальный аккаунт в Django, и аутентифицирует текущего пользователя.
    Возвращает HttpResponse Django, который следует вернуть клиенту.
    """
    register_func = get_func(get_setting('ONESOCIAL_REGISTER_FUNC'))

    user = register_func(social_account)

    social_account.user = user
    social_account.save()

    return complete_login(request, social_account)


def complete_login(request, social_account):
    """
    Аутентифицирует текущего пользователя по социальному аккаунту.
    Возвращает HttpResponse Django, который следует вернуть клиенту.
    """
    login(request, social_account.user)

    return HttpResponseRedirect(get_setting('ONESOCIAL_LOGGED_IN_URL'))
