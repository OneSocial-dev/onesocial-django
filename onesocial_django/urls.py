from django.urls import path

from . import views


app_name = 'onesocial'
urlpatterns = [
    path('login/<str:network>/', views.LoginView.as_view(), name='login'),
    path('complete-login/', views.CompleteLoginView.as_view(), name='complete-login'),
]
