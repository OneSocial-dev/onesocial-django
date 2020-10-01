from django.urls import reverse


def get_redirect_uri(request):
    return request.build_absolute_uri(reverse('onesocial:complete-login'))
