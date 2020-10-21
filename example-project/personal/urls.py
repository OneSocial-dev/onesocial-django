from django.urls import path

from . import views


app_name = 'personal'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('confirm-username/<str:account_token>/', views.ConfirmUsernameView.as_view(), name='confirm-username'),
]
