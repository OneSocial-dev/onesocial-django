from django.contrib import admin
from django.urls import include, path
from django.views import generic


urlpatterns = [
    path('', generic.RedirectView.as_view(pattern_name='personal:login'), name='home'),
    path('admin/', admin.site.urls),
    path('personal/', include('personal.urls')),
    path('onesocial/', include('onesocial_django.urls')),
]
