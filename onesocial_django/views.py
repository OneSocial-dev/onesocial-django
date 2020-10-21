import logging
from datetime import timedelta
from urllib.parse import urlencode

import onesocial
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views import generic

from .models import SocialAccount, SocialProfile
from .settings import get_func, get_setting
from .utils import complete_login, complete_registration, get_redirect_uri

logger = logging.getLogger(__name__)


class LoginView(generic.View):
    """
    Вью инициализации входа через соцсети. Принимает один параметр через URL -
    network, код социальной сети. Перенаправляет пользователя на страницу авторизации
    в социальной сети.
    """
    def get(self, request, network):
        oauth = onesocial.OAuth(
            client_id=get_setting('ONESOCIAL_CLIENT_ID'),
            client_secret=get_setting('ONESOCIAL_CLIENT_SECRET'),
        )
        init_uri = oauth.init(
            network=network,
            response_type=onesocial.OAuth.CODE,
            redirect_uri=get_redirect_uri(request),
        )
        return HttpResponseRedirect(init_uri)


class CompleteLoginView(generic.View):
    """
    Вью завершения входа через соцсети. На эту вью пользователь попадает после
    авторизации в соцсети.

    Для новых пользователей создает объекты SocialAccount и SocialProfile,
    затем вызывает ONESOCIAL_VALIDATE_FUNC. Если ONESOCIAL_VALIDATE_FUNC не вернул
    HttpResponse, завершает регистрацию с помощью onesocial_django.utils.complete_registration.

    Для старых пользователей получает существует SocialAccount и аутентифицирует их
    с помощью onesocial_django.utils.complete_login.

    В случае успеха перенаправляет на ONESOCIAL_LOGGED_IN_URL.

    В случае ошики перенаправляет на ONESOCIAL_ERROR_URL.
    """
    def make_social_account(self, request, grant):
        state = request.GET.get('state', '')

        try:
            return SocialAccount.objects.get(access_token=grant.access_token)
        except SocialAccount.DoesNotExist:
            pass

        try:
            profile = onesocial.UsersAPI(access_token=grant.access_token).me()
        except onesocial.OneSocialError as e:
            logger.exception("Error while requesting user profile")
            return HttpResponseRedirect(get_setting('ONESOCIAL_ERROR_URL') + '?' + urlencode({
                'error': e.code,
                'error_description': e.message,
                'state': state,
            }))

        try:
            return SocialAccount.objects.get(profile__network=profile.network, profile__uid=profile.uid)
        except SocialAccount.DoesNotExist:
            pass

        social_account = SocialAccount(access_token=grant.access_token)

        if grant.expires_in:
            social_account.expires_at = timezone.now() + timedelta(seconds=grant.expires_in)

        social_account.save()

        SocialProfile.objects.create(
            account=social_account,
            uid=profile.uid,
            network=profile.network,
            human_name=profile.human_name,
            username=profile.username,
            email=profile.email,
            picture=profile.picture,
        )

        return social_account

    def get(self, request):
        state = request.GET.get('state', '')

        if 'error' in request.GET:
            error = request.GET['error']
            error_description = request.GET.get('error_description', '')
            return HttpResponseRedirect(get_setting('ONESOCIAL_ERROR_URL') + '?' + urlencode({
                'error': error,
                'error_description': error_description,
                'state': state,
            }))

        code = request.GET.get('code')
        if not code:
            raise Http404()

        oauth = onesocial.OAuth(
            client_id=get_setting('ONESOCIAL_CLIENT_ID'),
            client_secret=get_setting('ONESOCIAL_CLIENT_SECRET'),
        )

        try:
            grant = oauth.token(code=code, redirect_uri=get_redirect_uri(request))
        except onesocial.OneSocialError as e:
            logger.exception("Error while requesting OneSocial access token")
            return HttpResponseRedirect(get_setting('ONESOCIAL_ERROR_URL') + '?' + urlencode({
                'error': e.code,
                'error_description': e.message,
                'state': state,
            }))

        social_account = self.make_social_account(request, grant)
        if social_account.user:
            return complete_login(request, social_account)

        validate_func = get_func(get_setting('ONESOCIAL_VALIDATE_FUNC'))

        validation_response = validate_func(social_account)
        if validation_response:
            return validation_response

        return complete_registration(request, social_account)
