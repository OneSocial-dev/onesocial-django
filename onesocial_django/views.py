import logging
from urllib.parse import urlencode

import onesocial
from django.http.response import HttpResponseRedirect, Http404, HttpResponse
from django.views import generic

from .utils import get_redirect_uri
from .settings import get_setting

logger = logging.getLogger(__name__)


class LoginView(generic.View):
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

        return HttpResponse(grant.access_token)
