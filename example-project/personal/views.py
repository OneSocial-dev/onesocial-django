from django.shortcuts import get_object_or_404, render
from django.views import generic
from onesocial_django.models import SocialAccount
from onesocial_django.utils import complete_registration

from .forms import ConfirmUsernameForm


class LoginView(generic.TemplateView):
    template_name = 'personal/login.html'


class ConfirmUsernameView(generic.View):
    template_name = 'personal/confirm-username.html'

    def get(self, request, account_token):
        account = get_object_or_404(SocialAccount, account_token=account_token)
        form = ConfirmUsernameForm(initial={'username': account.profile.username})
        return render(request, self.template_name, {
            'account': account,
            'form': form,
        })

    def post(self, request, account_token):
        account = get_object_or_404(SocialAccount, account_token=account_token)
        form = ConfirmUsernameForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {
                'account': account,
                'form': form,
            })

        account.profile.username = form.cleaned_data['username']
        account.profile.save()

        return complete_registration(account)
